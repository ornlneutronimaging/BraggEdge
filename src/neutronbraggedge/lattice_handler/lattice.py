"""Lattice parameter calculation from experimental Bragg edges."""

import ast
import configparser
from typing import Any, Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

from ..braggedges_handler.braggedge_calculator import BraggEdgeCalculator
from ..config import config_file as config_config_file
from ..models import LatticeStatistics

CrystalStructure = Literal["BCC", "FCC"]


class Lattice:
    """Calculate lattice parameters from experimental Bragg edge measurements.

    Given experimental Bragg edge values and crystal structure, this class
    calculates the lattice parameter for each reflection and provides
    statistical analysis of the results.

    Attributes
    ----------
    material : str or None
        Material name/symbol.
    crystal_structure : CrystalStructure
        Crystal structure type ("BCC" or "FCC").
    bragg_edge_array : NDArray
        Array of experimental Bragg edge values.
    bragg_edge_error_array : NDArray
        Array of errors for the Bragg edge values.
    hkl : list[list[int]]
        Miller indices for each Bragg edge.
    lattice_array : list[float]
        Calculated lattice parameters for each reflection.
    lattice_error : list[float]
        Errors in lattice parameters.
    lattice_statistics : dict[str, Any]
        Statistical summary (min, max, mean, median, std).

    Examples
    --------
    >>> from neutronbraggedge.lattice_handler.lattice import Lattice
    >>> bragg_edges = [4.05, 2.87, 2.34, 2.03]
    >>> errors = [0.01, 0.01, 0.01, 0.01]
    >>> lattice = Lattice(
    ...     material='Fe',
    ...     crystal_structure='BCC',
    ...     bragg_edge_array=bragg_edges,
    ...     bragg_edge_error_array=errors
    ... )
    >>> print(lattice.lattice_statistics['mean'])
    [2.866, 0.007]
    """

    space: int = 75

    material: str | None
    use_local_metadata: bool
    bragg_edge_array: NDArray[np.floating]
    bragg_edge_error_array: NDArray[np.floating]
    _crystal_structure: CrystalStructure
    _list_structure: list[str]
    hkl: list[list[int]]
    hkl_bragg_edge: list[tuple[list[int], float, float]]
    lattice_array: list[float]
    lattice_error: list[float]
    lattice_statistics: dict[str, Any]

    def __init__(
        self,
        material: str | None = None,
        crystal_structure: CrystalStructure | None = None,
        bragg_edge_array: ArrayLike | None = None,
        bragg_edge_error_array: ArrayLike | None = None,
        use_local_metadata_table: bool = True,
    ) -> None:
        """Initialize Lattice calculator.

        Parameters
        ----------
        material : str, optional
            Material name/symbol for reference.
        crystal_structure : {"BCC", "FCC"}
            Crystal structure type.
        bragg_edge_array : array-like
            Experimental Bragg edge wavelengths in Angstroms.
        bragg_edge_error_array : array-like, optional
            Errors for the Bragg edge values. If None, zeros are used.
        use_local_metadata_table : bool, default True
            Whether to use local metadata table.

        Raises
        ------
        ValueError
            If crystal_structure is not "BCC" or "FCC".
        """
        self.material = material
        self._crystal_structure = crystal_structure
        self.crystal_structure = crystal_structure  # only used to run test
        self.use_local_metadata = use_local_metadata_table
        self.bragg_edge_array = self._format_array(bragg_edge_array)
        self.bragg_edge_error_array = self._format_array(bragg_edge_error_array)

        # retrieve hkl
        o_bragg_calculator = BraggEdgeCalculator(
            structure_name=crystal_structure, lattice=None, number_of_set=len(bragg_edge_array)
        )
        o_bragg_calculator.calculate_hkl()
        self.hkl = o_bragg_calculator.hkl

        self._calculate()

    @property
    def crystal_structure(self) -> CrystalStructure:
        """Get the crystal structure type."""
        return self._crystal_structure

    @crystal_structure.setter
    def crystal_structure(self, structure_name: CrystalStructure | None) -> None:
        """Set and validate the crystal structure type."""
        _config_file = config_config_file
        config_obj = configparser.ConfigParser()
        config_obj.read(_config_file)
        self._list_structure = ast.literal_eval(config_obj["DEFAULT"]["list_structure"])

        if structure_name not in self._list_structure:
            raise ValueError(f"Structure name should be in the list {self._list_structure}")
        self._crystal_structure = structure_name

    def get_statistics(self) -> LatticeStatistics:
        """Get lattice statistics as a Pydantic model.

        Returns
        -------
        LatticeStatistics
            Pydantic model containing statistical summary of lattice parameters.

        Examples
        --------
        >>> lattice = Lattice(material='Fe', crystal_structure='BCC',
        ...                   bragg_edge_array=[4.05, 2.87],
        ...                   bragg_edge_error_array=[0.01, 0.01])
        >>> stats = lattice.get_statistics()
        >>> print(stats.mean)
        2.866
        >>> print(stats.model_dump_json(indent=2))
        """
        return LatticeStatistics(
            min=float(self.lattice_statistics["min"]),
            max=float(self.lattice_statistics["max"]),
            median=float(self.lattice_statistics["median"]),
            mean=float(self.lattice_statistics["mean"][0]),
            mean_error=float(self.lattice_statistics["mean"][1]),
            std=float(self.lattice_statistics["std"]),
        )

    def _format_array(self, bragg_edge_array: ArrayLike | None) -> NDArray[np.floating]:
        """Format input array, replacing None values with np.nan."""
        _bragg_edge_array_formated: list[float] = []

        if bragg_edge_array is None:
            sz = len(self.bragg_edge_array)
            _bragg_edge_array_formated_arr: NDArray[np.floating] = np.zeros(sz)
            return _bragg_edge_array_formated_arr

        for _value in bragg_edge_array:
            if _value is None:
                _value = np.nan
            _bragg_edge_array_formated.append(_value)
        _bragg_edge_array_formated_arr = np.array(_bragg_edge_array_formated)
        return _bragg_edge_array_formated_arr

    def _calculate(self) -> None:
        """Calculate lattice parameters step by step."""
        self._match_bragg_edge_with_hkl()
        self._calculate_lattice_array()
        self._calculate_lattice_statistics()

    def _match_bragg_edge_with_hkl(self) -> None:
        """Match each Bragg edge with its corresponding Miller indices."""
        _bragg_edge_array = self.bragg_edge_array
        _bragg_edge_array_error = self.bragg_edge_error_array

        zipped = zip(self.hkl, _bragg_edge_array, _bragg_edge_array_error)
        self.hkl_bragg_edge = list(zipped)

    def display_hkl_bragg_edge(self) -> bool:
        """Display the hkl-Bragg edge table.

        Returns
        -------
        bool
            Always returns True on successful display.
        """
        print("hkl Bragg Edge Table")
        print("=" * self.space)
        print("hkl \t\t Bragg Edge Value\t Bragg Edge Error \t Lattice")
        print("-" * self.space)
        _lattice_array = self.lattice_array
        for _index, _row in enumerate(self.hkl_bragg_edge):
            _key = _row[0]
            _value = _row[1]
            _error = _row[2]
            _lattice = _lattice_array[_index]
            if np.isnan(_error):
                print(f"{_key!r}\t {_value:.5f} \t\t\t {_error:.5f} \t\t\t {_lattice:.5f}")
            else:
                print(f"{_key!r}\t {_value:.5f} \t\t {_error:.5f} \t\t {_lattice:.5f}")
        print("-" * self.space)
        print("")
        return True

    def _calculate_lattice_array(self) -> None:
        """Calculate lattice parameter for each hkl reflection."""
        _hkl_bragg_edge = self.hkl_bragg_edge
        _lattice_array: list[float] = []
        _lattice_error_array: list[float] = []
        for _row in _hkl_bragg_edge:
            _hkl = _row[0]
            _bragg_edge = _row[1]
            _bragg_error = _row[2]
            [_lattice, _lattice_error] = self._calculate_lattice_coefficient(
                hkl=_hkl, bragg_edge=_bragg_edge, bragg_error=_bragg_error
            )
            _lattice_array.append(_lattice)
            _lattice_error_array.append(_lattice_error)

        self.lattice_array = _lattice_array
        self.lattice_error = _lattice_error_array

    def _calculate_lattice_coefficient(
        self,
        hkl: list[int] | None = None,
        bragg_edge: float | None = None,
        bragg_error: float | None = None,
    ) -> list[float]:
        """Calculate lattice parameter from a single hkl and Bragg edge."""
        _h, _k, _l = hkl
        _term1 = np.sqrt(_h**2 + _k**2 + _l**2)
        _term2 = bragg_edge / 2.0

        _lattice = _term2 * _term1
        _lattice_error = _term1 * bragg_error / 2.0

        return [_lattice, _lattice_error]

    def _calculate_lattice_statistics(self) -> None:
        """Calculate statistics of the lattice parameter array."""
        _lattice_statistics: dict[str, Any] = {}

        # min
        _min = np.nanmin(self.lattice_array)
        _lattice_statistics["min"] = _min

        # max
        _max = np.nanmax(self.lattice_array)
        _lattice_statistics["max"] = _max

        # median
        _median = np.nanmedian(self.lattice_array)
        _lattice_statistics["median"] = _median

        # mean
        _mean = np.nanmean(self.lattice_array)
        _error = self._calculate_mean_error(self.lattice_error)
        _lattice_statistics["mean"] = [_mean, _error]

        # std
        _std = np.nanstd(self.lattice_array)
        _lattice_statistics["std"] = _std

        self.lattice_statistics = _lattice_statistics

    def _calculate_mean_error(self, lattice_error: list[float]) -> float:
        """Calculate propagated error for the mean lattice parameter."""
        _mean_error = 0.0
        _index = 0
        _sum = 0.0
        for _error in lattice_error:
            if not np.isnan(_error):
                _step1 = _error * _error
                _sum += _step1
                _index += 1
        _mean_error = np.sqrt(_sum) / _index
        return _mean_error

    def display_lattice_statistics(self) -> None:
        """Display lattice statistics via logger."""
        _lattice_statistics = self.lattice_statistics
        print("Lattice Statistics")
        print("=" * self.space)
        print(f"min: {_lattice_statistics['min']:.5f}")
        print(f"max: {_lattice_statistics['max']:.5f}")
        print(f"median: {_lattice_statistics['median']:.5f}")
        print(f"mean: {_lattice_statistics['mean'][0]:.5f} +/- {_lattice_statistics['mean'][1]:.5f}")
        print(f"std: {_lattice_statistics['std']:.5f}")
        print("-" * self.space)
        print("")

    def display_recap(self) -> None:
        """Display a summary of inputs and calculation results."""
        print(" -- Recap --")
        print("=" * self.space)
        print(f"Material: {self.material!r}")
        print(f"Crystal Structure: {self._crystal_structure!r}")
        print("-" * self.space)
        print("")

        self.display_hkl_bragg_edge()
        self.display_lattice_statistics()

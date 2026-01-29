"""Bragg edge calculation module for crystalline materials."""

import os
from typing import Any, Literal, TypedDict

from .braggedges_handler.braggedge_calculator import BraggEdgeCalculator
from .material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
from .models import BraggEdgeEntry, BraggEdgeResult
from .utilities import Utilities

CrystalStructure = Literal["BCC", "FCC"]


class NewMaterialDict(TypedDict):
    """Type definition for new material dictionary.

    Attributes
    ----------
    name : str
        Material name/symbol.
    lattice : float
        Lattice constant in Angstroms.
    crystal_structure : CrystalStructure
        Crystal structure type ("BCC" or "FCC").
    """

    name: str
    lattice: float
    crystal_structure: CrystalStructure


class BraggEdge:
    """Calculate Bragg edges for crystalline materials.

    This class retrieves material metadata and calculates Bragg edge positions
    for neutron diffraction analysis.

    Attributes
    ----------
    material : list[str]
        List of material names.
    hkl : dict[str, list[list[int]]]
        Miller indices for each material.
    bragg_edges : dict[str, list[float]]
        Bragg edge wavelengths in Angstroms for each material.
    d_spacing : dict[str, list[float]]
        Interplanar spacing in Angstroms for each material.
    metadata : dict[str, Any]
        Material metadata including lattice and crystal structure.

    Examples
    --------
    Calculate Bragg edges for Iron:

    >>> from neutronbraggedge.braggedge import BraggEdge
    >>> handler = BraggEdge(material='Fe', number_of_bragg_edges=4)
    >>> print(handler.bragg_edges['Fe'])
    [4.0538, 2.8664, 2.3404, 2.0269]

    Use a custom material:

    >>> custom = [{'name': 'MyMat', 'lattice': 3.5, 'crystal_structure': 'FCC'}]
    >>> handler = BraggEdge(new_material=custom)

    Get Pydantic model result:

    >>> result = handler.to_result('Fe')
    >>> print(result.model_dump_json())
    """

    hkl: dict[str, list[list[int]]] | None = None
    metadata: dict[str, Any] | None = None
    bragg_edges: dict[str, list[float]] | None = None
    d_spacing: dict[str, list[float]] | None = None
    material: list[str]
    number_of_bragg_edges: int
    use_local_metadata_table: bool
    lattice: dict[str, float]
    crystal_structure: dict[str, CrystalStructure]
    _calculator: dict[str, BraggEdgeCalculator]

    def __init__(
        self,
        material: str | list[str] | None = None,
        new_material: list[NewMaterialDict] | None = None,
        number_of_bragg_edges: int = 10,
        use_local_metadata_table: bool = True,
    ) -> None:
        """Initialize BraggEdge calculator.

        Parameters
        ----------
        material : str or list[str], optional
            Material name(s) such as 'Ni', 'Fe'. Either `material` or
            `new_material` must be provided.
        new_material : list[NewMaterialDict], optional
            List of custom material definitions with 'name', 'lattice',
            and 'crystal_structure' keys.
        number_of_bragg_edges : int, default 10
            Number of Bragg edges to calculate.
        use_local_metadata_table : bool, default True
            If True, use local metadata table. If False, fetch from Wikipedia.

        Raises
        ------
        ValueError
            If neither `material` nor `new_material` is provided, or if
            `new_material` has an invalid format.
        """
        if material is None:
            if new_material is None:
                raise ValueError("No material or new_material defined!")
            else:
                # parse dictionary
                list_material: list[str] = []
                try:
                    for _element in new_material:
                        _name = _element["name"]
                        list_material.append(_name)
                        _lattice_constant = _element["lattice"]
                        _crystal_structure = _element["crystal_structure"]
                except:
                    raise ValueError("Check the format of the new element array!")

                material = list_material

        if type(material) is not list:
            material = [material]

        self.material = material
        self.number_of_bragg_edges = number_of_bragg_edges
        self.use_local_metadata_table = use_local_metadata_table

        self._retrieve_metadata(new_material=new_material)
        self._calculate_hkl()
        self._calculate_braggedges()

    def to_result(self, material: str) -> BraggEdgeResult:
        """Convert calculation results to a Pydantic model.

        Parameters
        ----------
        material : str
            Material name to get results for.

        Returns
        -------
        BraggEdgeResult
            Pydantic model containing all calculation results.

        Raises
        ------
        KeyError
            If the specified material was not calculated.

        Examples
        --------
        >>> handler = BraggEdge(material='Fe', number_of_bragg_edges=4)
        >>> result = handler.to_result('Fe')
        >>> print(result.lattice)
        2.8664
        >>> print(result.model_dump_json(indent=2))
        """
        if material not in self.material:
            raise KeyError(f"Material '{material}' not found. Available: {self.material}")

        entries = []
        _hkl = self.hkl[material]
        _d_spacing = self.d_spacing[material]
        _bragg_edges = self.bragg_edges[material]

        for i in range(len(_d_spacing)):
            entries.append(
                BraggEdgeEntry(
                    h=_hkl[i][0],
                    k=_hkl[i][1],
                    l=_hkl[i][2],
                    d_spacing=_d_spacing[i],
                    bragg_edge=_bragg_edges[i],
                )
            )

        return BraggEdgeResult(
            material=material,
            lattice=self.metadata["lattice"][material],
            crystal_structure=self.metadata["crystal_structure"][material],
            use_local_table=self.use_local_metadata_table,
            entries=entries,
        )

    def get_experimental_lattice_parameter(
        self,
        experimental_bragg_edge_values: list[float] | None = None,
        experimental_bragg_edge_error: list[float] | None = None,
    ) -> None:
        """Calculate experimental lattice parameter from Bragg edge values.

        Note: This method is not yet implemented. Use the Lattice class directly
        for experimental lattice parameter calculations.

        Parameters
        ----------
        experimental_bragg_edge_values : list[float], optional
            Array of experimental Bragg edge values.
        experimental_bragg_edge_error : list[float], optional
            Array of errors for the Bragg edge values.

        Raises
        ------
        ValueError
            If `experimental_bragg_edge_values` is not provided, or if
            `experimental_bragg_edge_error` length doesn't match.
        NotImplementedError
            This method is not yet implemented.
        """
        if experimental_bragg_edge_values is None:
            raise ValueError("Please provide an array of bragg edge values")

        if experimental_bragg_edge_error is not None:
            if len(experimental_bragg_edge_error) != len(experimental_bragg_edge_values):
                raise ValueError("Make sure exp. bragg edge value and error have the same size!")

        raise NotImplementedError(
            "get_experimental_lattice_parameter is not yet implemented. "
            "Use the Lattice class directly for experimental lattice calculations."
        )

    def _retrieve_metadata(self, new_material: list[NewMaterialDict] | None = None) -> None:
        """Retrieve lattice and crystal structure metadata for materials."""
        _lattice: dict[str, float] = {}
        _crystal_structure: dict[str, CrystalStructure] = {}

        if new_material is None:  # retrieve infos from ascii table
            for _material in self.material:
                _handler = RetrieveMaterialMetadata(material=_material, use_local_table=self.use_local_metadata_table)
                _lattice[_material] = _handler.lattice
                _crystal_structure[_material] = _handler.crystal_structure

        else:  # local infos
            for _element in new_material:
                _material = _element["name"]
                _local_lattice = _element["lattice"]
                _local_crystal_structure = _element["crystal_structure"]

                _lattice[_material] = _local_lattice
                _crystal_structure[_material] = _local_crystal_structure

        self.lattice = _lattice
        self.crystal_structure = _crystal_structure

        self.metadata = {"lattice": self.lattice, "crystal_structure": self.crystal_structure}

    def _calculate_hkl(self) -> None:
        """Calculate Miller indices up to number_of_bragg_edges."""
        calculator: dict[str, BraggEdgeCalculator] = {}
        _hkl: dict[str, list[list[int]]] = {}

        for _material in self.material:
            _structure_name = self.metadata["crystal_structure"][_material]
            _lattice = self.metadata["lattice"][_material]

            _calculator = BraggEdgeCalculator(
                structure_name=_structure_name, lattice=_lattice, number_of_set=self.number_of_bragg_edges
            )

            _calculator.calculate_hkl()
            calculator[_material] = _calculator
            _hkl[_material] = _calculator.hkl

        self._calculator = calculator
        self.hkl = _hkl

    def _calculate_braggedges(self) -> None:
        """Calculate Bragg edge wavelengths and d-spacing values."""
        _d_spacing: dict[str, list[float]] = {}
        _bragg_edges: dict[str, list[float]] = {}

        for _material in self.material:
            _calculator = self._calculator[_material]

            _calculator.calculate_bragg_edges()
            _d_spacing[_material] = _calculator.d_spacing
            _bragg_edges[_material] = _calculator.bragg_edges

        self.d_spacing = _d_spacing
        self.bragg_edges = _bragg_edges

    def __repr__(self) -> str:
        """Display calculation results via logger."""
        nbr_ticks = 45

        for _material in self.material:
            print("=" * nbr_ticks)
            print(f"Material: {_material}")
            print(f"Lattice : {self.metadata['lattice'][_material]:.4f}\u212b")
            print(f"Crystal Structure: {self.metadata['crystal_structure'][_material]}")
            print(f"Using local metadata Table: {self.use_local_metadata_table}")
            print("=" * nbr_ticks)
            print(" h | k | l |\t d (\u212b)  |\t BraggEdge")
            print("-" * nbr_ticks)

            _hkl = self.hkl[_material]
            _bragg_edges = self.bragg_edges[_material]
            _d_spacing = self.d_spacing[_material]

            for index in range(len(_d_spacing)):
                h, k, l = _hkl[index]
                print(f" {h} | {k} | {l} |\t {_d_spacing[index]:.5f} |\t {_bragg_edges[index]:.5f}")

            print("=" * nbr_ticks)

        return ""

    def export(self, filename: str | None = None, file_type: str = "csv") -> None:
        """Export calculation results to a file.

        Parameters
        ----------
        filename : str, optional
            Output file path.
        file_type : str, default "csv"
            Output format. Only "csv" is currently supported.

        Raises
        ------
        OSError
            If no filename is provided.
        NotImplementedError
            If an unsupported file type is requested.
        """
        if filename is None:
            raise OSError

        for _material in self.material:
            _filename = self._format_filename(filename, _material)
            _metadata = self._format_metadata(_material)
            _data = self._format_data(_material)

            if file_type == "csv":
                Utilities.save_csv(filename=_filename, data=_data, metadata=_metadata)

            else:
                raise NotImplementedError

    def _format_filename(self, filename: str, material: str) -> str:
        """Format output filename with material suffix."""
        _filename, _extension = os.path.splitext(filename)
        new_filename = os.path.join(_filename + "_" + material + _extension)
        return new_filename

    def _format_metadata(self, _material: str) -> list[str]:
        """Format metadata for file header."""
        _metadata: list[str] = []
        _metadata.append("Material: %s" % _material)
        _metadata.append("Lattice : %.4fAngstroms" % self.metadata["lattice"][_material])
        _metadata.append("Crystal Structure: %s" % self.metadata["crystal_structure"][_material])
        _metadata.append("Using local metadata Table: %s" % self.use_local_metadata_table)
        _metadata.append("")
        _metadata.append("h, k, l, d(Angstroms), BraggEdge")
        return _metadata

    def _format_data(self, _material: str) -> list[list[int | float]]:
        """Format calculation data for file output."""
        _data: list[list[int | float]] = []
        _hkl = self.hkl[_material]
        _bragg_edges = self.bragg_edges[_material]
        _d_spacing = self.d_spacing[_material]
        for index in range(len(_d_spacing)):
            _data.append([_hkl[index][0], _hkl[index][1], _hkl[index][2], _d_spacing[index], _bragg_edges[index]])
        return _data

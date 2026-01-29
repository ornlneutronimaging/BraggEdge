import ast
import configparser

import numpy as np

from ..config import config_file as config_config_file
from .structure_handler import HKL, CrystalStructure, StructureHandler


class BraggEdgeCalculator:
    """
    This class calculates the h, k, and l values allowed for the given structure.
    The number of h,k,l set is by default set to 10 but can be changed

    Args:
    structure_name: default 'FCC'. Must be either ['FCC', 'BCC']

    """

    _structure: CrystalStructure
    _number_of_set: int
    _list_structure: list[str]
    lattice: float | None
    hkl: list[HKL]
    bragg_edges: list[float]
    d_spacing: list[float]

    def __init__(
        self,
        structure_name: CrystalStructure = "FCC",
        lattice: float | None = None,
        number_of_set: int = 10,
    ) -> None:
        self.structure = structure_name  # only used to test validity of input
        self._structure = structure_name
        self._number_of_set = number_of_set
        self.lattice = lattice

    @property
    def structure(self) -> CrystalStructure:
        return self._structure

    @structure.setter
    def structure(self, structure_name: CrystalStructure) -> None:
        _config_file = config_config_file
        config_obj = configparser.ConfigParser()
        config_obj.read(_config_file)
        self._list_structure = ast.literal_eval(config_obj["DEFAULT"]["list_structure"])

        if structure_name not in self._list_structure:
            raise ValueError(f"Structure name should be in the list {self._list_structure}")
        self._structure = structure_name

    def calculate_hkl(self) -> None:
        _structure_handler = StructureHandler(structure=self._structure, number_of_set=self._number_of_set)
        self.hkl = _structure_handler.hkl

    def calculate_bragg_edges(self) -> None:
        """This calculate the d_spacing and bragg edges of the various h, k and l"""
        if self.lattice is None:
            raise ValueError

        _bragg_edges_array: list[float] = []
        _d_spacing: list[float] = []
        for _hkl in self.hkl:
            _result = self._calculate_individual_bragg_edge(lattice=self.lattice, h=_hkl[0], k=_hkl[1], l=_hkl[2])
            _d_spacing.append(_result)
            _bragg_edges_array.append(2.0 * _result)
        self.bragg_edges = _bragg_edges_array
        self.d_spacing = _d_spacing

    def _calculate_individual_bragg_edge(
        self,
        lattice: float | None = None,
        h: int = 1,
        k: int = 1,
        l: int = 1,
    ) -> float:
        _den = np.sqrt(h**2 + k**2 + l**2)
        return float(lattice) / _den

"""This file will handle work to retrieve the right h,k and l set of data for the various
structures
"""

from collections.abc import Generator
from typing import Literal

# from .braggedge_values_calculator import BraggEdgeValuesCalculator
MAX_INDEX = 30

# Type alias for Miller indices
HKL = list[int]  # [h, k, l]
CrystalStructure = Literal["BCC", "FCC"]


class BCCHandler:
    """BCC type handler

    For this type, h+k+l must be an even number

    """

    hkl: list[HKL]
    number_of_set: int

    def __init__(self, number_of_set: int) -> None:
        self.hkl = []
        self.number_of_set = number_of_set
        self.calculate_hkl()

    def _hkl_generator(self, number_of_h: int) -> Generator[HKL, None, None]:
        """generator that is used to produced the right hkl for cyrstal structure"""
        h, k, l = 1, 0, 0
        for h in range(1, number_of_h):
            for k in range(number_of_h):
                if k > h:
                    continue
                for l in range(number_of_h):
                    if l > k:
                        continue
                    _sum = h + k + l
                    if _sum % 2 == 0:
                        yield [h, k, l]

    def calculate_hkl(self) -> None:
        """calculate the list of hkl for BCC crystal structure"""
        _hkl_list = self._hkl_generator(MAX_INDEX)
        _result: list[HKL] = []
        for i in range(self.number_of_set):
            _result.append(next(_hkl_list))
        self.hkl = _result


class FCCHandler:
    """FCC type handler

    For this type, h, k and l must have the same parity

    """

    hkl: list[HKL]
    number_of_set: int

    def __init__(self, number_of_set: int) -> None:
        self.hkl = []
        self.number_of_set = number_of_set
        self.calculate_hkl()

    def _hkl_generator(self, number_of_h: int) -> Generator[HKL, None, None]:
        """generator used to produce right set of hkl parameters"""
        for h in range(1, number_of_h):
            for k in range(0, number_of_h):
                if k > h:
                    continue
                for l in range(0, number_of_h):
                    if l > k:
                        continue
                    if self._same_parity(h, k, l):
                        yield [h, k, l]

    def _same_parity(self, h: int, k: int, l: int) -> bool:
        """This function check if the 3 variables h, k, l have the same parity or not

        Args:
        h
        k
        l

        Return:
        True if h, k and l have the same parity
        False if h, k and l do not have the same parity

        """
        if (self._is_even(h) and self._is_even(k) and self._is_even(l)) or (
            not self._is_even(h) and not self._is_even(k) and not self._is_even(l)
        ):
            return True
        return False

    def _is_even(self, n: int) -> bool:
        """Check if a variable n is even

        Args:
        n variable to check

        Return:
        True if n is even
        False is n is odd
        """
        if n % 2 == 0:
            return True
        return False

    def calculate_hkl(self) -> None:
        """calculate the hkl allowed for a FCC crystal structure"""
        _hkl_list = self._hkl_generator(MAX_INDEX)
        _result: list[HKL] = []
        for i in range(self.number_of_set):
            _result.append(next(_hkl_list))
        self.hkl = _result


class StructureHandler:
    """Various structure handler"""

    hkl: list[HKL]
    structure: CrystalStructure
    number_of_set: int

    def __init__(self, structure: CrystalStructure, number_of_set: int = 10) -> None:
        if structure not in ["BCC", "FCC"]:
            raise ValueError("structure not implemented yet")

        self.structure = structure
        self.number_of_set = number_of_set

        _handler: BCCHandler | FCCHandler
        if structure == "FCC":
            _handler = FCCHandler(number_of_set=self.number_of_set)
        elif structure == "BCC":
            _handler = BCCHandler(number_of_set=self.number_of_set)

        self.hkl = _handler.hkl

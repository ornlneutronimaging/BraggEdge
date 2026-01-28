"""Tests for StructureHandler classes."""

import pytest

from neutronbraggedge.braggedges_handler.structure_handler import FCCHandler, StructureHandler


class TestStructureHandler:
    """Tests for structure handler functionality."""

    def test_calling_with_wrong_structure(self):
        """Calling an unknown structure raises an error."""
        with pytest.raises(ValueError):
            StructureHandler("HCC")

    def test_getting_the_right_first_hkl_for_BCC(self):
        """First h,k,l values are correct for BCC."""
        handler = StructureHandler("BCC", 1)
        list_hkl = handler.hkl
        assert list_hkl[0] == [1, 1, 0]

    def test_getting_the_right_amount_of_hkl_for_BCC(self):
        """Right number of hkl set is returned for BCC."""
        handler = StructureHandler("BCC", 10)
        list_hkl = handler.hkl
        nbr_hkl = len(list_hkl)
        assert nbr_hkl == 10

    def test_getting_the_right_first_hkl_value_for_BCC(self):
        """First few hkl set calculated are correct for BCC."""
        handler = StructureHandler("BCC", 10)
        list_hkl = handler.hkl
        assert list_hkl[1] == [2, 0, 0]
        assert list_hkl[2] == [2, 1, 1]
        assert list_hkl[3] == [2, 2, 0]
        assert list_hkl[4] == [2, 2, 2]

    def test_getting_the_right_amount_of_hkl_for_FCC(self):
        """Right number of hkl set is returned for FCC."""
        handler = StructureHandler("FCC", 10)
        list_hkl = handler.hkl
        nbr_hkl = len(list_hkl)
        assert nbr_hkl == 10

    def test_getting_the_right_first_hkl_value_for_FCC(self):
        """First few hkl set calculated are correct for FCC."""
        handler = StructureHandler("FCC", 10)
        list_hkl = handler.hkl
        assert list_hkl[0] == [1, 1, 1]
        assert list_hkl[1] == [2, 0, 0]
        assert list_hkl[2] == [2, 2, 0]
        assert list_hkl[3] == [2, 2, 2]
        assert list_hkl[4] == [3, 1, 1]

    def test_is_even_algorithm(self):
        """is_even algorithm is correct."""
        fcc = FCCHandler(10)
        assert fcc._is_even(0) is True
        assert fcc._is_even(1) is False

    def test_same_parity_algorithm(self):
        """same_parity algorithm is correct."""
        fcc = FCCHandler(10)
        assert fcc._same_parity(1, 1, 1) is True
        assert fcc._same_parity(1, 1, 2) is False

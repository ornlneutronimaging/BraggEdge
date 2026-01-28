"""Tests for BraggEdgeCalculator class."""

import pytest

from neutronbraggedge.braggedges_handler.braggedge_calculator import BraggEdgeCalculator


class TestBraggEdgeCalculator:
    """Tests for Bragg Edge calculator functionality."""

    def test_calling_without_arguments(self):
        """Class can be called with default arguments."""
        handler = BraggEdgeCalculator()
        assert handler.structure == "FCC"

    def test_braggedge_calculator_error_when_bad_structure_given(self):
        """Error is raised when bad structure given."""
        structure_name = "FakeStructure"
        with pytest.raises(ValueError):
            BraggEdgeCalculator(structure_name)

    def test_right_structure_name_is_passed_in_constructor(self):
        """Structure name passed in constructor is correctly used."""
        structure_name = "BCC"
        handler = BraggEdgeCalculator(structure_name=structure_name)
        assert handler.structure == "BCC"

    def test_right_structure_name_is_passed_in_assigned(self):
        """Structure name assigned is correctly saved."""
        structure_name = "BCC"
        handler = BraggEdgeCalculator()
        handler.structure = structure_name
        assert handler.structure == "BCC"

    def test_right_hkl_number_calculated_for_BCC(self):
        """Right number of hkl sets is returned for BCC."""
        structure_name = "BCC"
        handler = BraggEdgeCalculator(structure_name=structure_name, number_of_set=5)
        handler.calculate_hkl()
        hkl = handler.hkl
        assert len(hkl) == 5

    def test_right_hkl_number_calculated_for_FCC(self):
        """Right number of hkl sets is returned for FCC."""
        structure_name = "FCC"
        handler = BraggEdgeCalculator(structure_name=structure_name, number_of_set=5)
        handler.calculate_hkl()
        hkl = handler.hkl
        assert len(hkl) == 5

    def test_right_hkl_set_is_calculated_for_FCC(self):
        """Right set of hkl sets is returned for FCC."""
        structure_name = "FCC"
        handler = BraggEdgeCalculator(structure_name=structure_name, number_of_set=5)
        handler.calculate_hkl()
        hkl = handler.hkl
        assert hkl[0] == [1, 1, 1]
        assert hkl[1] == [2, 0, 0]
        assert hkl[2] == [2, 2, 0]
        assert hkl[3] == [2, 2, 2]
        assert hkl[4] == [3, 1, 1]

    def test_right_hkl_set_is_calculated_for_BCC(self):
        """Right set of hkl sets is returned for BCC."""
        structure_name = "BCC"
        handler = BraggEdgeCalculator(structure_name=structure_name, number_of_set=5)
        handler.calculate_hkl()
        hkl = handler.hkl
        assert hkl[0] == [1, 1, 0]
        assert hkl[1] == [2, 0, 0]
        assert hkl[2] == [2, 1, 1]
        assert hkl[3] == [2, 2, 0]
        assert hkl[4] == [2, 2, 2]

    def test_calculate_bragg_edges_algorithm_fail_when_no_lattice_given(self):
        """ValueError is correctly raised when no lattice is provided."""
        handler = BraggEdgeCalculator(structure_name="BCC")
        with pytest.raises(ValueError):
            handler.calculate_bragg_edges()

    def test_d_spacing_for_first_hkl_of_bcc(self):
        """d_spacing values for the first BCC structure are correct."""
        handler = BraggEdgeCalculator(structure_name="BCC", lattice=1.0)
        handler.calculate_hkl()
        handler.calculate_bragg_edges()
        assert handler.d_spacing[0] == pytest.approx(0.7071, abs=0.0001)
        assert handler.d_spacing[1] == pytest.approx(0.5, abs=0.0001)
        assert handler.d_spacing[2] == pytest.approx(0.4083, abs=0.0001)

    def test_bragg_edge_for_first_hkl_of_bcc(self):
        """Bragg edge values for the first BCC structure are correct."""
        handler = BraggEdgeCalculator(structure_name="BCC", lattice=1.0)
        handler.calculate_hkl()
        handler.calculate_bragg_edges()
        assert handler.bragg_edges[0] == pytest.approx(1.4142, abs=0.0001)
        assert handler.bragg_edges[1] == pytest.approx(1.0, abs=0.0001)
        assert handler.bragg_edges[2] == pytest.approx(0.8165, abs=0.0001)

    def test_d_spacing_for_first_hkl_of_fcc(self):
        """d_spacing values for the first FCC structure are correct."""
        handler = BraggEdgeCalculator(structure_name="FCC", lattice=1.0)
        handler.calculate_hkl()
        handler.calculate_bragg_edges()
        assert handler.d_spacing[0] == pytest.approx(1.1547 / 2.0, abs=0.0001)
        assert handler.d_spacing[1] == pytest.approx(1.0 / 2.0, abs=0.0001)
        assert handler.d_spacing[2] == pytest.approx(0.7071 / 2.0, abs=0.0001)

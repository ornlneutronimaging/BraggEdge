"""Tests for Lattice class."""

import math

import numpy as np
import pytest

from neutronbraggedge.lattice_handler.lattice import Lattice


class TestLattice:
    """Tests for lattice handling functionality."""

    def test_lattice_error_when_bad_structure_given(self):
        """Value Error is raised when bad structure given."""
        crystal_structure = "FakeStructure"
        with pytest.raises(ValueError):
            Lattice(None, crystal_structure)

    def test_correctly_hkl_returned_for_Si_3entries(self):
        """hkl array correctly calculated and reported for 3 entries."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1, 2, 3])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        hkl_expected = [[1, 1, 1], [2, 0, 0], [2, 2, 0]]
        assert o_lattice.hkl == hkl_expected

    def test_correctly_hkl_returned_for_Si_4entries_with_None(self):
        """hkl array correctly calculated and reported for 4 entries with None."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1, 2, None, 3])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        hkl_expected = [[1, 1, 1], [2, 0, 0], [2, 2, 0], [2, 2, 2]]
        assert o_lattice.hkl == hkl_expected

    def test_bragg_edge_crystal_structure_correctly_created(self):
        """Bragg edge crystal structure correctly created."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()

        expected_first_key = [1, 1, 1]
        expected_first_value = 1.1
        assert o_lattice.hkl_bragg_edge[0][0] == expected_first_key
        assert o_lattice.hkl_bragg_edge[0][1] == expected_first_value

        expected_second_key = [2, 0, 0]
        expected_second_value = 2.2
        assert o_lattice.hkl_bragg_edge[1][0] == expected_second_key
        assert o_lattice.hkl_bragg_edge[1][1] == expected_second_value

    def test_bragg_edge_crystal_structure_correctly_created_for_incomplete_list(self):
        """Bragg edge crystal structure correctly created for incomplete list."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1.1, None, None, 4.4])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()

        expected_first_key = [1, 1, 1]
        expected_first_value = 1.1
        assert o_lattice.hkl_bragg_edge[0][0] == expected_first_key
        assert o_lattice.hkl_bragg_edge[0][1] == expected_first_value

        expected_second_key = [2, 0, 0]
        assert o_lattice.hkl_bragg_edge[1][0] == expected_second_key
        assert math.isnan(o_lattice.hkl_bragg_edge[1][1])

    def test_hkl_bragg_edge_correctly_displayed(self):
        """hkl bragg edge correctly displayed."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        assert o_lattice.display_hkl_bragg_edge()

    def test_lattice_coefficient_correctly_calculated(self):
        """Lattice coefficient correctly calculated for [1,1,1]."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        assert len(bragg_edge_array) == len(o_lattice.lattice_array)
        assert o_lattice.lattice_array[0] == pytest.approx(0.952628, abs=0.00001)

    def test_lattice_statistics(self):
        """Lattice statistics correctly calculated for Si."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        o_lattice._calculate_lattice_statistics()
        statistics = o_lattice.lattice_statistics

        delta = 1e-4
        assert statistics["std"] == pytest.approx(2.549745, abs=delta)
        assert statistics["min"] == pytest.approx(0.952628, abs=delta)
        assert statistics["max"] == pytest.approx(7.621024, abs=delta)
        assert statistics["median"] == pytest.approx(3.433452, abs=delta)
        assert statistics["mean"][0] == pytest.approx(3.860139, abs=delta)

    def test_display_statistics(self):
        """Lattice statistics correctly displayed for Si."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        o_lattice._calculate_lattice_statistics()
        o_lattice.display_lattice_statistics()

    def test_display_recap(self):
        """Lattice recap displayed correctly."""
        material = "Si"
        crystal_structure = "FCC"
        bragg_edge_array = np.array([1.1, 2.2, 3.3, 4.4])
        o_lattice = Lattice(material=material, crystal_structure=crystal_structure, bragg_edge_array=bragg_edge_array)
        o_lattice._match_bragg_edge_with_hkl()
        o_lattice._calculate_lattice_array()
        o_lattice._calculate_lattice_statistics()
        o_lattice.display_recap()

"""Tests for BraggEdge class."""

import numpy as np
import pytest

from neutronbraggedge.braggedge import BraggEdge


class TestBraggEdge:
    """Tests for main BraggEdge functionality."""

    def test_raise_error_when_nothing_passed_in(self):
        """Error is raised when no material are passed in."""
        with pytest.raises(ValueError):
            BraggEdge()

    def test_raise_error_when_bad_new_material_input_format(self):
        """Error is raised when the new_material array format is wrong."""
        new_material = [{"wrong_name": "Ta", "wrong_lattice_constant": 34545}]
        with pytest.raises(ValueError):
            BraggEdge(None, new_material)

    def test_retrieve_correct_metadata_for_single_local_material(self):
        """Correct metadata are retrieved for a single local material."""
        new_material = [{"name": "Ta", "lattice": 0.5, "crystal_structure": "BCC"}]
        handler = BraggEdge(new_material=new_material)
        metadata = handler.metadata
        assert metadata["lattice"]["Ta"] == 0.5
        assert metadata["crystal_structure"]["Ta"] == "BCC"

    def test_retrieve_correct_metadata_for_multi_local_material(self):
        """Correct metadata are retrieved for a couple of local material."""
        new_material = [
            {"name": "Ta", "lattice": 0.5, "crystal_structure": "BCC"},
            {"name": "Ni", "lattice": 1.5, "crystal_structure": "FCC"},
        ]
        handler = BraggEdge(new_material=new_material)
        metadata = handler.metadata
        assert metadata["lattice"]["Ta"] == 0.5
        assert metadata["lattice"]["Ni"] == 1.5
        assert metadata["crystal_structure"]["Ta"] == "BCC"
        assert metadata["crystal_structure"]["Ni"] == "FCC"

    def test_calculate_d_spacing_for_single_local_material(self):
        """d_spacing calculation is correct for a single local material."""
        new_material = [{"name": "Ta", "lattice": 5.0, "crystal_structure": "BCC"}]
        handler = BraggEdge(new_material=new_material)
        d_spacing = handler.d_spacing
        assert d_spacing["Ta"][0] == pytest.approx(3.5355, abs=0.0001)

    def test_calculate_hkl_for_single_local_material(self):
        """hkl calculation is correct for a single local material."""
        new_material = [{"name": "Ta", "lattice": 5.0, "crystal_structure": "BCC"}]
        handler = BraggEdge(new_material=new_material)
        hkl = handler.hkl
        assert hkl["Ta"][0] == [1, 1, 0]
        assert hkl["Ta"][1] == [2, 0, 0]

    def test_retrieving_correct_metadata_for_Ni(self):
        """Correct metadata are returned for Ni."""
        handler = BraggEdge(material="Ni")
        metadata = handler.metadata
        assert metadata["lattice"]["Ni"] == pytest.approx(3.5238, abs=0.01)
        assert metadata["crystal_structure"]["Ni"] == "FCC"

    def test_retrieving_correct_number_and_first_2_values_hkl_for_Si(self):
        """Correct hkl first 2 values are returned for Si, and the correct number."""
        handler = BraggEdge(material="Si", number_of_bragg_edges=4)
        hkl = handler.hkl["Si"]
        assert hkl[0] == [1, 1, 1]
        assert hkl[1] == [2, 0, 0]
        assert len(hkl) == 4

    def test_calculating_d_spacing_values_for_Ni(self):
        """First 3 d_spacing are correct for Ni."""
        handler = BraggEdge(material="Ni", number_of_bragg_edges=4)
        d_spacing = handler.d_spacing["Ni"]
        assert d_spacing[0] == pytest.approx(2.0345, abs=0.001)
        assert d_spacing[1] == pytest.approx(1.7619, abs=0.001)
        assert d_spacing[2] == pytest.approx(1.2459, abs=0.001)

    def test_retrieving_first_2_values_hkl_for_Fe(self):
        """Correct hkl first 2 values are returned for Fe."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        hkl = handler.hkl["Fe"]
        assert hkl[0] == [1, 1, 0]
        assert hkl[1] == [2, 0, 0]
        assert hkl[2] == [2, 1, 1]
        assert hkl[3] == [2, 2, 0]

    def test_calculating_bragg_edges_for_Fe(self):
        """First 3 bragg_edges are correct for Fe."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        bragg_edges = handler.bragg_edges["Fe"]
        assert bragg_edges[0] == pytest.approx(4.0537, abs=0.001)
        assert bragg_edges[1] == pytest.approx(2.8664, abs=0.001)
        assert bragg_edges[2] == pytest.approx(2.3404, abs=0.001)

    def test_printing_report(self):
        """metadata/hkl/braggedges are correctly output."""
        # Just verify no exception is raised
        BraggEdge(material="Ni", number_of_bragg_edges=5)

    def test_create_export_csv_no_file_raise_error(self):
        """IOError is raised when no file name given."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        with pytest.raises(IOError):
            handler.export()

    def test_create_export_csv_metadata(self):
        """Correct metadata data are created for Fe when using create output file."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        metadata = handler._format_metadata("Fe")
        assert metadata[0] == "Material: Fe"
        assert metadata[1] == "Lattice : 2.8664Angstroms"
        assert metadata[2] == "Crystal Structure: BCC"
        assert metadata[3] == "Using local metadata Table: True"

    def test_create_export_csv_data(self):
        """Correct data are created for Fe when using create output file."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        data = handler._format_data("Fe")
        assert data[0][0] == 1
        assert data[0][3] == pytest.approx(2.02685, abs=0.0001)
        assert data[0][4] == pytest.approx(4.05370, abs=0.0001)
        assert data[2][3] == pytest.approx(1.17020, abs=0.0001)
        assert data[2][4] == pytest.approx(2.34041, abs=0.0001)

    def test_create_export_csv_file_created(self, tmp_path):
        """Correct output CSV file is created."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        filename = str(tmp_path / "test_output.txt")
        handler.export(filename=filename, file_type="csv")
        expected_file = tmp_path / "test_output_Fe.txt"
        assert expected_file.is_file()

    def test_create_export_unsuported_file_raise_error(self):
        """NotImplementedError raised when trying to create unsupported output format."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        filename = "remove_me_Fe.txt"
        with pytest.raises(NotImplementedError):
            handler.export(filename, "do_not_exist_yet")

    def test_calculate_experimental_lattice_with_no_input_provided(self):
        """ValueError raised if no experimental bragg edge array provided."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        with pytest.raises(ValueError):
            handler.get_experimental_lattice_parameter()

    def test_calculate_experimental_lattice_with_value_and_error_different_size(self):
        """Bragg edge value and error have different sizes raises ValueError."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        exp_bragg_value = np.array([1, 2, 3])
        exp_bragg_error = np.array([0.1, 0.2])
        with pytest.raises(ValueError):
            handler.get_experimental_lattice_parameter(exp_bragg_value, exp_bragg_error)

    def test_calculate_experimental_lattice_raises_not_implemented_error(self):
        """NotImplementedError raised when calling get_experimental_lattice_parameter with valid inputs.

        This method is not yet implemented and should raise NotImplementedError
        directing users to use the Lattice class directly.
        """
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        exp_bragg_value = np.array([4.0537, 2.8664, 2.3404, 2.0269])
        exp_bragg_error = np.array([0.001, 0.001, 0.001, 0.001])
        with pytest.raises(NotImplementedError):
            handler.get_experimental_lattice_parameter(exp_bragg_value, exp_bragg_error)

    def test_loading_single_material_in_list(self):
        """Single element Al data listed in a list correctly calculated."""
        # Just verify no exception is raised
        BraggEdge(material=["Al"], number_of_bragg_edges=4)

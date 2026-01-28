"""Tests for RetrieveMaterialMetadata class."""

import pytest

from neutronbraggedge.material_handler.retrieve_material_metadata import RetrieveMaterialMetadata


class TestRetrieveMaterialMetadata:
    """Tests for retrieving material metadata from local and web sources."""

    def test_retrieve_lattice_of_si_via_web(self):
        """Value of lattice retrieved from Si via web table."""
        retrieve_material = RetrieveMaterialMetadata(material="Si", use_local_table=False)
        lattice_expected = 5.431
        assert retrieve_material.lattice == pytest.approx(lattice_expected, abs=0.001)

    def test_retrieve_lattice_of_si_via_local_table(self):
        """Value of lattice retrieved from Si via local table."""
        retrieve_material = RetrieveMaterialMetadata(material="Si", use_local_table=True)
        lattice_expected = 5.431591  # higher precision on local table
        assert retrieve_material.lattice == lattice_expected

    def test_raise_name_error_no_arguments(self):
        """NameError is raised when no arguments is given."""
        with pytest.raises(NameError):
            RetrieveMaterialMetadata()

    def test_raise_key_error_material_unknown(self):
        """KeyError is raised if material is unknown."""
        with pytest.raises(KeyError):
            RetrieveMaterialMetadata("unknown")

    def test_retrieving_full_list_of_material(self):
        """Full list of material available returned."""
        retrieve_material = RetrieveMaterialMetadata(material="all", use_local_table=False)

        list_returned = retrieve_material.full_list_material()
        # Check that expected materials are present (Wikipedia content may change order)
        expected_materials = ["C (diamond)", "Si", "Ge"]
        for material in expected_materials:
            assert material in list_returned

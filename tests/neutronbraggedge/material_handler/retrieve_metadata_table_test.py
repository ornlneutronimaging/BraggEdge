"""Tests for RetrieveMetadataTable class."""

import pytest

from neutronbraggedge.material_handler.retrieve_metadata_table import RetrieveMetadataTable


class TestRetrieveMetadataTable:
    """Tests for retrieving metadata tables."""

    @pytest.mark.skip(reason="Not using the url database right now")
    def test_retrieve_table_from_url(self):
        """Check if the table is correctly loaded from URL."""
        retrieve_meta = RetrieveMetadataTable(use_local_table=False)
        table = retrieve_meta.get_table()
        shape = table.shape

        nbr_column = 3
        assert shape[1] == nbr_column

        value_0_0 = "Diamond (FCC)"
        assert table.values[0][1] == value_0_0

    def test_retrieve_local_table(self):
        """Check if the local table is correctly loaded."""
        retrieve_meta = RetrieveMetadataTable()
        table = retrieve_meta.get_table()
        shape = table.shape

        nbr_column = 3
        assert shape[1] == nbr_column

        value_0_0 = "Diamond (FCC)"
        assert table.values[0][1] == value_0_0

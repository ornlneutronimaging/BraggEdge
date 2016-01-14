import unittest
import os
from python.braggedge import config
from python.braggedge.retrieve_metadata_table import RetrieveMetadataTable


class TestRetrieveMetadataTable(unittest.TestCase):

    def setUp(self):
        _config_file = config.config_file
        self._config_file = os.path.abspath(_config_file)

    def test_retrieve_table(self):
        """checking if table is the right one by checking a few labels"""
        retrieve_meta = RetrieveMetadataTable()
        retrieve_meta.retrieve_table()
        table_raw = retrieve_meta.raw_table

        first_element_should_be = 'Material'
        first_element_is = table_raw[0][0]
        self.assertEqual(first_element_is, first_element_should_be)

        last_element_should_be = 'Ref'
        last_element_is = table_raw[3][0]
        self.assertEqual(last_element_is, last_element_should_be)

    def test_reformated_table(self):
        """checking that the table has been correctly reformated"""
        retrieve_meta = RetrieveMetadataTable()
        retrieve_meta.retrieve_table()
        retrieve_meta.format_table()
        _table = retrieve_meta.get_table()
        _shape = _table.shape

        nbr_column = 3
        self.assertEqual(_shape[1], nbr_column)
        
        value_0_0 = 'Diamond (FCC)'
        self.assertEqual(value_0_0, _table.values[0][1])


if __name__ == '__main__':
    unittest.main()

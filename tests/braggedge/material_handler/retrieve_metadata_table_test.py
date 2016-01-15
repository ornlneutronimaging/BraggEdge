import unittest
import os
from python.braggedge.material_handler import config
from python.braggedge.material_handler.retrieve_metadata_table import RetrieveMetadataTable
#from braggedge import config
#from braggedge import material_hanlder



class TestRetrieveMetadataTable(unittest.TestCase):

    def setUp(self):
        _config_file = config.config_file
        self._config_file = os.path.abspath(_config_file)

    def test_retrieve_table_from_url(self):
        """checking if the table is correctly loaded from URL"""
       
        retrieve_meta = RetrieveMetadataTable()
        _table = retrieve_meta.get_table()
        _shape = _table.shape

        nbr_column = 3
        self.assertEqual(_shape[1], nbr_column)
        
        value_0_0 = 'Diamond (FCC)'
        self.assertEqual(value_0_0, _table.values[0][1])

    def test_retrieve_table_from_local(self):
        """checking the local table can be retrieved"""
        pass


if __name__ == '__main__':
    unittest.main()

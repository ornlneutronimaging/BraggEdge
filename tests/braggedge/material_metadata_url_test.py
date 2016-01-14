import unittest
import os
from python.braggedge import config


class TestMaterialMetadataURL(unittest.TestCase):

    def setUp(self):
        _config_file = config.config_file
        self._config_file = os.path.abspath(_config_file)

    #def test_file_exist(self):
        #"""Checking if config file can be read"""
        #self.assertTrue(os.path.isfile(self._config_file))

    #def test_table_retrieved(self):
        #"""This will check that the link is correct by retrieving the right table"""
        #import configparser
        #import pandas as pd
        #config = configparser.ConfigParser()
        #config.read(self._config_file)
        #url = config['DEFAULT']['material_metadata_url']
        #table_list = pd.read_html(url)
        #self.assertEqual(len(table_list), 1)

if __name__ == '__main__':
    unittest.main()

import unittest
import os

class TestMaterialMetadataURL(unittest.TestCase):

    def setUp(self):
        _config_file = 'config.cfg'
        self._config_file = os.path.abspath(_config_file)

    def test_file_exist(self):
        """Checking if config file can be read"""
        self.assertTrue(os.path.isfile(self._config_file))

    def test_url_link(self):
        """This will check that the url works"""
        import configparser
        import pandas as pd
        config = configparser.ConfigParser()
        config.read(self._config_file)
        url = config['DEFAULT']['material_metadata_url']
        table_list = pd.read_html(url)
        self.assertEqual(len(table_list), 1)

if __name__ == '__main__':
    unittest.main()

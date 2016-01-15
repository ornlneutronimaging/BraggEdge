"""
This class will retrieve the table from the URL and reformat it to be able to 
quickly retrieve the metadata for a given material
"""

import pandas as pd
import configparser
from python.braggedge.material_handler import config
#import config


class RetrieveMetadataTable(object):
    """ Metadata table retriever """
    
    def __init__(self):
        self._retrieve_url()
        
    def _retrieve_url(self):
        self._config_file = config.config_file
        config_obj = configparser.ConfigParser()
        config_obj.read(self._config_file)
        self.url = config_obj['DEFAULT']['material_metadata_url']
        
    def retrieve_table(self):
        try:
            self.retrieve_table_from_url()
        except:
            self.retrieve_table_local()
            
    def retrieve_table_local(self):
        pass


    def retrieve_table_from_url(self):
        table_list = pd.read_html(self.url)
        self.raw_table = table_list[0]
        self.format_table_from_url()
        
    def format_table_from_url(self):
        _table = self.raw_table
        _table.columns = _table.values[0][:]
        _table = _table[1:]
        _table = _table.set_index('Material')
        self.table = _table

    def get_table(self):
        self.retrieve_table()
        return self.table
        
if __name__ == '__main__':
    retrieve_meta = RetrieveMetadataTable()
    _table = retrieve_meta.get_table()

 #   retrieve_meta.format_table()
#    _table = retrieve_meta.get_table()
#    print(_table.values[0][1])
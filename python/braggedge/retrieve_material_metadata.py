"""
This class will automatically retrieve the lattice parameter and the crystal structure of a given
element
"""


class RetrieveMaterialMetadata(object):
    """ Retrieve the metadata for a given material """
    
    def __init__(self, material=None):
        self._material = material
        
    def _retrieve_table(self):
        """retrieve the table using the url defined in the config file"""
        metadata_table = RetrieveMetadataTable()
        table = metadata_table.get_table()
        
        
        
        
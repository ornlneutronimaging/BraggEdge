from .material_handler.retrieve_material_metadata import RetrieveMaterialMetadata


class BraggEdge(object):
    """This is from where the user will retrieve all metadtaa and calculation"""
    
    def __init__(self, material=None, 
                 number_of_bragg_edges=10, 
                 use_local_metadata_table=True):

        self.material = material
        self.number_of_bragg_edges = number_of_bragg_edges
        self.use_local_metadata_table = use_local_metadata_table
        
        self.retrieve_metadata()
        self.retrieve_hkl()
        
    def retrieve_metadata(self):
        _handler = RetrieveMaterialMetadata(material = self.material,
                                            use_local_table = self.use_local_metadata_table)
        self.lattice = _handler.lattice
        self.crystal_structure = _handler.crystal_structure
    
        self.metadata = {'lattice': self.lattice, 
                'crystal_structure': self.crystal_structure}

    def retrieve_hkl(self):
        pass
        
    def __repr__(self):
        """This will display the metadata/hkl/d_spacing/bragg edge values"""
        raise NotImplementedError
    
    
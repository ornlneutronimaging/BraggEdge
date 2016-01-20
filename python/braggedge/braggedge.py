from .material_handler.retrieve_material_metadata import RetrieveMaterialMetadata
from .braggedges_handler.braggedge_calculator import BraggEdgeCalculator


class BraggEdge(object):
    """This is from where the user will retrieve all metadtaa and calculation"""
    
    def __init__(self, material=None, 
                 number_of_bragg_edges=10, 
                 use_local_metadata_table=True):

        self.material = material
        self.number_of_bragg_edges = number_of_bragg_edges
        self.use_local_metadata_table = use_local_metadata_table
        
        self.retrieve_metadata()
        self.calculate_hkl()
        self.calculate_braggedges()
        
    def retrieve_metadata(self):
        """This method retrieves the lattice and crystal structure of the material"""
        _handler = RetrieveMaterialMetadata(material = self.material,
                                            use_local_table = self.use_local_metadata_table)
        self.lattice = _handler.lattice
        self.crystal_structure = _handler.crystal_structure
    
        self.metadata = {'lattice': self.lattice, 
                'crystal_structure': self.crystal_structure}

    def calculate_hkl(self):
        """This method calculate the set of hkl up to the number_of_bragg_edges specified"""
        _calculator = BraggEdgeCalculator(structure_name = self.metadata['crystal_structure'],
                                          lattice = self.metadata['lattice'],
                                          number_of_set = self.number_of_bragg_edges)
        _calculator.calculate_hkl()
        self._calculator = _calculator
        self.hkl = _calculator.hkl

    def calculate_braggedges(self):
        """This method calculate the braggedges values (and the d_spacing in the same time)"""
        _calculator = self._calculator
        _calculator.calculate_bragg_edges()
        self.d_spacing = _calculator.d_spacing
        self.bragg_edges = _calculator.bragg_edges
        
    def __repr__(self):
        """This will display the metadata/hkl/d_spacing/bragg edge values"""
        raise NotImplementedError
    
    
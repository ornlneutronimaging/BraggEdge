import sys
from .structure_handler import StructureHandler


class BraggEdgeValuesCalculator(object):
    """
    This class calculates the h, k, and l values allowed for the given structure.
    The number of h,k,l set is by default set to 10 but can be changed
    
    Args:
    structure_name: default 'FCC'. Must be either ['FCC', 'BCC']
    
    """
    
    _list_structure = ['FCC', 'BCC']

    def __init__(self, structure_name="FCC"):
        self._structure = structure_name
            
    @property
    def structure(self):
        return self._structure
    
    @structure.setter
    def structure(self, structure_name):
        if not (structure_name in self._list_structure):
            raise ValueError("Structure name should be in the list " , self._list_structure)
        self._structure = structure_name
        
    def get_hkl(self):
        _structure_handler = StructureHandler(structure = structure,
            number_of_set = number_of_set)      
        return _structure_handler.get_hkl()
            
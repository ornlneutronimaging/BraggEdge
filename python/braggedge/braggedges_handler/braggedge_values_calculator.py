import sys


class BraggEdgeValuesCalculator(object):
    
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
        
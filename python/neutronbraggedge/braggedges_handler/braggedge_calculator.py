import sys
import numpy as np
import configparser
from .structure_handler import StructureHandler
from ..config import config_file as config_config_file


class BraggEdgeCalculator(object):
    """
    This class calculates the h, k, and l values allowed for the given structure.
    The number of h,k,l set is by default set to 10 but can be changed
    
    Args:
    structure_name: default 'FCC'. Must be either ['FCC', 'BCC']
    
    """
    
    def __init__(self, structure_name="FCC", lattice=None, number_of_set=10):
        self.structure = structure_name #only used to test validity of input
        self._structure = structure_name
        self._number_of_set = number_of_set
        self.lattice = lattice

    @property
    def structure(self):
        return self._structure
    
    @structure.setter
    def structure(self, structure_name):
        
        _config_file = config_config_file
        print(_config_file)
        config_obj = configparser.ConfigParser()
        config_obj.read(_config_file)
        self._list_structure = config_obj['DEFAULT']['list_structure']
        
        if not (structure_name in self._list_structure):
            raise ValueError("Structure name should be in the list " , self._list_structure)
        self._structure = structure_name
        
    def calculate_hkl(self):
        _structure_handler = StructureHandler(structure = self._structure,
            number_of_set = self._number_of_set)      
        self.hkl = _structure_handler.hkl
        
    def calculate_bragg_edges(self):
        """This calculate the d_spacing and bragg edges of the various h, k and l"""
        if self.lattice is None:
            raise ValueError
        
        _bragg_edges_array = []
        _d_spacing = []
        for _hkl in self.hkl:
            _result = self._calculate_individual_bragg_edge(lattice = self.lattice,
                                                            h = _hkl[0],
                                                            k = _hkl[1],
                                                            l = _hkl[2])
            _d_spacing.append(_result)
            _bragg_edges_array.append(2. * _result)
        self.bragg_edges = _bragg_edges_array
        self.d_spacing = _d_spacing
            
    def _calculate_individual_bragg_edge(self, lattice=None,
                                         h=1, k=1, l=1):
        _den = np.sqrt(h**2 + k**2 + l**2)
        return float(lattice)/_den
        

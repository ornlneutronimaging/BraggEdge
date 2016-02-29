import numpy as np
import configparser
from ..config import config_file as config_config_file
from ..braggedges_handler.braggedge_calculator import BraggEdgeCalculator


class Lattice(object):
    """When the Bragg Edges, crystal structure and hkl are known, this class calculates the
    lattice parameter
    """
    
    material = None
    crystal_structure = None
    use_local_metadata = True
    bragg_edge_array = None
    
    def __init__(self, material=None, 
                 crystal_structure=None, 
                 bragg_edge_array=None,
                 use_local_metadata_table=True):
        
        self.material = material
        self._crystal_structure = crystal_structure  
        self.crystal_structure = crystal_structure #only used to run test
        self.use_local_metadata = use_local_metadata_table
        self.bragg_edge_array = bragg_edge_array
    
        #retrieve hkl
        o_bragg_calculator = BraggEdgeCalculator(structure_name = crystal_structure, 
                                                lattice = None, 
                                                number_of_set = len(bragg_edge_array))
        o_bragg_calculator.calculate_hkl()
        self.hkl = o_bragg_calculator.hkl
    
    @property
    def crystal_structure(self):
        return self._crystal_structure
    
    @crystal_structure.setter
    def crystal_structure(self, structure_name):
        _config_file = config_config_file
        config_obj = configparser.ConfigParser()
        config_obj.read(_config_file)
        self._list_structure = config_obj['DEFAULT']['list_structure']
        
        if not (structure_name in self._list_structure):
            raise ValueError("Structure name should be in the list " , self._list_structure)
        self._crystal_structure = structure_name
        
    def calculate(self):
        """calculate the lattice parameters step by step"""
        self._match_bragg_edge_with_hkl()
        self._calculate_lattice_array()

    def _match_bragg_edge_with_hkl(self):
        """Match each bragg edge with its equivalent hkl"""
        _bragg_edge_array = self.bragg_edge_array
        if not (type(_bragg_edge_array) is np.ndarray):
            raise TypeError("Type of array not supported, make sure the array is of type Numpy!")
        
        zipped = zip(self.hkl, _bragg_edge_array)
        self.hkl_bragg_edge = list(zipped)
        
    def display_hkl_bragg_edge(self):
        """Display the hkl_bragg_edge list using pretty table form"""
        print("hkl Bragg Edge Table")
        print("=============================")
        print("hkl \t\t Bragg Edge")
        print("-----------------------------")
        for _row in self.hkl_bragg_edge:
            _key = _row[0]
            _value = _row[1]
            print("%r\t %.4f" %(_key, _value))
        print("-----------------------------")
        return True

    def _calculate_lattice_array(self):
        """Calculate the array of lattice parameters"""
        _hkl_bragg_edge = self.hkl_bragg_edge
        _lattice_array = []
        for _row in _hkl_bragg_edge:
            _hkl = _row[0]
            _bragg_edge = _row[1]
            _lattice = self._calculate_lattice_coefficient(hkl = _hkl,
                                                          bragg_edge = _bragg_edge)
            _lattice_array.append(_lattice)
        self.lattice_array = _lattice_array
            
    def _calculate_lattice_coefficient(self, hkl=None, bragg_edge=None):
        """Calculate the lattice coefficient for the given set of hkl and bragg edge"""
        _h, _k, _l = hkl
        _term1 = np.sqrt(_h**2 + _k**2 + _l**2)
        _term2 = bragg_edge/2.
        
        _lattice = _term2 * _term1
        return _lattice
        
        
        
    
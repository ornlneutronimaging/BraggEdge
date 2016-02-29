import numpy as np
import configparser
from ..config import config_file as config_config_file
from ..braggedges_handler.braggedge_calculator import BraggEdgeCalculator


class Lattice(object):
    """When the Bragg Edges, crystal structure and hkl are known, this class calculates the
    lattice parameter
    """
    
    space = 50
    
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
        self.bragg_edge_array = self._format_array(bragg_edge_array)
    
        #retrieve hkl
        o_bragg_calculator = BraggEdgeCalculator(structure_name = crystal_structure, 
                                                lattice = None, 
                                                number_of_set = len(bragg_edge_array))
        o_bragg_calculator.calculate_hkl()
        self.hkl = o_bragg_calculator.hkl
        
        self.calculate()
    
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
        
    def _format_array(self, bragg_edge_array):
        """Make sure that None value are replaced by np.NaN"""
        _bragg_edge_array_formated = []
        for _value in bragg_edge_array:
            if _value is None:
                _value = np.NaN
            _bragg_edge_array_formated.append(_value)
        _bragg_edge_array_formated = np.array(_bragg_edge_array_formated)
        return _bragg_edge_array_formated
        
    def calculate(self):
        """calculate the lattice parameters step by step"""
        self._match_bragg_edge_with_hkl()
        self._calculate_lattice_array()
        self._calculate_lattice_statistics()

    def _match_bragg_edge_with_hkl(self):
        """Match each bragg edge with its equivalent hkl"""
        _bragg_edge_array = self.bragg_edge_array
        
        zipped = zip(self.hkl, _bragg_edge_array)
        self.hkl_bragg_edge = list(zipped)
        
    def display_hkl_bragg_edge(self):
        """Display the hkl_bragg_edge list using pretty table form"""
        print("hkl Bragg Edge Table")
        print("=" * self.space)
        print("hkl \t\t Bragg Edge \t Lattice")
        print("-" * self.space)
        _lattice_array = self.lattice_array
        for _index, _row in enumerate(self.hkl_bragg_edge):
            _key = _row[0]
            _value = _row[1]
            _lattice = _lattice_array[_index]
            print("%r\t %.4f\t\t %.4f" %(_key, _value, _lattice))
        print("-" * self.space)
        print()
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
    
    def _calculate_lattice_statistics(self):
        """Calculate the statistics of the lattice array
        - median 
        - average
        - mean
        - std (standard deviation)
        - min
        - max
        """
        _lattice_statistics = {}
        
        #min
        _min = np.nanmin(self.lattice_array)
        _lattice_statistics['min'] = _min
        
        #max
        _max = np.nanmax(self.lattice_array)
        _lattice_statistics['max'] = _max
        
        #median
        _median = np.nanmedian(self.lattice_array)
        _lattice_statistics['median'] = _median
        
        #mean
        _mean = np.nanmean(self.lattice_array)
        _lattice_statistics['mean'] = _mean
        
        #std
        _std = np.nanstd(self.lattice_array)
        _lattice_statistics['std'] = _std
        
        self.lattice_statistics = _lattice_statistics
        
    def display_lattice_statistics(self):
        """Display the lattice statistics using a pretty table form"""
        _lattice_statistics = self.lattice_statistics
        print("Lattice Statistics")
        print("=" * self.space)
        print("min: %.5f" %_lattice_statistics['min'])
        print("max: %.5f" %_lattice_statistics['max'])
        print("median: %.5f" %_lattice_statistics['median'])
        print("mean: %.5f" %_lattice_statistics['mean'])
        print("std: %.5f" %_lattice_statistics['std'])
        print("-" * self.space)
        print("")
    
    def display_recap(self):
        print(" -- Recap --")
        print("=" * self.space)
        print("Material: %r" %self.material)
        print("Crystal Structure: %r" %self._crystal_structure)
        print("-" * self.space)
        print("")
        
        self.display_hkl_bragg_edge()
        self.display_lattice_statistics()
        
        
"""This file will handle work to retrieve the right h,k and l set of data for the various
structures
"""
#from .braggedge_values_calculator import BraggEdgeValuesCalculator
MAX_INDEX = 30

class BCCHandler(object):
    """BCC type handler
    
    For this type, h+k+l must be an even number
    
    """
    
    hkl = []
    
    def __init__(self, number_of_set):
        self.number_of_set = number_of_set
        self.calculate_hkl()

    def calculate_hkl(self):
        index = 0
        _hkl = []
        for h in range(1, MAX_INDEX):
            for k in range(0, MAX_INDEX):
                for l in range(0, MAX_INDEX):
                    if ((h + k + l) % 2 == 1) and (h >= k) and (k >= l):
                        _hkl.append([h, k, l])
                        index += 1
                        if index >= self.number_of_set:
                            self.hkl = _hkl
                            return
        

class FCCHandler(object):
    """FCC type handler"""
    
    hkl = []
    
    def __init__(self, number_of_set):
        self_number_of_set = number_of_set
        
class StructureHandler(object):
    """Various structure handler"""
    
    hkl = []
    
    def __init__(self, structure, number_of_set = 10):
        if not (structure in ["BCC", "FCC"]):
            raise ValueError("structure not implemented yet")

        self.structure = structure
        self.number_of_set = number_of_set
        
        if structure is 'FCC':
            _handler = FCCHandler(number_of_set = self.number_of_set)
        elif structure is 'BCC':
            _handler = BCCHandler(number_of_set = self.number_of_set)

        self.hkl = _handler.hkl
        

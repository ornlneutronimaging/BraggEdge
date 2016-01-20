"""This file will handle work to retrieve the right h,k and l set of data for the various
structures
"""
#from .braggedge_values_calculator import BraggEdgeValuesCalculator
MAX_INDEX = 30

class BCCHandler(object):
    """BCC type handler
    
    For this type, h+k+l must be an even number
    
    """
    
    def __init__(self, number_of_set):
        self.hkl = []
        self.number_of_set = number_of_set
        self.calculate_hkl()

    def _hkl_generator(self, number_of_h):
        h, k, l = 1, 0, 0
        for h in range(1, number_of_h):
            for k in range(number_of_h):
                if k > h:
                    continue
                for l in range(number_of_h):
                    if l > k:
                        continue
                    _sum = h + k + l
                    if _sum % 2 == 1:
                        yield [h, k, l]
        
    def calculate_hkl(self):
        _hkl_list = self._hkl_generator(20)
        _result = []
        for i in range(self.number_of_set):
            _result.append(next(_hkl_list))
            print(_result)
        self.hkl = _result


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
        

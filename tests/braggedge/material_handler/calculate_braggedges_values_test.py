import unittest
import os
from braggedge.braggedges_handler.braggedge_values_calculator import BraggEdgeValuesCalculator


class TestBraggEdgesHandler(unittest.TestCase):

    def setUp(self):
        pass

    def test_calling_without_arguments(self):
        """Testing that class can be called with default arguments from python2 and 3"""
        _handler = BraggEdgeValuesCalculator()
        self.assertEqual("FCC", _handler.structure)
        
    def test_right_structure_name_is_passed_in_constructor(self):
        """Assert that structure name passed in constructor is correctly used"""
        _structure_name = "BCC"
        _handler = BraggEdgeValuesCalculator(structure_name = _structure_name)
        self.assertEqual("BCC", _handler.structure)
        
    def test_right_structure_name_is_passed_in_assigned(self):
        """Assert that structure name assigned is correctly saved"""
        _structure_name = "BCC"
        _handler = BraggEdgeValuesCalculator()
        _handler.structure = _structure_name
        self.assertEqual("BCC", _handler.structure)


if __name__ == '__main__':
    unittest.main()

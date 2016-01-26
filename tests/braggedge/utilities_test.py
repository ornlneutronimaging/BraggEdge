import unittest
import os
import numpy as np
from python.braggedge.utilities import Utilities


class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert_time_units_raise_value_error_when_no_data_provided(self):
        """Assert in utilities - ValueError raised when no data provided"""
        self.assertRaises(ValueError, Utilities.convert_time_units)
    
    def test_convert_time_units_raise_value_error_when_units_not_supported(self):
        """Assert in utilities - ValueError raised when no units converted"""
        self.assertRaises(ValueError, Utilities.convert_time_units, 45, 'bad_units', 's')
        self.assertRaises(ValueError, Utilities.convert_time_units, 45, 's', 'bad_units')
        self.assertRaises(ValueError, Utilities.convert_time_units, 45, 'bad_units', 'bad_units')

    def test_convert_time_units_single_value(self):
        """Assert in utilities - converting single time units value"""
        pass
    

if __name__ == '__main__':
    unittest.main()

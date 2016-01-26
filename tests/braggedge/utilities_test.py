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

    def test_get_time_conversion_coeff(self):
        """Assert in utilities - correct time coefficient are returned"""
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 's', 
                                                                to_units = 's'))
        self.assertEqual(1.e3, Utilities.get_time_conversion_coeff(from_units = 's',
                                                                   to_units = 'ms'))
        self.assertEqual(1.e6, Utilities.get_time_conversion_coeff(from_units = 's',
                                                                   to_units = 'micros'))
        self.assertEqual(1.e9, Utilities.get_time_conversion_coeff(from_units = 's',
                                                                   to_units = 'ns'))
        
        self.assertEqual(1.e-3, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                   to_units = 's'))
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                to_units = 'ms'))
        self.assertEqual(1e3, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                to_units = 'micros'))
        self.assertEqual(1e6, Utilities.get_time_conversion_coeff(from_units = 'ms',
                                                                to_units = 'ns'))

        self.assertEqual(1.e-6, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                   to_units = 's'))
        self.assertEqual(1.e-3, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                to_units = 'ms'))
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                to_units = 'micros'))
        self.assertEqual(1e3, Utilities.get_time_conversion_coeff(from_units = 'micros',
                                                                to_units = 'ns'))

        self.assertEqual(1e-9, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 's'))
        self.assertEqual(1e-6, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 'ms'))
        self.assertEqual(1e-3, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 'micros'))
        self.assertEqual(1, Utilities.get_time_conversion_coeff(from_units = 'ns',
                                                                to_units = 'ns'))
        
    def test_get_time_conversion_raise_error(self):
        """Assert in utilities - ValueError is raised when wrong units given"""
        self.assertRaises(ValueError, Utilities.get_time_conversion_coeff, 's', 'bad_units')
        self.assertRaises(ValueError, Utilities.get_time_conversion_coeff, 'bad_units', 's')
        self.assertRaises(ValueError, Utilities.get_time_conversion_coeff, 'bad_units', 'bad_units')


    def test_convert_time_units_single_value(self):
        """Assert in utilities - converting single time units value"""
        self.assertEqual(5, Utilities.convert_time_units(data = 5,
                                                         from_units = 's',
                                                         to_units = 's'))
        self.assertAlmostEqual(15.e-6, Utilities.convert_time_units(data = 15.,
                                                         from_units = 'micros',
                                                         to_units = 's'),
                               delta = 0.00001)
        
    def test_convert_time_units_list_array(self):
        """Assert in utilities - converting list time units value"""
        _data = [1, 2, 3, 4, 5]
        self.assertTrue(all(_data == Utilities.convert_time_units(data = _data,
                                                             from_units = 's',
                                                             to_units = 's')))
        
    def tets_convert_time_units_numpy_array(self):
        """Assert in utilities - converting numpy array time units value"""
        _data = np.array([1., 2., 3., 4., 5.])
        self.assertTrue(all(_data == Utilities.convert_time_units(data = _data,
                                                             from_units = 's',
                                                             to_units = 's')))

if __name__ == '__main__':
    unittest.main()

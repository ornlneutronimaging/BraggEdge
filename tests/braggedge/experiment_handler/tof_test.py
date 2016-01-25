import unittest
import os
import numpy as np
from python.braggedge.experiment_handler.tof import TOF


class TofTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_loading_manual_tof_in_s_units(self):
        """Assert TOF(s) array is correctly manually loaded"""
        _tof_array = [1., 2., 3., 4., 5., 6., 7., 8., 9.]
        _tof_handler = TOF(tof = _tof_array)
        self.assertTrue(all(_tof_array == _tof_handler.tof))

    def test_loaind_manual_tof_raise_error_if_no_data_provided(self):
        """Assert that ValueError is raised if not tof array provided"""
        self.assertRaises(ValueError, TOF)

    def test_loading_manual_tof_in_micros_units(self):
        """Assert TOF(micros) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.e6, 2.e6, 3.e6, 4.e6, 5.e6, 6.e6, 7.e6, 8.e6, 9.e6])
        _tof_units = 'micros'
        _tof_handler = TOF(tof = _tof_array, units = _tof_units)
        self.assertTrue(all(_tof_array*1.e-6 == _tof_handler.tof))
        
    def test_loading_manual_tof_in_ms_units(self):
        """Assert TOF(ms) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.e3, 2.e3, 3.e3, 4.e3, 5.e3, 6.e3, 7.e3, 8.e3, 9.e3])
        _tof_units = 'ms'
        _tof_handler = TOF(tof = _tof_array, units = _tof_units)
        self.assertTrue(all(_tof_array*1.e-3 == _tof_handler.tof))

    def test_loading_manual_tof_in_ns_units(self):
        """Assert TOF(ms) array is correctly manually loaded and units are converted"""
        _tof_array = np.array([1.e9, 2.e9, 3.e9, 4.e9, 5.e9, 6.e9, 7.e9, 8.e9, 9.e9])
        _tof_units = 'ns'
        _tof_handler = TOF(tof = _tof_array, units = _tof_units)
        self.assertTrue(all(_tof_array*1.e-9 == _tof_handler.tof))

    def test_loading_manual_tof_units_not_implemented_yet(self):
        """Assert that an error is thrown when the units is not recognized"""
        _tof_array = np.array([1.e9, 2.e9, 3.e9, 4.e9, 5.e9, 6.e9, 7.e9, 8.e9, 9.e9])
        _tof_units = 'crazys'
        self.assertRaises(NotImplementedError, None, TOF, _tof_array, _tof_units)

    #def test_loading_manual_none_numpy_tof_in_micros_units(self):
        #"""Assert TOF(micros) python array is correctly manually loaded and converted to s"""
        #_tof_array = [1.e6, 2.e6, 3.e6]
        #_units = 'micros'
        #_tof_handler = TOF(tof = _tof_array, units=_units)
        #self.assertEqual([1., 2., 3.], _tof_handler.tof) 
        #self.assertEqual('s', _tof_handler.units)
        

if __name__ == '__main__':
    unittest.main()

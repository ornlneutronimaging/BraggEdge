import unittest
import os
from python.braggedge.experiment_handler.tof import TOF


class TofTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_loading_manual_tof_in_s_units(self):
        """Assert TOF(s) array is correctly manually loaded"""
        _tof_array = [1., 2., 3., 4., 5., 6., 7., 8., 9.]
        _tof_handler = TOF(tof = _tof_array)
        self.assertTrue(all(_tof_array == _tof_handler.tof))
        
    #def test_loading_manual_none_numpy_tof_in_micros_units(self):
        #"""Assert TOF(micros) python array is correctly manually loaded and converted to s"""
        #_tof_array = [1.e6, 2.e6, 3.e6]
        #_units = 'micros'
        #_tof_handler = TOF(tof = _tof_array, units=_units)
        #self.assertEqual([1., 2., 3.], _tof_handler.tof) 
        #self.assertEqual('s', _tof_handler.units)
        

if __name__ == '__main__':
    unittest.main()

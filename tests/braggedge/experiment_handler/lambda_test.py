import unittest
import os
import numpy as np
from python.braggedge.experiment_handler.lambda_wavelength import LambdaWavelength


class TofTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_loading_manual_lambda_array(self):
        """Assert in LambdaWavelength - manual loading of array"""
        _lambda_array = [1., 2., 3., 4., 5., 6., 7., 8., 9.]
        _lambda_handler = LambdaWavelength(data = _lambda_array)
        
#        self.assertTrue(False)
#        self.assertTrue(all(_tof_array == _tof_handler.tof))

if __name__ == '__main__':
    unittest.main()

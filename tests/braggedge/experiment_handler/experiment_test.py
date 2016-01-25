import unittest
import os
import numpy as np
from python.braggedge.experiment_handler.tof import TOF
from python.braggedge.experiment_handler.experiment import Experiment


class ExperimentTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_experiment_value_error_when_no_tof_provided(self):
        """Assert in experiemnt that ValueError is raised when tof array is missing"""
        self.assertRaises(ValueError, Experiment)

    def test_experiment_value_error_when_missing_argument_for_lambda_calculation(self):
        """Assert in experiment that ValueError is raised when detector_offset or LDS are missing for lambda calculation"""
        _tof = [1., 2., 3., 4., 5., 6., 7.]
        self.assertRaises(ValueError, Experiment, _tof)
        self.assertRaises(ValueError, Experiment, _tof, None, 1)
        self.assertRaises(ValueError, Experiment, _tof, None, None, 2)
        
    def test_experiment_value_error_when_lambda_provided_and_either_lds_or_offset_missing(self):
        """Assert in experiment that ValueError is raised when LdS and offset are missing when lambda provided"""
        _tof = [1., 2., 3., 4., 5., 6., 7.]
        _lambda = [11., 12., 13., 14., 15., 16., 17.]
        self.assertRaises(ValueError, Experiment, _tof, _lambda)

    def test_experiment_value_error_when_lambda_and_tof_not_same_size(self):
        """Assert in experiment that ValueError is raised when tof and lambda array do not have the same size"""
        _tof = [1., 2., 3., 4., 5., 6., 7.]
        _lambda = [11., 12., 13., 14., 15.]
        self.assertRaises(ValueError, Experiment, _tof, _lambda, 10)
        
    
    

if __name__ == '__main__':
    unittest.main()

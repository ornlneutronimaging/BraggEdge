from .tof import TOF
from ..constants import mn, h
from ..utilities import Utilities

class Experiment(object):
    """Class that allows:
       - convert the TOF scale into Lambda
       - distance sample - detector
       - detector time offset
       
       Arguments:
       * tof: tof array in s
       * lambda_array: mandatory only if detector_offset or distance_sample_detector are unknown
       * distance_sample_detector: mandatory only if lambda is the unknown parameter (m)
       * detector_offset: mandatory only if lambda is the unknown parameter (micros)
       """
    
    def __init__(self, tof=None, lambda_array=None, 
                 distance_sample_detector_m=None, 
                 detector_offset_micros=None):
        if tof is None:
            raise ValueError("Missing TOF array")
        self.tof_array = tof
        self.distance_sample_detector = distance_sample_detector_m
        self.detector_offset_micros = detector_offset_micros
        self.lambda_array = lambda_array

        # if lambda_array is unknown, both distance_sample_detector and detector_offset must be provided
        if lambda_array is None:
            if (distance_sample_detector_m is None) or (detector_offset_micros is None):
                raise ValueError("Mssing arguments to calculate lambda_array")

        # if lambda_array is provided, either distance_sample_detector_m or detector_offset_micros can be missing,
        # but not both
        if lambda_array is not None:
            if (distance_sample_detector_m is None) and (detector_offset_micros is None):
                raise ValueError("Missing either distance_sample detector or detector_offset")

            if len(lambda_array) != len(tof):
                raise ValueError("TOF and Lambda do not have the same size !")

            if distance_sample_detector is None:
                self.calculate_distance_sample_detector()
            else:
                self.calculate_detector_offset()

        else:
            self.calculate_lambda()
        
    def calculate_distance_sample_detector(self):
        """return the distance sample detector
        
        If lambda_array and tof_array are provided, the distance is calculated
        Otherwise, the distance_sample_detector must be provided
        """
        pass

    def calculate_detector_offset(self):
        """return the detector time offset value
        
        If lambda_array and tof_array are provided, the offset is calculated
        Otherwise, the detector_offset argument must be provided
        """
        pass
    
    def calculate_lambda(self):
        """return the lambda array when tof_array, distance_sample_detector and detector_offset are provided"""
        _tof = self.tof_array
        lSD = self.distance_sample_detector
        detector_offset_micros = self.detector_offset_micros
        detector_offset_s = Utilities.convert_time_units(detector_offset_micros,
                                                         from_units = 'micros',
                                                         to_units = 's')
        
        self._h_over_MnLds = h / (mn * lSD)
        
        _lambda = []
        for t in _tof:
            _value = t * self._h_over_MnLds
            _lambda.append(_value)
            
            
        self.lambda_array = _lambda
        
        
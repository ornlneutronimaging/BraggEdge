from .tof import TOF

class Experiment(object):
    """Class that allows:
       - convert the TOF scale into Lambda
       - distance sample - detector
       - detector time offset
       
       Arguments:
       * tof: tof array in s
       * lambda_array: mandatory only if detector_offset or distance_sample_detector are unknown
       * distance_sample_detector: mandatory only if lambda is the unknown parameter
       * detector_offset: mandatory only if lambda is the unknown parameter
       
       
       """
    
    def __init__(self, tof=None, lambda_array=None, distance_sample_detector=None, detector_offset=None):
        if tof is None:
            raise ValueError("Missing TOF array")
        self.tof_array = tof
        self.distance_sample_detector = distance_sample_detector
        self.detector_offset = detector_offset
        self.lambda_array = lambda_array

        # if lambda_array is unknown, both distance_sample_detector and detector_offset must be provided
        if lambda_array is None:
            if (distance_sample_detector is None) or (detector_offset is None):
                raise ValueError("Mssing arguments to calculate lambda_array")

        # if lambda_array is provided, either distance_sample_detector or detector_offset can be missing,
        # but not both
        if lambda_array is not None:
            if (distance_sample_detector is None) and (detector_offset is None):
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
        pass
        
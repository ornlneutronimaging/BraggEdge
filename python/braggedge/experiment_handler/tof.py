import numpy as np
import os


class TOFunits(object):
    """This class defines the various units of TOF supported by the application"""
    units = ['s','micros','nanos']

    def __init__(self, units):
        pass



class TOF(object):
    """This class handles the loading of the TOF and the automatic conversion to 's'"""
    
    def __init__(self, input_file=None, tof=None, units='s'):
        """Constructor of the TOF class
        
        Arguments:
        * input_file: optional input file name. If file exist, data will be automatically loaded
        * tof: optional tof array. This argument will be ignored if input_file is not None
        * units: optional units of the tof array (default to 'seconds')
        
        """

        if (input_file is not None) and (os.path.isfile(input_file)):
            self.input_file = input_file
        else:
            if (tof is not None) and (not type(tof) is np.ndarray):
                self.tof = np.array(tof)

        self.units = TOFunits(units)
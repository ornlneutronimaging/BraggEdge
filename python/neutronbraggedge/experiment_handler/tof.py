import numpy as np
import os
from ..utilities import Utilities


class TOF(object):
    """This class handles the loading of the TOF and the automatic conversion to 's'"""
    
    def __init__(self, filename=None, tof=None, units='s'):
        """Constructor of the TOF class
        
        Arguments:
        * filename: optional input file name. If file exist, data will be automatically loaded 
        (only CSV file is supported so far)
           example: file_tof.txt
                    #first row of the file
                    1.
                    2.
                    3.
                    4.
                    5.

        * tof: optional tof array. This argument will be ignored if filename is not None
        * units: optional units of the input tof array (default to 'seconds')

        Raises:
        * ValueError: - input file provided as the wrong format
                      - neither input file and tof_array are provided
                      
        * IOError: - file does not exist
        
        """

        if (filename is not None):
            if os.path.isfile(filename):
                self.filename = filename
                self.load_data()
            else:
                raise IOError("File does not exist")
        else:
            if (tof is not None):
                if (not type(tof) is np.ndarray):
                    self.tof = np.array(tof)
                else:
                    self.tof = tof
            else:
                raise ValueError("Please provide a tof array")

        if self.tof is None:
            raise ValueError("Please provide a tof array")

        if units is not 's':
            self.tof = Utilities.convert_time_units(data = tof,
                                                    from_units = units,
                                                    to_units = 's')
        
        
    def load_data(self):
        """Load the data from the filename name provided"""
        
        # only loaded implemented so far !
        self.tof = Utilities.load_csv(filename = self.filename)
        
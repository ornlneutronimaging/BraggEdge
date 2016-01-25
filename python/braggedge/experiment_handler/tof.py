import numpy as np
import os


class TOF(object):
    """This class handles the loading of the TOF and the automatic conversion to 's'"""
    
    def __init__(self, input_file=None, tof=None, units='s'):
        """Constructor of the TOF class
        
        Arguments:
        * input_file: optional input file name. If file exist, data will be automatically loaded 
        (only CSV file is supported so far)
           example: file_tof.txt
                    #first row of the file
                    1.
                    2.
                    3.
                    4.
                    5.

        * tof: optional tof array. This argument will be ignored if input_file is not None
        * units: optional units of the input tof array (default to 'seconds')

        Raises:
        * ValueError: - input file provided as the wrong format
                      - neither input file and tof_array are provided
                      
        * IOError: - file does not exist
        
        """

        if (input_file is not None):
            if os.path.isfile(input_file):
                self.input_file = input_file
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
            self._convert_units(input_units = units,
                                input_tof = tof)
            
        
    def _convert_units(self, input_units = 's', input_tof = None):
        """Converts the tof array from the units provided to s
        
        Arguments:
        * input_units: Default 's', but can be 'micros', 'nano', 'ms'
        * input_tof: numpy 1D array
        """
        if input_units is 'micros':
            _coeff = 1.e-6
        elif input_units is 'ns':
            _coeff = 1.e-9
        elif input_units is 'ms':
            _coeff = 1.e-3
        else:
            raise NotImplementedError
        
        self.tof = input_tof * _coeff
        
    def load_data(self):
        """Load the data from the input_file name provided"""
        
        # only loaded implemented so far !
        self._load_csv()
        
    def _load_csv(self):
        """Load the CSV input file where data have only 1 row"""
        _input_file = self.input_file
        try:
            f = open(_input_file, 'r')
            _tof = []
            for _line in f:
                if '#' in _line:
                    continue
                _value = float(_line.strip())
                _tof.append(_value)
                self.tof = _tof
        except:
            raise ValueError("Bad file format")
            
        
import numpy as np


class Utilities(object):

    list_of_time_units = ['s', 'ms', 'micros', 'ns']

    @staticmethod
    def convert_time_units(data=None, from_units='micros', to_units='s'):
        """convert the time units
        
        Parameters:
        * vdata: single data or array of value to convert
        * from_units: default 'micros'. Must be either ['s','micros','ns']
        * to_units: default 's'. Must be either ['s', 'micros', 'ns']
        
        """
        if data is None:
            raise ValueError("Please provide data to convert")

        list_of_time_units = Utilities.list_of_time_units
        if ( not (from_units in list_of_time_units) or
             not (to_units in list_of_time_units)):
            raise ValueError("Units convertion not supported")
    
        coeff = Utilities.get_time_conversion_coeff(from_units = from_units,
                                               to_units = to_units)
        
        if (type(data) is list):
            data = np.array(data)
        
        return data * coeff
    
    @staticmethod
    def get_time_conversion_coeff(from_units='micros', to_units='s'):
        """return the coefficient to use to convert from first units to second units
        
        Arguments:
        * from_units: default 'micros'. Must be in the list of list_of_time_units
        * to_units: default 's'. Must be in the list of list_of_time_units
        
        Returns:
        * coefficient to apply to data to convert from first units to second units provided
        
        Raises:
        * ValueError: if any of the units is not supported
        """

        if (not (from_units in Utilities.list_of_time_units) or
        not(to_units in Utilities.list_of_time_units)):
            raise ValueError("Units not supported")

        if from_units == to_units:
            return 1
        
        if from_units == 's':
            if to_units == 'ms': return 1.e3
            if to_units == 'micros': return 1.e6
            if to_units == 'ns': return 1.e9
            
        if from_units == 'ms':
            if to_units == 's': return 1.e-3
            if to_units == 'micros': return 1.e3
            if to_units == 'ns': return 1.e6

        if from_units == 'micros':
            if to_units == 's': return 1.e-6
            if to_units == 'ms': return 1.e-3
            if to_units == 'ns': return 1.e3

        if from_units == 'ns':
            if to_units == 's': return 1.e-9
            if to_units == 'ms': return 1.e-6
            if to_units == 'micros': return 1.e-3

    @staticmethod
    def array_multiply_coeff(data=None, coeff=1):
        """multiply each element of the array by the coeff
        
        Parameters:
        * data: array to apply coefficient on
        * coeff: default value is 1. Coefficient to apply
        
        Returns:
        * data * coefficient
        """
        if data is None:
            return None
    
        final_data = np.array([])
        for _item in data:
            _value = float(_item) * float(coeff)
            final_data = np.append(final_data, _value)
            
        return final_data
    
    @staticmethod
    def array_add_coeff(data=None, coeff=1.):
        """Add coefficient to each element of the array
        
        Parameters:
        * data: array to apply coefficient on
        * coeff: default value is 1. Coefficient to apply
        
        Returns:
        * data + coefficient
        """
        if data is None:
            return None
        
        final_data = np.array([])
        for index in range(len(data)):
            _item = data[index]
            _value = _item + coeff
            final_data = np.append(final_data, _value)
            
        return final_data
            
    @staticmethod
    def load_csv(filename=None):
        """Load a csv file and return its content
        
        Parameters:
        * filename: name of the csv file to load
        
        Returns:
        contents of the file as an array item for each line
        
        Raise:
        ValueError if format is wrong
        
        """
        _input_file = filename
        try:
            f = open(_input_file, 'r')
            _tof = []
            for _line in f:
                if '#' in _line:
                    continue
                _value = float(_line.strip())
                _tof.append(_value)
            return _tof
        except:
            raise ValueError("Bad file format")        
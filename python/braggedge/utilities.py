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

        
    
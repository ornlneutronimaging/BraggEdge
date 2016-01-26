class Utilities(object):

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

        list_of_time_units = ['s', 'micros', 'ns']
        if ( not (from_units in list_of_time_units) or
             not (to_units in list_of_time_units)):
            raise ValueError("Units convertion not supported")
    
        
        
        
    def arrayByValue(cls, array, value):
        for [index,_ele] in enumerate(array):
            array[index] = float(array[index]) * value
        return array
    
    def convertTOF(cls, TOFarray=None, from_units='micros', to_units='ms'):
        try:
            if TOFarray is None:
                return None
            if from_units == to_units:
                return TOFarray
            if from_units == 'micros':
                if to_units == 'ms':		
                    return arrayByValue(TOFarray,0.001)
                else:
                    raise NameError(to_units)
            elif from_units == 'ms':
                if to_units == 'micros':
                    return arrayByValue(TOFarray, 1000)
                else:
                    raise NameError(to_units)
            else:
                raise NameError(from_units)
        except NameError:
            print('units not supported')
            return None    
        
    
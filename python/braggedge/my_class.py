class MyClass(object):
    '''
    this is a demo class to check the documentation
    '''
    
    def __init__(self):
        '''
        constructor of the MyClass class
        '''
        self.a = 10
        
    def __repr__(self):
        '''
        to get info about the class
        '''
        return("self.a is %d" %self.a)
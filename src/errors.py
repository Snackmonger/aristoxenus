'''Errors used in the program.'''

class AristoxenusError(Exception):
    '''Parent exception for all errors generated by this library.'''
    

class ArgumentError(AristoxenusError):
    '''Error signifying that an argument is unacceptable in some way.'''


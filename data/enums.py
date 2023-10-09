from enum import StrEnum, auto

class OOBOptions(StrEnum):
    '''
    Options for handling out-of-bounds intervals 
    in limited interval structures.
    '''
    INTEGRATE_LOW = auto()
    INTEGRATE_HIGH = auto()
    ERROR = auto()
    IGNORE = auto()


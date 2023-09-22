from enum import StrEnum, auto

class OOBOptions(StrEnum):
    '''
    Options for handling out-of-bounds intervals 
    in limited interval structures.
    '''
    INTEGRATE = auto()
    OCT_INTEGRATE = auto()
    ERROR = auto()
    IGNORE = auto()
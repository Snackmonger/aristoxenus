from enum import StrEnum, auto

# mostly we're using py files as namespaces for constants,
# so the enum is a bit out of place in that context.
# maybe all the constants should really be enums? i don't
# really know what the relative advantages of each are

class OOBOptions(StrEnum):
    '''
    Options for handling out-of-bounds intervals 
    in limited interval structures.
    '''
    INTEGRATE_LOW = auto()
    INTEGRATE_HIGH = auto()
    ERROR = auto()
    IGNORE = auto()


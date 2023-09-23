
class IntervalOutOfBoundsError(ValueError):
    '''
    Error indicating that the interval is not within the legal limits.

    The error is only emitted if the user has set the LimitedIntervalStructure
    parameter 'oob' to 'error'
    '''


class MisconfiguredOOBError(ValueError):
    '''
    Error indicating that the LimitedIntervalStructure has parameter 'oob' set to a
    value not present in the OOBOptions enum.
    '''


class HeptatonicScaleError(ValueError):
    '''
    Error indicating that a scale does not conform to the heptatonic scale pattern or nomenclature.
    '''
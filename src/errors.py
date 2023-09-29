class IntervalOutOfBoundsError(ValueError):
    '''
    Error indicating that the interval is not within the legal limits.

    The error is only emitted if the user has set the LimitedIntervalStructure
    parameter `oob` to 'error'.
    '''

class MisconfiguredOOBError(ValueError):
    '''
    Error indicating that the LimitedIntervalStructure has parameter `oob` set
    to a value not present in the `OOBOptions` enum.
    '''

class NoteNameError(ValueError):
    ''' 
    Error indicating that an unrecognized note name was passed.
    '''

class HeptatonicScaleError(ValueError):
    '''
    Error indicating that a scale does not conform to the heptatonic scale 
    pattern or nomenclature.
    '''


class ChordNameError(ValueError):
    '''
    Error indicating that the alphabetical note name in a chord is not one of 
    the note names in the list returned from `nomenclature.legal_chord_names`.
    '''


class ChordSymbolError(ValueError):
    ''' 
    Error indicating that one or more of the suffixes of a chord symbol are 
    incompatible with the parser.
    '''
    
class OctaveRotationError(ValueError):
    '''
    Error indicating that the requested rotation cannot be performed on 
    structures exceeding the compass of one octave.
    '''


class UnknownKeywordError(ValueError):
    ''' 
    Error indicating that the passed keyword was not recognized in context.    
    '''


class IntervalOutOfBoundsError(ValueError):
    """Error that indicates that the given interval exceeded the expected range."""

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
    

class UnknownKeywordError(ValueError):
    ''' 
    Error indicating that the passed keyword was not recognized in context.    
    '''
from src.bit_manipulation import next_mode, previous_mode


class IntervalStructure():
    '''
    General purpose template for any type of interval structure stored as an integer.
    '''

    def __init__(self, value: int):
        self.value: int = value

    def __int__(self):
        return self.value

    def __index__(self):
        return int(self)

    def __add__(self, interval: int) -> int:
        return self.value | interval

    def __sub__(self, interval: int) -> int:
        return self.value ^ interval

    def __iadd__(self, interval: int) -> 'IntervalStructure':
        self.value |= interval
        return self

    def __isub__(self, interval: int) -> 'IntervalStructure':
        self.value ^= interval
        return self

    def __len__(self) -> int:
        return self.value.bit_count()

    def __repr__(self):
        return str(f'{self.value} = {bin(self.value)}')
    
    def next_inversion(self) -> int:
        '''Rotate the pitch collection left to begin with the next flipped bit.'''
        return next_mode(self.value)
    
    def previous_inversion(self) -> int:
        '''Rotate the pitch collection right to begin with the previous flipped bit.'''
        return previous_mode(self.value)


class Octave(IntervalStructure):
    '''
    Representation of the octave as a 12-bit integer.
    
    The octave provides a structural paradigm in which any interval beyond
    its compass is recognized as a transposition of an interval within its
    compass.
    '''
    
    def __init__(self, value: int=1) -> None:
        super().__init__(value)
        self.__bits: int = 12


class DoubleOctave(IntervalStructure):
    '''
    Representation of the double octave as a 24-bit integer.
    
    The double octave provides a structural paradigm in which the intervals
    of each octave are recognized as distinct (or partially distinct) from
    one another.

    Schema:
        ========  ========  ======== 
        aaaaaaaa  aaaabbbb  bbbbbbbb  
        ========  ========  ======== 

        a = 12-bit upper octave
        b = 12-bit lower octave

    As with other intervallic schemata, the least significant bit is the 
    root/tonic of the structure.
    '''

    def __init__(self, value: int=1) -> None:
        super().__init__(value)
        self.__bits: int = 24

    def bind_octaves(self, lower: int, higher: int) -> int:
        '''Take two 12-bit octaves and bind them into a 24-bit double octave.'''
        return (lower << int(self.__bits/2)) | higher
    
    def union(self) -> int:
        '''Return a 12-bit integer representing the interval overlap of the two octaves.'''
        return self.lower | self.upper

    @property
    def lower(self) -> int:
        '''Return the lower octave.'''
        return (self.value >> int(self.__bits/2))

    @lower.setter
    def lower(self, lower: int) -> None:
        '''Set the value of the lower octave.'''
        self.value = self.bind_octaves(lower, self.upper)

    @property
    def upper(self) -> int:
        '''Return the upper octave.'''
        return self.value & (2 ** int(self.__bits / 2) - 1)

    @upper.setter
    def upper(self, upper: int) -> None:
        '''Set the value of the upper octave.'''
        self.value = self.bind_octaves(self.lower, upper)




    
class Chord():
    '''
    Representation of a chord in its abstract and realized states.

    Abstract Structure:
    In the typical practice, intervals beyond the limit of the double
    octave do not have any meaning in the structural context of a chord.
    In other words, although the interval of a 9th is meaningful, the 
    interval of a 16th is not. Typically, if a note exists in one octave,
    it is not repeated in the other (but this is not a fixed rule).

    Real Structure:
    In practice, a chord often spans three or more octaves, and the specific
    voicing of a chord (that is, the specific way in which each interval of
    the chord is arranged relative to all the others) contributes greatly to
    the overall feeling imparted by the chord's sound.

    Therefore, we want to track both the abstract structure of a chord TYPE, 
    and the real structure of a chord VOICING.


    BASE CLASS
        We use the double octave as a canonical abstraction of the chord.
        This inits the chord to a single note.
        Presumably, we then call methods to define the structure...?
        We want the abstract structure to be an accurate reflection of
        the real structure, so I guess it needs to be derived from the 
        real structure, but how do we distinguish between a #5 in one octave
        and a b13 in another when we try to assign the intervals to an 
        abstraction? Or is it better to use a single octave as the base?
    '''

    def __init__(self):
        super().__init__()
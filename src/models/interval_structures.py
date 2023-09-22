from typing import Literal, cast

from ..decorators import pos_only, check_oob
from ..bitwise import next_mode, previous_mode
from ..errors import IntervalOOBError


OOB_OPTIONS = Literal['integrate', 'oct_integrate', 'error', 'ignore']

class IntervalStructure():
    '''
    General purpose template for any type of interval structure stored as an integer.
    '''

    def __init__(self, value: 'int | IntervalStructure'):
        self.value: int = int(value)

    def __int__(self):
        return self.value

    def __index__(self):
        return int(self)

    @pos_only
    def __add__(self, interval: int) -> int:
        return self.value | interval

    @pos_only
    def __sub__(self, interval: int) -> int:
        return (self.value ^ interval) + 1

    @pos_only
    def __iadd__(self, interval: int) -> 'IntervalStructure':
        self.value |= interval
        return self

    @pos_only
    def __isub__(self, interval: int) -> 'IntervalStructure':
        self.value ^= interval + 1
        return self

    def __len__(self) -> int:
        return self.value.bit_length()

    def __repr__(self):
        return str(f'{self.value} = {bin(self.value)} :: {self.value.bit_count()}/{len(self)} bits')
    
    def next_inversion(self) -> None:
        '''Rotate the pitch collection left to begin with the next flipped bit.'''
        
    
    def previous_inversion(self) -> None:
        '''Rotate the pitch collection right to begin with the previous flipped bit.'''
        


class LimitedIntervalStructure(IntervalStructure):
    '''
    Representation of an interval structure that has a limit to its range.

    If the class attempts to add notes that are out of bounds, we use the 'oob'
    attribute to define how it handles the conflict.
    '''
    
    def __init__(self,
                 bits: int,
                 value: int = 1,
                 oob: OOB_OPTIONS = 'integrate') -> None:
        if value.bit_length() <= bits:
            super().__init__(value)
        else:
            raise IntervalOOBError(bin(value), value.bit_length(), bits)
        self.__bits: int = bits
        self.oob: str = oob


    @property
    def bits(self) -> int:
        '''Public reference for private bit-limit.'''
        return self.__bits


    @check_oob
    @pos_only
    def __iadd__(self, interval: int) -> 'LimitedIntervalStructure':
        return super().__iadd__(interval)


    @check_oob
    @pos_only
    def __isub__(self, interval: int) -> 'LimitedIntervalStructure':
        return super().__isub__(interval)
    

    def next_inversion(self) -> None:
        '''Rotate the pitch collection left to begin with the next flipped bit.'''
        self.value = next_mode(self.value, self.__bits)
    

    def previous_inversion(self) -> None:
        '''Rotate the pitch collection right to begin with the previous flipped bit.'''
        self.value = previous_mode(self.value, self.__bits)


class Octave(LimitedIntervalStructure):
    ...




class DoubleOctave(LimitedIntervalStructure):
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
    '''

    def __init__(self):
        super().__init__()



class SATBChord(Chord):
    '''
    Representation of a four-note chord.

    The chord has a canonical form based on its idealized structure.

    The chord has a real form in an inversion/drop voicing.

    Some chords are inversions of other chords (Am7=C6, Am7b5=Cm6, etc.),
    so the canonical form helps to define the polarity of the tonal
    character. This can also be used to make modal-type structures, using
    the inversions that aren't typically considered separate chords.
    '''
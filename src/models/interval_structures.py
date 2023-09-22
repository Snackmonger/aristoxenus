from typing import Literal

from ..decorators import pos_only, check_oob
from ..bitwise import next_mode, previous_mode
from ..errors import IntervalOutOfBoundsError, HeptatonicScaleError


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
        self.value = (self.value ^ interval) +1
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
            raise IntervalOutOfBoundsError(bin(value), value.bit_length(), bits)
        self.__bits: int = bits
        self.oob: str = oob


    @property
    def inversions(self) -> tuple[int, ...]:
        '''
        Return a tuple containing the integer representations of all possible
        inversions of the current interval structure.
        '''
        rotations: list[int] = []
        for _ in range(self.value.bit_count()):
            self.next_inversion()
            rotations.append(int(self))
        return tuple(rotations)


    @property
    def bits(self) -> int:
        '''Public reference for private bit-limit.'''
        return self.__bits


    @check_oob
    @pos_only
    def __iadd__(self, interval: 'int | IntervalStructure') -> 'LimitedIntervalStructure':
        self.value |= int(interval)
        return self


    @check_oob
    @pos_only
    def __isub__(self, interval: 'int | IntervalStructure') -> 'LimitedIntervalStructure':
        self.value = (self.value ^ int(interval)) +1
        return self
    

    def next_inversion(self) -> None:
        '''Rotate the pitch collection left to begin with the next flipped bit.'''
        self.value = next_mode(self.value, self.__bits)
    

    def previous_inversion(self) -> None:
        '''Rotate the pitch collection right to begin with the previous flipped bit.'''
        self.value = previous_mode(self.value, self.__bits)


class Octave(LimitedIntervalStructure):
    '''
    Representation of the octave as a 12-bit integer.

    The octave provides a structural paradigm in which all intervals
    can be expressed as numbers between 1 and 2. 

    As with other intervallic schemata, the least significant bit is the 
    root/tonic of the structure.
    '''
    def __init__(self, value: int = 1):
        super().__init__(12, value)


class DoubleOctave(LimitedIntervalStructure):
    '''
    Representation of the double octave as a 24-bit integer.
    
    The double octave provides a structural paradigm in which the intervals
    between 1 and 2 are recognized as distinct (or partially distinct) from
    the intervals between 2 and 4.

    As with other intervallic schemata, the least significant bit is the 
    root/tonic of the structure.
    '''

    def __init__(self, value: int = 1) -> None:
        super().__init__(24, value)

    def bind_octaves(self, lower: int, higher: int) -> int:
        '''Take two 12-bit octaves and bind them into a 24-bit double octave.'''
        return (lower << int(self.bits/2)) | higher
    
    def union(self) -> int:
        '''Return a 12-bit integer representing the interval overlap of the two octaves.'''
        return self.lower | self.upper

    @property
    def lower(self) -> int:
        '''Return the lower octave.'''
        return (self.value >> int(self.bits/2))

    @lower.setter
    def lower(self, lower: int) -> None:
        '''Set the value of the lower octave.'''
        self.value = self.bind_octaves(lower, self.upper)

    @property
    def upper(self) -> int:
        '''Return the upper octave.'''
        return self.value & (2 ** int(self.bits / 2) - 1)

    @upper.setter
    def upper(self, upper: int) -> None:
        '''Set the value of the upper octave.'''
        self.value = self.bind_octaves(self.lower, upper)


class Scale(Octave):
    '''
    Abstraction of a scale of 1 - 12 notes. 
    '''

    def __init__(self, value: int = 1) -> None:
        super().__init__(value)
        self.tones = self.value.bit_count()

    
    def chords(self,
               key: str = 'C',
               structure: str = 'tertial',
               extent: str|int = 'triad',
               ) -> list[str]:
        '''
        Return a list of chords for this scale.

        Params:
                structure   ::  defines the pattern of how the chord is built
                extent      ::  defines how many notes will be used in chord

        Chord structure may be any of the values in the ChordStructure enum.
        In this context, the values 'tertial', 'quartal', etc. mean 'take
        every X note' rather than 'take a major/minor 3rd' or 'take a perfect 
        or augmented fourth'.

        Extent may either be a Greek name from the GreekNumberGroups enum, or
        an integer between 1 and 7.
        '''


class HeptatonicScale(Scale):
    '''
    Abstraction of a heptatonic scale.
    '''
    def __init__(self, value: int = 1) -> None:
        if value.bit_count() != 7:
            raise HeptatonicScaleError(value.bit_count())
        super().__init__(value)
        self.tones = self.value.bit_count()


class Chord(DoubleOctave):
    '''
    Representation of a chord in its abstract and realized states.
    '''

    def __init__(self, value: int = 1):
        super().__init__(value)



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
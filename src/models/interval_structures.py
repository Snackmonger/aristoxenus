from typing import Literal, Self

from src import bitwise
from data import errors
from src import parsing

from src.decorators import pos_only, check_oob

# Sketches of some classes. They don't figure into anything right now, but I'll work them out later.

# note to self: pos_only decorator can just be abs()
OOB_OPTIONS = Literal['integrate_low', 'integrate_high', 'error', 'ignore']


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
    def __iadd__(self, interval: int) -> Self:
        self.value |= interval
        return self

    @pos_only
    def __isub__(self, interval: int) -> Self:
        self.value = (self.value ^ interval) + 1
        return self

    def __len__(self) -> int:
        return self.value.bit_length()

    def __repr__(self):
        return str(f'{self.value} = {bin(self.value)} :: {self.value.bit_count()}/{len(self)} bits')


class LimitedIntervalStructure(IntervalStructure):
    '''
    Representation of an interval structure that has a limit to its range.

    If the class attempts to add intervals that are out of bounds, we use the `oob`
    attribute to define how it handles the conflict.
    '''

    def __init__(self,
                 bits: int,
                 value: int = 1,
                 oob: OOB_OPTIONS = 'integrate_low') -> None:
        
        if value.bit_length() <= bits:
            super().__init__(value)
        else:
            raise errors.IntervalOutOfBoundsError(
                f'Max bits: {bits} Current bits: {value.bit_length()} (={bin(value)})')
        self.__bits: int = bits
        self.oob: str = oob


    @property
    def inversions(self) -> tuple[int, ...]:
        '''
        A list containing the integer representations of all possible
        inversions of the current interval structure. 
        
        This is determined by
        looking at the length of the whole structure, so multi-octave interval
        structures rotate all their octaves as one long loop.
        '''
        rotations: list[int] = []
        for _ in range(self.value.bit_count()):
            self.next_inversion()
            rotations.append(int(self))
        return tuple(rotations)


    @property
    def intervals(self) -> tuple[int, ...]:
        '''
        A list of the intervals in the current interval structure.
        '''
        return tuple(bitwise.iterate_intervals(int(self)))


    @property
    def bits(self) -> int:
        '''An integer representing the maximum number of bits in the structure.'''
        return self.__bits


    @check_oob
    @pos_only
    def __iadd__(self, interval: 'int | IntervalStructure') -> Self:
        self.value |= int(interval)
        return self


    @check_oob
    @pos_only
    def __isub__(self, interval: 'int | IntervalStructure') -> Self:
        self.value = (self.value ^ int(interval)) + 1
        return self


    def next_inversion(self) -> None:
        '''Rotate the pitch collection left to begin with the next flipped bit.'''
        self.value = bitwise.next_inversion(self.value, self.__bits)


    def previous_inversion(self) -> None:
        '''Rotate the pitch collection right to begin with the previous flipped bit.'''
        self.value = bitwise.previous_inversion(self.value, self.__bits)


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
        return (self.value & int(self.bits/2) **2 -1)

    @lower.setter
    def lower(self, lower: int) -> None:
        '''Set the value of the lower octave.'''
        if bitwise.validate_interval_structure(lower, int(self.__bits/2)):
            self.value = self.bind_octaves(lower, self.upper)

    @property
    def upper(self) -> int:
        '''Return the upper octave.'''
        return self.value & ((2 ** int(self.bits / 2) -1) << self.bits)

    @upper.setter
    def upper(self, upper: int) -> None:
        '''Set the value of the upper octave.'''
        if bitwise.validate_interval_structure(upper, int(self.__bits/2)):
            self.value = self.bind_octaves(self.lower, upper)


class Scale(Octave):
    '''
    Abstraction of a scale of 1 - 12 notes. 
    '''

    def __init__(self, value: int = 1) -> None:
        super().__init__(value)
        self.tones = self.value.bit_count()


class HeptatonicScale(Scale):
    '''
    Abstraction of a heptatonic scale.
    '''

    def __init__(self, value: int = 1) -> None:
        if value.bit_count() != 7:
            raise errors.HeptatonicScaleError(value.bit_count())
        super().__init__(value)
        self.tones = self.value.bit_count()


class Chord(DoubleOctave):
    '''
    Representation of a chord in its abstract and realized states.
    '''

    def __init__(self, value: int = 1):
        super().__init__(value)


    @classmethod
    def from_symbol(cls, chord_symbol: str) -> 'Chord':
        '''
        Return an instance of Chord from a chord symbol.

        Parameters
        ----------
        chord_symbol : str
            A symbolic representation of a chord. Most standard chord symbols
            will be recognizable

        Returns
        -------
        Chord
            An instance of Chord with the structure indicated by the chord 
            symbol.
        '''
        chord_structure: int = parsing.parse_chord_symbol(chord_symbol)
        return cls(chord_structure)
    
    @classmethod
    def from_structure(cls, interval_structure: int) -> 'Chord':
        prototype: DoubleOctave = DoubleOctave()
        if interval_structure.bit_length() <= prototype.bits:
            return cls(interval_structure)
        prototype += interval_structure
        return cls(int(prototype))


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

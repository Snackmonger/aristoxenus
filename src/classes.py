'''
This module provides a set of object-oriented interfaces for manipulating
musical data using the functions in the ``functions`` module.

For a more data-oriented interface for accessing the backend functions, 
see ``api.py``.
'''
import re
from typing import Sequence

from src.constants import (
    DROP_2_AND_3_VOICING,
    DROP_2_AND_4_VOICING,
    DROP_2_VOICING,
    DROP_3_VOICING,
    HEPTATONIC_SCALES,
    HEPTATONIC_SUPPLEMENT,
    MODAL_SERIES_KEYS,
    RE_VALIDATE_NOTE_NAME,
    SLASH_SYMBOL,
    TONES
)
from src.errors import ArgumentError
from src.functions import (
    chordify_heptatonic_sus,
    chordify_heptatonic_tertial,
    decode_note_name,
    drop_voicing,
    get_heptatonic_scale_notes,
    name_chord,
    order_interval_names,
    rotate_chord,
    rotate_interval_structure
)
from src.structures import ChordData

class Chord:
    '''
    The Chord class provides a simple interface for manipulating chord
    structures.
    '''
    def __init__(
        self,
        note_names: Sequence[str],
        interval_symbols: Sequence[str],
        interval_structure: Sequence[int]
        ) -> None:
        self.note_names = note_names
        self.interval_symbols = interval_symbols
        self.interval_structure = interval_structure

    @property
    def root(self) -> str:
        '''
        The note name that serves as the root of the chord's structure.
        '''
        i = self.interval_symbols.index("1")
        return self.note_names[i]

    @property
    def symbol(self) -> str:
        '''
        The basic symbol by which the chord can be identified.
        '''
        intervals = order_interval_names(self.interval_symbols)
        if self.note_names[0] != self.root:
            main = self.root + name_chord(intervals)
            bass = self.note_names[0]
            return main + SLASH_SYMBOL + bass
        return self.root + name_chord(intervals)

    @property
    def __is_close(self) -> bool:
        ordered = order_interval_names(self.interval_symbols)
        return ordered == tuple(x for x in self.interval_symbols)

    def reset(self) -> 'Chord':
        '''Return the close voiced root position of this chord.'''
        order = order_interval_names(self.interval_symbols)
        names: list[str] = []
        symbols: list[str] = []
        intervals: list[int] = []
        for x in order:
            i = self.interval_symbols.index(x)
            names.append(self.note_names[i])
            symbols.append(self.interval_symbols[i])
            intervals.append(self.interval_structure[i])
        for i, interval in enumerate(intervals):
            if interval > 11:
                intervals[i] = interval % TONES
        return self.__class__(tuple(names), tuple(symbols), tuple(intervals))

    @classmethod
    def from_ChordData(cls, data: ChordData) -> 'Chord':
        '''
        Return a Chord object with the same data as the given 
        ChordData instance.
        '''
        chord = cls(
            data.note_names, 
            data.interval_symbols, 
            data.interval_structure)
        return chord

    def to_ChordData(self) -> ChordData:
        ''' 
        Return a ChordData object with the same data as this instance
        of Chord.
        '''
        return ChordData(self.note_names, self.interval_symbols, self.interval_structure)

    def __repr__(self) -> str:
        note_names = self.note_names
        interval_symbols = self.interval_symbols
        interval_structure = self.interval_structure
        return self.__class__.__name__ + f"({note_names=}, {interval_symbols=}, {interval_structure=})"

    def invert(self, degree: int) -> 'Chord':
        '''
        Return an inversion of this chord, rotated to the given degree.

        NOTE: The chord should be inverted, then voiced! If the order is not
        followed, the program will reset the chord before inverting it!

        Examples
        --------

        '''
        if self.__is_close:
            chord = self
        else:
            chord = self.reset()
        result = rotate_chord(chord.to_ChordData(), degree)
        return self.from_ChordData(result)

    def voicing(self, voicing: Sequence[int] | str) -> 'Chord':
        '''
        Return a voicing of this chord, according to the given structure.

        NOTE: The chord should be inverted, then voiced! If the order is not
        followed, the program will reset the chord before inverting it!

        Examples
        --------

        '''
        if isinstance(voicing, str):
            if voicing in ['d2', 'drop2', 'drop_2']:
                voicing = DROP_2_VOICING
            elif voicing in ['d3', 'drop3', 'drop_3']:
                voicing = DROP_3_VOICING
            elif voicing in ['d23', 'drop23', 'drop2and3', 'drop_2_and_3', 'drop2_3']:
                voicing = DROP_2_AND_3_VOICING
            elif voicing in ['d24', 'drop24', 'drop2and4', 'drop_2_and_4', 'drop2_4']:
                voicing = DROP_2_AND_4_VOICING
            else:
                return self

        result = drop_voicing(self.to_ChordData(), voicing)
        return self.from_ChordData(result)


class Scale:
    '''Middleman placeholder for now.'''

class HeptatonicScale(Scale):
    '''
    This class provides a simple interface for manipulating scale forms and
    the chords derived from them.
    '''
    def __init__(
        self, 
        keynote: str = 'C', 
        scale_name: str = 'diatonic', 
        mode_name: str = 'ionian'
        ) -> None:
        self.keynote = keynote
        self.scale_name = scale_name
        self.mode_name = mode_name

    @property
    def __kn(self) -> tuple[int, int]:
        '''The deciphered keynote.'''
        if not re.search(RE_VALIDATE_NOTE_NAME, self.keynote):
            raise ArgumentError('Unable to parse note name.')
        return decode_note_name(self.keynote)

    @property
    def interval_structure(self) -> tuple[int, ...]:
        '''The interval structure of this scaleform.'''
        if (n := HEPTATONIC_SCALES[self.scale_name]) or (
            n := HEPTATONIC_SUPPLEMENT[self.scale_name]):
            base = n
            if self.mode_name in MODAL_SERIES_KEYS:
                m = MODAL_SERIES_KEYS.index(self.mode_name)
                return rotate_interval_structure(base, m)
            raise ArgumentError(f"Unable to parse mode name {self.mode_name}")
        raise ArgumentError(f"Unable to parse scale name {self.scale_name}")
    
    @property
    def note_names(self) -> tuple[str, ...]:
        '''The note names for this scaleform and keynote.'''
        return get_heptatonic_scale_notes(self.interval_structure, *self.__kn)

    def __tertial(self, degree: int, size: int) -> Chord:
        '''Get a tertial chord with the given parameters.'''
        degree -= 1
        if degree > len(self.note_names):
            degree %= len(self.note_names)
        ch_scale = chordify_heptatonic_tertial(
            self.interval_structure, self.__kn, size)
        chord = ch_scale[degree]
        return Chord.from_ChordData(chord)
    
    def __sus(self, degree: int, size: int, sus: int) -> Chord:
        '''Get a sus chord with the given parameters.'''
        degree -= 1
        if degree > len(self.note_names):
            degree %= len(self.note_names)
        ch_scale = chordify_heptatonic_sus(
            self.interval_structure, self.__kn, size, sus)
        chord = ch_scale[degree]
        return Chord.from_ChordData(chord)
    
    def tertial_triad(self, degree: int) -> Chord:
        '''Get the tertial triad at the given scale degree.'''
        return self.__tertial(degree, 3)
    
    def tertial_tetrad(self, degree: int) -> Chord:
        '''Get the tertial tetrad at the given scale degree.'''
        return self.__tertial(degree, 4)
 
    def sus2_triad(self, degree: int) -> Chord:
        '''Get the sus2 triad at the given scale degree.'''
        return self.__sus(degree, 3, 2)

    def sus4_triad(self, degree: int) -> Chord:
        '''Get the sus4 triad at the given scale degree.'''
        return self.__sus(degree, 3, 4)
    
    def sus2_tetrad(self, degree: int) -> Chord:
        '''Get the sus2 tetrad at the given scale degree.'''
        return self.__sus(degree, 4, 2)
    
    def sus4_tetrad(self, degree: int) -> Chord:
        '''Get the sus4 tetrad at the given scale degree.'''
        return self.__sus(degree, 4, 4)

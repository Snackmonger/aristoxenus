'''
This module provides a set of object-oriented interfaces for manipulating
musical data using the functions in the ``src.core`` module.

For a more data-oriented interface for accessing the ``src.core`` functions,
see the ``src.api`` module.
'''
import re
from typing import Sequence

from src.constants import (
    D2,
    D23,
    D24,
    D3,
    DROP_2_AND_3_VOICING,
    DROP_2_AND_4_VOICING,
    DROP_2_VOICING,
    DROP_3_VOICING,
    HEPTATONIC_SCALES,
    HEPTATONIC_SUPPLEMENT,
    MODAL_SERIES_KEYS,
    RE_PARSE_NOTE_NAME,
    SLASH_SYMBOL,
    TONES
)
from src.errors import ArgumentError
from src.core import (
    ChordData,
    NoteData,
    chordify_heptatonic_sus,
    chordify_heptatonic_tertial,
    decode_note_name,
    apply_drop_voicing,
    get_heptatonic_scale_notes,
    encode_chord_symbol,
    decode_chord_symbol,
    resolve_scale_name,
    sort_interval_names,
    rotate_chord,
    rotate_interval_structure
)

__all__ = [
    'Chord', 
    'HeptatonicScale'
]

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
        self.slash = False

    @property
    def root(self) -> str:
        '''
        The note name that serves as the root of the chord's structure.
        '''
        i = self.interval_symbols.index(str(1))
        return self.note_names[i]

    @property
    def symbol(self) -> str:
        '''
        The basic symbol by which the chord can be identified.
        '''
        intervals = sort_interval_names(self.interval_symbols)
        if self.note_names[0] != self.root and self.slash:
            main = self.root + encode_chord_symbol(intervals)
            bass = self.note_names[0]
            return main + SLASH_SYMBOL + bass
        return self.root + encode_chord_symbol(intervals)

    def __repr__(self) -> str:
        note_names = self.note_names
        interval_symbols = self.interval_symbols
        interval_structure = self.interval_structure
        return self.__class__.__name__ + f"({note_names=}, {interval_symbols=}, {interval_structure=})"

    @property
    def __is_close(self) -> bool:
        ordered = sort_interval_names(self.interval_symbols)
        return ordered == tuple(x for x in self.interval_symbols)

    def reset(self) -> 'Chord':
        '''Return the close voiced root position of this chord.'''
        order = sort_interval_names(self.interval_symbols)
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
    def from_symbol(cls, symbol: str) -> 'Chord':
        

        # TODO: we need to rewrite the regex for chord parsing in case
        # of slash chords
        parsed_intervals = decode_chord_symbol(symbol)


    @classmethod
    def from_ChordData(cls, data: ChordData) -> 'Chord':
        '''
        Return a Chord object with the same data as the given 
        ChordData instance.
        '''
        chord = cls(
            tuple(data.note_names),
            tuple(data.interval_symbols),
            tuple(data.interval_structure)
        )
        return chord

    def to_ChordData(self) -> ChordData:
        ''' 
        Return a ChordData object with the same data as this instance
        of Chord.
        '''
        return ChordData(self.symbol, self.note_names, self.interval_symbols, self.interval_structure)

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
            if voicing == D2:
                voicing = DROP_2_VOICING
            elif voicing == D3:
                voicing = DROP_3_VOICING
            elif voicing in D23:
                voicing = DROP_2_AND_3_VOICING
            elif voicing in D24:
                voicing = DROP_2_AND_4_VOICING
            else:
                return self

        result = apply_drop_voicing(self.to_ChordData(), voicing)
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({" ".join(self.note_names)})"

    @property
    def __kn(self) -> NoteData:
        '''The deciphered keynote.'''
        if not re.search(RE_PARSE_NOTE_NAME, self.keynote):
            raise ArgumentError('Unable to parse note name.')
        return decode_note_name(self.keynote)

    @property
    def interval_structure(self) -> tuple[int, ...]:
        '''The interval structure of this scaleform.'''
        return resolve_scale_name(self.scale_name, self.mode_name)

    @property
    def note_names(self) -> tuple[str, ...]:
        '''The note names for this scaleform and keynote.'''
        return get_heptatonic_scale_notes(self.__kn, self.interval_structure)
    
    @staticmethod
    def __validate_degree(degree: int) -> bool:
        if degree not in range(1, 8):
            raise ArgumentError(f"Scale degree must be between 1 and 7 ({degree=})")
        return True
    
    @staticmethod
    def __validate_size(size: int) -> bool:
        if size not in range(3, 8):
            raise ArgumentError(f"Chord size must be between 3 and 7 ({size=})")
        return True

    def get_tertial_chord(self, degree: int, size: int) -> Chord:
        '''
        Derive a tertial chord from the current scale configuration.

        Parameters
        ----------
        degree : int
            The scale degree that will serve as the chord's root (1 to 7)
        size : int
            The number of notes to include in the chord (3 to 7)

        Returns
        -------
        Chord
            A chord derived from this scale.

        Raises
        ------
        ArgumentError
            If any of the parameters does not adhere to the limits above.
        '''
        self.__validate_degree(degree)
        self.__validate_size(size)
        degree -= 1
        if degree > len(self.note_names):
            degree %= len(self.note_names)
        ch_scale = chordify_heptatonic_tertial(self.__kn,
            self.interval_structure,  size)
        chord = ch_scale[degree]
        return Chord.from_ChordData(chord)

    def get_sus_chord(self, degree: int, size: int, sus: int) -> Chord:
        '''
        Derive a suspended chord from the current scale configuration.

        Parameters
        ----------
        degree : int
            The scale degree that will serve as the chord's root (1 to 7)
        size : int
            The number of notes to include in the chord (3 to 7)
        sus : int
            The scale degree that will replace the third of the chord (2 or 4)

        Returns
        -------
        Chord
            A chord derived from this scale.

        Raises
        ------
        ArgumentError
            If any of the parameters does not adhere to the limits above.
        '''
        self.__validate_degree(degree)
        self.__validate_size(size)
        if sus not in [2, 4]:
            raise ArgumentError(f"Can only suspend 2 or 4 ({sus=})")
        degree -= 1
        if degree > len(self.note_names):
            degree %= len(self.note_names)
        ch_scale = chordify_heptatonic_sus(self.__kn, self.interval_structure,  size, sus)
        chord = ch_scale[degree]
        return Chord.from_ChordData(chord)

    def tertial_triad(self, degree: int) -> Chord:
        '''Get the tertial triad at the given scale degree.'''
        return self.get_tertial_chord(degree, 3)

    def tertial_tetrad(self, degree: int) -> Chord:
        '''Get the tertial tetrad at the given scale degree.'''
        return self.get_tertial_chord(degree, 4)

    def sus2_triad(self, degree: int) -> Chord:
        '''Get the sus2 triad at the given scale degree.'''
        return self.get_sus_chord(degree, 3, 2)

    def sus4_triad(self, degree: int) -> Chord:
        '''Get the sus4 triad at the given scale degree.'''
        return self.get_sus_chord(degree, 3, 4)

    def sus2_tetrad(self, degree: int) -> Chord:
        '''Get the sus2 tetrad at the given scale degree.'''
        return self.get_sus_chord(degree, 4, 2)

    def sus4_tetrad(self, degree: int) -> Chord:
        '''Get the sus4 tetrad at the given scale degree.'''
        return self.get_sus_chord(degree, 4, 4)

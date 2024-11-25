
from typing import Optional, Sequence

from aristoxenus.core.annotations import (
    ChordData,
    ChordStyle
)
from aristoxenus.core.chord_symbol import (
    encode_chord_symbol,
    get_chord_style
)
from aristoxenus.core.constants import (
    CHORD_DIM,
    CHORD_MAJ,
    CHORD_MIN,
    CLOSE,
    D2,
    D23,
    D24,
    D3,
    DIM_SYMBOL,
    DROP_2_AND_3_VOICING,
    DROP_2_AND_4_VOICING,
    DROP_2_VOICING,
    DROP_3_VOICING,
    INTERVAL_NAMES,
    INTERVAL_STRUCTURE,
    MAJ_SYMBOL,
    MIN_SYMBOL,
    NOTE_NAMES,
    OPEN,
    SLASH,
    SLASH_SYMBOL,
    TONES
)
from aristoxenus.core.interval import sort_interval_names
from aristoxenus.core.resolve import resolve_chord_symbol
from aristoxenus.core.rotate import rotate_chord
from aristoxenus.core.voicing import apply_drop_voicing

__all__ = [
    'Chord'
]

class Chord:
    '''
    The Chord class provides a simple interface for manipulating chord
    structures.
    '''

    def __init__(
        self,
        note_names: Optional[Sequence[str]] = None,
        interval_names: Optional[Sequence[str]] = None,
        interval_structure: Optional[Sequence[int]] = None
    ) -> None:
        note_names = note_names or ('C', 'E', 'G', 'B')
        interval_names = interval_names or ('1', '3', '5', '7')
        interval_structure = interval_structure or (0, 4, 7, 11)
        self.note_names = tuple(note_names)
        self.interval_names = tuple(interval_names)
        self.interval_structure = tuple(interval_structure)
        self.__slash = True
        self.__maj_symbol = CHORD_MAJ
        self.__min_symbol = CHORD_MIN
        self.__dim_symbol = CHORD_DIM

    @property
    def root(self) -> str:
        '''
        The note name that serves as the root of the chord's structure.
        '''
        i = self.interval_names.index(str(1))
        return self.note_names[i]

    @property
    def symbol(self) -> str:
        '''
        The basic symbol by which the chord can be identified.
        '''
        intervals = sort_interval_names(self.interval_names)
        if self.note_names[0] != self.root and self.__slash:
            symb = encode_chord_symbol(
                interval_names=intervals,
                style=ChordStyle(
                    maj_symbol=self.__maj_symbol,
                    min_symbol=self.__min_symbol,
                    dim_symbol=self.__dim_symbol
                )
            )
            main = self.root + symb
            bass = self.note_names[0]
            return main + SLASH_SYMBOL + bass
        return self.root + encode_chord_symbol(intervals)

    def __repr__(self) -> str:
        note_names = self.note_names
        interval_symbols = self.interval_names
        interval_structure = self.interval_structure
        chord_symbol = self.symbol
        return self.__class__.__name__ + f"({chord_symbol=}, {note_names=}, {interval_symbols=}, {interval_structure=})"

    @property
    def __is_close(self) -> bool:
        ordered = sort_interval_names(self.interval_names)
        return ordered == tuple(x for x in self.interval_names)

    def reset(self) -> 'Chord':
        '''
        Return the close-voiced root position form of this chord.
        '''
        order = sort_interval_names(self.interval_names)
        names: list[str] = []
        symbols: list[str] = []
        intervals: list[int] = []
        for x in order:
            i = self.interval_names.index(x)
            names.append(self.note_names[i])
            symbols.append(self.interval_names[i])
            intervals.append(self.interval_structure[i])
        for i, interval in enumerate(intervals):
            if interval > 11:
                intervals[i] = interval % TONES
        return self.__class__(tuple(names), tuple(symbols), tuple(intervals))

    @classmethod
    def from_symbol(cls, symbol: str) -> 'Chord':
        '''
        Return a Chord object with the notes implied in the given chord symbol.

        Parameters
        ----------
        symbol : str
            A chord symbol, e.g. 'Cmaj7', 'Edim9', 'F#mM7', 'Gmin6/Bb'.

        Returns
        -------
        Chord
            An object with data extrapolated from the given symbol.
        '''
        chord = cls.from_ChordData(resolve_chord_symbol(symbol))
        style = get_chord_style(symbol)
        return chord.set_style(style)

    @classmethod
    def from_ChordData(cls, data: ChordData, style: Optional[ChordStyle] = None) -> 'Chord':
        '''
        Return a Chord object with the same data as the given 
        ChordData dictionary.
        '''
        chord = cls(
            note_names=tuple(data[NOTE_NAMES]),
            interval_names=tuple(data[INTERVAL_NAMES]),
            interval_structure=tuple(data[INTERVAL_STRUCTURE])
        )
        if style:
            return chord.set_style(style)
        return chord

    def get_style(self) -> ChordStyle:
        '''Return a dictionary of the chord's style configuration.'''
        return {
            SLASH: self.__slash,
            MAJ_SYMBOL: self.__maj_symbol,
            MIN_SYMBOL: self.__min_symbol,
            DIM_SYMBOL: self.__dim_symbol
        }

    def set_style(self, style:  ChordStyle) -> 'Chord':
        '''Configure the chord's style with a dictionary of options.'''
        self.__slash = style.get(SLASH, True)
        self.__maj_symbol = style.get(MAJ_SYMBOL, CHORD_MAJ)
        self.__min_symbol = style.get(MIN_SYMBOL, CHORD_MIN)
        self.__dim_symbol = style.get(DIM_SYMBOL, CHORD_DIM)
        return self

    def to_ChordData(self) -> ChordData:
        ''' 
        Return a dictionary of basic chord data without style configurations.
        '''
        return ChordData(
            chord_symbol=self.symbol,
            note_names=self.note_names,
            interval_names=self.interval_names,
            interval_structure=self.interval_structure)

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
        return self.from_ChordData(result, style=self.get_style())

    def apply_voicing(self, voicing: Sequence[int] | str) -> 'Chord':
        '''
        Return a voicing of this chord, according to the given structure.

        NOTE: The chord should be inverted, then voiced! If the order is not
        followed, the program will reset the chord before inverting it!

        Examples
        --------

        '''
        if isinstance(voicing, str):
            if voicing in [D2, OPEN]:
                voicing = DROP_2_VOICING
            elif voicing == D3:
                voicing = DROP_3_VOICING
            elif voicing == D23:
                voicing = DROP_2_AND_3_VOICING
            elif voicing == D24:
                voicing = DROP_2_AND_4_VOICING
            elif voicing == CLOSE:
                inversion = sort_interval_names(
                    self.interval_names).index(self.interval_names[0])
                return self.reset().invert(inversion)
            else:
                return self

        result = apply_drop_voicing(self.to_ChordData(), voicing)
        return self.from_ChordData(result, style=self.get_style())

    def use_slash(self, slash: bool) -> 'Chord':
        '''Configure the slash notation in the chord symbol.'''
        self.__slash = slash
        return self

    def set_maj_symbol(self, maj_symbol: str) -> 'Chord':
        '''Configure the 'major' symbol in the chord symbol.'''
        self.__maj_symbol = maj_symbol
        return self

    def set_min_symbol(self, min_symbol: str) -> 'Chord':
        '''Configure the 'minor' symbol in the chord symbol.'''
        self.__min_symbol = min_symbol
        return self

    def set_dim_symbol(self, dim_symbol: str) -> 'Chord':
        '''Configure the 'diminished' symbol in the chord symbol.'''
        self.__dim_symbol = dim_symbol
        return self

    def __len__(self) -> int:
        return len(self.note_names)

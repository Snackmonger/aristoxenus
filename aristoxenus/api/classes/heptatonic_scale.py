import re
from typing import Sequence

from aristoxenus.api.classes.chord import Chord
from aristoxenus.api.classes.note import Note
from aristoxenus.api.classes.scale import Scale
from aristoxenus.core.annotations import (
    NoteNameData
)
from aristoxenus.core.chordify import (
    chordify_heptatonic_sus, 
    chordify_heptatonic_tertial
)
from aristoxenus.core.constants import (
    HEPTATONIC_SCALES,
    NOTES,
    RE_PARSE_NOTE_NAME
)
from aristoxenus.core.heptatonic_spelling import (
    get_heptatonic_interval_names, 
    get_heptatonic_note_names
)
from aristoxenus.core.errors import ArgumentError
from aristoxenus.core.note_name import decode_note_name
from aristoxenus.core.resolve import (
    resolve_scale_alias, 
    resolve_heptatonic_scale
)
from aristoxenus.core.validation import validate_heptatonic_structure

__all__ = [
    'HeptatonicScale'
]



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
        if scale_name not in HEPTATONIC_SCALES:
            config = resolve_scale_alias(scale_name)
            if not validate_heptatonic_structure(resolve_heptatonic_scale(*config)):
                raise ArgumentError("This class can only be initialized with a heptatonic scale.")
            scale_name = config[0]
            mode_name = config[1]
            
        self.keynote = keynote
        self.scale_name = scale_name
        self.mode_name = mode_name


    @property
    def __kn(self) -> NoteNameData:
        '''The deciphered keynote.'''
        if not re.search(RE_PARSE_NOTE_NAME, self.keynote):
            raise ArgumentError('Unable to parse note name.')
        return decode_note_name(self.keynote)
    
    def get_degree(self, degree: int) -> Note:
        octave = 1
        if degree > NOTES:
            octave = int(degree / NOTES) + 1
            degree %= NOTES
        degree -= 1
        return Note(
            note_name=self.note_names[degree], 
            interval_name=self.interval_names[degree], 
            octave=octave
        )
    
    def get_native_pattern(self, pattern: Sequence[int]) -> tuple[Note, ...]:
        notes: list[Note] = []
        for i in pattern:
            notes.append(self.get_degree(i))
        return tuple(notes)

    @property
    def interval_structure(self) -> tuple[int, ...]:
        '''The interval structure of this scaleform.'''
        return resolve_heptatonic_scale(self.scale_name, self.mode_name)

    @property
    def note_names(self) -> tuple[str, ...]:
        '''The note names for this scaleform and keynote.'''
        return get_heptatonic_note_names(self.__kn, self.interval_structure)
    
    @property
    def interval_names(self) -> tuple[str, ...]:
        return get_heptatonic_interval_names(self.interval_structure)

    def get_tertial_chord(self, degree: int = 1, size: int = 3) -> Chord:
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
        if degree not in range(1, 8): 
            raise ArgumentError(f"Scale degree must be between 1 and 7 ({degree=})")
        if size not in range(3, 8):
            raise ArgumentError(f"Chord size must be between 3 and 7 ({size=})")

        degree -= 1
        if degree > len(self.note_names):
            degree %= len(self.note_names)
        ch_scale = chordify_heptatonic_tertial(self.__kn,
                                               self.interval_structure,  size)
        chord = ch_scale[degree]
        return Chord.from_ChordData(chord)

    def get_sus_chord(self, degree: int = 1, size: int = 3, sus: int = 2) -> Chord:
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
        if degree not in range(1, 8): 
            raise ArgumentError(f"Scale degree must be between 1 and 7 ({degree=})")
        if size not in range(3, 8):
            raise ArgumentError(f"Chord size must be between 3 and 7 ({size=})")
        if sus not in [2, 4]:
            raise ArgumentError(f"Can only suspend 2 or 4 ({sus=})")
        degree -= 1
        if degree > len(self.note_names):
            degree %= len(self.note_names)
        ch_scale = chordify_heptatonic_sus(
            self.__kn, self.interval_structure,  size, sus)
        chord = ch_scale[degree]
        return Chord.from_ChordData(chord)

    def get_tertial_triad(self, degree: int) -> Chord:
        '''Get the tertial triad at the given scale degree.'''
        return self.get_tertial_chord(degree, 3)

    def get_tertial_tetrad(self, degree: int) -> Chord:
        '''Get the tertial tetrad at the given scale degree.'''
        return self.get_tertial_chord(degree, 4)

    def get_sus2_triad(self, degree: int) -> Chord:
        '''Get the sus2 triad at the given scale degree.'''
        return self.get_sus_chord(degree, 3, 2)

    def get_sus4_triad(self, degree: int) -> Chord:
        '''Get the sus4 triad at the given scale degree.'''
        return self.get_sus_chord(degree, 3, 4)

    def get_sus2_tetrad(self, degree: int) -> Chord:
        '''Get the sus2 tetrad at the given scale degree.'''
        return self.get_sus_chord(degree, 4, 2)

    def get_sus4_tetrad(self, degree: int) -> Chord:
        '''Get the sus4 tetrad at the given scale degree.'''
        return self.get_sus_chord(degree, 4, 4)

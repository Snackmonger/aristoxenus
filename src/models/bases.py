from typing import Sequence


from src import (
    bitwise,
    nomenclature,
    parsing,
    rendering,
    interface
)
from .mixins import (
    ConverterMixin,
    MaterialMixin,
    ParserMixin
)


class Chord(ParserMixin, MaterialMixin, ConverterMixin):

    """
    PROTOTYPE
    ---------

    Interfaces
    ++++++++++
    As separate operations:
    scale = HeptatonicStructure(scale, mode, key)
    chord = scale.chord_scale(1)
    chord = chord.invert(3)
    chord = chord.voice((1, 3))

    As chained methods:
    chord = HeptatonicStructure(scale, mode, key).chord_scale(1).invert(3).voice((1, 3))

    Nomenclature
    ++++++++++++
    This class is a bit tricky to conceptualize, because we want to allow the user to 
    generate a chord without reference to any parent system. But this also means that 
    we have to be generic in our descriptions of the relations between notes.

    We need some kind of normalization method that can make some basic assumptions 
    about how a chord with an E root (E#, Ebb, etc.) should assume that the 7
    interval must be a D note (D##, Dbb, etc.) regardless of where it falls, and so on. 

    from_note_names(names) 
        - can easily generate an interval structure
        - to get the interval names:
            root provides the alphabetic start, assign 1234567 to ABCDEFG.
            if the note name in the chord has E, replace with 5 or whatever, 
            and keep the accidentals Ebb > 5bb
            we cannot reconstuct parent scale with certainty, we can get some
            cues about the interpretation of the structure.

    from_interval_structure(structure, keynote)
        - cannot distinguish between enharmonics: #4/b5 is ambiguous
            we can use the generic interval names
            then use the keynote as ABCDEFG index 0 and do the opposite of above.

            1, 3, b5 & Eb > Eb, G, Bbb
            use the encode_enharmonic(G#|Ab, G) >> G#, encode_enharmonic(A, B) >> Bbb

    from_chord_symbol(chord_symbol)
        - the chord symbol might contain information about its intervals' interpretation
            a tone is a 2 or a bb3, etc.
        - our chord symbol parsers will generate an integer interval structure where these
        distinctions will be lost...
        - unless we modify the existing system to return the specific intervals along with
        the integer structure when we parse the chord symbol??

    """

    def __init__(self) -> None:
        self.base_chord: str
        self.interval_structure: int
        self.note_names: tuple[str, ...]
        self.interval_names: tuple[str, ...]

    def __repr__(self) -> str:
        return f"<<{self.base_chord}>> [{' '.join(self.interval_names)} == {' '.join(self.note_names)}]"

    @classmethod
    def from_interval_structure(cls, interval_structure: int, keynote: str = "C") -> "Chord":
        chord_notes = interface.render_plain(
            interval_structure=interval_structure, keynote=keynote)
        return cls.from_note_names(chord_notes)

    @classmethod
    def from_note_names(cls, note_names: Sequence[str]) -> "Chord":
        new = cls()
        new.interval_structure = parsing.parse_literal_sequence(
            note_names=note_names)
        new.base_chord = note_names[0] + \
            cls.parse_interval_structure_as_chord_symbol(
                new.interval_structure)
        new.interval_names = rendering.render_plain(
            new.interval_structure, nomenclature.twelve_tone_scale_intervals())
        new.note_names = tuple(note_names)
        return new

    @classmethod
    def from_chord_symbol(cls, chord_symbol: str) -> "Chord":
        new = cls()
        data = parsing.parse_chord_symbol(chord_symbol=chord_symbol)
        new.note_names = data["note_names"]
        new.interval_structure = data["interval_structure"]
        new.interval_names = data["interval_names"]
        new.base_chord = chord_symbol
        return new

    def __copy(self) -> "Chord":
        """Return a deep copy of this instance."""
        new = self.__class__()
        new.note_names = self.note_names
        new.interval_structure = self.interval_structure
        new.interval_names = self.interval_names
        new.base_chord = self.base_chord
        return new

    def variants(self) -> tuple[int]:
        """Return all the canonical voicings in all the possible inversions
        for this chord.
        """

    def invert(self, inversion: int) -> "Chord":
        """Return a new instance of self in the given inversion."""
        new = self.__copy()
        new.note_names = self.note_names[inversion:] + self.note_names[:inversion]
        new.interval_names = self.interval_names[inversion:] + self.interval_names[:inversion]
        structure = self.interval_structure
        size = 12 if structure.bit_length() <= 12 else 24
        for _ in range(inversion):
            structure = bitwise.next_inversion(structure, size)
        new.interval_structure = structure
        return new

    def voice(self, voicing: tuple[int, int]) -> "Chord":
        """Return a new instance of self in the given voicing."""

    def count_halfsteps(self, note_1: int, note_2: int) -> int:
        """Return the number of halfsteps that separate two notes.

        Args:
            note_1, note_2 : Either note names, like "F#", or interval names,
            like "b3".
        """

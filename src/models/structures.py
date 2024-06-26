from typing import Sequence

from data import (
    annotations,
    constants,
    keywords
)
from src import (
    bitwise,
    nomenclature,
    parsing,
    rendering,
    interface,
    utils
)
from src.models.components import (
    Converter,
    Nomenclator,
    Parser
)


class Chord(Parser, Nomenclator, Converter):

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
        self.parent_is_known: bool

    def __repr__(self) -> str:
        return f"<<{self.base_chord}>> [{' '.join(self.interval_names)} == {' '.join(self.note_names)}]"

    @classmethod
    def from_interval_structure(cls, interval_structure: int, keynote: str = "C") -> "Chord":
        chord = cls.parse_interval_structure_as_chord_symbol(interval_structure)
        return cls.from_chord_symbol(chord)

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

    def variants(self) -> tuple[int, ...]:
        """Return all the canonical voicings in all the possible inversions
        for this chord.
        """

    def invert(self, inversion: int = 1) -> "Chord":
        """Return a new instance of self in the given inversion."""
        new = self.__copy()
        new.note_names = self.note_names[inversion:] + \
            self.note_names[:inversion]
        new.interval_names = self.interval_names[inversion:] + \
            self.interval_names[:inversion]
        structure = self.interval_structure
        size = 12 if structure.bit_length() <= 12 else 24
        for _ in range(inversion):
            structure = bitwise.next_inversion(structure, size)
        new.interval_structure = structure
        return new

    def voice(self, voicing: tuple[int, int]) -> "Chord":
        """Return a new instance of self in the given voicing."""

    def count_halfsteps(self, lower: str, higer: str) -> int:
        """Return the number of halfsteps that separate two notes.

        Args:
            note_1, note_2 : Either note names, like "F#", or interval names,
            like "b3".
        """


class HeptatonicStructure(Converter, Parser, Nomenclator):
    def __init__(self,
                 keynote: str,
                 scale_name: annotations.HeptatonicScales = keywords.DIATONIC,
                 modal_name: annotations.ModalNames = keywords.IONIAN,
                 ) -> None:
        self.scale_name: annotations.HeptatonicScales = scale_name
        self.modal_name: annotations.ModalNames = modal_name
        self.keynote: str = keynote

        # Populate details.
        data = interface.heptatonic_form(
            keynote, 
            scale_name, 
            modal_name
        )
        self.interval_structure: int = data[keywords.INTERVAL_STRUCTURE]
        self.interval_scale: tuple[str, ...] = data[keywords.INTERVAL_SCALE]
        self.interval_map: dict[str, str] = data[keywords.INTERVAL_MAP]
        self.binomial_rendering: tuple[str, ...] = data[keywords.BINOMIAL_RENDERING]
        self.forced_rendering: tuple[str, ...] = data[keywords.FORCED_RENDERING]
        self.best_keynote: str = data[keywords.BEST_KEYNOTE]
        self.best_rendering: tuple[str, ...] = data[keywords.BEST_RENDERING]
        self.scientific_map: dict[str, str] = nomenclature.heptatonic_range(
            self.forced_rendering
        )

    def scale_segment(self, start: int, end: int, descending: bool = False, octaves: int = 1) -> tuple[str, ...]:
        """Return a segment of the scale running from a starting degree to 
        an ending degree, and containing all the notes in between.

        Args:
            start:  The relative degree (1 to 7) that will begin the sequence.
            end:    The relative degree (1 to 7) that will end the sequence.
            descending: Flag to decide whether to reverse the final result.
            octaves: The number of octaves that the segment will span.
        """
        # Adjust for 0 index
        start -= 1
        end -= 1
        for x in [start, end]:
            if x not in range(7):
                raise ValueError(
                    "Must be a number between 1 and 7, inclusive.")
        if not 0 < octaves < constants.NUMBER_OF_OCTAVES:
            raise ValueError(
                f"Octaves must be between 1 and {constants.NUMBER_OF_OCTAVES}")
        if start == end and octaves == 1:
            octaves = 2

        segment = list(self.forced_rendering)
        if descending:
            segment.reverse()
        segment = list(utils.shift_array(
            segment, self.forced_rendering[start]))
        end = segment.index(self.forced_rendering[end]) + 1
        if octaves > 1:
            segment *= octaves
            end += (7 * (octaves - 1))
        return tuple(segment[: end])

    def contains(self, material: Sequence[int] | Sequence[str] | int | str) -> bool:
        """
        Test whether the given material is contained in the structure.

        Args:
            material: An integer representing an interval or interval 
            structure, or a string representing a note name,
            or an array of either of these types.
        Returns:
            True, if the material appears anywhere in the structure. 

        Notes:
            Intervals and interval structures will be considered from the
            tonic and will only match if the whole structure matches. This 
            means that although a major chord scale contains a minor chord on
            certain degrees, it would not match since the minor chord is not
            contained in the root position expression of the scaleform.
        """
        def __contains(material: int | str) -> bool:
            if isinstance(material, int):
                return bitwise.has_interval(self.interval_structure, material)
            return nomenclature.decode_enharmonic(material) in self.binomial_rendering

        if isinstance(material, (int, str)):
            return __contains(material)
        return all(__contains(x) for x in material)

    def chord_scale(self,
                    relative_degree: int,
                    notes: int = 3
                    ) -> Chord:
        """Return a chord from the chord scale of the instance's scaleform.

        Parameters:
            relative_degree: The scale degree from which to build the chord
            notes: The number of notes in the chord (default=3)
            formatting: A keyword indicating how to display the chord.

        Returns:
        {placeholder - default mapping of features, but this should become 
        its own class}
        """
        if not 0 < relative_degree < 8:
            raise ValueError(
                f"Requested degree must be between 1 and 7. Got value: {relative_degree}")
        if not 2 < notes < 8:
            raise ValueError(
                f"Number of notes must be between 2 and 7, inclusive. Got value: {notes}")
        chord_scale = interface.heptatonic_chord_scale(
            self.scale_name, self.modal_name, self.keynote, number_of_notes=notes)
        chord = Chord()
        ch_ = chord_scale["chord_scale"][relative_degree-1]
        chord.base_chord = ch_["chord_symbol"]
        chord.interval_names = ch_['interval_names']
        chord.note_names = ch_["note_names"]
        chord.interval_structure = ch_["interval_structure"]
        return chord

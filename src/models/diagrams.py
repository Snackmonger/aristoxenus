'''
Functions pertaining to making musical diagrams (aside from staff notation).
'''

import dataclasses

from src import nomenclature, utils
from data import (chord_symbols,
                  constants,
                  keywords)
from data.annotations import GuitarFretboard
from data.instrument_config import GUITAR_STANDARD_TUNING


def guitar_fretboard(strings: int = 6,
                     tuning: list[str] | tuple[str, ...] = GUITAR_STANDARD_TUNING,
                     frets: int = 24,
                     format_: str = keywords.SCIENTIFIC
                     ) -> GuitarFretboard:
    '''Return an array representing a guitar fretboard formatted to the given
    specifications.'''
    diagram: list[tuple[str, ...]] = []
    frets += 1
    if format_ is keywords.SCIENTIFIC:
        all_notes = nomenclature.scientific_range()
        tuning = list(map(nomenclature.decode_scientific_enharmonic, tuning))

    elif format_ is keywords.PLAIN:
        all_notes = nomenclature.chromatic() * constants.TONES
        tuning = list(map(nomenclature.decode_enharmonic, tuning))

    else:
        raise ValueError(format_)

    for string in range(strings):
        starting_note = all_notes.index(tuning[string])
        ending_note = starting_note + frets
        string_notes = all_notes[starting_note: ending_note]
        diagram.append(tuple(string_notes))

    diagram.reverse()
    return tuple(diagram)


def simplify_guitar_fretboard(fretboard: GuitarFretboard) -> GuitarFretboard:
    '''Take an array representing a guitar fretboard and make sure that all note
    names are in plain (not scientific) notation.'''
    new_diagram: list[tuple[str, ...]] = []
    for string in fretboard:
        new_diagram.append(tuple(map(nomenclature.decode_enharmonic, string)))

    return tuple(new_diagram)


def standard_fretboard() -> GuitarFretboard:
    """Shortcut to get a fretboard in standard 6 string tuning with 
    24 frets with plain binomial note names."""
    return simplify_guitar_fretboard(guitar_fretboard())


def filter_guitar_fretboard(fretboard: GuitarFretboard,
                            note_list: tuple[str, ...] | list[str]
                            ) -> GuitarFretboard:
    '''For the given fretboard array, replace any note that is not represented
    in the given list of notes with the "-" symbol.'''
    diagram: list[tuple[str, ...]] = []
    new_string: list
    for string in fretboard:
        new_string = []
        for note in string:
            new_string.append(note if note in note_list else "-")
        diagram.append(tuple(new_string))

    return tuple(diagram)


def get_positional_fingering(fretboard: GuitarFretboard,
                             starting_column: int,
                             span: int
                             ) -> GuitarFretboard:
    '''Return a slice of the columns of a guitar fretboard, representing the span
    of a positional fingering.'''
    diagram: list[tuple[str, ...]] = []
    for string in fretboard:
        diagram.append(tuple(note for index, note in enumerate(
            string) if index in range(starting_column, starting_column+span)))

    return tuple(diagram)


def convert_fretboard_to_relative(diagram: GuitarFretboard,
                                  tonal_centre: str
                                  ) -> GuitarFretboard:
    '''
    Convert a fretboard diagram to use interval symbols instead of note names.
    '''
    diagram = simplify_guitar_fretboard(diagram)
    interval_symbols = list(
        chord_symbols.interval_symbol_prescription.values())
    chromatic_ = utils.shift_list(nomenclature.chromatic(), tonal_centre)
    conversion: dict[str, str] = dict(zip(chromatic_, interval_symbols))

    new_diagram: list[tuple[str, ...]] = []
    for string in diagram:
        new_string = []
        for note in string:
            new_string.append(conversion[note])
        new_diagram.append(tuple(new_string))

    return tuple(new_diagram)


def get_interval_map(tonal_centre: str) -> dict[str, str]:
    """Get a dictionary mapping note names to interval names for a given 
    tonic note name. 

    By default, this function uses the Aristoxenus library's prescribed 12-tone 
    interval names, but these will not always describe the underlying scale 
    accurately (e.g. in the treatment of b3 vs #2, etc.)."""
    interval_symbols = list(
        chord_symbols.interval_symbol_prescription.values())
    chromatic_ = utils.shift_list(nomenclature.chromatic(), tonal_centre)
    return dict(zip(chromatic_, interval_symbols))


@dataclasses.dataclass
class FingeringNode:
    """Representation of a position in a fingering diagram, that can indicate
    a scale degree, finger, or musical note."""

    def __init__(self,
                 string: int,
                 fret: int,
                 finger: str | None = None,
                 note_name: str | None = None,
                 scale_degree: str | None = None,
                 is_active: bool = False,
                 is_scale_tone: bool = False,
                 is_chord_tone: bool = False,
                 is_chromatic_tone: bool = False,
                 shape: str = "circle",
                 shape_colour: str = "black",
                 text_colour: str = "white",
                 rendering_mode: str = keywords.FRET
                 ) -> None:

        # Used to evaluate the awkwardness of a fingering
        self.string: int = string
        self.fret: int = fret

        # Basic diagram information
        self.finger: str | None = finger
        self.note_name: str | None = note_name
        self.scale_degree: str | None = scale_degree
        self.rendering_mode: str = rendering_mode
        self.is_active: bool = is_active
        self.is_scale_tone: bool = is_scale_tone
        self.is_chord_tone: bool = is_chord_tone
        self.is_chromatic_tone: bool = is_chromatic_tone
        self.shape: str = shape
        self.shape_colour: str = shape_colour
        self.text_colour: str = text_colour


    def __repr__(self) -> str:
        if not self.is_active:
            return str()

        match self.rendering_mode:
            case keywords.FRET:
                return str(self.fret)
            case keywords.FINGER:
                if self.finger is not None:
                    return self.finger
            case keywords.NOTE_NAME:
                if self.note_name is not None:
                    return self.note_name
            case keywords.SCALE_DEGREE:
                if self.scale_degree is not None:
                    return self.scale_degree
            case _:
                raise ValueError(
                    f"Unrecognized rendering mode: {self.rendering_mode}")
        return str()



class GuitarFingeringDiagram:
    """Representation of a 4- or 5-fret fingering diagram in standard tuning, 
    that can display its nodes as names, intervals, or fingers, and that can
    turn nodes on and off in order to show arpeggios nested within scale 
    forms."""

    def __init__(self,
                 position: int,
                 fretboard: GuitarFretboard,
                 width: int,
                 fingering_type: str | None = None
                 ) -> None:
        
        # The fretboard is an absolute reference
        # point for notes in each postition.
        self.fretboard: GuitarFretboard = fretboard
        self.position: int = position

        # Width defines how many frets are covered in the fingering (4 or 5)
        self.width: int = width
        # Stretch defines which finger must cover two frets if width == 5.
        self.fingering_type: str | None = fingering_type

        # Override the default fingering diagram, if not None
        self.override: list[list[str]] | None = None

        self.grid: list[list[FingeringNode]] = self.refresh_grid()
        

    def refresh_grid(self) -> list[list[FingeringNode]]:
        """Create an array of FingeringNodes based on the information in the 
        ``fretboard`` and ``position`` and ``width`` attributes."""
        grid: list[list[FingeringNode]] = []
        for i, s in enumerate(self.fretboard):
            string: list[FingeringNode] = []
            for n in range(self.width):
                name: str = self.fretboard[i][self.position + n]
                fret: int = self.position + n
                string.append(FingeringNode(i, fret, note_name=name))
            grid.append(string)
        return grid
    

    @property
    def lowest_note(self) -> bool:
        """Indicate whether the current diagram is set so that the
        lowest note of the diagram is occupied by an active node."""
        return self.grid[0][0].is_active


    def clear_diagram(self) -> None:
        """Set all nodes in the diagram to OFF."""
        for string in self.grid:
            for note in string:
                note.is_active = False


    def flash_diagram(self) -> None:
        """Set all nodes in the diagram to ON."""
        for string in self.grid:
            for note in string:
                note.is_active = True


    def mask_note_names(self, note_names: list[str]) -> None:
        """Switch ON any node that contains one of the given note names, 
        and switch OFF any node that doesn't."""
        for string in self.grid:
            for note in string:
                note.is_active = note.note_name in note_names


    def define_scale(self, note_names: list[str]) -> None:
        """Raise the scale flag for any node that contains a scale tone, and
        conversely, raise the chromatic flag for any node that does not 
        contain a scale tone."""
        for string in self.grid:
            for note in string:
                note.is_scale_tone = note.note_name in note_names
                note.is_chromatic_tone = note.note_name not in note_names


    def define_chord(self, note_names: list[str]) -> None:
        """Raise the chord flag for any node that contains a chord tone."""
        for string in self.grid:
            for note in string:
                note.is_chord_tone = note.note_name in note_names


    def define_intervals(self, interval_map: dict[str, str]) -> None:
        """Add intervals to the fretboard diagram. This entails defining a key
        note and generating a map of note names to intervals, relative to that
        key note (use the ``get_interval_map`` function to do this).
        
        The intervals will exist for the whole fretboard; it is not necessary
        to redefine intervals for a different position or scale, but a new key
        does require new intervals."""
        for string in self.grid:
            for note in string:
                if note.note_name:
                    note.scale_degree = interval_map[note.note_name]


    def fade_scale(self, colour: str = "gray") -> None:
        """Recolour any node that contains a scale tone but does not contain 
        a chord tone. This allows us to show arpeggios in full-colour against
        their parent scale forms in faded colour."""
        for string in self.grid:
            for note in string:
                if note.is_scale_tone and not note.is_chord_tone:
                    note.shape_colour = colour
                    

    def apply_fingering(self) -> None:
        """Take the rules defined in ``width`` and ``stretch`` 
        attributes and assign fingerings to the nodes."""
        if self.override:
            for i, string in enumerate(self.grid):
                for j, note in enumerate(string):
                    note.finger = self.override[i][j]
            return

        fingers: list[str]
        if self.width == 4:
            fingers = ["i", "m", "a", "e"]
        elif self.fingering_type == keywords.INDEX:
            fingers = ["i", "i", "m", "a", "e"]
        elif self.fingering_type == keywords.PINKY:
            fingers = ["i", "m", "a", "e", "e"]

        for string in self.grid:
            for j, note in enumerate(string):
                note.finger = fingers[j]

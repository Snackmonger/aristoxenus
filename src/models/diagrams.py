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
    '''
    Return an array representing a guitar fretboard formatted to the given
    specifications.
    '''
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


def simplify_guitar_fretboard(diagram: GuitarFretboard) -> GuitarFretboard:
    '''
    Take an array representing a guitar fretboard and make sure that all note
    names are in plain (not scientific) notation.
    '''
    new_diagram: list[tuple[str, ...]] = []
    for string in diagram:
        new_diagram.append(tuple(map(nomenclature.decode_enharmonic, string)))
        
    return tuple(new_diagram)


def standard_fretboard() -> GuitarFretboard:
    """Shortcut to get a fretboard in standard 6 string tuning with 
    24 frets with plain binomial note names."""
    return simplify_guitar_fretboard(guitar_fretboard())


def filter_guitar_fretboard(guitar_tuning: GuitarFretboard,
                            note_list: tuple[str, ...] | list[str]
                            ) -> GuitarFretboard:
    '''
    For the given fretboard array, replace any note that is not represented
    in the given list of notes with the "-" symbol.
    '''
    diagram: list[tuple[str, ...]] = []
    new_string: list
    for string in guitar_tuning:
        new_string = []
        for note in string:
            new_string.append(note if note in note_list else "-")
        diagram.append(tuple(new_string))

    return tuple(diagram)


def get_positional_fingering(guitar_fingering: GuitarFretboard,
                             starting_column: int,
                             span: int
                             ) -> GuitarFretboard:
    '''
    Return a slice of the columns of a guitar fretboard, representing the span
    of a positional fingering.
    '''
    diagram: list[tuple[str, ...]] = []
    for string in guitar_fingering:
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
    interval_symbols = list(chord_symbols.interval_symbol_prescription.values())
    chromatic_ = utils.shift_list(nomenclature.chromatic(), tonal_centre)
    conversion: dict[str, str] = dict(zip(chromatic_, interval_symbols))

    new_diagram: list[tuple[str, ...]] = []
    for string in diagram:
        new_string = []
        for note in string:
            new_string.append(conversion[note])
        new_diagram.append(tuple(new_string))

    return tuple(new_diagram)


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
                 repr_mode: str = keywords.FRET
                 ) -> None:
        
        self.string: int = string
        self.fret: int = fret
        self.finger: str | None =  finger
        self.note_name: str | None = note_name
        self.scale_degree: str | None = scale_degree
        self.is_active: bool = is_active
        self.repr_mode: str = repr_mode


        # Graphics display options
        self.shape: str
        self.colour: str | tuple[int, int, int]


    def __repr__(self) -> str:
        if not self.is_active:
            return str()
        
        if self.repr_mode is keywords.FRET:
            return str(self.fret)

        match self.repr_mode:
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
                raise ValueError(f"Unrecognized rendering mode: {self.repr_mode}")
        return str()


    def flip(self) -> None:
        self.is_active = not self.is_active


class GuitarFingering:
    """Representation of a 4- or 5-fret fingering diagram in standard tuning, 
    that can display its nodes as names, intervals, or fingers, and that can
    turn nodes on and off in order to show arpeggios nested within scale 
    forms.
    
    The fingering diagrams assume that we are using standard tuning, and are
    mostly intended for use with the diatonic scale and those scales that are
    related by 1 transformation but that do not contain a hemiolion."""
    def __init__(self,
                 position: int,
                 fretboard: GuitarFretboard,
                 width: int,
                 stretch: str | None = None
                 ) -> None:
        
        self.position: int = position
        self.fretboard: GuitarFretboard = fretboard
        self.width: int = width
        self.stretch: str | None = stretch
        self.grid: list[list[FingeringNode]] = [[FingeringNode(string, position + n, note_name=fretboard[string][position + n]) for n in range(width)] for string in range(len(fretboard))]
        self.override: list[list[str]] | None = None
        

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
        """Switch off any node that does not have a note named in the given 
        list."""
        for string in self.grid:
            for note in string:
                if note.note_name not in note_names:
                    note.is_active = False


    def define_intervals(self, interval_diagram: GuitarFretboard) -> None:
        """Add intervals to the fretboard diagram. This entails defining a key
        note and generating a layout relative to that note; see the function
        ``convert_fretboard_to_relative`` to do this."""
        if self.position + self.width > len(interval_diagram):
            raise ValueError(f"Fingering is not compatible with the given diagram. Position={self.position}, diagram length={len(interval_diagram)}")
        diagram = interval_diagram[self.position: self.position + self.width]

        for i, string in enumerate(diagram):
            for j, note in enumerate(string):
                self.grid[i][j].scale_degree = note
                

    def apply_fingering(self) -> None:
        """Take the rules defined in width and stretch attributes and make a 
        fingering pattern."""
        if self.override:
            for i, string in enumerate(self.grid):
                for j, note in enumerate(string):
                    note.finger = self.override[i][j]
            return
        
        fingers: list[str]
        if self.width == keywords.CLOSE:
            fingers = ["i", "m", "a", "e"]
        elif self.stretch == keywords.INDEX:
            fingers = ["i", "i", "m", "a", "e"]
        elif self.stretch == keywords.PINKY:
            fingers = ["i", "m", "a", "e", "e"]

        for string in self.grid:
            for j, note in enumerate(string):
                note.finger = fingers[j]
        





    


    

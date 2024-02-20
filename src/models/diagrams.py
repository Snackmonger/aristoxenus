'''
Functions pertaining to making musical diagrams (aside from staff notation).
'''
from src import nomenclature, utils
from data import (chord_symbols,
                  constants,
                  keywords)
from data.annotations import GuitarFretboard, NodeDisplayReport
from data.intervallic_canon import DIATONIC_SCALE
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
    new_string: list[str]
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
    new_string: list[str]
    new_diagram: list[tuple[str, ...]] = []
    for string in diagram:
        new_string = []
        for note in string:
            new_string.append(conversion[note])
        new_diagram.append(tuple(new_string))

    return tuple(new_diagram)


def get_interval_map(tonal_centre: str, scale: int = DIATONIC_SCALE) -> dict[str, str]:
    """Get a dictionary mapping note names to interval names for a given 
    tonic note name and heptatonic scale form.

    This function will always preserve the correct interval names for the 
    given heptatonic scale, plus 5 supplementary interval names that occupy
    the chromatic gaps in the scale."""
    interval_symbols = list(nomenclature.twelve_tone_scale_intervals(scale))
    chromatic_ = utils.shift_list(nomenclature.chromatic(), tonal_centre)
    return dict(zip(chromatic_, interval_symbols))


class FingeringNode:
    """Representation of a position in a fingering diagram, that can indicate
    a scale degree, finger, or musical note, and can be represented by various
    shapes and colours."""

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
                 shape: str = keywords.CIRCLE,
                 shape_colour: str = keywords.BLACK,
                 shape_size: int = 2,
                 text_colour: str = keywords.WHITE,
                 text_size: int = 14,
                 rendering_mode: str = keywords.INTERVAL
                 ) -> None:

        # Location of the node in the array
        # (Not currently used)
        self.string: int = string
        self.fret: int = fret

        # Identity
        self.note_name: str | None = note_name
        self.interval: str | None = scale_degree
        self.finger: str | None = finger
        self.rendering_mode: str = rendering_mode

        # Rendering flags
        self.is_active: bool = is_active
        self.is_scale_tone: bool = is_scale_tone
        self.is_chord_tone: bool = is_chord_tone
        self.is_chromatic_tone: bool = is_chromatic_tone

        # Rendering options
        self.shape: str = shape
        self.shape_colour: str = shape_colour
        self.shape_size: int = shape_size
        self.text_colour: str = text_colour
        self.text_size: int = text_size

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
            case keywords.INTERVAL:
                if self.interval is not None:
                    return self.interval
            case _:
                raise ValueError(
                    f"Unrecognized rendering mode: {self.rendering_mode}")
        return str()

    def change_settings(self, report: NodeDisplayReport) -> None:
        """Update the settings for this node's display options."""
        for k, v in report.items():
            if hasattr(self, k) and k in list(NodeDisplayReport.__annotations__):
                setattr(self, k, v)


class GuitarFingeringDiagram:
    """Representation of a 4- or 5-fret fingering diagram in standard tuning, 
    that can display its nodes as names, intervals, or fingers, and that can
    turn nodes on and off in order to show arpeggios nested within scale 
    forms."""

    def __init__(self,
                 position: int = 5,
                 fretboard: GuitarFretboard = standard_fretboard(),
                 width: int = 5
                 ) -> None:

        # The fretboard is an absolute reference point for notes in each
        # postition. If we want to change the tuning, number of notes, or
        # number of frets, we have to create a new instance with the proper
        # base fretboard.
        self.fretboard: GuitarFretboard = fretboard

        # Position determines which fret will be the lowest in the diagram.
        self.position: int = position

        # Width defines how many frets are shown in the diagram (4 or 5)
        self.width: int = width

        # A table of nodes that can be turned on/off and change appearance.
        self.grid: list[list[FingeringNode]] = self.new_grid()

    def new_grid(self) -> list[list[FingeringNode]]:
        """Create an array of FingeringNodes based on the information in the 
        ``fretboard``, ``position``, and ``width`` attributes."""
        grid: list[list[FingeringNode]] = []
        for i, s in enumerate(self.fretboard):
            string: list[FingeringNode] = []
            for n in range(self.width):
                name: str = self.fretboard[i][self.position + n]
                fret: int = self.position + n
                string.append(FingeringNode(i, fret, note_name=name))
            grid.append(string)
        return grid

    def change_position(self, position: int) -> None:
        """Change the position of the diagram.

        This entails creating a new grid, so we transfer the old node
        options from the current grid to the new grid, maintianing the current
        display options."""

        self.position = position
        new: "GuitarFingeringDiagram" = self.__class__(
            position, self.fretboard, self.width)
        mode = self.grid[0][0].rendering_mode
        new.define_scale(self.active_names)
        new.define_intervals(self.interval_map)
        new.turn_on_names(self.active_names)
        new.apply_rendering_mode(mode)
        self.grid = new.grid

    @property
    def interval_map(self) -> dict[str, str]:
        """Return a list of all interval names for which at least 1 node is active."""
        return {x.note_name: x.interval for s in self.grid for x in s if x.interval and x.note_name}

    @property
    def active_names(self) -> list[str]:
        """Return a list of all note names for which at least 1 node is active."""
        return [x.note_name for s in self.grid for x in s if x.is_active and x.note_name]

    @property
    def keynote(self) -> str:
        """Return the note name that correlates to the interval 1."""
        for s in self.grid:
            for x in s:
                if x.interval and x.interval == "1":
                    assert isinstance(x.note_name, str)
                    return x.note_name
        raise ValueError("Keynote data not available.")

    @property
    def lowest_note_is_aligned(self) -> bool:
        """Indicate whether the current diagram is set so that the
        lowest note of the diagram is occupied by an active node."""
        return self.grid[0][0].is_active

    @property
    def number_of_strings(self) -> int:
        """Return the number of strings (rows) in the current fretboard."""
        return len(self.fretboard)

    @property
    def number_of_frets(self) -> int:
        """Return the number of frets (columns) in the current fretboard."""
        return len(self.fretboard[0])

    def positions(self, scale: list[str]) -> list[int]:
        """Return the fret numbers where the given scale has notes on the
        lowest string, up to fret 12."""
        return [i for i, s in enumerate(self.fretboard[0]) if s in scale and 0 < i < 13]

    def clear_diagram(self) -> None:
        """Set all nodes in the diagram to OFF."""
        for string in self.grid:
            for node in string:
                node.is_active = False

    def flash_diagram(self) -> None:
        """Set all nodes in the diagram to ON."""
        for string in self.grid:
            for node in string:
                node.is_active = True

    def apply_fingering(self, string: int, fingering: str) -> None:
        """Change the fingering of the given string to the given type."""

        # This should be moved somewhere else
        types = {keywords.INDEX: ["i", "i", "m", "a", "e"],
                 keywords.PINKY: ["i", "m", "a", "e", "e"]}

        fingers = types[fingering]
        for j, note in enumerate(self.grid[string]):
            note.finger = fingers[j]

    def apply_rendering_mode(self, rendering_mode: str) -> None:
        """Change the rendering mode of the diagram's nodes."""
        for string in self.grid:
            for node in string:
                node.rendering_mode = rendering_mode

    def apply_display_options(self, report: NodeDisplayReport) -> None:
        """Apply the display options contained in the given report."""
        interval: str = report["interval"]
        for s in self.grid:
            for n in s:
                if n.interval == interval:
                    n.change_settings(report)

    def orient(self, scale: list[str], interval_map: dict[str, str], chord: list[str]) -> None:
        """Orient the current diagram to the given scale, chord, and 
        intervallic perspective."""
        self.turn_on_names(scale)
        self.define_scale(scale)
        self.define_chord(chord)
        self.define_intervals(interval_map)

    def turn_on_names(self, note_names: list[str]) -> None:
        """Switch ON any node that contains one of the given note names, 
        and switch OFF any node that doesn't."""
        for string in self.grid:
            for node in string:
                node.is_active = node.note_name in note_names

    def define_scale(self, note_names: list[str]) -> None:
        """Raise the scale flag for any node that contains a scale tone, and
        conversely, raise the chromatic flag for any node that does not 
        contain a scale tone."""
        for string in self.grid:
            for node in string:
                node.is_scale_tone = node.note_name in note_names
                node.is_chromatic_tone = node.note_name not in note_names

    def define_chord(self, note_names: list[str]) -> None:
        """Raise the chord flag for any node that contains a chord tone."""
        for string in self.grid:
            for node in string:
                node.is_chord_tone = node.note_name in note_names

    def define_intervals(self, interval_map: dict[str, str]) -> None:
        """Add intervals to the fretboard diagram. This entails defining a key
        note and generating a map of note names to intervals, relative to that
        key note (use the ``get_interval_map`` function to do this).

        The intervals will exist for the whole fretboard; it is not necessary
        to redefine intervals for a different position or scale, but a new key
        does require new intervals."""
        for string in self.grid:
            for node in string:
                if node.note_name:
                    node.interval = interval_map[node.note_name]

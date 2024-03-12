"""Type aliases to make the syntax of type hints easier to read."""

from typing import Mapping, Sequence, TypeAlias, TypedDict, Literal


GuitarFretboard: TypeAlias = Sequence[Sequence[str]]

###############################################################################
# Canonical scaleform sets
###############################################################################

HeptatonicScales = Literal["diatonic",
                           "altered",
                           "hemitonic",
                           "hemiolic",
                           "diminished",
                           "augmented",
                           "harmonic",
                           "biseptimal",
                           "paleochromatic"]

ModalNames = Literal['ionian', 
                     'dorian', 
                     'phrygian', 
                     'lydian', 
                     'mixolydian', 
                     'aeolian', 
                     'locrian']

###############################################################################
# Chord permutations
###############################################################################

class TriadConspectus(TypedDict):
    '''
    A collection of all permutations of a triad's inversions and voicings.
    '''
    canonical_name: str
    canonical_form: int
    close: dict[str, int]
    open: dict[str, int]


class TetradConspectus(TypedDict):
    '''
    A collection of all permutations of a tetrad's inversions and voicings.
    '''
    canonical_name: str
    canonical_form: int
    close: dict[str, int]
    drop_2: dict[str, int]
    drop_3: dict[str, int]
    drop_2_and_4: dict[str, int]


TriadInventory: TypeAlias = Sequence[TriadConspectus]
TetradInventory: TypeAlias = Sequence[TetradConspectus]
ChordInventory: TypeAlias = TriadInventory | TetradInventory

###############################################################################
# Data associated with specific callback functions in the GUI
###############################################################################

class ScaleformReport(TypedDict):
    """Report about a scaleform selection. 

    Used by the GUI to handle the state of the scale selector widget.
    """
    scale_name: HeptatonicScales
    modal_name: ModalNames
    keynote: str


class FingeringReport(TypedDict):
    """Report about the fingering of a string on a guitar.

    Used by the GUI to handle the state of the string fingering widgets.
    """
    string: int
    fingering: str


class NodeDisplayReport(TypedDict):
    """Report about the display options for nodes in the guitar fingering
    diagram.

    Used by the GUI to handle the state of the node display widgets.
    """
    interval: str
    shape: str
    size: int
    shape_colour: str
    text_colour: str
    text_size: int


class ArpeggioFormReport(TypedDict):
    """Report about an arpeggio selection.

    Used by the GUI to handle the state of the arpeggio selector widget.
    """
    number_of_notes: int  # triad, tetrad
    base_interval: int  # tertial, quartal
    current_rotation: int  # keeps the chord's intervals synched
    node_display_reports: list[NodeDisplayReport]



###############################################################################
# Data assembled for return through the API
###############################################################################


class HeptatonicChord(TypedDict):
    """A representation of a chordform contextualized in its parent scale and 
    modal rotation. 

    The intervals of the chord will respect the logic of the nomenclature of
    the parent form, e.g. natural 2 might be spelled bb3 in some contexts, etc.
    """
    numeric_degree: str
    root: str
    notes: list[str]
    interval_structure: int
    interval_names: list[str]
    chord_symbol: str
    roman_degree: str

class APIChordScaleResponse(TypedDict):
    """A response from the API containing information about the member chords
    of a scaleform.
    """
    scale: str
    mode: str
    keynote: str
    notes: int
    step: int
    chord_scale: list[HeptatonicChord]

class APIScaleFormResponse(TypedDict):
    """Response from the API containing information about a scaleform and its
    properties.
    """
    scale_name: str
    modal_name: str
    interval_structure: int
    interval_scale: list[str]
    interval_map: dict[str, str]
    keynote: str
    chromatic_rendering: list[str]
    alphabetic_rendering: list[str]
    optimal_keynote: str
    optimal_rendering: list[str]

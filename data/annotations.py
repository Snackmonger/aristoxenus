"""Type aliases to make the syntax of type hints easier to read."""

from typing import Sequence, TypeAlias, TypedDict, Literal



###############################################################################
# Canonical scaleform sets
###############################################################################

HeptatonicScales: TypeAlias = Literal["diatonic",
                           "altered",
                           "hemitonic",
                           "hemiolic",
                           "diminished",
                           "augmented",
                           "harmonic",
                           "biseptimal",
                           "paleochromatic"]

ModalNames: TypeAlias = Literal['ionian', 
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
# Data assembled for return through the API
###############################################################################


class APIChordSymbolResponse(TypedDict):
    """A response from the API containing information about a chord symbol."""
    chord_symbol: str
    note_names: tuple[str, ...]
    interval_structure: int


class HeptatonicChord(TypedDict):
    """A representation of a chordform contextualized in its parent scale and 
    modal rotation. 

    The intervals of the chord will respect the logic of the nomenclature of
    the parent form, e.g. natural 2 might be spelled bb3 in some contexts, etc.
    """
    numeric_degree: str
    root: str
    notes: list[str]
    binomial_notes: list[str]
    interval_structure: int
    interval_names: list[str]
    chord_symbol: str
    roman_chord: str
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
    interval_scale: tuple[str, ...]
    interval_map: dict[str, str]
    keynote: str
    chromatic_rendering: tuple[str, ...]
    alphabetic_rendering: tuple[str, ...]
    optimal_keynote: str
    optimal_rendering: tuple[str, ...]

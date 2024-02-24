"""Type aliases to make the syntax of type hints easier to read."""

from typing import Mapping, Sequence, TypeAlias, TypedDict, NotRequired


GuitarFretboard: TypeAlias = tuple[tuple[str, ...], ...]


class ChordConspectus(TypedDict):
    '''
    A collection of all permutations of a chord's inversions and voicings.

    Individual keys will vary depending on chord type (triad/tetrad).
    '''
    canonical_name: str
    canonical_form: int
    close: NotRequired[Mapping[str, int]]
    open: NotRequired[Mapping[str, int]]
    drop_2: NotRequired[Mapping[str, int]]
    drop_3: NotRequired[Mapping[str, int]]
    drop_2_and_4: NotRequired[Mapping[str, int]]


ChordInventory: TypeAlias = tuple[ChordConspectus, ...]


class ScaleformReport(TypedDict):
    """Report about a scaleform selection. 
    
    Used by the GUI to handle the state of the scale selector widget.
    """
    scale_name: str
    modal_name: str
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
    number_of_notes: int # triad, tetrad
    base_interval: int  # tertial, quartal
    current_rotation: int # keeps the chord's intervals synched
    node_display_reports: list[NodeDisplayReport] # not sure if this will be needed


class APIScaleFormResponse(TypedDict):
    """Response from the API containing information about a scaleform and its
    properties.
    """
    scale_name: str
    modal_name: str
    interval_structure: int
    interval_scale: Sequence[str]
    interval_map: Mapping[str, str]
    keynote: str
    chromatic_rendering: Sequence[str]
    alphabetic_rendering: Sequence[str]
    optimal_keynote: str
    optimal_rendering: Sequence[str]

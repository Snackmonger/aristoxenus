"""Type aliases to make the syntax of type hints easier to read."""

from typing import TypeAlias, TypedDict, NotRequired


GuitarFretboard: TypeAlias = tuple[tuple[str, ...], ...]


class ChordConspectus(TypedDict):
    '''
    A collection of all permutations of a chord's inversions and voicings.

    Individual keys will vary depending on chord type (triad/tetrad).
    '''
    canonical_name: str
    canonical_form: int
    close: NotRequired[dict[str, int]]
    open: NotRequired[dict[str, int]]
    drop_2: NotRequired[dict[str, int]]
    drop_3: NotRequired[dict[str, int]]
    drop_2_and_4: NotRequired[dict[str, int]]

ChordInventory: TypeAlias = tuple[ChordConspectus, ...]


class ScaleformReport(TypedDict):
    """Report about a scaleform."""
    scale: str
    mode: str
    keynote: str


class FingeringReport(TypedDict):
    """Report about the fingering of a string on a guitar."""
    string: int
    fingering: str


class NodeDisplayReport(TypedDict):
    interval: str
    shape: str
    size: int
    colour: str
    text_colour: str
    text_size: int

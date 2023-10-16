from typing import TypedDict, NotRequired

GuitarFretboard = tuple[tuple[str, ...], ...]


class ScaleConspectus(TypedDict):
    ...


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


InventoryConspectus = tuple[ChordConspectus | ScaleConspectus, ...]


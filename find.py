from typing import Sequence, TypedDict

from src.constants import (
    HEPTATONIC_SCALES,
    HEPTATONIC_SUPPLEMENT,
    MODAL_SERIES_KEYS,
    SCALE_ALIASES
)
from src.core import rotate_interval_structure


class ScalePatternResponse(TypedDict):
    '''
    Data from the ``find_pattern`` API endpoint.
    '''
    interval_structure: tuple[int, ...]
    scale_name: str
    modal_name: str
    aliases: tuple[str, ...]


def find_pattern(interval_structure: Sequence[int] | int) -> ScalePatternResponse:
    '''
    Search the list of scale names for a given scale pattern.

    Parameters
    ----------
    interval_structure : Sequence[int] | int
        A scale pattern, either a collection of integers representing
        intervals in 12-tone temperament, or a single 12-bit integer 
        representing an interval structure in binary (LSB==unison).

    Returns
    -------
    ScalePatternResponse
        The input, the scale and modal names of the given form, and any
        known aliases.

    Raises
    ------
    ValueError
        If the input pattern is not valid.

    TimeoutError
        If the input pattern cannot be found.
    '''

    # When a scale pattern is int, LSB is the unison, so all valid scales
    # must be odd numbers, e.g. 2741 = 101010110101 -> [0, 2, 4, 5, 7, 9, 11]
    if isinstance(interval_structure, int):
        if interval_structure % 2 == 0:
            raise ValueError(
                f"Scale pattern integers must be odd numbers ({interval_structure=}).")
        interval_structure = [i for i in range(12) if (
            n := 1 << i) & interval_structure == n]

    for scale_group in [HEPTATONIC_SCALES, HEPTATONIC_SUPPLEMENT]:
        for scale, base in scale_group.items():
            for i, mode in enumerate(MODAL_SERIES_KEYS):
                pattern = rotate_interval_structure(base, i)
                if set(pattern) == set(interval_structure):
                    aliases = [name for name, (s, m) in SCALE_ALIASES.items() if (
                        s == scale and m == mode)]
                    return ScalePatternResponse(
                        interval_structure=tuple(interval_structure),
                        scale_name=scale,
                        modal_name=mode,
                        aliases=tuple(aliases)
                    )

    # TODO: check other types of scales after this...

    raise TimeoutError("Checked all known scales with no match.")


find_pattern(2741)

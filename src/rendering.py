
from typing import Optional, Sequence
from data import (
    constants
)
from src import (
    nomenclature
)

def render_plain(
    interval_structure: int, 
    chromatic_scale: Sequence[str] | None = None
    ) -> tuple[str, ...]:
    """
    Return a human-readable list of strings representing the interval structure
    in the given accidental style.

    :param interval_structure: An integer representing the interval structure
        to be rendered.
    :param chromatic_scale: The 12-note chromatic scale you want to use to 
        render the structure. Default is the binomials.
    :return: A rendering of the given interval structure in the given chromatic
        accidental style.

    .. note::
        If the number of notes in the interval structure exceeds those of the
        chromatic scale, we extend the scale to accommodate the extra notes.
        The resulting structure will make no distinction between octaves. Use
        this function when you want to display a basic abstract structure 
        quickly.

    :Example:
    >>> render_plain(0b101010110101, nomenclature.chromatic())
    ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    >>> render_plain(0b10000100010000001, nomenclature.chromatic())
    ['C', 'G', 'B', 'E']
    """

    if chromatic_scale is None:
        chromatic_scale = nomenclature.get_chromatic_octave(constants.BINOMIALS)
    chromatic_scale_ = list(chromatic_scale)
    if interval_structure.bit_length() > len(chromatic_scale):
        chromatic_scale_ *= 8

    rendering: list[str] = []
    for interval in range(0, interval_structure.bit_length()):
        binary_column: int = 1 << interval
        if (interval_structure & binary_column) == binary_column:
            rendering.append(chromatic_scale_[interval])

    return tuple(rendering)


def render_scientific(
    interval_structure: int,
    scientific_range: Optional[Sequence[str]] = None
    ) -> tuple[str, ...]:
    """
    eturn a human-readable rednering of the given interval structure in the 
    given accidental style, in scientific notation.

    :param interval_structure: An integer representing an interval structure
        of any length and bit-count.
    :param scientific_range: An array of scientific note names to use as the 
        basis of the rendering. Must be at least as long as the interval 
        structure, defaults to 12-TET.
    :return: A tuple of note names in scientific notation representing the given
        interval structure.
    """
    scientific_range = scientific_range or nomenclature.scientific_range()
    rendering: list[str] = []
    for interval in range(0, interval_structure.bit_length()):
        binary_column: int = 1 << interval
        if (interval_structure & binary_column) == binary_column:
            rendering.append(scientific_range[interval])
    return tuple(rendering)

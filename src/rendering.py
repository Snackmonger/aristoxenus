
from data import constants
from src import nomenclature, utils


def render_plain(interval_structure: int, 
           chromatic_scale: list[str] | None = None
           ) -> list[str]:
    '''
    Return a human-readable list of strings representing the interval structure
    in the given accidental style.

    Parameters
    ----------
    interval_structure : int
        An integer representing the interval collection to be rendered.
    chromatic_scale : list[str], optional
        The 12-note chromatic scale you want to use to render the structure.
        Pass either the sharps, flats, binomials, or a custom group of mixed
        accidentals. Default is binomials.

    Returns
    -------
    list[str]
        A rendering of the given interval structure in the given chromatic
        accidental style.

    Notes
    -----
    If the number of notes in the interval structure exceeds those of the 
    chromatic scale, we extend the scale to accommodate the extra notes.
    The resulting structure will make no distinction between octaves. Use 
    this function when you want to display a basic abstract structure quickly.

    Examples
    --------
    >>> render_plain(0b101010110101, nomenclature.chromatic())
    ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    >>> render_plain(0b10000100010000001, nomenclature.chromatic())
    ['C', 'G', 'B', 'E']
    >>> render_plain(0b10000000010000001, utils.shift_list(nomenclature.chromatic(), 'D#|Eb'))
    ['D#|Eb', 'G#|Ab', ]
    
    '''
    if chromatic_scale is None:
        chromatic_scale = nomenclature.chromatic(constants.BINOMIALS)
    if interval_structure.bit_length() > len(chromatic_scale):
        chromatic_scale *= 8

    rendering: list[str] = []
    for interval in range(0, interval_structure.bit_length()):
        binary_column: int = 1 << interval
        if (interval_structure & binary_column) == binary_column:
            rendering.append(chromatic_scale[interval])

    return rendering




def render_scientific(interval_structure: int,
           accidental_notes: list[str] | tuple[str, ...],
           starting_note: str
           ) -> list[str]:
    '''
    Return a human-readable rednering of the given interval structure in the 
    given accidental style, in scientific notation.


    Parameters
    ----------
    interval_structure : int
        An integer representing the interval collection to be rendered.
    accidental_notes : list[str]
        A list of 5 note names, either the sharps, the flats, or the 
        binomials.
    starting_note : str
        A note name in scientific notation that will serve as the lowest note 
        of the rendered structure.

    Returns
    -------
    list[str]
        A list of note names in scientific notation representing the given
        interval structure.

    Raises
    ------
    ValueError
        -If the accidentals are not sharps, flats, or binomials.
        -If the starting note is not a legal scientific note name for the
        requested accidental type.

    Examples
    --------
    >>>

    '''
    scientific_range: list[str] = nomenclature.scientific_range(accidental_notes)
    scientific_range = utils.shift_list(scientific_range, starting_note)

    rendering: list[str] = []
    for interval in range(0, interval_structure.bit_length()):
        binary_column: int = 1 << interval
        if (interval_structure & binary_column) == binary_column:
            rendering.append(scientific_range[interval])
    return rendering


"""Functions that represent the end-points of an API."""

from data import (
    annotations,
    chord_symbols,
    constants, 
    errors,
    keywords,
    intervallic_canon
)
from src import (
    nomenclature,
    rendering,
    bitwise,
    utils,
    permutation,
    parsing
)

# from src.nomenclature import (
#     decode_enharmonic,
#     encode_enharmonic,
#     force_heptatonic,
#     best_heptatonic,
#     name_heptatonic_intervals,
#     get_interval_map
# )

# __all__ = [
#     "chromatic",
#     "render_heptatonic_form",
#     "heptatonic_chord_scale",
#     "decode_enharmonic",
#     "encode_enharmonic",
#     "force_heptatonic",
#     "best_heptatonic",
#     "name_heptatonic_intervals",
#     "get_interval_map",
#     "parse_chord_symbol"
# ]





def chromatic(keynote: str = "C", binomial: bool = False) -> tuple[str, ...]:
    """Return a chromatic scale starting at the given keynote. 

    Parameters
    ----------
        keynote:    The note name that serves as the tonic of the scale.
        binomial:   Flag that overrides the default accidental type.

    Notes
    -----
    By default, the function will create a chromatic scale with the same
    type of accidentals as the keynote. If the keynote is a natural, then
    the accidentals will be those of the natural major scale in that key.
    If the keynote is an irregular spelling of a natural (e.g. B#), then
    the scale will use the enharmonically correct note names (at least one
    of which will have a double accidental), plus five names to fill the gaps.
    """
    if binomial or keynote not in constants.LEGAL_ROOT_NAMES:
        keynote = nomenclature.decode_enharmonic(keynote)
        return utils.shift_array(nomenclature.chromatic(), keynote)

    if keynote in constants.ACCIDENTAL_HALFSTEPS:
        dummy = nomenclature.best_heptatonic(keynote)
        return nomenclature.twelve_tone_scale_names(dummy)

    accidental_type = nomenclature.get_accidental_keyword(keynote)

    notes: tuple[str, ...]
    match accidental_type:
        case keywords.SHARP:
            notes = nomenclature.chromatic(constants.SHARPS)
        case keywords.FLAT:
            notes = nomenclature.chromatic(constants.FLATS)
        case _:
            dummy = nomenclature.best_heptatonic(keynote)
            return nomenclature.twelve_tone_scale_names(dummy)

    if keynote not in notes:
        raise errors.NoteNameError(keynote)

    return utils.shift_array(notes, keynote)


def render_heptatonic_form(keynote: str, scale_name: annotations.HeptatonicScales = keywords.DIATONIC, modal_name: annotations.ModalNames = keywords.IONIAN) -> annotations.APIScaleFormResponse:
    '''
    Return a collection of data about a given scaleform configuration.

    Parameters
    ----------
    scale_name : str
        A recognized scale name.
    modal_name : str
        A recognized modal name.
    keynote : str
        A recognized note name (any natural, sharp, flat, or binomial with no 
        more than 1 accidental)

    Returns
    -------
    dict[str, str|tuple[str, ...]|list[str]]
        A dictionary containing information about the rendering under the 
        following keys:
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
    '''
    scale_base: int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale_name]
    modal_rotations: int = keywords.MODAL_SERIES.index(modal_name)
    scale_base = bitwise.get_modal_form(scale_base, modal_rotations)
    binomial_base: tuple[str, ...] = chromatic(
        nomenclature.decode_enharmonic(keynote), binomial=True)

    # Chromatic rendering will use binomials (the 'absolute' spelling)
    binomial_rendering: tuple[str, ...] = rendering.render_plain(
        scale_base, binomial_base)

    # Optimal rendering is that which has the fewest accidentals, while
    # still maintaining the alphabetic order (the 'correct' spelling).
    best_rendering: tuple[str, ...] = nomenclature.best_heptatonic(
        keynote, scale_base)

    # Alphabetic rendering forces the nomenclature to follow the given
    # keynote, even if it makes an awkward spelling. If the keynote was
    # a binomial, use the optimal rendering instead.
    forced_rendering: tuple[str, ...] = best_rendering
    if not keynote in constants.BINOMIALS:
        forced_rendering = nomenclature.force_heptatonic(
            keynote, scale_base)

    # Interval scale is a list of intervals in the scale, spelled correctly so
    # that there is exactly one each of 12334567, plus any accidentals.
    interval_scale: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        scale_base)

    # Interval map is a dictionary of the chromatic binomials to the
    # 7 correct interval names, plus 5 supplementary names, which can be used
    # to supply chromatic accidentals to the scale intervals. The interval map
    # for just the scale notes could be dict(zip(optimal_rendering, interval_scale))
    interval_map: dict[str, str] = nomenclature.get_interval_map(
        keynote, scale_base, True)

    return annotations.APIScaleFormResponse(scale_name=scale_name,
                                  modal_name=modal_name,
                                  interval_structure=scale_base,
                                  interval_scale=interval_scale,
                                  interval_map=interval_map,
                                  keynote=keynote,
                                  binomial_rendering=binomial_rendering,
                                  forced_rendering=forced_rendering,
                                  best_keynote=best_rendering[0],
                                  best_rendering=best_rendering)


def heptatonic_chord_scale(scale: annotations.HeptatonicScales, mode: annotations.ModalNames, keynote: str, number_of_notes: int | str = 3, base_step: int | str = 2, roman_lower: bool = False) -> annotations.APIChordScaleResponse:
    '''
    Create chords from the nomenclaturally-correct form of the given scale 
    and return a list of dictionaries representing the chords built from each 
    degree of that scale, spelled according to the nomenclature of the parent 
    scale.

    Parameters
        scale: A name representing a canonical scale base.
        mode: A name representing a degree of scalar rotation.
        keynote: The tonal centre of the scale.
        number_of_notes: The number of notes in each chord. Default=3.
        base_step: The number of scale steps between chord tones. Default=2. 
        roman_lower: Use lowercase Roman numerals in minors. Default=False.

    Return
        dict {
            scale: str
            mode: str
            keynote: str
            notes: int
            step: int
            chord_scale: list[
                dict {
                    numeric_degree: str
                    root: str
                    notes: list[str]
                    interval_structure: int
                    interval_names: list[str]
                    chord_symbol: str
                    roman_degree: str
                    }
                ]
            }

    Examples
        >>> x = heptatonic_chord_scale("diatonic", "ionian", "C", 4)
        >>> x[0]
        {'numeric_degree': '1', 'root': 'C', 'notes': ['C', 'E', 'G', 'B'], 'interval_structure': 2193, 'interval_names': ['1', '3', '5', '7']}

    '''
    if isinstance(number_of_notes, str):
        number_of_notes = utils.decode_numeration(number_of_notes)
    if isinstance(base_step, str):
        base_step = utils.decode_numeration(base_step)

    base: int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale]
    rotations: int = keywords.MODAL_SERIES.index(mode)
    interval_structure: int = bitwise.get_modal_form(base, rotations)
    note_names: tuple[str, ...] = nomenclature.force_heptatonic(keynote,
                                                                interval_structure)
    parent_interval_names: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        interval_structure)
    chords: dict[str, int] = permutation.chordify(interval_structure,
                                                  number_of_notes,
                                                  base_step)
    collection: list[annotations.HeptatonicChord] = []

    for i, note in enumerate(note_names):
        new_notes: list[str] = list(utils.shift_array(note_names, note))
        interval_names: list[str] = list(nomenclature.name_heptatonic_intervals(
            new_notes))
        upper_octave: list[str] = []
        for interval_name in interval_names:
            for char in interval_name:
                if char.isdigit():
                    upper_octave.append(
                        interval_name.replace(char, str(int(char)+7)))
        interval_names += upper_octave
        new_notes += new_notes

        if number_of_notes > len(new_notes):
            number_of_notes = len(new_notes)

        chord = new_notes[::base_step][:number_of_notes]
        binomial_notes = [nomenclature.decode_enharmonic(x) for x in chord]
        chord_intervals = interval_names[::base_step][:number_of_notes]
        chord_base = parsing.parse_interval_names_as_chord_symbol(
            chord_intervals)
        chord_symbol = note + chord_base
        roman_degree = utils.romanize_intervals(parent_interval_names[i])[0]
        if chord_symbols.CHORD_FLAT_3 in chord_intervals and roman_lower:
            roman_degree = roman_degree.lower()
        roman_chord = roman_degree + chord_base

        # TODO: The chord should also have a 'neutral' name, so that
        # weird contextual spellings like G7bb3b5 also have mis-spelled
        # alternatives like G7b5sus2
        x = annotations.HeptatonicChord(
            numeric_degree=parent_interval_names[i],
            roman_degree=roman_degree,
            root=note,
            notes=chord,
            binomial_notes=binomial_notes,
            interval_structure=list(
                chords.values())[i],
            interval_names=chord_intervals,
            chord_symbol=chord_symbol,
            roman_chord=roman_chord
        )
        collection.append(x)

    return annotations.APIChordScaleResponse(scale=scale,
                                   mode=mode,
                                   keynote=keynote,
                                   notes=number_of_notes,
                                   step=base_step,
                                   chord_scale=collection)


def parse_chord_symbol(symbol: str) -> annotations.APIChordSymbolResponse:
    """
    For the given chord symbol, return a list of note names and an integer
    representing the chord's interval structure.

    Args:
        symbol: A chord symbol, e.g. "C", "Dmin7b5", "Faug7b9", "Gbdim11"
    Returns:
        dict {
            note_names: The notes of the chord.
            interval_structure: An integer representing the structure.
        }
    Raises:
        ChordNameError: If the symbol's root is not a legal note name.
    """
    root = parsing.remove_chord_prefix(symbol)[0]
    root = nomenclature.decode_enharmonic(root)
    result = parsing.parse_chord_symbol(symbol)
    binomial_chromatic = chromatic(root, binomial=True)
    note_names = rendering.render_plain(result, binomial_chromatic)

    return {keywords.CHORD_SYMBOL: symbol,
            keywords.INTERVAL_STRUCTURE: result,
            keywords.NOTE_NAMES: note_names}


def render_plain(interval_structure: int, keynote: str) -> tuple[str, ...]:
    """
    Take an integer representing an interval structure and return a set of 
    note names in plain notation (i.e. without scientific numerals) beginning
    at the given keynote. 

    Args:
        interval_structure: An integer representing an interval structure.
        keynote: A note name to serve as the basis of the rendered form.

    Returns:
        A sequence of note names representing the interval structure.
    """
    accidentals: tuple[str, ...] = nomenclature.get_accidentals(keynote)
    binomial: bool = accidentals == constants.BINOMIALS
    ch_: tuple[str, ...] = chromatic(keynote, binomial)
    return rendering.render_plain(interval_structure, ch_)


class Chord:
    def __init__(self):
        self.interval_structure: int

    def invert(self) -> "Chord":
        ...



FORMATTING_TYPES = [keywords.PLAIN,
                    keywords.BINOMIAL,
                    keywords.SCIENTIFIC,
                    keywords.SCIENTIFIC+"_"+keywords.BINOMIAL]

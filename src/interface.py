"""Functions that represent the end-points of an API."""


from typing import Optional

from src import (nomenclature,
                 rendering,
                 bitwise,
                 utils,
                 permutation)

from data import (annotations,
                  constants,
                  keywords,
                  intervallic_canon)


def chromatic(keynote: str = "C", accidental_type: Optional[str] = None) -> list[str]:
    """Return a chromatic scale in the given accidental style 
    (default=binomial) and starting at the given keynote (default=C).
    """
    if not accidental_type:
        accidental_type = nomenclature.get_accidental_keyword(keynote)

    # Catch fuzzy keyword
    keys = [keywords.BINOMIAL, keywords.FLAT, keywords.SHARP]
    for k in keys:
        if accidental_type == k + "s":
            accidental_type = accidental_type[:-1]

    notes: list[str]
    match accidental_type:
        case keywords.BINOMIAL:
            notes = nomenclature.chromatic(constants.BINOMIALS)
        case keywords.SHARP:
            notes = nomenclature.chromatic(constants.SHARPS)
        case keywords.FLAT:
            notes = nomenclature.chromatic(constants.FLATS)
        case _:
            notes = nomenclature.chromatic(constants.BINOMIALS)

    if keynote not in notes:
        raise ValueError(f"Unknown keynote: {keynote}")

    return utils.shift_list(notes, keynote)


def render_heptatonic_form(
        scale_name: annotations.HeptatonicScales,
        modal_name: annotations.ModalNames,
        keynote: str
) -> annotations.APIScaleFormResponse:
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
    modal_rotations: int = keywords.MODAL_NAME_SERIES.index(modal_name)
    scale_base = bitwise.get_modal_form(scale_base, modal_rotations)
    binomial_base: list[str] = chromatic(
        nomenclature.decode_enharmonic(keynote))

    # Chromatic rendering will use binomials (the 'absolute' spelling)
    chromatic_rendering: list[str] = rendering.render_plain(scale_base, binomial_base)

    # Optimal rendering is that which has the fewest accidentals, while
    # still maintaining the alphabetic order (the 'correct' spelling).
    optimal_rendering: list[str] = nomenclature.best_heptatonic(keynote, scale_base)

    # Alphabetic rendering forces the nomenclature to follow the given
    # keynote, even if it makes an awkward spelling. If the keynote was
    # a binomial, use the optimal rendering instead.
    alphabetic_rendering: list[str] = optimal_rendering
    if not keynote in constants.BINOMIALS:
        alphabetic_rendering = nomenclature.force_heptatonic(keynote, scale_base)

    # Interval scale is a list of intervals in the scale, spelled correctly so
    # that there is exactly one each of 12334567, plus any accidentals.
    interval_scale: list[str] = nomenclature.name_heptatonic_intervals(scale_base)
    
    # Interval map is a dictionary of the chromatic binomials to the
    # 7 correct interval names, plus 5 supplementary names, which can be used
    # to supply chromatic accidentals to the scale intervals. The interval map
    # for just the scale notes could be dict(zip(optimal_rendering, interval_scale))
    interval_map: dict[str, str] = nomenclature.get_interval_map(keynote, scale_base, True)

    # NOTE: if the above flag is False, then the scale notes will have their 'real' names.

    return annotations.APIScaleFormResponse(scale_name=scale_name,
                                            modal_name=modal_name,
                                            interval_structure=scale_base,
                                            interval_scale=interval_scale,
                                            interval_map=interval_map,
                                            keynote=keynote,
                                            chromatic_rendering=chromatic_rendering,
                                            alphabetic_rendering=alphabetic_rendering,
                                            optimal_keynote=optimal_rendering[0],
                                            optimal_rendering=optimal_rendering)


# TODO: this function needs a more sophisticated wrapper that can
# decide how to make roman numeral chord symbols.
def heptatonic_chord_scale(scale: annotations.HeptatonicScales,
                           mode: annotations.ModalNames,
                           keynote: str,
                           number_of_notes: int | str = 3,
                           base_step: int | str = 2
                           ) -> list[annotations.HeptatonicChord]:
    '''
    Create chords from the nomenclaturally-correct form of the given scale 
    and return a list of dictionaries representing the chords built from each 
    degree of that scale, spelled according to the nomenclature of the parent 
    scale.

    Parameters
    ----------
    scale : annotations.HeptatonicScales
        A name representing a canonical scale base.
    mode : annotations.ModalNames
        A name representing a degree of scalar rotation.
    keynote : str
        A name representing the tonal centre of the scale.
    number_of_notes : int | str, optional
        The number of notes in the chord, by default 3. This can be expressed
        with an integer, or a keyword representing a chord type (e.g. "triad")
    base_step : int | str, optional
        The number of scale steps between chord tones, by default 2. This can
        be expressed with an integer or a keyword representing a step type 
        (e.g. "tertial"). Note that the number of steps starts at 0, so that
        2 == tertial.

    Return
    ------
    list of dict of
        degree: str               : The root interval in the parent scale.
        root: str                 : The root note of the chord.
        notes: list[str]          : The spelling of the notes of the chord.
        interval_structure: int   : A number representing the chord structure.
        interval_names: list[str] : The spelling of the intervals of the chord.

    Examples
    --------
    >>> x = heptatonic_chord_scale("diatonic", "ionian", "C", 4)
    >>> x[0]
    {'numeric_degree': '1', 'root': 'C', 'notes': ['C', 'E', 'G', 'B'], 'interval_structure': 2193, 'interval_names': ['1', '3', '5', '7']}

    '''
    if isinstance(number_of_notes, str):
        number_of_notes = nomenclature.decode_numeric_keyword(number_of_notes)
    if isinstance(base_step, str):
        base_step = nomenclature.decode_numeric_keyword(base_step)

    base: int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale]
    rotations: int = keywords.MODAL_NAME_SERIES.index(mode)
    interval_structure: int = bitwise.get_modal_form(base, rotations)
    note_names: list[str] = nomenclature.best_heptatonic(keynote,
                                            interval_structure)
    parent_interval_names: list[str] = nomenclature.name_heptatonic_intervals(
        interval_structure)
    chords: dict[str, int] = permutation.chordify(interval_structure,
                                                  number_of_notes,
                                                  base_step)
    collection: list[annotations.HeptatonicChord] = []

    for i, note in enumerate(note_names):
        new_notes: list[str] = utils.shift_list(note_names, note)
        interval_names: list[str] = nomenclature.name_heptatonic_intervals(
            new_notes)
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
        chord_intervals = interval_names[::base_step][:number_of_notes]
        x = annotations.HeptatonicChord(numeric_degree=parent_interval_names[i],
                                        root=note,
                                        notes=chord,
                                        interval_structure=list(
                                            chords.values())[i],
                                        interval_names=chord_intervals)
        collection.append(x)
    return collection

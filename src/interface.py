"""Functions that represent the end-points of an API."""

from src import (nomenclature,
                 rendering,
                 bitwise,
                 utils,
                 permutation,
                 parsing)

from data import (annotations as A,
                  chord_symbols as CS,
                  constants as C, errors,
                  keywords as K,
                  intervallic_canon as IC)


def chromatic(keynote: str = "C", binomial: bool = False) -> tuple[str, ...]:
    """Return a chromatic scale in the given accidental style 
    (default=binomial) and starting at the given keynote (default=C).
    """
    if binomial or keynote not in C.LEGAL_ROOT_NAMES:
        keynote = nomenclature.decode_enharmonic(keynote)
        return utils.shift_array(nomenclature.chromatic(), keynote)
    
    if keynote in C.ACCIDENTAL_HALFSTEPS:
        dummy = nomenclature.best_heptatonic(keynote)
        return nomenclature.twelve_tone_scale_names(dummy)

    accidental_type = nomenclature.get_accidental_keyword(keynote)

    notes: tuple[str, ...]
    match accidental_type:
        case K.SHARP:
            notes = nomenclature.chromatic(C.SHARPS)
        case K.FLAT:
            notes = nomenclature.chromatic(C.FLATS)
        case _:
            dummy = nomenclature.best_heptatonic(keynote)
            return nomenclature.twelve_tone_scale_names(dummy)

    if keynote not in notes:
        raise errors.NoteNameError(keynote)

    return utils.shift_array(notes, keynote)


def render_heptatonic_form(scale_name: A.HeptatonicScales, modal_name: A.ModalNames, keynote: str) -> A.APIScaleFormResponse:
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
    scale_base: int = IC.HEPTATONIC_SYSTEM_BY_NAME[scale_name]
    modal_rotations: int = K.MODAL_NAME_SERIES.index(modal_name)
    scale_base = bitwise.get_modal_form(scale_base, modal_rotations)
    binomial_base: tuple[str, ...] = chromatic(
        nomenclature.decode_enharmonic(keynote), binomial=True)

    # Chromatic rendering will use binomials (the 'absolute' spelling)
    chromatic_rendering: tuple[str, ...]= rendering.render_plain(
        scale_base, binomial_base)

    # Optimal rendering is that which has the fewest accidentals, while
    # still maintaining the alphabetic order (the 'correct' spelling).
    optimal_rendering: tuple[str, ...] = nomenclature.best_heptatonic(
        keynote, scale_base)

    # Alphabetic rendering forces the nomenclature to follow the given
    # keynote, even if it makes an awkward spelling. If the keynote was
    # a binomial, use the optimal rendering instead.
    alphabetic_rendering: tuple[str, ...] = optimal_rendering
    if not keynote in C.BINOMIALS:
        alphabetic_rendering = nomenclature.force_heptatonic(
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

    # NOTE: if the above flag is False, then the scale notes will have their 'real' names.

    return A.APIScaleFormResponse(scale_name=scale_name,
                                  modal_name=modal_name,
                                  interval_structure=scale_base,
                                  interval_scale=interval_scale,
                                  interval_map=interval_map,
                                  keynote=keynote,
                                  chromatic_rendering=chromatic_rendering,
                                  alphabetic_rendering=alphabetic_rendering,
                                  optimal_keynote=optimal_rendering[0],
                                  optimal_rendering=optimal_rendering)


def heptatonic_chord_scale(scale: A.HeptatonicScales, mode: A.ModalNames, keynote: str, number_of_notes: int | str = 3, base_step: int | str = 2, roman_lower: bool = False) -> A.APIChordScaleResponse:
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
    roman_lower : bool, default=False
        Flag that decides whether to use lower-case Roman numerals for 
        minor chords (e.g. iimin7 vs IImin7)

    Return
    ------
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
    --------
    >>> x = heptatonic_chord_scale("diatonic", "ionian", "C", 4)
    >>> x[0]
    {'numeric_degree': '1', 'root': 'C', 'notes': ['C', 'E', 'G', 'B'], 'interval_structure': 2193, 'interval_names': ['1', '3', '5', '7']}

    '''
    if isinstance(number_of_notes, str):
        number_of_notes = nomenclature.decode_numeric_keyword(number_of_notes)
    if isinstance(base_step, str):
        base_step = nomenclature.decode_numeric_keyword(base_step)

    base: int = IC.HEPTATONIC_SYSTEM_BY_NAME[scale]
    rotations: int = K.MODAL_NAME_SERIES.index(mode)
    interval_structure: int = bitwise.get_modal_form(base, rotations)
    note_names: tuple[str, ...] = nomenclature.force_heptatonic(keynote,
                                                         interval_structure)
    parent_interval_names: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        interval_structure)
    chords: dict[str, int] = permutation.chordify(interval_structure,
                                                  number_of_notes,
                                                  base_step)
    collection: list[A.HeptatonicChord] = []

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
        chord_intervals = interval_names[::base_step][:number_of_notes]
        chord_base = parsing.parse_interval_names_as_chord_symbol(
            chord_intervals)
        chord_symbol = note + chord_base
        roman_degree = utils.romanize_intervals(parent_interval_names[i])[0]
        if CS.CHORD_FLAT_3 in chord_intervals and roman_lower:
            roman_degree = roman_degree.lower()
        roman_degree += chord_base
        x = A.HeptatonicChord(numeric_degree=parent_interval_names[i],
                              root=note,
                              notes=chord,
                              interval_structure=list(
            chords.values())[i],
            interval_names=chord_intervals,
            chord_symbol=chord_symbol,
            roman_degree=roman_degree)
        collection.append(x)

    return A.APIChordScaleResponse(scale=scale,
                                   mode=mode,
                                   keynote=keynote,
                                   notes=number_of_notes,
                                   step=base_step,
                                   chord_scale=collection)


def parse_chord_symbol(symbol: str) -> str:
    root = parsing.remove_chord_prefix(symbol)[0]
    root = nomenclature.decode_enharmonic(root)
    result = parsing.parse_chord_symbol(symbol)
    binomial_chromatic = chromatic(root, binomial=True)
    note_names = rendering.render_plain(result, binomial_chromatic)
    return ", ".join(note_names)

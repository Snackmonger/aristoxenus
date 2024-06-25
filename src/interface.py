"""Functions that represent the end-points of an API."""

from data import (
    annotations,
    chord_symbols,
    constants,
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


def infer_chromatic(keynote: str = "C", binomial: bool = False) -> tuple[str, ...]:
    """
    Return a chromatic scale starting at the given keynote, with the notes
    named so as to respect the key signature of that tonic.

    :param keynote: The note name that serves as the tonic of the scale, 
        defaults to "C"
    :param binomial: Flag that overrides the default accidental type and 
        returns chromatic binomials instead, defaults to False
    :return: A tuple of note names that respect the given style.

    Note names will respect the given accidental, even if it's not the ideal
    spelling.
    :Example:
    >>> interface.infer_chromatic("D#")
    ('D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D')
    >>> interface.infer_chromatic("Eb")
    ('Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D')

    Any single accidental will be accepted as the basis of a chromatic scale,
    and the resulting note names will ensure that 
    :Example:
    >>> interface.infer_chromatic("Cb")
    ('Cb', 'C', 'Db', 'D', 'Eb', 'Fb', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb')
    >>> interface.infer_chromatic("B#")
    ('B#', 'C#', 'C##', 'D#', 'D##', 'E#', 'F#', 'F##', 'G#', 'G##', 'A#', 'A##')

    But multiple accidentals will be reducted to their simplest form.
    :Example:
    >>> interface.infer_chromatic("Cbb")
    ('Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A')
    >>> interface.infer_chromatic("D##")
    ('E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#')

    Any unknown note names will return C with sharps.
    :Example:
    >>> interface.infer_chromatic("Mb")
    ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

    Binomials will be resolved automatically to their optimal form.
    :Example:
    >>> interface.infer_chromatic("G#|Ab")
    ('Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G')

    But the ``binomial`` flag will ensure that binomials really are returned.
    :Example:
    >>> interface.infer_chromatic("G#|Ab", binomial=True)
    ('G#|Ab', 'A', 'A#|Bb', 'B', 'C', 'C#|Db', 'D', 'D#|Eb', 'E', 'F', 'F#|Gb', 'G')

    And the ``binomial`` flag overrides any other recognized name.
    :Example:
    >>> interface.infer_chromatic("Cbb", binomial=True)
    ('A#|Bb', 'B', 'C', 'C#|Db', 'D', 'D#|Eb', 'E', 'F', 'F#|Gb', 'G', 'G#|Ab', 'A')
    """
    if keynote not in list(nomenclature.get_enharmonic_decoder()) + list(constants.BINOMIALS):
        keynote = "C"
    if binomial:
        keynote = nomenclature.decode_enharmonic(keynote)
        return utils.shift_array(nomenclature.get_chromatic_octave(), keynote)
    if len(keynote) > 2:
        keynote = nomenclature.decode_enharmonic(keynote)
        dummy = nomenclature.best_heptatonic(keynote)
        return nomenclature.twelve_tone_scale_names(dummy)
    if keynote in constants.BINOMIALS or keynote in constants.NATURALS:
        dummy = nomenclature.best_heptatonic(keynote)
        return nomenclature.twelve_tone_scale_names(dummy)
    if keynote in constants.ACCIDENTAL_HALFSTEPS:
        dummy = nomenclature.force_heptatonic(keynote)
        return nomenclature.twelve_tone_scale_names(dummy)

    accidental_type = nomenclature.get_accidental_keyword(keynote)
    notes: tuple[str, ...] = ()
    if accidental_type == keywords.SHARP:
        notes = nomenclature.get_chromatic_octave(constants.SHARPS)
    elif accidental_type == keywords.FLAT:
        notes = nomenclature.get_chromatic_octave(constants.FLATS)
    return utils.shift_array(notes, keynote)


def render_heptatonic_form(
        keynote: str,
        scale_name: annotations.HeptatonicScales = keywords.DIATONIC,
        modal_name: annotations.ModalNames = keywords.IONIAN
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
    dict{
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
        }
    '''
    scale_base: int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale_name]
    modal_rotations: int = keywords.MODAL_SERIES.index(modal_name)
    scale_base = bitwise.get_rotation(scale_base, modal_rotations)
    binomial_base: tuple[str, ...] = infer_chromatic(
        nomenclature.decode_enharmonic(keynote), binomial=True)

    # Chromatic rendering will use binomials (the 'absolute' 12-tone spelling).
    binomial_rendering: tuple[str, ...] = rendering.render_plain(
        scale_base, binomial_base)

    # Best rendering is that which has the fewest accidentals, while
    # still maintaining the alphabetic order (the 'correct' spelling).
    best_rendering: tuple[str, ...] = nomenclature.best_heptatonic(
        keynote, scale_base)

    # Forced rendering ensures that the nomenclature follows the given
    # keynote, even if it makes an awkward spelling.
    forced_rendering: tuple[str, ...] = best_rendering
    if not keynote in constants.BINOMIALS:
        forced_rendering = nomenclature.force_heptatonic(
            keynote, scale_base)

    # Interval scale is a list of intervals in the scale, spelled correctly so
    # that there is exactly one each of 12334567, plus any accidentals.
    # E.g. 1 b2 #3 #4 5 b6 b7
    interval_scale: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        scale_base)

    # Interval map is a dictionary of the chromatic binomials to the
    # 7 correct interval names, plus 5 supplementary names to fill the gaps.
    # This mapping helps ensure that weird scales have a corresponding
    # chromatic that respects their interval names (e.g. that #5 is not b6).
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


def heptatonic_chord_scale(
        scale: annotations.HeptatonicScales,
        mode: annotations.ModalNames,
        keynote: str,
        number_of_notes: int | str = 3,
        base_step: int | str = 2,
        roman_lower: bool = False
) -> annotations.APIChordScaleResponse:
    '''
    Create chords from the nomenclaturally-correct form of the given scale 
    and return a list of dictionaries representing the chords built from each 
    degree of that scale, spelled according to the nomenclature of the parent 
    scale.

    Parameters
    ----------
    scale: str
        A name representing a canonical scale base.
    mode: str
        A name representing a degree of scalar rotation.
    keynote: str
        The tonal centre of the scale.
    number_of_notes: int
        The number of notes in each chord. Default=3.
    base_step: int
        The number of scale steps between chord tones. Default=2. 
    roman_lower: bool
        Use lowercase Roman numerals in minors. Default=False.

    Returns
    -------
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
        number_of_notes = utils.decode_numeration(number_of_notes)
    if isinstance(base_step, str):
        base_step = utils.decode_numeration(base_step)

    base: int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale]
    rotations: int = keywords.MODAL_SERIES.index(mode)
    interval_structure: int = bitwise.get_rotation(base, rotations)
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
            note_names=tuple(chord),
            binomial_notes=tuple(binomial_notes),
            interval_structure=list(
                chords.values())[i],
            interval_names=tuple(chord_intervals),
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

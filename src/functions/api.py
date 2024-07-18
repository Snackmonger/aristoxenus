"""
This module serves as a facade interface to simplify using the the lower-level
functions defined in the other modules in the ``src.functions`` package. 
"""

from src.data import (
    annotations,
    chord_symbols,
    constants,
    keywords,
    intervallic_canon
)
from src.functions import (
    nomenclature,
    rendering,
    bitwise,
    utils,
    permutation,
    parsing
)

__all__ = ["heptatonic_scale_form",
           "heptatonic_chord_scale"]

def heptatonic_scale_form(
        keynote: str = "C",
        scale_name: annotations.HeptatonicScales = keywords.DIATONIC,
        modal_name: annotations.ModalNames = keywords.IONIAN
) -> annotations.APIScaleFormResponse:
    '''
    Return a collection of data about a given scaleform configuration.

    Parameters
    ----------
    keynote : str
        A recognized note name (any natural, sharp, flat, or binomial with no 
        more than 1 accidental).
    scale_name : annotations.HeptatonicScales, optional
        A recognized scale name, by default keywords.DIATONIC.
    modal_name : annotations.ModalNames, optional
        A recognized modal name, by default keywords.IONIAN.

    Returns
    -------
    annotations.APIScaleFormResponse
        A dictionary with the following keys:

        scale_name: str
            The canonical name of the base scale form.
        modal_name: str
            The canonical name of the degree of modal rotation from the base.
        interval_structure: int
            The unique integer expression of this scale form.
        interval_scale: tuple[str, ...]
            An array of interval names using Indian numerals.
        interval_map: dict[str, str]
            A chromatic scale that respects the scaleform's unique interval 
            names.
        keynote: str
            The real keynote of the scaleform.
        binomial_rendering: tuple[str, ...]
            The binomial names of the scaleform's notes.
        forced_rendering: tuple[str, ...]
            The names for the scale notes, using the real keynote.
        best_keynote: str
            The best name for the given keynote.
        best_rendering: tuple[str, ...]
            The best names for the scale notes, using the best keynote.

    Examples
    --------
    >>> scale = interface.heptatonic_form("Eb", "diatonic", "locrian")
    >>> scale['scale_name'] 
    'diatonic'
    >>> scale['modal_name']
    'locrian' 
    >>> scale['interval_structure']
    1387 
    >>> scale['interval_scale']
    ('1', 'b2', 'b3', '4', 'b5', 'b6', 'b7') 
    >>> scale['interval_map']
    {'D#|Eb': '1', 'E': 'b2', 'F': '2', 'F#|Gb': 'b3', 'G': '3', 'G#|Ab': '4', 'A': 'b5', 'A#|Bb': '5', 'B': 'b6', 'C': '6', 'C#|Db': 'b7', 'D': '7'}
    >>> scale['keynote']
    'Eb'
    >>> scale['binomial_rendering']
    ('D#|Eb', 'E', 'F#|Gb', 'G#|Ab', 'A', 'B', 'C#|Db')
    'forced_rendering': ('Eb', 'Fb', 'Gb', 'Ab', 'Bbb', 'Cb', 'Db'), 
    >>> scale['best_keynote'] 
    'D#'
    >>> scale['best_rendering']
    ('D#', 'E', 'F#', 'G#', 'A', 'B', 'C#')
    '''
    scale_base: int = intervallic_canon.HEPTATONIC_ORDER_KEY_TO_VALUE_MAP[scale_name]
    modal_rotations: int = keywords.MODAL_SERIES_KEYS.index(modal_name)
    scale_base = bitwise.get_rotation(scale_base, modal_rotations)
    binomial_base: tuple[str, ...] = utils.shift_array(
        nomenclature.generate_chromatic_octave(),
        nomenclature.decode_enharmonic(keynote)
    )

    # Chromatic rendering will use binomials (the 'absolute' 12-tone spelling).
    binomial_rendering: tuple[str, ...] = rendering.render_plain(
        scale_base, binomial_base
    )
    # Best rendering is that which has the fewest accidentals, while
    # still maintaining the alphabetic order (the 'correct' spelling).
    best_rendering: tuple[str, ...] = nomenclature.best_heptatonic(
        keynote,
        scale_base
    )
    # Forced rendering ensures that the nomenclature follows the given
    # keynote, even if it makes an awkward spelling.
    forced_rendering: tuple[str, ...] = best_rendering
    if not keynote in constants.BINOMIALS:
        forced_rendering = nomenclature.force_heptatonic(
            keynote,
            scale_base
        )
    # Interval scale is a list of intervals in the scale, spelled correctly so
    # that there is exactly one each of 12334567, plus any accidentals.
    # E.g. 1 b2 #3 #4 5 b6 b7
    interval_scale: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        scale_base
    )
    # Interval map is a dictionary of the chromatic binomials to the
    # 7 correct interval names, plus 5 supplementary names to fill the gaps.
    # This mapping helps ensure that weird scales have chromatic interval
    # names that respect their non-chromatic scale interval names.
    interval_map: dict[str, str] = nomenclature.get_interval_map(
        keynote,
        scale_base,
        True
    )
    return annotations.APIScaleFormResponse(
        scale_name=scale_name,
        modal_name=modal_name,
        interval_structure=scale_base,
        interval_scale=interval_scale,
        interval_map=interval_map,
        keynote=keynote,
        binomial_rendering=binomial_rendering,
        forced_rendering=forced_rendering,
        best_keynote=best_rendering[0],
        best_rendering=best_rendering
    )


def heptatonic_chord_scale(
        keynote: str = "C",
        scale_name: annotations.HeptatonicScales = keywords.DIATONIC,
        modal_name: annotations.ModalNames = keywords.IONIAN,
        number_of_notes: int | str = 3,
        base_step: int | str = 2,
        roman_lower: bool = False
) -> annotations.APIChordScaleResponse:
    """
    Create chords from the nomenclaturally-correct form of the given scale 
    and return a list of dictionaries representing the chords built from each 
    degree of that scale, spelled according to the nomenclature of the parent 
    scale.

    Parameters
    ----------
    scale_name: str
        The canonical name of the base scale form.
    modal_name: str
        The canonical name of the degree of modal rotation from the base.
    keynote: str
        The tonal centre of the scale form.
    number_of_notes: int
        The number of notes in each chord. Default=3.
    base_step: int
        The number of scale steps between chord tones. Default=2. 
    roman_lower: bool
        Use lowercase Roman numerals in minors. Default=False.

    Returns
    -------
    annotations.APIChordScaleResponse
        A dictionary with the following keys:
        
        scale_name: str
            The canonical name of the base scale form.
        modal_name: str
            The canonical name of the degree of modal rotation from the base.
        keynote: str
            The tonal centre of the scale form.
        number_of_notes: int
            The number of notes in each chord.
        base_step: int
            The number of scale steps between chord tones.
        chord_scale: list
            A list of dictionaries with information for each chord, containing
            the following keys:

            numeric_degree: str
                The scale degree from which the chord was built, in Indian 
                numeral notation.
            root: str
                The note name of the root of the chord.
            notes: list[str]
                The note names of the chord.
            interval_structure: int
                A unique integer representing the chord form.
            interval_names: list[str]
                The names of the intervals, in Indian numeral notation.
            chord_symbol: str
                The symbol used to designate this chord. For nomenclature, see
                ``notes.style_guide.rst``.
            roman_degree: str
                The scale degree from which the chord was built, in Roman
                numeral notation.

    Examples
    --------
    >>> x = heptatonic_chord_scale("diatonic", "ionian", "C", 4)
    >>> x[0]
    {'numeric_degree': '1', 'root': 'C', 'notes': ['C', 'E', 'G', 'B'], 'interval_structure': 2193, 'interval_names': ['1', '3', '5', '7']}
    """
    if isinstance(number_of_notes, str):
        number_of_notes = utils.decode_numeration(number_of_notes)
    if isinstance(base_step, str):
        base_step = utils.decode_numeration(base_step)

    base: int = intervallic_canon.HEPTATONIC_ORDER_KEY_TO_VALUE_MAP[scale_name]
    rotations: int = keywords.MODAL_SERIES_KEYS.index(modal_name)
    interval_structure: int = bitwise.get_rotation(base, rotations)
    note_names: tuple[str, ...] = nomenclature.force_heptatonic(keynote,
                                                                interval_structure)
    parent_interval_names: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        interval_structure)
    chords: dict[str, int] = permutation.chordify(interval_structure,
                                                  number_of_notes,
                                                  base_step)
    chord_scale: list[annotations.HeptatonicChord] = []

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
        chord_scale.append(x)

    return annotations.APIChordScaleResponse(scale_name=scale_name,
                                             modal_name=modal_name,
                                             keynote=keynote,
                                             number_of_notes=number_of_notes,
                                             base_step=base_step,
                                             chord_scale=chord_scale)

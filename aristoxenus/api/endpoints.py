'''
Aristoxenus Data-Oriented API
-----------------------------

The functions in this module serve as endpoints that assemble musical data 
produced by the various functions in the ``core`` module. All endpoints 
return dictionaries populated by simple data types (str, int, bool, tuple, 
dict, None).

For a more behaviour-oriented interface for accessing the ``core`` 
functions, see the objects available in the ``classes`` module.
'''
# TODO: all functions in this module should have examples in their docstring
# for the benefit of the user. In this case, it's better to be a bit more
# explicit so we really make our point clearly.

from typing import (
    Iterable,
    Optional
)
from aristoxenus.core.annotations import (
    ChordData,
    ChordStyle,
    ChordSymbolData,
    HeptatonicScaleData
)
from aristoxenus.core.chord_symbol import encode_chord_symbol
from aristoxenus.core.chordify import (
    chordify_heptatonic_sus,
    chordify_heptatonic_tertial
)
from aristoxenus.core.constants import (
    CHORD_DIM,
    CHORD_MAJ,
    CHORD_MIN,
    CHORD_SYMBOL,
    CLOSE,
    D2,
    D23,
    D24,
    D3,
    DIATONIC,
    DIM_SYMBOL,
    DROP_2_AND_3_VOICING,
    DROP_2_AND_4_VOICING,
    DROP_2_VOICING,
    DROP_3_VOICING,
    INTERVAL_NAMES,
    IONIAN,
    MAJ_SYMBOL,
    MIN_SYMBOL,
    NOTE_NAME,
    NOTE_NAMES,
    OPEN, 
    SLASH,
    SLASH_SYMBOL,
    SUS2,
    SUS4,
    TERTIAL,
    TONES,
    VOICINGS
)
from aristoxenus.core.convert_names import convert_interval_names_to_roman_names
from aristoxenus.core.heptatonic_spelling import (
    get_best_heptatonic_names,
    get_heptatonic_interval_names,
    get_heptatonic_note_names
)
from aristoxenus.core.errors import (
    ArgumentError,
    StringValidationError
)
from aristoxenus.core.note_name import decode_note_name
from aristoxenus.core.resolve import (
    resolve_chord_symbol,
    resolve_heptatonic_scale
)
from aristoxenus.core.rotate import (
    rotate_chord
)
from aristoxenus.core.validation import validate_interval_name
from aristoxenus.core.voicing import apply_drop_voicing
from aristoxenus.core.interval import (
    calculate_formula,
    sort_interval_names
)

__all__ = [
    'get_chord_from_symbol',
    'get_chord_symbol',
    'get_heptatonic_chord',
    'get_heptatonic_scale'
]





def get_heptatonic_scale(keynote: Optional[str] = None, scale_name: Optional[str] = None, mode_name: Optional[str] = None) -> HeptatonicScaleData:
    '''
    Return a collection of note and interval names for a given scale form.

    Parameters
    ----------
    keynote : str, optional
        _description_, by default None = 'C'
    scale_name : str, optional
        _description_, by default None = 'diatonic'
    modal_name : str, optional
        _description_, by default None = 'ionian'

    Returns
    -------
    HeptatonicScaleResponse
        keynote: str
            The requested keynote.
        scale_name: str
            The requested scale name.
        modal_name: str
            The requested modal name.
        interval_structure: tuple[int, ...]
            An interval structure matching the given scale/mode configuration.
        interval_names: tuple[str, ...]
            A tuple of interval names representing the form (e.g. '3', 'b5').
        roman_names: tuple[str, ...]
            A tuple of Roman interval names (e.g. 'III', 'bV'), presented in
            upper case with appropriate accidentals.
        requested_rendering: tuple[str, ...]
            A tuple of alphabetic note names (e.g. 'A#', 'Gb') representing 
            the scale form, derived from the requested keynote.
        recommended_keynote: str
            The recommended name for the keynote, in case it has two names
            (e.g. A# = Bb).
        recommended_rendering: tuple[str, ...]
            The recommended note names for the form, derived from the 
            recommended keynote.

    Raises
    ------
    ArgumentError
        - If the keynote cannot be recognized (e.g. 'M#').
        - If the scale or mode name cannot be resolved.

    TODO: Examples
    '''
    keynote = keynote or 'C'
    if (n := decode_note_name(keynote)):
        tonic = n
    else:
        raise StringValidationError(keynote, NOTE_NAME)
    scale_name = scale_name or DIATONIC
    interval_structure = resolve_heptatonic_scale(scale_name, mode_name)
    interval_scale = get_heptatonic_interval_names(interval_structure)
    roman_names = convert_interval_names_to_roman_names(interval_scale)
    requested_rendering = get_heptatonic_note_names(tonic, interval_structure)
    recommended_rendering = get_best_heptatonic_names(tonic, interval_structure)
    recommended_keynote = recommended_rendering[0]
    step_formula = calculate_formula(interval_structure)
    return HeptatonicScaleData(
        keynote=keynote,
        scale_name=scale_name,
        mode_name=mode_name,
        interval_structure=interval_structure,
        interval_names=interval_scale,
        roman_names=roman_names,
        requested_rendering=requested_rendering,
        recommended_keynote=recommended_keynote,
        recommended_rendering=recommended_rendering,
        step_formula=step_formula
    )


def get_heptatonic_chord(keynote: str = 'C', scale_name: str = DIATONIC, mode_name: str = IONIAN, chord_degree: int = 1, chord_size: int = 3, chord_inversion: int = 0, chord_voicing: str = CLOSE, structure: str = TERTIAL, chord_style: Optional[ChordStyle] = None) -> ChordData:
    '''
    Create a single chord from a given parent scale's chord scale.

    Parameters
    ----------
    keynote : str, optional
        The keynote of the parent scale, by default 'C'
    scale_name : str, optional
        The name of the parent scale, by default 'diatonic'
    modal_name : str, optional
        The name of the parent mode, by default 'ionian'
    chord_degree : int, optional
        What degree of the parent scale to derive the chord from, by default 1.
        Must be between 1-7.
    chord_size : int, optional
        How many notes should be in the derived chord, by default 3.
        Must be between 3-7.
    chord_inversion : int, optional
        Which inversion the chord be in, by default 0.
        Must be between 1 and chord_size -1.
    chord_voicing : str, optional
        Which voicing the chord should be in, by default 'close'. 
        Choices are 'open', 'close','d2', 'd3', 'd23', 'd24'.
    structure : str, optional
        What structural principal will be used to build the chord.
        Choices are 'tertial', 'sus2', and 'sus4'.
    use_slash : bool, by default False
        If True, the chord symbol will represent the inversion with slash 
        notation.

    Returns
    -------
    ChordResponse
        A dictionary of basic chord data without reference to the parent scale.

    TODO: Examples
    '''
    scale_root = decode_note_name(keynote)
    interval_structure = resolve_heptatonic_scale(scale_name, mode_name)
    chord_scale: tuple[ChordData, ...]
    voicing: tuple[int, ...] = tuple()
    
    if chord_voicing not in VOICINGS:
        chord_voicing = CLOSE

    if chord_size not in range(3, 8):
        chord_size = 3

    if chord_voicing in [D3, D24, D23] and chord_size == 3:
        chord_voicing = D2

    if chord_degree not in range(1, 8):
        chord_degree = 1

    if chord_inversion not in range(chord_size):
        chord_inversion = 0

    if structure == TERTIAL:
        chord_scale = chordify_heptatonic_tertial(
            interval_structure=interval_structure,
            keynote=scale_root,
            number_of_notes=chord_size
        )

    elif structure == SUS2:
        chord_scale = chordify_heptatonic_sus(
            interval_structure=interval_structure,
            keynote=scale_root,
            number_of_notes=chord_size,
            sus=2
        )
    elif structure == SUS4:
        chord_scale = chordify_heptatonic_sus(
            interval_structure=interval_structure,
            keynote=scale_root,
            number_of_notes=chord_size,
            sus=4
        )
    else:
        raise ArgumentError(f'Unknown structural modifier {structure=}')

    chord = chord_scale[chord_degree - 1]
    root = chord[NOTE_NAMES][0]
    chord = rotate_chord(chord, chord_inversion)

    # If the user wants slash notation, we regenerate the symbol to reflect
    # the inverted bass note.
    if chord_style and SLASH in chord_style:
        bass = chord[NOTE_NAMES][0]
        chord[CHORD_SYMBOL] = (
            root
            + encode_chord_symbol(chord[INTERVAL_NAMES], chord_style)
            + SLASH_SYMBOL
            + bass
        )

    if chord_voicing == CLOSE:
        return chord

    voicing = VOICINGS[chord_voicing]
    return apply_drop_voicing(chord, voicing)


def get_chord_symbol(intervals: Iterable[int | str], config: Optional[ChordStyle] = None) -> ChordSymbolData:
    '''
    Get a string that describes the given intervals as a chord form.

    Parameters
    ----------
    intervals : Iterable[int  |  str]
        A collection of intervals, either strings (e.g. "#4") or integers
        (e.g. 6), assuming that unison is "1" in strings and 0 in integers.
        Note that integers cannot express relative interval names (6 = '#4' 
        and 'b5'), and will always default to the same dummy identities.
    config : Optional[dict[str, str]], optional
        A dictionary of configuration settings: 'maj_symbol', 'min_symbol', 
        'dim_symbol', by default None, which supplies 'maj', 'min', and 
        'dim', respectively. Although our chord system recognizes augmented
        symbols as input, it does not generate them as output (we use '#5') 
        and so has no setting for augmented symbols.

    Returns
    -------
    ChordSymbolResponse
        A dictionary of all input data, plus the chord symbol generated from 
        that input.

    TODO: Examples
    '''
    dummy_names = ('1', 'b2', '2', 'b3', '3', '4',
                   'b5', '5', '#5', '6', 'b7', '7')
    validated_intervals: list[str] = []

    for interval in intervals:
        if isinstance(interval, int):
            interval %= TONES
            validated_intervals.append(dummy_names[interval])
        else:
            if validate_interval_name(interval):
                validated_intervals.append(interval)
    config = config or {}
    validated_config: ChordStyle = {}
    validated_config[MAJ_SYMBOL] = config.get(MAJ_SYMBOL, CHORD_MAJ)
    validated_config[MIN_SYMBOL] = config.get(MIN_SYMBOL, CHORD_MIN)
    validated_config[DIM_SYMBOL] = config.get(DIM_SYMBOL, CHORD_DIM)

    symbol = encode_chord_symbol(validated_intervals, validated_config)
    return ChordSymbolData(
        interval_names=sort_interval_names(validated_intervals),
        chord_symbol=symbol,
        configuration=validated_config
    )


def get_chord_from_symbol(chord_symbol: str) -> ChordData:
    '''
    Generate data about a chord's configuration based on its chord symbol.

    If the chord has an alphabetic root, then the note names will be 
    alphabetic note names. If the chord has a Roman numeral root, then
    the note names will be Roman numerals. 

    NOTE: Chords with Roman numerals cannot be used with slash notation 
    (e.g. 'Am7/G' PASS, 'ii7m' PASS, 'iiim/IV' FAIL, 'V7/3' FAIL).

    NOTE: Slash notation will attempt to rotate the chord to the indicated 
    inversion. If the slashed bass note is not present, then the chord will
    be superimposed over that bass in its root position. Slash notation 
    is most effective with triads and tetrads spanning less than an octave;
    chords spanning more than an octave often have awkward inversions!

    Parameters
    ----------
    chord_symbol : str
        The chord symbol from which to generate the chord data.

    Returns
    -------
    ChordResponse
        A set of data describing the chord configuration extrapolated from 
        the given symbol.

    TODO: Examples
    '''
    return resolve_chord_symbol(chord_symbol)

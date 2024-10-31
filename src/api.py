'''
Aristoxenus Endpoint API

The endpoints in this module assemble musical data produced by the various
functions in the ``src.core`` module. All endpoints return JSON friendly 
dictionaries.

For a more behaviour-oriented interface for accessing the ``src.core`` 
functions, see the ``src.classes`` module.
'''
from typing import Any, Iterable, Literal, Optional, TypedDict
from src.constants import (
    ALTERED,
    CHORD_DIM,
    CHORD_MAJ,
    CHORD_MIN,
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
    HEPTATONIC_SCALES,
    HEPTATONIC_SUPPLEMENT,
    INTERVAL_STRUCTURE,
    IONIAN,
    MAJ_SYMBOL,
    MIN_SYMBOL,
    MODAL_SERIES_KEYS,
    OPEN,
    SUS2,
    SUS4,
    TERTIAL,
    TONES
)
from src.errors import ArgumentError
from src.core import (
    get_best_heptatonic_spelling,
    ChordData,
    chordify_heptatonic_sus,
    chordify_heptatonic_tertial,
    decode_note_name,
    apply_drop_voicing,
    encode_chord_symbol,
    get_heptatonic_interval_symbols,
    get_heptatonic_scale_notes,
    is_valid_interval_name,
    rotate_chord,
    rotate_interval_structure,
    sort_interval_names
)

__all__ = [
    'get_heptatonic_scale', 
    'get_heptatonic_chord'
]

class HeptatonicScaleForm(TypedDict):
    '''
    A dictionary of information about a heptatonic scale form.

    Response from ``get_heptatonic_scale`` API endpoint.
    '''
    keynote: str
    scale_name: str
    modal_name: str
    interval_structure: tuple[int, ...]
    interval_scale: tuple[str, ...]
    requested_rendering: tuple[str, ...]
    recommended_keynote: str
    recommended_rendering: tuple[str, ...]


class HeptatonicChord(TypedDict):
    '''
    A dictionary of information about a chord form.

    Response from ``get_heptatonic_chord`` API endpoint.
    '''
    chord_symbol: str
    note_names: tuple[str, ...]
    interval_structure: tuple[int, ...]
    interval_names: tuple[str, ...]

class ChordSymbol(TypedDict):
    intervals: tuple[str, ...]
    symbol: str



def get_heptatonic_scale(
    keynote: str = "C",
    scale_name: str = DIATONIC,
    modal_name: str = IONIAN
) -> HeptatonicScaleForm:
    '''
    Return a collection of note and interval names for a given scale form.

    Parameters
    ----------
    keynote : str, optional
        _description_, by default 'C'
    scale_name : str, optional
        _description_, by default 'diatonic'
    modal_name : str, optional
        _description_, by default 'ionian'

    Returns
    -------
    HeptatonicScaleFormAPIResponse
        keynote: str
            The requested keynote.
        scale_name: str
            The requested scale name.
        modal_name: str
            The requested modal name.
        interval_structure: tuple[int, ...]
            An interval structure matching the given scale/mode configuration.
        interval_scale: tuple[str, ...]
            A tuple of interval names representing the form (e.g. '3', 'b5').
        requested_rendering: tuple[str, ...]
            A tuple of note names representing the form (e.g. 'A#', 'Gb'), 
            derived from the requested keynote.
        recommended_keynote: str
            The recommended name for the keynote, in case it has two names
            (e.g. A# = Bb).
        recommended_rendering: tuple[str, ...]
            The recommended note names for the form, derived from the 
            recommended keynote.

    Raises
    ------
    ArgumentError
        - If the keynote cannot be recognized (e.g. M#).
        - If the modal name is not one of 'ionian', 'dorian', etc.
        - If the scale name is not one of our names and isn't one of
        the supplemental names.

    Examples
    --------
    >>> scale = heptatonic_scale_form('C', 'diatonic', 'phrygian')
    >>> for k, v in scale.items():
    ...     print(k, v)
    ... 
    keynote C
    scale_name diatonic
    modal_name phrygian
    interval_structure (0, 1, 3, 5, 7, 8, 10)
    interval_scale ('1', 'b2', 'b3', '4', '5', 'b6', 'b7')
    requested_rendering ('C', 'Db', 'Eb', 'F', 'G', 'Ab', 'Bb')
    recommended_keynote C
    recommended_rendering ('C', 'Db', 'Eb', 'F', 'G', 'Ab', 'Bb')

    >>> scale = heptatonic_scale_form('A#', 'diatonic', 'lydian') 
    >>> for k, v in scale.items():
    ...     print(k, v)
    ...
    keynote A#
    scale_name diatonic
    modal_name lydian
    interval_structure (0, 2, 4, 6, 7, 9, 11)
    interval_scale ('1', '2', '3', '#4', '5', '6', '7')
    requested_rendering ('A#', 'B#', 'C##', 'D##', 'E#', 'F##', 'G##')
    recommended_keynote Bb
    recommended_rendering ('Bb', 'C', 'D', 'E', 'F', 'G', 'A')

    >>> scale = heptatonic_scale_form('G', 'altered', 'dorian')   
    >>> for k, v in scale.items():
    ...     print(k, v)
    ...
    keynote G
    scale_name altered
    modal_name dorian
    interval_structure (0, 2, 3, 5, 7, 9, 11)
    interval_scale ('1', '2', 'b3', '4', '5', '6', '7')
    requested_rendering ('G', 'A', 'Bb', 'C', 'D', 'E', 'F#')
    recommended_keynote G
    recommended_rendering ('G', 'A', 'Bb', 'C', 'D', 'E', 'F#')
    '''

    if (n := HEPTATONIC_SCALES.get(scale_name)) or (n := HEPTATONIC_SUPPLEMENT.get(scale_name)):
        base_scale = n
    else:
        raise ArgumentError(f"Unable to resolve scale name: {scale_name}")

    if modal_name in MODAL_SERIES_KEYS:
        modal_rotations = MODAL_SERIES_KEYS.index(modal_name)
    else:
        raise ArgumentError(f"Unable to resolve modal name: {modal_name}")

    if (n := decode_note_name(keynote)):
        note = n
    else:
        raise ArgumentError(f"Unable to resolve keynote: {keynote}")

    interval_structure = rotate_interval_structure(
        base_scale, modal_rotations)
    interval_scale = get_heptatonic_interval_symbols(interval_structure)
    requested_rendering = get_heptatonic_scale_notes(note,
        interval_structure)
    recommended_rendering = get_best_heptatonic_spelling(
        keynote, interval_structure)
    recommended_keynote = recommended_rendering[0]

    return HeptatonicScaleForm(
        keynote=keynote,
        scale_name=scale_name,
        modal_name=modal_name,
        interval_structure=interval_structure,
        interval_scale=interval_scale,
        requested_rendering=requested_rendering,
        recommended_keynote=recommended_keynote,
        recommended_rendering=recommended_rendering
    )


def get_heptatonic_chord(
        keynote: str = 'C',
        scale_name: str = DIATONIC,
        modal_name: str = IONIAN,
        chord_degree: Literal[1, 2, 3, 4, 5, 6, 7] = 1,
        chord_size: Literal[3, 4, 5, 6, 7] = 3,
        chord_inversion: int = 0,
        chord_voicing: Literal['open', 'close',
                               'd2', 'd3', 'd23', 'd24'] = CLOSE,
        structure: Literal['tertial', 'sus2', 'sus4'] = TERTIAL,
        use_slash: bool = False
) -> HeptatonicChord:
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
        What degree of the parent scale to derive the chord from, by default 1
    chord_size : Literal[3, 4, 5, 6, 7], optional
        How many notes should be in the derived chord, by default 3
    chord_inversion : int, optional
        Which inversion the chord be in, by default 0
    chord_voicing : Literal['open', 'close','d2', 'd3', 'd23', 'd24'], optional
        Which voicing the chord should be in, by default 'close'
    use_slash : bool, by default False
        If True, the chord symbol will represent the inversion with slash 
        notation.

    Returns
    -------
    SimpleChord
        A dictionary of basic chord data without reference to the parent scale.
    '''
    scale = get_heptatonic_scale(keynote, scale_name, modal_name)
    voicing: tuple[int, ...] = tuple()
    voicings = {
        OPEN: DROP_2_VOICING,
        D2: DROP_2_VOICING,
        D3: DROP_3_VOICING,
        D23: DROP_2_AND_3_VOICING,
        D24: DROP_2_AND_4_VOICING
    }
    if chord_voicing not in voicings:
        chord_voicing = CLOSE

    if chord_size not in range(3, 8):
        chord_size = 3

    if chord_voicing in [D3, D24, D23] and chord_size == 3:
        chord_voicing = D2

    if chord_degree not in range(1, 8):
        chord_degree = 1

    if chord_inversion not in range(chord_size):
        chord_inversion = 0

    root = decode_note_name(keynote)
    interval_structure = scale[INTERVAL_STRUCTURE]
    chord_scale = tuple[ChordData, ...]

    if structure == TERTIAL:
        chord_scale = chordify_heptatonic_tertial(
        parent_structure=interval_structure, 
        keynote=root, 
        number_of_notes=chord_size
        )
        
    elif structure == SUS2:
        chord_scale = chordify_heptatonic_sus(
            parent_structure=interval_structure,
            keynote=root,
            number_of_notes=chord_size,
            sus=2
        )
    elif structure == SUS4:
        chord_scale = chordify_heptatonic_sus(
            parent_structure=interval_structure,
            keynote=root,
            number_of_notes=chord_size,
            sus=4
        )
    else:
        raise ArgumentError(f'Unknown structural modifier {structure=}')
    
    chord = chord_scale[chord_degree - 1]
    chord = rotate_chord(chord, chord_inversion)

    # If the user wants slash notation, we regenerate the symbol to reflect
    # the inverted bass note.
    if use_slash:
        chord.chord_symbol = keynote + encode_chord_symbol(chord.interval_symbols)

    if chord_voicing == CLOSE:
        return HeptatonicChord(**vars(chord))

    voicing = voicings[chord_voicing]
    return HeptatonicChord(**vars(apply_drop_voicing(chord, voicing)))


def get_chord_symbol_from_intervals(intervals: Iterable[int | str | Any], config: Optional[dict[str, str]] = None) -> ChordSymbol:

    # Dummy names are used in place of integers.
    d = get_heptatonic_interval_symbols()
    a = get_heptatonic_interval_symbols(HEPTATONIC_SCALES[ALTERED])
    supplement = d + a
    dummy_names = sort_interval_names(set(supplement))
    _intervals: list[str] = []
    for i, interval in enumerate(intervals):
        if isinstance(interval, int):
            interval %= TONES
            _intervals[i] = dummy_names[interval]
        elif isinstance(interval, str):
            if is_valid_interval_name(interval):
                _intervals.append(interval)

    _config: dict[str, str] = {}
    if not config:
        config = {}

    _config[MAJ_SYMBOL] = config.get(MAJ_SYMBOL, CHORD_MAJ)
    _config[MIN_SYMBOL] = config.get(MIN_SYMBOL, CHORD_MIN)
    _config[DIM_SYMBOL] = config.get(DIM_SYMBOL, CHORD_DIM)

    symbol = encode_chord_symbol(_intervals, **_config)
    return ChordSymbol(intervals=sort_interval_names(_intervals), symbol=symbol)


def get_chord_intervals_from_symbol(chord_symbol: str) -> HeptatonicChord | ChordSymbol:
    ...
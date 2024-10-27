'''
Aristoxenus General API

The API provides bulk or selected data compiled from the backend functions.

For a more object-oriented interface for accessing the backend functions, 
see ``classes.py``.
'''
from typing import Literal
from src.annotations import (
    SimpleChord,
    HeptatonicChordScale,
    HeptatonicScaleForm,
    TetradInversions,
    TetradProfile,
    TriadInversions,
    TriadProfile
)
from src.constants import (
    CLOSE,
    DIATONIC,
    DROP_2_AND_3_VOICING,
    DROP_2_AND_4_VOICING,
    DROP_2_VOICING,
    DROP_3_VOICING,
    HEPTATONIC_SCALES,
    HEPTATONIC_SUPPLEMENT,
    IONIAN,
    MODAL_SERIES_KEYS
)
from src.errors import ArgumentError
from src.functions import (
    best_heptatonic_spelling,
    chordify_heptatonic_tertial,
    decode_note_name,
    drop_voicing,
    get_heptatonic_interval_symbols,
    get_heptatonic_scale_notes,
    name_chord,
    romanize_intervals,
    rotate_chord,
    rotate_interval_structure
)
from src.structures import ChordData


def heptatonic_scale_form(
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
    requested_rendering = get_heptatonic_scale_notes(*note,
        interval_structure)
    recommended_rendering = best_heptatonic_spelling(
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


def heptatonic_chord_scale(
    keynote: str = 'C',
    scale_name: str = DIATONIC,
    modal_name: str = IONIAN
) -> HeptatonicChordScale:
    '''
    Return a complete report about the given scale's chords.

    These will include triads and tetrads in tertial, sus2,
    and sus4 form, as well as their inversions and voicings.

    Parameters
    ----------
    keynote : str, optional
        The tonic of the parent scale, by default 'C'
    scale_name : str, optional
        The name of the parent scale, by default 'diatonic'
    modal_name : str, optional
        The name of the modal rotation, by default 'ionian'

    Returns
    -------
    HeptatonicChordScale
        _description_

    >>> from src.api import heptatonic_chord_scale
    >>> x = heptatonic_chord_scale('C', 'diatonic', 'ionian')
    >>> from pprint import pprint
    >>> pprint(x)

    TODO: Add sus2 and sus4 triads and tetrads using the 
    '''
    scale_data = heptatonic_scale_form(keynote, scale_name, modal_name)
    interval_structure = scale_data['interval_structure']
    interval_names = scale_data['interval_scale']
    note = decode_note_name(keynote)
    roman_names = romanize_intervals(interval_names)

    close_triads = chordify_heptatonic_tertial(interval_structure, note, 3)
    close_tetrads = chordify_heptatonic_tertial(interval_structure, note, 4)

    triads: list[TriadInversions] = []
    tetrads: list[TetradInversions] = []
    for i in range(7):
        # Basic categorical information
        triad_chord_symbol = name_chord(close_triads[i].interval_symbols)
        tetrad_chord_symbol = name_chord(close_tetrads[i].interval_symbols)
        root_note = close_triads[i].note_names[0]
        degree = interval_names[i]
        roman = roman_names[i]

        # Triads
        # ------
        triad_rootpos = TriadProfile(
            close_voicing=SimpleChord(**vars(close_triads[i])),
            open_voicing=SimpleChord(**vars(
                drop_voicing(close_triads[i], DROP_2_VOICING)))
        )
        triad_inversions: list[TriadProfile] = []
        inversions = (1, 2)
        for inversion in inversions:
            rot_ch = rotate_chord(close_triads[i], inversion)
            opench = drop_voicing(rot_ch, DROP_2_VOICING)
            triad_inversions.append(
                TriadProfile(close_voicing=SimpleChord(**vars(rot_ch)),
                             open_voicing=SimpleChord(**vars(opench))
                             )
            )
        triads.append(
            TriadInversions(
                chord_symbol=triad_chord_symbol,
                root_note=root_note,
                scale_degree=degree,
                roman_degree=roman,
                root_position=triad_rootpos,
                first_inversion=triad_inversions[0],
                second_inversion=triad_inversions[1]
            )
        )

        # Tetrads
        # -------
        tetrads_rootpos = TetradProfile(
            close_voicing=SimpleChord(**vars(close_tetrads[i])),
            drop_2_voicing=SimpleChord(**vars(drop_voicing(
                close_tetrads[i], DROP_2_VOICING))),
            drop_3_voicing=SimpleChord(**vars(drop_voicing(
                close_tetrads[i], DROP_3_VOICING))),
            drop_2_and_3_voicing=SimpleChord(**vars(drop_voicing(
                close_tetrads[i], DROP_2_AND_3_VOICING))),
            drop_2_and_4_voicing=SimpleChord(**vars(drop_voicing(
                close_tetrads[i], DROP_2_AND_4_VOICING)))
        )
        inversions = (1, 2, 3)
        tetrad_inversions: list[TetradProfile] = []
        for inversion in inversions:
            tetrad_inversions.append(
                TetradProfile(
                    close_voicing=SimpleChord(**vars(
                        rotate_chord(close_tetrads[i], inversion))),
                    drop_2_voicing=SimpleChord(**vars(drop_voicing(rotate_chord(
                        close_tetrads[i], inversion), DROP_2_VOICING))),
                    drop_3_voicing=SimpleChord(**vars(drop_voicing(rotate_chord(
                        close_tetrads[i], inversion), DROP_3_VOICING))),
                    drop_2_and_3_voicing=SimpleChord(**vars(drop_voicing(rotate_chord(
                        close_tetrads[i], inversion), DROP_2_AND_3_VOICING))),
                    drop_2_and_4_voicing=SimpleChord(**vars(drop_voicing(rotate_chord(
                        close_tetrads[i], inversion), DROP_2_AND_4_VOICING)))
                )
            )
        tetrads.append(
            TetradInversions(
                chord_symbol=tetrad_chord_symbol,
                root_note=root_note,
                scale_degree=degree,
                roman_degree=roman,
                root_position=tetrads_rootpos,
                first_inversion=tetrad_inversions[0],
                second_inversion=tetrad_inversions[1],
                third_inversion=tetrad_inversions[2]
            )
        )

    return HeptatonicChordScale(
        keynote=keynote,
        scale_name=scale_name,
        modal_name=modal_name,
        tertial_triads=tuple(triads),
        tertial_tetrads=tuple(tetrads)
    )


def tertial_chord_from_heptatonic_scale(
        keynote: str = 'C',
        scale_name: str = DIATONIC,
        modal_name: str = IONIAN,
        chord_degree: Literal[1, 2, 3, 4, 5, 6, 7] = 1,
        chord_size: Literal[3, 4, 5, 6, 7] = 3,
        chord_inversion: int = 0,
        chord_voicing: Literal['open', 'close',
                               'd2', 'd3', 'd23', 'd24'] = CLOSE
) -> SimpleChord:
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
    chord_size : Literal[3, 4], optional
        How many notes should be in the derived chord, by default 3
    chord_inversion : int, optional
        Which inversion the chord should present, by default 0
    chord_voicing : Literal['open', 'close','d2', 'd3', 'd23', 'd24'], optional
        Which voicing of notes should the chord present, by default CLOSE

    Returns
    -------
    SimpleChord
        A dictionary of basic chord data without reference to the parent scale.
    '''
    scale = heptatonic_scale_form(keynote, scale_name, modal_name)
    voicing: tuple[int, ...] = tuple()
    if chord_voicing not in ['open', 'close', 'd2', 'd3', 'd23', 'd24']:
        chord_voicing = CLOSE

    if chord_size not in range(3, 8):
        chord_size = 3

    if chord_voicing in ['d3', 'd24', 'd23'] and chord_size == 3:
        chord_voicing = 'd2'

    if chord_degree not in range(1, 8):
        chord_degree = 1

    if chord_inversion not in range(chord_size):
        chord_inversion = 0

    chord: ChordData = chordify_heptatonic_tertial(
        scale['interval_structure'], decode_note_name(keynote), chord_size)[chord_degree]
    chord = rotate_chord(chord, chord_inversion)
    if chord_voicing == CLOSE:
        return SimpleChord(**vars(chord))
    voicings = {
        'open': DROP_2_VOICING,
        'd2': DROP_2_VOICING,
        'd3': DROP_3_VOICING,
        'd23': DROP_2_AND_3_VOICING,
        'd24': DROP_2_AND_4_VOICING
    }
    voicing = voicings[chord_voicing]
    return SimpleChord(**vars(drop_voicing(chord, voicing)))

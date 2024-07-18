'''
Functions relating to permuting different types of interval structures.
'''
from typing import Sequence
from src.data import (
    annotations,
    constants,
    errors,
    intervallic_canon,
    keywords,
    permutation_data
)
from src.functions import (
    bitwise,
    nomenclature,
    utils
)

def chordify(interval_structure: int, notes: int | str = 3, step: int | str = 2) -> dict[str, int]:
    '''
    Return a dict of chords for the given scale and structural principles.

    Parameters
    ----------
    interval_structure : int
        An integer not exceeding 12 bits representing the parent scale
    notes : int | str, optional
        The number of notes to include, or a keyword denoting the same 
        (e.g. 'triad'), by default 3
    step : int | str, optional
        The number of steps between chord tones, or a keyword denoting 
        the same (e.g. 'tertial'). The steps start on 0, so 2=tertial, 
        by default 2

    Returns
    -------
    dict[str, int]
        A mapping of each interval name in the scale to the chord built from
        that degree.

    Raises
    ------
    errors.IntervalStructureError
        If the interval structure exceeds 12 bits.

    Examples
    --------
    The triads of the diatonic scale:
    >>> from src.data.intervallic_canon import DIATONIC_SCALE
    >>> chordify(DIATONIC_SCALE)
    {'1': 145, '2': 137, '3': 137, '4': 145, '5': 145, '6': 137, '7': 73}
    >>> chordify(DIATONIC_SCALE, 3)
    {'1': 145, '2': 137, '3': 137, '4': 145, '5': 145, '6': 137, '7': 73}

    The tetrads of the diatonic scale, quartal voicing:
    >>> chordify(DIATONIC_SCALE, 4, 3)
    {'1': 67617, '2': 33825, '3': 33825, '4': 67649, '5': 66593, '6': 33825, '7': 33825}
    >>> chordify(0b101010110101, 'tetrad', 'quartal')
    {'1': 67617, '2': 33825, '3': 33825, '4': 67649, '5': 66593, '6': 33825, '7': 33825}
    '''
    
    # Convert keywords to ints
    if isinstance(notes, str):
        notes = utils.decode_numeration(notes)
    if isinstance(step, str):
        step = utils.decode_numeration(step)

    if not bitwise.validate_interval_structure(interval_structure, 12):
        raise errors.IntervalStructureError(interval_structure)

    interval_names: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        interval_structure)
    chord_scale: dict[str, int] = {}
    chord_intervals: list[int] = []
    full_range: int

    # Grab the intervals for each mode and use them to derive chords
    for i, inversion in enumerate(bitwise.get_inversions(interval_structure, 12)):
        full_range = bitwise.extend_structure(inversion)
        chord_intervals = list(bitwise.iterate_intervals(full_range))[
            ::step][:notes]
        chord_scale.update(
            {interval_names[i]: bitwise.reduce_intervals(chord_intervals)})

    return chord_scale


def chordify_note_names(note_names: Sequence[str], notes: int | str = 3, step: int | str = 2) -> dict[str, tuple[str, ...]]:
    '''
    Return a dict of chords for the given scale and structural principles.

    This dictionary is intended for chords in plain notation,
    and will not properly create chords in scientific notation.

    Parameters
    ----------
    note_names : list[str] | tuple[str, ...]
        A set of plain note names in any style to serve as the parent scale.
    notes : int | str, optional
        The number of notes that each chord will have; default=3
    step : int | str, optional
        The number of notes to skip when constructing the chord; default=2

    Returns
    -------
    dict[str, tuple[str, ...]]
        A collection of chords organized by scale degree.

    Notes
    -----
    Since some scales might mix sharps and flats, this function does not 
    attempt to validate or normalize note names, and is capable of producing
    an invalid scale.
    '''
    if len(note_names) != 7:
        raise errors.HeptatonicScaleError(note_names)
    if isinstance(notes, str):
        notes = utils.decode_numeration(notes)
    if isinstance(step, str):
        step = utils.decode_numeration(step)

    chord_scale: dict[str, tuple[str, ...]] = {}
    intervals: tuple[str, ...] = nomenclature.name_heptatonic_intervals(
        note_names)
    roman_intervals: tuple[str, ...] = utils.romanize_intervals(intervals)

    for i, note_name in enumerate(note_names):
        base: list[str] = list(utils.shift_array(note_names, note_name))
        full_range: list[str] = base * constants.NUMBER_OF_OCTAVES
        chord_form: list[str] = full_range[::step][:notes]
        chord_scale.update({roman_intervals[i]: tuple(chord_form)})

    return chord_scale


def spread_triad(chord_structure: int) -> int:
    '''
    Return a version of the given chord in which the middle note is 
    transposed up by an octave.

    Parameters
    ----------
    chord_structure : int
        A chord structure not exceeding 12 bits.

    Returns
    -------
    int
        A rearranged chord structure not exceeding 24 bits.

    Examples
    --------
    >>> bin(spread_triad(0b10010001))
    '0b10000000010000001'
    '''
    if not bitwise.validate_interval_structure(chord_structure, 12, 3):
        raise errors.IntervalStructureError(chord_structure)

    return drop_voicing(chord_structure, permutation_data.DROP_2_VOICING)


def drop_voicing(chord_structure: int, drop_notes: Sequence[int]) -> int:
    '''
    Adjust the intervals in a given chord structure to produce a 'drop' 
    voicing.

    Parameters
    ----------
    chord_structure : int
        An integer representing the structure of a chord.
    drop_notes : Sequence[int]
        The notes of the chord that will be shifted to produce the new 
        voicing. These represent the flipped bits in the chord structure,
        so that index 0 is the least significant bit.
        Some common options are included in `data.constants` as `DROP_2`,
        `DROP_2_AND_4`, and `DROP_3`.

    Returns
    -------
    int
        The same chord, but with the given modifications to its intervals.

    Notes
    -----
    The 'drop' logic produces a voicing in a different inversion from the 
    starting chord:

        C E G B -> G C E B (drop the G, results in a 2nd inversion major7)

    This function expresses drop chords in terms of *raised* intervals:

        C E G B -> C E B G (raise the G, results in a root position major7)

    This situation entails that a drop chord must be generated from the 
    corresponding inversion of a close-voiced chord. If a chord is "dropped"
    before it is rotated, then the "inversions" will actually represent a 
    variety of drop types:

        C E B G (starting point: 'root position' drop 2 Cmaj7)
        E B G C (first rotation: a '1st inversion' drop 2&4 Cmaj7)
        B G C E (second rotation: a '3rd inversion' drop 3 Cmaj7)
        G C E B (third rotation: a '2nd inversion' drop 2 Cmaj7)

    Although drop chords are typically 4-note voicings, the function can 
    accommodate larger structures as well, as long as the indices are
    present in the given interval structure (0 is the lowest note).

    Examples
    --------
    >>> bin(drop_voicing(0b100010010001, permutation_data.DROP_2_VOICING))
    '0b10000100010000001'
    >>> bin(drop_voicing(0b100010010001, permutation_data.DROP_3_VOICING))
    '0b10010000100000000001'
    >>> bin(drop_voicing(0b100010010001, permutation_data.DROP_2_AND_4_VOICING))
    '0b100000010000000010000001'
    '''
    intervals = list(bitwise.iterate_intervals(chord_structure))
    for interval in drop_notes:
        intervals[interval] = bitwise.transpose_interval(intervals[interval])
    return bitwise.reduce_intervals(intervals)


def triad_variants() -> annotations.TriadInventory:
    '''
    Return a tuple containing all known triads and their voicing variants.

    Returns
    -------
    tuple[dict[str, str | int | dict[str, int]], ...]
        A tuple of dictionaries, each dictionary containing:
            canonical_name: str
            canonical_form: int
            close: dict{
                root_position: int
                first_inversion: int
                second_inversion: int}
            open: dict{ same as above }
    '''
    triads = intervallic_canon.TRIADS_KEY_TO_VALUE_MAP

    variants: list[annotations.TriadConspectus] = []
    for name, triad in triads.items():
        open_triad = spread_triad(triad)
        close_inversions = bitwise.get_inversions(triad, constants.TONES)
        open_inversions = bitwise.get_inversions(open_triad, constants.TONES*2)
        inversion_names = [keywords.NUMBERED_INVERSIONS[x] for x in range(3)]
        variants.append(annotations.TriadConspectus(canonical_name=name,
                                                    canonical_form=triad,
                                                    close=dict(
                                                        zip(inversion_names, close_inversions)),
                                                    open=dict(zip(inversion_names, open_inversions))))

    return tuple(variants)


def tetrad_variants() -> annotations.TetradInventory:
    '''
    Return a tuple containing all known tetrads and their voicing variants.

    Returns
    -------
    tuple[dict[str, str | int | dict[str, int]], ...]
        A tuple of dictionaries, each dictionary containing:
            canonical_name: str
            canonical_form: int
            close: dict{
                root_position: int
                first_inversion: int
                second_inversion: int
                third_inversion: int}
            drop_2: dict{ same as above }
            drop_3: dict{ same as above }
            drop_2_and_4: dict{ same as above }

    Examples
    --------
    >>> x = tetrad_variants()

    3 = Minor 6 chord

    >>> bin(x[3]['close']['root_position'])
    '0b1010001001'
    >>> bin(x[3]['close']['first_inversion'])
    '0b1001010001'
    >>> bin(x[3]['close']['second_inversion'])
    '0b100100101'
    >>> bin(x[3]['close']['third_inversion'])
    '0b10001001001'
    '''
    tetrads = intervallic_canon.TETRADS_KEY_TO_VALUE_MAP

    variants: annotations.TetradInventory = []
    inversion_names = [keywords.NUMBERED_INVERSIONS[x] for x in range(4)]

    for name, tetrad in tetrads.items():
        inversions: tuple[int, ...] = bitwise.get_inversions(
            tetrad, constants.TONES)
        innerdict = annotations.TetradConspectus(
            canonical_name=name,
            canonical_form=tetrad,
            close={},
            drop_2={},
            drop_3={},
            drop_2_and_4={}
        )
        for i, inversion in enumerate(inversions):
            # We iterate the inversions THEN generate the drop voicings.
            # See `permutation.drop_voicing` for info.
            inversion_name: str = inversion_names[i]
            drop2: int = drop_voicing(inversion, permutation_data.DROP_2_VOICING)
            drop3: int = drop_voicing(inversion, permutation_data.DROP_3_VOICING)
            drop24: int = drop_voicing(inversion, permutation_data.DROP_2_AND_4_VOICING)

            innerdict[keywords.CLOSE].update({inversion_name: inversion})
            innerdict[keywords.DROP_2].update({inversion_name: drop2})
            innerdict[keywords.DROP_3].update({inversion_name: drop3})
            innerdict[keywords.DROP_2_AND_4].update({inversion_name: drop24})

        variants.append(innerdict)

    return tuple(variants)


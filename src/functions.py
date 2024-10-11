'''Functions used in the program. 

This module is the meat of the program. Although the functions in this module
can be used as-is, the API supplied by ``api.py`` makes it easier to get the
end results.
'''
import re
from typing import (
    Sequence,
    Iterable,
    Optional
)
from lib.numerus import Numerus

from src.constants import (
    CHORD_11,
    CHORD_13,
    CHORD_2,
    CHORD_3,
    CHORD_4,
    CHORD_5,
    CHORD_6,
    CHORD_7,
    CHORD_9,
    CHORD_ADD,
    CHORD_AUGMENTED_SYMBOLS,
    CHORD_DIM,
    CHORD_DIM_SYMBOLS,
    CHORD_DOUBLE_FLAT_3,
    CHORD_DOUBLE_FLAT_7,
    CHORD_FLAT_3,
    CHORD_FLAT_5,
    CHORD_FLAT_7,
    CHORD_HALFDIM_SYMBOLS,
    CHORD_MAJ,
    CHORD_MAJOR_SYMBOLS,
    CHORD_MIN,
    CHORD_MINOR_SYMBOLS,
    CHORD_NO,
    CHORD_SHARP_3,
    CHORD_SHARP_5,
    CHORD_SUS,
    EXTENSION,
    FLAT_SYMBOL,
    MAIN,
    MODIFICATION,
    RE_PARSE_CHORD_SYMBOL,
    SHARP_SYMBOL,
    DIATONIC,
    HEPTATONIC_SCALES,
    NATURAL_NAMES,
    NOTES,
    RE_SPLIT_NOTE_NAME,
    TONES
)
from src.errors import ArgumentError
from src.structures import ChordData


def names_are_heptatonic(note_names: Sequence[str]) -> bool:
    '''
    Return true if the given note names make up a valid heptatonic scale.

    Parameters
    ----------
    note_names : Sequence[str]
        A sequence of note names.

    Returns
    -------
    bool
        True, if there are seven unique notes.

    Example
    -------
    >>> names_are_heptatonic(['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'])
    True
    >>> names_are_heptatonic(['C#', 'D#', 'E#', 'F', 'G#', 'A#', 'B#'])
    False
    >>> names_are_heptatonic(['C', 'D#', 'E', 'F', 'G', 'Ab', 'Bb'])
    True
    >>> names_are_heptatonic(['C', 'D#', 'Eb', 'F', 'G', 'Ab', 'Bb'])
    False
    '''
    new: list[int] = []
    for name_idx, accidentals in [decode_note_name(x) for x in note_names]:
        new.append(HEPTATONIC_SCALES[DIATONIC][name_idx] + accidentals)
    return len(set(new)) == NOTES


def structure_is_heptatonic(interval_structure: Sequence[int]) -> bool:
    '''
    Return true if the given interval structure makes up a valid heptatonic
    scale.

    Parameters
    ----------
    interval_structure : Sequence[int]
        A sequence of integers representing intervals.

    Returns
    -------
    bool
        True, if there are seven unique intervals.

    Example
    -------
    >>> structure_is_heptatonic([1, 2, 3, 4, 5, 6, 7])
    True
    >>> structure_is_heptatonic([1, 3, 3, 4, 5, 6, 7])
    False
    >>> structure_is_heptatonic([1, 2, 4, 5, 6, 7])
    False
    '''
    return len(set(interval_structure)) == NOTES


def encode_note_name(natural_note_idx: int, accidentals: int) -> str:
    '''
    Get a note symbol with the given name and number of accidentals.

    Parameters
    ----------
    natural_note_idx : int
        The index of the natural note name to use as the base.
    accidentals : int
        The number of accidentals to add. Use negative numbers for
        flats.

    Returns
    -------
    str
        A note symbol with the given name and number of accidentals.

    Example
    -------
    >>> encode_note_name(0, 0)
    'C'
    >>> encode_note_name(1, 1)
    'D#'
    >>> encode_note_name(2, -1)
    'Eb'
    >>> encode_note_name(6, 1)
    'B#'
    >>> encode_note_name(3, 4)
    'F####'
    '''
    natural_name: str = NATURAL_NAMES[natural_note_idx]
    return add_accidentals_to_note_name(natural_name, accidentals)


def decode_note_name(note_name: str) -> tuple[int, int]:
    '''
    For the given note name, return a tuple containing two integers:
    the index of the alphabetic name and the number (+/-) of accidentals.

    Parameters
    ----------
    note_name : str
        A note name with any number of accidentals.

    Returns
    -------
    tuple[int, int]
        The index of the alphabetic name, plus the number of accidentals 
        in the note name (a negative number represents flats).

    Raises
    ------
    UnknownSymbolError
        If the note name does not conform to the expected format (e.g. begins
        with an unrecognizable root).

    Example
    -------
    >>> decode_note_name('B#')
    (6, 1)
    >>> decode_note_name('C')
    (0, 0)
    >>> decode_note_name('D#')
    (1, 1)
    >>> decode_note_name('Eb')
    (2, -1)
    >>> decode_note_name('E####')
    (2, 4)
    '''
    name = re.match(RE_SPLIT_NOTE_NAME, note_name)
    if name:
        name = name.groupdict()
        accidentals: int = name['accidentals'].count(
            '#') - name['accidentals'].count('b')
        return NATURAL_NAMES.index(name['note_name']), accidentals
    raise ArgumentError(f'Unknown note name symbol: {note_name}')


def add_accidentals_to_note_name(note_name: str, accidentals: int) -> str:
    '''
    Add the given number of accidentals to the given note name.

    Parameters
    ----------
    note_name : str
        An alphabetic name.
    accidentals : int
        The number of accidentals to add. Use negative numbers for
        flats.

    Returns
    -------
    str
        The original alphabetic name with the given number of accidentals
        added.

    Examples
    --------
    >>> add_accidentals_to_note_name('D', -1)
    'Db'
    >>> add_accidentals_to_note_name('F', 1)
    'F#'
    >>> add_accidentals_to_note_name('C', 3)
    'C###'
    '''
    if accidentals > 0:
        return note_name + '#' * (accidentals)
    return note_name + 'b' * (-accidentals)


def add_accidentals_to_interval_name(interval_name: str, accidentals: int) -> str:
    '''
    Add the given number of accidentals to the given interval name.

    Parameters
    ----------
    interval_name : str
        A numeric digit from 1-7.
    accidentals : int
        The number of accidentals to add. Use negative numbers for
        flats.

    Returns
    -------
    str
        The given number of accidentals with the original interval digit added.

    Examples
    --------
    >>> add_accidentals_to_interval_name('IV', -1)
    'bIV'
    >>> add_accidentals_to_interval_name('VII', -2)
    'bbVII'
    >>> add_accidentals_to_interval_name('II', 1)
    '#II'
    '''
    if accidentals > 0:
        return '#' * (accidentals) + interval_name
    return 'b' * (-accidentals) + interval_name


def get_heptatonic_scale_notes(interval_structure: Sequence[int], root_note_idx: int, root_accidentals: int) -> tuple[str, ...]:
    '''
    Return the note names for the given scale form, root note, and root accidentals.

    Parameters
    ----------
    interval_structure : Sequence[int]
        A sequence of integers representing the intervals of a scale form.
    root_note_idx : int
        The index of the alphabetic name to use as the root base.
    root_accidentals : int
        The number of accidentals to add to the alphabetic base name.
        Use negative numbers for flats.

    Returns
    -------
    tuple[str, ...]
        A tuple of the seven alphabetic names in the appropriate order and 
        with the appropriate number of accidentals.

    Example
    -------
    >>> get_heptatonic_scale_notes([0, 2, 4, 5, 7, 9, 11], 0, 0)
    ('C', 'D', 'E', 'F', 'G', 'A', 'B')
    >>> get_heptatonic_scale_notes([0, 2, 4, 5, 7, 9, 11], 1, 1)
    ('D#', 'E#', 'F##', 'G#', 'A#', 'B#', 'C##')
    >>> get_heptatonic_scale_notes([0, 2, 3, 5, 7, 9, 10], 1, 0)
    ('D', 'E', 'F', 'G', 'A', 'B', 'C')
    >>> get_heptatonic_scale_notes([0, 2, 3, 5, 7, 9, 10], 0, 0)
    ('C', 'D', 'Eb', 'F', 'G', 'A', 'Bb')
    >>> get_heptatonic_scale_notes([0, 1, 3, 4, 6, 8, 10], 0, 1)
    ('C#', 'D', 'E', 'F', 'G', 'A', 'B')
    >>> get_heptatonic_scale_notes([0, 2, 4, 5, 7, 9, 11], 5, -1)
    ('Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G')
    '''
    result: list[str] = []
    root_pitch: int = HEPTATONIC_SCALES[DIATONIC][root_note_idx] + \
        root_accidentals
    for i in range(NOTES):
        new_note_idx = (i + root_note_idx) % NOTES
        tones_offset = ((i + root_note_idx) // NOTES) * TONES
        original_value = HEPTATONIC_SCALES[DIATONIC][new_note_idx]
        relative_value = root_pitch + interval_structure[i]
        accidentals = relative_value - (original_value + tones_offset)
        note_name = encode_note_name(new_note_idx, accidentals)
        result.append(note_name)
    return tuple(result)


def get_binomial_structure_notes(interval_structure: Sequence[int], root_idx: int) -> tuple[str, ...]:
    '''
    Return a neutrally-spelled version of a given interval structure, using binomial
    note names wherever accidentals are needed (e.g. 'C#|Db'). 

    Parameters
    ----------
    interval_structure : Sequence[int]
        The interval structure you want to mask
    root_idx : int
        The 12-tone index of the note that will serve as the tonic/root.

    Returns
    -------
    tuple[str, ...]
        A collection of note names representing the structure.
    '''
    chromatic = ['C', 'C#|Db', 'D', 'D#|Eb', 'E',
                 'F', 'F#|Gb', 'G', 'G#|Ab', 'A', 'A#|Bb', 'B']
    chromatic = chromatic[root_idx:] + chromatic[:root_idx]
    return tuple(chromatic[x % TONES] for x in interval_structure)


def get_heptatonic_interval_symbols(interval_structue: Sequence[int], octave: bool = False) -> tuple[str, ...]:
    '''
    Return the numeric interval symbols for the given scale form.

    Parameters
    ----------
    interval_structure : Sequence[int]
        A sequence of integers representing the intervals of a scale form.
    octave : bool
        Flag whether to extend the structure into the second octave, by 
        default False.

    Returns
    -------
    tuple[str, ...]
        A tuple of the digits 1-7 with the appropriate accidentals.

    Examples
    --------
    >>> get_heptatonic_interval_symbols([0, 1, 4, 5, 6, 8, 9])
    ('1', 'b2', '3', '4', 'b5', 'b6', 'bb7')
    >>> get_heptatonic_interval_symbols([0, 1, 4, 5, 6, 8, 9], octave=True)
    ('1', 'b2', '3', '4', 'b5', 'b6', 'bb7', '8', 'b9', '10', '11', 'b12', 'b13', 'bb14')
    >>> get_heptatonic_interval_symbols([0, 2, 4, 6, 7, 9, 11])
    ('1', '2', '3', '#4', '5', '6', '7')
    >>> get_heptatonic_interval_symbols([0, 2, 4, 5, 7, 8, 9])
    ('1', '2', '3', '4', '5', 'b6', 'bb7')
    >>> get_heptatonic_interval_symbols([0, 2, 4, 5, 8, 9, 11])
    ('1', '2', '3', '4', '#5', '6', '7')
    >>> get_heptatonic_interval_symbols([0, 2, 3, 5, 6, 9, 11])
    ('1', '2', 'b3', '4', 'b5', '6', '7')
    >>> get_heptatonic_interval_symbols([0, 1, 4, 5, 7, 8, 10])
    ('1', 'b2', '3', '4', '5', 'b6', 'b7')
    >>> get_heptatonic_interval_symbols([0, 2, 3, 5, 7, 9, 10])
    ('1', '2', 'b3', '4', '5', '6', 'b7')
    >>> get_heptatonic_interval_symbols([0, 2, 4, 5, 6, 9, 10])
    ('1', '2', '3', '4', 'b5', '6', 'b7')
    >>> get_heptatonic_interval_symbols([0, 1, 3, 4, 6, 8, 10])
    ('1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7')
    >>> get_heptatonic_interval_symbols([0, 2, 4, 6, 7, 8, 11])
    ('1', '2', '3', '#4', '5', 'b6', '7')
    '''
    if not structure_is_heptatonic(interval_structue):
        raise ArgumentError(
            f'Interval structure must be heptatonic (structure={interval_structue}).')
    result: list[str] = []
    for i in range(NOTES if not octave else NOTES * 2):
        degree_name = (i % (TONES if not octave else TONES * 2)) + 1
        normal_value = HEPTATONIC_SCALES[DIATONIC][i % NOTES]
        actual_value = interval_structue[i % len(interval_structue)] % TONES
        accidentals = actual_value - normal_value
        interval_name = add_accidentals_to_interval_name(
            str(degree_name), accidentals)
        result.append(interval_name)
    return tuple(result)


def romanize_intervals(interval_names: Sequence[str] | str) -> tuple[str, ...]:
    '''
    Convert Indian numeral interval name(s) to use Roman numerals instead.

    Parameters
    ----------
    interval_names : Sequence[str] | str
        A string or array of strings representing interval symbols using Indian 
        numerals (e.g 'b3').

    Returns
    -------
    tuple[str, ...]
        A tuple containing the same interval symbol(s) expressed using Roman 
        numerals (e.g. 'bIII').

    Raises
    ------
    ArgumentError
        If the interval name cannot be parsed. We expect that interval names
        will consist of a numeral plus one or more preceding accidentals.
        Numerals up to 3999 can be parsed, 

    Examples
    --------
    >>> romanize_intervals('b3')
    ('bIII',)
    >>> romanize_intervals(['#5', 'b6'])
    ('#V', 'bVI')
    >>> romanize_intervals('#3')
    ('#III',)
    >>> romanize_intervals('bb7')
    ('bbVII',)
    >>> romanize_intervals('b6')
    ('bVI',)
    '''
    if isinstance(interval_names, str):
        interval_names = [interval_names]
    roman_intervals: list[str] = []
    for interval in interval_names:
        for number in range(1, 8):
            if (x := str(number)) in interval:
                try:
                    r = Numerus.encode_roman_numeral(number)
                except ValueError as e:
                    raise ArgumentError(
                        f"Unable to parse number: {number}") from e
                roman_interval: str = interval.replace(x, r)
                roman_intervals.append(roman_interval)
    return tuple(roman_intervals)


def is_enharmonically_natural(name_idx: int, accidentals: int) -> bool:
    '''
    Test whether a note is equivalent to a natural note name, considering 
    the enharmonic equivalence of any accidentals.

    Parameters
    ----------
    note_name : str
        Any note name.

    Returns
    -------
    bool
        True, if the note is enharmonically equivalent to a natural.

    Examples
    --------
    >>> is_enharmonically_natural(2, 1)
    True
    >>> is_enharmonically_natural(1, 1)
    False
    '''
    name_idx, accidentals = simplify_note_name(name_idx, accidentals)
    return accidentals == 0


def simplify_note_name(name_idx: int, accidentals: int) -> tuple[int, int]:
    '''
    Take a note name that has accidentals and return the simplest 
    enharmonically-equivalent name. 

    Parameters
    ----------
    name_idx : int
        The index of the note name.
    accidentals : int
        The number of accidentals in the note.

    Returns
    -------
    tuple[int, int]
        A tuple with the index of the new name and new accidentals (0 or 1).

    Examples
    --------
    >>> simplify_note_name(2, 4)
    (4, 1)
    >>> simplify_note_name(3, 4)
    (5, 0)
    >>> simplify_note_name(6, 4)
    (1, 1)
    '''
    if accidentals == 0:
        return name_idx, accidentals
    value = (HEPTATONIC_SCALES[DIATONIC][name_idx] + accidentals) % TONES
    if value in HEPTATONIC_SCALES[DIATONIC]:
        return HEPTATONIC_SCALES[DIATONIC].index(value), 0
    if accidentals > 1:
        value -= 1
        return HEPTATONIC_SCALES[DIATONIC].index(value), 1
    value += 1
    return HEPTATONIC_SCALES[DIATONIC].index(value), -1


def rotate_interval_structure(interval_structure: Sequence[int], mode_idx: int) -> tuple[int, ...]:
    '''
    Rotate an interval structure so as to rephrase the intervals from the
    perspective of the new modal starting index.

    Parameters
    ----------
    interval_structure : Sequence[int]
        A sequence of integers representing intervals in semitones.
    mode_idx : int
        The index that will serve as the new '0' of the resulting scale form.

    Returns
    -------
    tuple[int, ...]
        A tuple of integers representing the original scale pattern from 
        the new modal perspective.

    Example
    -------
    >>> rotate_interval_structure([0, 2, 4, 5, 7, 9, 11], 2)
    (0, 1, 3, 5, 7, 8, 10)
    '''
    modal_semitones_offset = interval_structure[mode_idx]
    pitches: list[int] = []
    for i in range(len(interval_structure)):
        new_note_idx = (i + mode_idx) % len(interval_structure)
        original_value = interval_structure[new_note_idx]
        tones_offset = ((i + mode_idx) // len(interval_structure)) * TONES
        new_value = original_value - modal_semitones_offset + tones_offset
        pitches.append(new_value)
    return tuple(pitches)


def get_heptatonic_double_octave(
        interval_structure: Sequence[int]
) -> tuple[int, ...]:
    '''
    Extend the range of a scale pattern to two octaves.

    Parameters
    ----------
    interval_structure : Sequence[int]
        An array of integers representing the intervals of a heptatonic scale.

    Returns
    -------
    tuple[int, ...]
        An array with the original intervals, plus the same intervals an 
        octave higher.

    Example
    -------
    >>> get_heptatonic_double_octave([0, 2, 4, 5, 7, 9, 11])
    (0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23)
    '''
    double_octave = list(interval_structure)
    for i in range(NOTES):
        double_octave.append(interval_structure[i] + 12)
    return tuple(double_octave)


def chordify_heptatonic_tertial(
        parent_structure: Sequence[int],
        keynote: tuple[int, int],
        number_of_notes: int
) -> tuple[ChordData, ...]:
    '''
    Create a tertial chord scale with the given parameters.

    Parameters
    ----------
    parent_structure : Sequence[int]
        A list of intervals representing the scale from which the chords
        will be derived.
    keynote : tuple[int, int]
        A pair containing 1) the index of the alphabetic keynote and 2) the
        number of accidentals (+/-) of the keynote.
    number_of_notes : int
        How many notes to take in sequence.

    Returns
    -------
    tuple[ChordData, ...]
        A tuple of ChordData representing the requested chord scale.
    '''
    if number_of_notes > 7:
        raise ArgumentError("Chords can be generated with a maximum of 7 notes.")
    chords: list[ChordData] = []
    note_names = get_heptatonic_scale_notes(parent_structure, *keynote)

    for i in range(NOTES):
        root = note_names[i]
        chord_interval_structure = rotate_interval_structure(
            parent_structure, i)
        root_data = decode_note_name(root)
        modal_names = get_heptatonic_scale_notes(
            chord_interval_structure, *root_data)
        interval_symbols = get_heptatonic_interval_symbols(
            chord_interval_structure)
        if number_of_notes > 4:
            modal_names += modal_names
            interval_symbols = get_heptatonic_interval_symbols(
                chord_interval_structure, True)
            chord_interval_structure = get_heptatonic_double_octave(
                chord_interval_structure)

        chords.append(
            ChordData(
                modal_names[::2][:number_of_notes],
                interval_symbols[::2][:number_of_notes],
                chord_interval_structure[::2][:number_of_notes]
            )
        )
    return tuple(chords)


def chordify_heptatonic_sus(
        parent_structure: Sequence[int], 
        keynote: tuple[int, int], 
        number_of_notes: int,
        sus: int
        ) -> tuple[ChordData, ...]:
    if number_of_notes > 7:
        raise ArgumentError("Chords can be generated with a maximum of 7 notes.")
    if not sus in (2, 4):
        raise ArgumentError(f"Unknown sus note (={sus})")
    
    chords: list[ChordData] = []
    note_names = get_heptatonic_scale_notes(parent_structure, *keynote)
    if sus == 2:
        pattern = [0, 1, 4, 6, 8, 10, 12]
    else:
        pattern = [0, 3, 4, 6, 8, 10, 12]

    for i in range(NOTES):
        root = note_names[i]
        chord_interval_structure = rotate_interval_structure(
            parent_structure, i)
        root_data = decode_note_name(root)
        modal_names = get_heptatonic_scale_notes(
            chord_interval_structure, *root_data)
        interval_symbols = get_heptatonic_interval_symbols(
            chord_interval_structure)
        if number_of_notes > 4:
            modal_names += modal_names
            interval_symbols = get_heptatonic_interval_symbols(
                chord_interval_structure, True)
            chord_interval_structure = get_heptatonic_double_octave(
                chord_interval_structure)

        ch_names = [modal_names[i] for i in pattern][:number_of_notes]
        ch_symbols = [interval_symbols[i] for i in pattern][:number_of_notes]
        ch_structure = [chord_interval_structure[i] for i in pattern][:number_of_notes]
        chords.append(ChordData(ch_names, ch_symbols, ch_structure))
    return tuple(chords)

def drop_voicing(chord_data: ChordData, drop_notes: Sequence[int]) -> ChordData:
    '''
    Create a drop voicing for the given chord.

    Parameters
    ----------
    chord_data : ChordData
        The chord that will be modified.
    drop_notes : Sequence[int]
        The indices of the intervals to be modified. These are actually
        raised rather than dropped, in order that the new voicing will have
        the same inversion as the old one.
        E.g. (0, 4, 7, 11), [1] -> (0, 7, 11, 16)
             (C, E, G, B),  [1] -> (C, G, B, E)
        The indicies are not the same as the 'drop' notes, so this function
        should be used with the provided constants (DROP_2_VOICING &c.).

    Returns
    -------
    ChordData
        A chord with the original intervals modified according to the given

    Raises
    ------
    ArgumentError
        If one of the drop notes is already the bass (= 0). We do this to 
        ensure that the output is in the same inversion as the input.

    Examples
    --------
    >>> from src.structures import ChordData
    >>> from src.constants import DROP_2_VOICING, DROP_2_AND_4_VOICING, DROP_3_VOICING, DROP_2_AND_3_VOICING
    >>> x = ChordData(['C', 'E', 'G', 'B'], ["1", "3", "5", "7"], [1, 4, 7, 11])
    >>> drop_voicing(x, DROP_2_VOICING)
    ChordData(note_names=('C', 'G', 'B', 'E'), interval_symbols=('1', '5', '7', '3'), interval_structure=(1, 7, 11, 16))
    >>> drop_voicing(x, DROP_3_VOICING)
    ChordData(note_names=('C', 'B', 'E', 'G'), interval_symbols=('1', '7', '3', '5'), interval_structure=(1, 11, 16, 19))
    >>> drop_voicing(x, DROP_2_AND_4_VOICING)
    ChordData(note_names=('C', 'G', 'E', 'B'), interval_symbols=('1', '5', '3', '7'), interval_structure=(1, 7, 16, 23))
    >>> drop_voicing(x, DROP_2_AND_3_VOICING)
    ChordData(note_names=('C', 'E', 'B', 'G'), interval_symbols=('1', '3', '7', '5'), interval_structure=(1, 4, 11, 19))
    '''
    interval_structure = list(chord_data.interval_structure)
    note_names = list(chord_data.note_names)
    interval_symbols = list(chord_data.interval_symbols)
    for i in drop_notes:
        if i == 0:
            raise ArgumentError("Interval 0 cannot be modified.")
        interval = chord_data.interval_structure[i]
        interval_structure.remove(interval)
        interval_structure.append(interval + TONES)
        name = chord_data.note_names[i]
        note_names.remove(name)
        note_names.append(name)
        symbol = chord_data.interval_symbols[i]
        interval_symbols.remove(symbol)
        interval_symbols.append(symbol)

    return ChordData(note_names=tuple(note_names),
                     interval_symbols=tuple(interval_symbols),
                     interval_structure=tuple(interval_structure))


def order_interval_names(interval_names: Iterable[str]) -> tuple[str, ...]:
    '''Take an unordered iterable of interval names and order them according
    to their numerical digit.

    Examples
    --------
    >>> order_interval_names(["1", "b5", "7", "b3"])
    ('1', 'b3', 'b5', '7')
    >>> order_interval_names(["b7", "1", "5", "#11", "3"])
    ('1', '3', '5', 'b7', '#11')
    '''
    def extract_digit(name: str) -> int:
        digit = ''
        for char in name:
            if char.isdigit():
                digit += char
        return int(digit)
    return tuple(sorted(interval_names, key=extract_digit))


def name_chord(
    interval_names: Sequence[str],
    maj_symbol: str = CHORD_MAJ,
    min_symbol: str = CHORD_MIN,
    dim_symbol: str = CHORD_DIM
) -> str:
    '''
    Parse a list of interval names into a chord symbol.

    Major, minor, and diminished chords can have customizable symbols, so
    you could have e.g. 'maj', or 'M', or 'Δ', etc. according to preference.

    Half-diminished, augmented, and other types of altered chords are
    simply spelled with an explicit alteration, e.g. min7b5, 7#5, maj7#5,
    so they cannot be customized.

    Sus chords are always 'sus', so they cannot be customized.

    Parameters
    ----------
    interval_names: Sequence[str]
        The interval names you want to parse as a chord.
    maj_symbol : str, optional
        What symbol will represent major chords, by default "maj"
    min_symbol : str, optional
        What symbol will represent minor chords, by default "min"
    dim_symbol : str, optional
        What symbol will represent diminished chords, by default "dim"

    Examples
    --------
    >>> name_chord(["1","3","5"])
    'maj'
    >>> name_chord(["1","3","5", "7"])
    'maj7'
    >>> name_chord(["1","3","5", "7", "9"])
    'maj9'
    >>> name_chord(["1","3","5", "9"])
    'majadd9'
    >>> name_chord(["1","3","5", "7", "9", "11"])
    'maj11'
    >>> name_chord(["1","3","5", "7", "9", "11", "13"])
    'maj13'
    >>> name_chord(["1","3","5","7", "11"])
    'maj7add11'
    >>> name_chord(["1","3","5","7","9", "13"])
    'maj9add13'
    >>> name_chord(["1","3","5", "b7"])
    '7'
    >>> name_chord(["1","3","5", "b7", "9"])
    '9'
    >>> name_chord(["1","3","5", "b7", "9", "13"])
    '9add13'
    >>> name_chord(["1","b3","5"])
    'min'
    >>> name_chord(["1","b3","5", "b7", "9"])
    'min9'
    >>> name_chord(["1","b3","5", "9"])
    'minadd9'
    >>> name_chord(["1","b3","5", "7"])
    'minmaj7'
    >>> name_chord(["1","b3","5", "7", "9"])
    'minmaj9'
    >>> name_chord(["1","b3","5", "7", "11"])
    'minmaj7add11'
    >>> name_chord(["1","b3","5", "7", "9", "11", "13"])
    'minmaj13'
    >>> name_chord(["1","b3","b5", "b7"])
    'min7b5'
    >>> name_chord(["1","b3","b5", "b7", "9"])
    'min9b5'
    >>> name_chord(["1","b3","b5", "b7", "9", "11", "13"])
    'min13b5'
    >>> name_chord(["1","b3","b5", "bb7"])
    'dim7'
    >>> name_chord(["1","b3","b5", "bb7", "9"])
    'dim9'
    >>> name_chord(["1","b3","b5", "bb7", "9", "11"])
    'dim11'
    >>> name_chord(["1","3","7","9"])
    'maj9no5'
    >>> name_chord(["1","2","5"])
    'sus2'
    >>> name_chord(["1","bb3","5"])
    'susbb3'
    >>> name_chord(["1","#3","5"])
    'sus#3'
    >>> name_chord(["1","4","5"])
    'sus4'
    >>> name_chord(["1","2","5", "7"])
    'maj7sus2'
    >>> name_chord(["1","2","5", "b7"])
    '7sus2'
    >>> name_chord(["1","2","5", "bb7"])
    'sus2bb7'
    >>> name_chord(["1","3","5", "bb7"])
    'majbb7'
    >>> name_chord(["1","bb3","#5","7"])
    'maj7susbb3#5'
    >>> name_chord(["1","bb3","b5","bb7","9"])
    'susbb3b5bb7add9'
    >>> name_chord(["1", "5","bb7","9"])
    'no3bb7add9'
    '''
    DIM7 = [CHORD_FLAT_3, CHORD_FLAT_5, CHORD_DOUBLE_FLAT_7]
    DOM7 = [CHORD_3, CHORD_FLAT_7]
    EXTENSIONS = [CHORD_9, CHORD_11, CHORD_13]

    parse = set(interval_names)

    # A chord symbol is made up of a series of suffixes, each of which
    # implies something about the chord's structure. Not all suffixes
    # will be present (and in fact cannot all be present simultaneously).
    # They have been ordered with a view to making the resulting symbols
    # easier to read, including a few unusual chord structures implied
    # in some of the more exotic parent scales.
    normal3: str = ""
    primary: str = ""
    secondary: str = ""
    sus: str = ""
    alt5: str = ""
    alt7: str = ""
    add: str = ""
    no5: str = ""
    no3: str = ""
    extensions: str = ""

    # Any note that has been accounted for by the parsing process is
    # discarded so it can't be misinterpreted later.
    parse.discard(str(1))

    # Convenience functions
    def has_third() -> Optional[str]:
        for x in [CHORD_3, CHORD_FLAT_3]:
            if x in interval_names:
                return x
        return None

    def has_p5() -> Optional[str]:
        if CHORD_5 in interval_names:
            return CHORD_5
        return None

    def has_alt5() -> Optional[str]:
        for x in [CHORD_FLAT_5, CHORD_SHARP_5]:
            if x in interval_names:
                return x
        return None

    def is_dim() -> bool:
        return set(DIM7).issubset(interval_names)

    def is_dom() -> bool:
        return set(DOM7).issubset(interval_names)

    def has_sus() -> Optional[tuple[str, ...]]:
        candidates: list[str] = []
        for x in [CHORD_SHARP_3, CHORD_2, CHORD_DOUBLE_FLAT_3, CHORD_4]:
            if x in interval_names:
                candidates.append(x)
        if candidates:
            return tuple(candidates)
        return None

    # Pre-handle special cases.
    # Diminished chord implies specific structure.
    if is_dim():
        normal3 = dim_symbol
        primary = CHORD_7
        parse.difference_update(set(DIM7))
    else:
        # Exotic chords are allowed to have bb7 in our system, but since the
        # bb accidental might conflict with the note name in a 7th chord
        # (e.g. 'Bbb7'), we compel it to take the alt7 slot instead of the
        # primary 7 slot.
        if CHORD_DOUBLE_FLAT_7 in parse:
            alt7 = CHORD_DOUBLE_FLAT_7
            parse.discard(CHORD_DOUBLE_FLAT_7)
        # A chord with an altered 5th must always have an explicit alt5 symbol,
        # unless it's diminished.
        if (n := has_alt5()):
            alt5 = n
            parse.discard(n)
        # A chord with no 5th must have an explicit no5 symbol, unless it's
        # diminished.
        elif not has_p5():
            no5 = CHORD_NO + CHORD_5
        else:
            # The fifth is implied in any other chord and has no symbol.
            parse.discard(CHORD_5)
    # Dominant chord implies specific structure.
    if is_dom():
        primary = CHORD_7
        parse.difference_update(set(DOM7))

    # Main chord parsing is mostly a 1:1 symbol matching, with a few
    # exceptions.
    # Chords in our system are always given an explicit symbol for
    # their third, unless they are one of the implicit symbols
    # above, or they have a suspension in place of a third.
    if (n := has_third()):
        if is_dim() or is_dom():
            pass
        elif n == CHORD_3:
            normal3 = maj_symbol
            # A 7 symbol in a major chord implies a natural 7
            if CHORD_7 in parse:
                primary = CHORD_7
                parse.discard(CHORD_7)
        elif n == CHORD_FLAT_3:
            normal3 = min_symbol
            # A 7 symbol in most chords implies a flat 7, so
            # the natural 7 requires a special symbol.
            if CHORD_7 in parse:
                parse.discard(CHORD_7)
                primary = maj_symbol + CHORD_7
            if CHORD_FLAT_7 in parse:
                parse.discard(CHORD_FLAT_7)
                primary = CHORD_7
        parse.discard(n)
    # Our system allows for sus chords with notes that could technically be
    # considered thirds. We categorize #3 and bb3 as 'sus' chords a) because
    # they cannot reasonably be labeled major or minor, b) so that their
    # accidental cannot stand next to the root note (i.e. Dsusbb3 is less
    # ambiguous than Dbb3).
    elif (candidates := has_sus()):
        # Normally, we expect to have only one medial note (a third or a
        # suspended note). If there's more than one note that could stand
        # as a suspension, treat the first as a suspension, and any others
        # as additions (e.g. 1, 2, 4, 5 -> sus2add4).
        candidates = list(candidates)
        main = candidates.pop(0)
        sus = CHORD_SUS + main
        parse.discard(main)
        for x in candidates:
            if x:
                add += CHORD_ADD + x
                parse.discard(x)
        if CHORD_7 in parse:
            parse.discard(CHORD_7)
            primary = maj_symbol + CHORD_7
        elif CHORD_FLAT_7 in parse:
            parse.discard(CHORD_FLAT_7)
            primary = CHORD_7
    # Any chord without a medial must have an explicit no3 symbol
    else:
        no3 = CHORD_NO + CHORD_3

    # Our system treats primary extension symbols as implying all previous
    # extensions in the series, i.e. a 13 chord includes 7, 9, 11, 13.
    # If this series is interrupted by a missing or altered note, then the
    # primary extension is the last continuous extension, and any following
    # natural extensions are treated as additions (e.g. C9#11add13).
    largest: str = ""
    if primary:
        checked: list[str] = []
        for i, extension in enumerate(EXTENSIONS):
            prev = EXTENSIONS[i - 1] if i > 0 else None
            if extension in parse:
                if not prev or prev in checked:
                    largest = extension
                    parse.discard(extension)
                    checked.append(extension)
                else:
                    add += CHORD_ADD + extension
                    parse.discard(extension)
                    checked.append(extension)
        if largest:
            primary = primary.replace(CHORD_7, largest)

    # The secondary suffix does not imlicitly absorb any other intervals,
    # so that 1, 3, 5, 6, 9, 11, 13 -> maj6add9add11add13
    if CHORD_6 in parse:
        secondary = CHORD_6
        parse.discard(CHORD_6)

    # If the primary suffix already exists, treat the 6 as an addition.
    if secondary and primary:
        add += CHORD_ADD + secondary
        secondary = ""

    # Any extension with an accidental can simply be suffixed on its own.
    # Natural extensions may encounter ambiguities and must be treated as
    # additions (e.g. Emaj#11 vs Emajadd11)
    for extension in list(parse):
        if not any([SHARP_SYMBOL in extension, FLAT_SYMBOL in extension]):
            add += CHORD_ADD + extension
            parse.discard(extension)

    # By this point, the list of intervals only contains non-chord tone
    # extensions with accidentals.
    extensions = "".join(parse)

    # Most suffixes will be empty strings in any given chord.
    symbols: list[str] = [
        normal3,
        primary,
        secondary,
        sus,
        no3,
        no5,
        alt5,
        alt7,
        extensions,
        add
    ]
    final_form = "".join(symbols)
    return final_form


def name_intervals(chord_symbol: str) -> tuple[str, ...]:
    '''
    Parse a chord symbol into a list of interval names.

    Parameters
    ----------
    chord_symbol : str
        The chord symbol you want to parse. Most common symbols should be
        recognized.

    Returns
    -------
    tuple[str, ...]
        A tuple of interval names implied in the chord symbol.

    Raises
    ------
    ArgumentError
        If the chord symbol contains an illegal character/configuration.

    Examples
    --------
    >>> name_intervals('C')          
    ('1', '3', '5')
    >>> name_intervals('Cmaj7')
    ('1', '3', '5', '7')
    >>> name_intervals('CM7')   
    ('1', '3', '5', '7')
    >>> name_intervals('Cm7') 
    ('1', 'b3', '5', 'b7')
    >>> name_intervals('Cmin7') 
    ('1', 'b3', '5', 'b7')
    >>> name_intervals('Cmin11') 
    ('1', 'b3', '5', 'b7', '9', '11')
    >>> name_intervals('Cmin11b5') 
    ('1', 'b3', 'b5', 'b7', '9', '11')
    >>> name_intervals('C7aug')    
    ('1', '3', '#5', 'b7')
    >>> name_intervals('Caug7')
    ('1', '3', '#5', 'b7')
    >>> name_intervals('C+7')
    ('1', '3', '#5', 'b7')
    >>> name_intervals('C7+')
    ('1', '3', '#5', 'b7')
    >>> name_intervals('Cdim11nobb7')
    ('1', 'b3', 'b5', '9', '11')
    >>> name_intervals('Cmin11b5')    
    ('1', 'b3', 'b5', 'b7', '9', '11')
    >>> name_intervals('Co7')      
    ('1', 'b3', 'b5', 'bb7')
    >>> name_intervals('Cmin7b5add11') 
    ('1', 'b3', 'b5', 'b7', '11')
    >>> name_intervals('Cminmaj7')     
    ('1', 'b3', '5', '7')
    >>> name_intervals('CminM7')   
    ('1', 'b3', '5', '7')
    >>> name_intervals('CmM7')   
    ('1', 'b3', '5', '7')
    >>> name_intervals('Cmaj7sus2')
    ('1', '2', '5', '7')
    >>> name_intervals('Csus4') 
    ('1', '4', '5')
    >>> name_intervals('Csus2')
    ('1', '2', '5')
    >>> name_intervals('C7sus4') 
    ('1', '4', '5', 'b7')
    >>> name_intervals('Csusbb3bb7') 
    ('1', 'bb3', '5', 'bb7')
    '''
    intervals: set[str] = {str(1), CHORD_5}
    # Regex sorts elements into three broad categories. The main symbol
    # generally defines the third and may imply something about the 7.
    # The extension is the 7th or any natural note that is allowed to replace
    # The modification is any other interval symbol, or an add, or a no.
    match = re.search(RE_PARSE_CHORD_SYMBOL, chord_symbol)
    if match is None:
        raise ArgumentError(f"Unable to parse chord symbol: {chord_symbol}")

    main = match.group(MAIN)
    extension = match.group(EXTENSION)
    modifications = match.group(MODIFICATION)
    ext_series: list[str] = [CHORD_7, CHORD_9, CHORD_11, CHORD_13]
    sus_intervals: list[str] = [
        CHORD_DOUBLE_FLAT_3, CHORD_SHARP_3, CHORD_4, CHORD_2]

    # 'C', 'A', 'F#'
    if main is None:
        intervals.add(CHORD_3)
        # 'C7', 'A11', 'F#13'
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                if interval == CHORD_7:
                    interval = CHORD_FLAT_7
                intervals.add(interval)
            extension = None

    # 'Cmaj', 'AM', 'F#Δ'
    elif main in CHORD_MAJOR_SYMBOLS:
        intervals.add(CHORD_3)
        # 'Cmaj7', 'AM7', 'F#Δ7'
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                intervals.add(interval)
            extension = None

    # 'Cdim', 'Ao'
    elif main in CHORD_DIM_SYMBOLS:
        intervals.add(CHORD_FLAT_3)
        intervals.add(CHORD_FLAT_5)
        intervals.discard(CHORD_5)
        # 'Cdim7', 'Ao9'
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                if interval == CHORD_7:
                    interval = CHORD_DOUBLE_FLAT_7
                intervals.add(interval)
            extension = None

    # 'Caug', 'A+'
    elif main in CHORD_AUGMENTED_SYMBOLS:
        intervals.add(CHORD_3)
        intervals.add(CHORD_SHARP_5)
        intervals.discard(CHORD_5)

    # 'Cø'
    elif main in CHORD_HALFDIM_SYMBOLS:
        intervals.add(CHORD_FLAT_3)
        intervals.add(CHORD_FLAT_5)
        intervals.discard(CHORD_5)

    # 'Cmin', 'Am', 'F#-'
    elif main in CHORD_MINOR_SYMBOLS:
        intervals.add(CHORD_FLAT_3)

    if extension:
        for symb in CHORD_MAJOR_SYMBOLS:
            if symb in extension:
                base = extension.replace(symb, '')
                if base in ext_series:
                    i = ext_series.index(base) + 1
                    for interval in ext_series[:i]:
                        intervals.add(interval)
        if extension in ext_series:
            i = ext_series.index(extension) + 1
            for interval in ext_series[:i]:
                if interval == CHORD_7:
                    interval = CHORD_FLAT_7
                intervals.add(interval)

    # Check modifications
    sub: list[str] = []
    # Special chords in our system might have sus bb3, #3.
    for sus in sus_intervals:
        if (n := CHORD_SUS + sus) in modifications:
            modifications.replace(n, '')
            intervals.add(sus)
            sub.extend([CHORD_3, CHORD_FLAT_3])

    # Special chords in our system might have bb7.
    if CHORD_DOUBLE_FLAT_7 in modifications:
        if (n := CHORD_NO + CHORD_DOUBLE_FLAT_7) in modifications:
            sub.append(CHORD_DOUBLE_FLAT_7)
            modifications.replace(n, '')
        else:
            if (n := CHORD_ADD + CHORD_DOUBLE_FLAT_7) in modifications:
                intervals.add(CHORD_DOUBLE_FLAT_7)
                modifications.replace(n, '')
            else:
                intervals.add(CHORD_DOUBLE_FLAT_7)
                modifications.replace(CHORD_DOUBLE_FLAT_7, '')

    # Most remaining symbols will be a bare interval name, an addition, or
    # a subtraction.
    for number in (13, 11, 9, 6, 5, 4, 3, 2):
        for accidental in [SHARP_SYMBOL, FLAT_SYMBOL, '']:
            interval = accidental + str(number)
            if (n := CHORD_ADD + interval) in modifications:
                intervals.add(interval)
                modifications = modifications.replace(n, '')
            if (n := CHORD_NO + interval) in modifications:
                sub.append(interval)
                modifications = modifications.replace(n, '')
            if interval in modifications:
                intervals.add(interval)
                modifications = modifications.replace(interval, '')
                if interval in [CHORD_SHARP_5, CHORD_FLAT_5]:
                    intervals.remove(CHORD_5)

    # Augmented symbols are either main or modification, e.g. Caug7 vs. C7aug
    for aug in CHORD_AUGMENTED_SYMBOLS:
        if aug in modifications:
            intervals.discard(CHORD_5)
            intervals.add(CHORD_SHARP_5)

    # Subtractions always treated last, in case they depend on an implication
    # in a preceding symbol.
    for s in sub:
        if s in intervals:
            intervals.remove(s)

    return order_interval_names(intervals)


def get_binomial(keynote: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    '''Take a tuple representing a note value that has another name and return
    a tuple of tuples with both variants.

    Examples
    --------
    >>> get_binomial((0, 1))
    ((0, 1), (1, -1))
    >>> get_binomial((1, 1))
    ((1, 1), (2, -1))
    >>> get_binomial((4, -1))
    ((4, -1), (3, 1))
    '''
    if is_enharmonically_natural(*keynote):
        raise ArgumentError(
            f"This function is only intended for accidental note names (keynote={keynote})")
    accidentals = keynote[1]
    alpha = keynote[0]
    if accidentals == 1:
        alpha += 1
        accidentals = -1
    elif accidentals == -1:
        alpha -= 1
        accidentals = 1
    return keynote, (alpha, accidentals)


def best_heptatonic_spelling(keynote: str, scale: Sequence[int]) -> tuple[str, ...]:
    '''
    Choose the best set of alphabetic note names for a given heptatonic scale
    and keynote. 

    Parameters
    ----------
    keynote : str
        An alphabetic keynote (not a Roman numeral).
    scale : Sequence[int]
        A collection of integers representing the intervals of a heptatonic
        scale.

    Returns
    -------
    tuple[str, ...]
        A collection of the optimal note names for this scale and keynote.

    Examples
    --------
    >>> best_heptatonic_spelling('A#', [0, 2, 4, 5, 7, 9, 11])
    ('Bb', 'C', 'D', 'Eb', 'F', 'G', 'A')
    '''
    if not structure_is_heptatonic(scale):
        raise ArgumentError(
            'This function is intended only for heptatonic scale forms.')

    note = simplify_note_name(*decode_note_name(keynote))
    # Naturals' default name is always the best.
    if is_enharmonically_natural(*note):
        return get_heptatonic_scale_notes(scale, *note)

    # Check both spelling variants of a binomial (black key) note.
    k1, k2 = get_binomial(note)
    s1 = get_heptatonic_scale_notes(scale, *k1)
    s2 = get_heptatonic_scale_notes(scale, *k2)
    s1_s, s1_f = 0, 0
    s2_s, s2_f = 0, 0
    for n in s1:
        if SHARP_SYMBOL in n:
            s1_s += n.count(SHARP_SYMBOL)
        if FLAT_SYMBOL in n:
            s1_f += n.count(FLAT_SYMBOL)
    for n in s2:
        if SHARP_SYMBOL in n:
            s2_s += n.count(SHARP_SYMBOL)
        if FLAT_SYMBOL in n:
            s2_f += n.count(FLAT_SYMBOL)
    t1 = s1_s + s1_f
    t2 = s2_s + s2_f
    # Best key is usually as simple as fewest total accidentals.
    if t1 < t2:
        return s1
    if t2 < t1:
        return s2
    # If the accidentals are equal, the best key is the one that does not
    # mix sharps and flats.
    if t1 == t2:
        m1 = s1_s > 0 and s1_f > 0
        m2 = s2_s > 0 and s2_f > 0
        if m1 and not m2:
            return s2
        if m2 and not m1:
            return s1

    # If both keys have the same number of sharps and flats, and they both
    # mix both types of accidentals, fall back arbitrarily to sharps.
    if SHARP_SYMBOL in encode_note_name(*k1):
        return s1
    return s2


def rotate_chord(chord: ChordData, new_bass_idx: int) -> ChordData:
    '''
    Rotate the elements in a chord so that it has a new starting point.

    Parameters
    ----------
    chord : ChordData
        A collection of chord information.
    new_bass_idx : int
        The index that will be first in the rotated form.

    Returns
    -------
    ChordData
        The input chord information, but rotated so that the elements at
        the given index are now first.

    Examples
    --------
    >>> rotate_chord(ChordData(['C', 'E', 'G'], ['1', '3', '5'], [0, 4, 7]), 1)
    ChordData(note_names=['E', 'G', 'C'], interval_symbols=['3', '5', '1'], interval_structure=(0, 3, 8))
    >>> rotate_chord(ChordData(['C', 'E', 'G'], ['1', '3', '5'], [0, 4, 7]), 2)
    ChordData(note_names=['G', 'C', 'E'], interval_symbols=['5', '1', '3'], interval_structure=(0, 5, 9))
    '''
    if not new_bass_idx in range(len(chord.interval_structure)):
        new_bass_idx %= len(chord.interval_structure)
    names = list(chord.note_names[new_bass_idx:]) + \
        list(chord.note_names[:new_bass_idx])
    symbols = list(chord.interval_symbols[new_bass_idx:]) + \
        list(chord.interval_symbols[:new_bass_idx])
    intervals = rotate_interval_structure(
        chord.interval_structure, new_bass_idx)
    return ChordData(names, symbols, intervals)

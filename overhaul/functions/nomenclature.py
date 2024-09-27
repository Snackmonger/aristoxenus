import csv
import pathlib
import re
from typing import Sequence

from overhaul.data.constants import (
    HEPTATONIC_SCALES,
    NATURAL_NAMES,
    RE_SPLIT_NOTE_NAME,
    NOTES,
    TONES,
    DIATONIC
)
from overhaul.data import errors
__parent_dir__ = str(pathlib.Path(__file__).resolve().parents[1])


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
    >>> names_are_heptatonic(["C#", "D#", "E#", "F#", "G#", "A#", "B#"])
    True
    >>> names_are_heptatonic(["C#", "D#", "E#", "F", "G#", "A#", "B#"])
    False
    >>> names_are_heptatonic(["C", "D#", "E", "F", "G", "Ab", "Bb"])
    True
    >>> names_are_heptatonic(["C", "D#", "Eb", "F", "G", "Ab", "Bb"])
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
    return len(set(interval_structure)) == 7


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
    Take a note name and return a tuple of the index of the alphabetic base in
    the naturals, plus the number of accidentals attached to the base.

    Parameters
    ----------
    note_name : str
        A note name with any number of accidentals.

    Returns
    -------
    tuple[int, int]
        The index of the alphabetic base, plus the number of accidentals 
        in the note name (a negative number represents flats).

    Raises
    ------
    UnknownSymbolError
        If the note name does not conform to the expected format (e.g. begins
        with an unrecognizable root).

    Example
    -------
    >>> decode_note_name("B#")
    (6, 1)
    >>> decode_note_name("C")
    (0, 0)
    >>> decode_note_name("D#")
    (1, 1)
    >>> decode_note_name("Eb")
    (2, -1)
    >>> decode_note_name("E####")
    (2, 4)
    '''
    name = re.match(RE_SPLIT_NOTE_NAME, note_name)
    if name:
        name = name.groupdict()
        accidentals: int = name["accidentals"].count(
            "#") - name["accidentals"].count("b")
        return NATURAL_NAMES.index(name["note_name"]), accidentals
    raise errors.UnknownSymbolError(f"Unknown note name symbol: {note_name}")


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
    '''
    if accidentals > 0:
        return '#' * (accidentals) + interval_name
    return 'b' * (-accidentals) + interval_name


def get_heptatonic_scale_notes(interval_structure: Sequence[int], root_note_idx: int, root_accidentals: int) -> tuple[str, ...]:
    '''
    Return the names for the given scale form, root note, and root accidentals.

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
    >>> get_heptatonic_interval_symbols([0, 1, 4, 5, 6, 8, 9], True)
    ('1', 'b2', '3', '4', 'b5', 'b6', 'bb7', '8', 'b9', '10', '11', 'b12', 'b13', 'bb14')
    '''
    if not structure_is_heptatonic(interval_structue):
        raise errors.HeptatonicScaleError
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


def encode_roman_numeral(indian_numeral: int) -> str:
    '''
    Convert an Indian numeral between 1 and 3,999 to a Roman numeral.

    Parameters
    ----------
    indian_numeral : int
        An integer between 1 and 3999.

    Returns
    -------
    str
        A string representing a Roman numeral.

    Raises
    ------
    errors.BadValueError
        If the number exceeds 3,999 in the Indian form.

    Examples
    --------
    >>> encode_roman_numeral(1449)
    'MCDXLIX'
    >>> encode_roman_numeral(1318)
    'MCCCXVIII'
    >>> encode_roman_numeral(959)
    'CMLIX'
    >>> encode_roman_numeral(263)
    'CCLXIII'
    '''
    if indian_numeral not in range(1, 4000):
        raise errors.BadValueError(indian_numeral)
    roman_numeral_: str = ''
    numerals: tuple[tuple[str, int], ...] = (('M', 1000),
                                             ('D', 500),
                                             ('C', 100),
                                             ('L', 50),
                                             ('X', 10),
                                             ('V', 5),
                                             ('I', 1))
    for numeral, value in numerals:
        while indian_numeral >= value:
            roman_numeral_ += numeral
            indian_numeral -= value
        for error, correction in {'IIII': 'IV',
                                  'VIV': 'IX',
                                  'XXXX': 'XL',
                                  'LXL': 'XC',
                                  'CCCC': 'CD',
                                  'DCD': 'CM'}.items():
            if error in roman_numeral_:
                roman_numeral_ = roman_numeral_.replace(error, correction)

    return roman_numeral_


def decode_roman_numeral(symbol: str) -> int:
    '''
    Convert a Roman numeral to an Indian numeral.

    Parameters
    ----------
    symbol : str
        A string representing a Roman numeral.

    Returns
    -------
    int
        An integer representing the given numeral.

    Examples
    --------
    >>> decode_roman_numeral('MCDXLIX')
    1449
    >>> decode_roman_numeral('MCCCXVIII')
    1318
    >>> decode_roman_numeral('CMLIX')
    959
    >>> decode_roman_numeral('CCLXIII')
    263
    '''
    numerals: tuple[tuple[str, int], ...] = (('M', 1000),
                                             ('D', 500),
                                             ('C', 100),
                                             ('L', 50),
                                             ('X', 10),
                                             ('V', 5),
                                             ('I', 1))
    values: list[int] = []
    for partial, value in {'IV': 4,
                           'IX': 9,
                           'XL': 40,
                           'XC': 90,
                           'CD': 400,
                           'CM': 900}.items():
        if partial in symbol:
            values.append(value)
            symbol = symbol.replace(partial, "")
    for numeral, value in numerals:
        if numeral in symbol:
            values.append(value*symbol.count(numeral))
    return sum(values)


def romanize_intervals(interval_names: Sequence[str] | str) -> tuple[str, ...]:
    '''
    Convert Indian numeral interval name(s) to use Roman numerals instead.

    Parameters
    ----------
    interval_names : Sequence[str] | str
        A string or array of strings representing interval symbols using Indian 
        numerals (e.g "b3").

    Returns
    -------
    tuple[str, ...]
        A tuple containing the same interval symbol(s) expressed using Roman 
        numerals (e.g. "bIII").

    Examples
    --------
    >>> romanize_intervals("b3")
    ('bIII',)
    >>> romanize_intervals(["#5", "b6"])
    ('#V', 'bVI')
    '''
    if isinstance(interval_names, str):
        interval_names = [interval_names]
    roman_intervals: list[str] = []
    for interval in interval_names:
        for number in range(1, 8):
            if (x := str(number)) in interval:
                roman_interval: str = interval.replace(
                    x, encode_roman_numeral(number))
                roman_intervals.append(roman_interval)
    return tuple(roman_intervals)


def encode_numeration(number: int, category: str) -> str:
    '''
    Encode a number as a keyword for the given category.

    Parameters
    ----------
    number : int
        The number to encode, between 1 and 15.
    category : str
        A category of numerical words, e.g. "ordinal", "cardinal".

    Returns
    -------
    str
        A string representing the number in the given category.

    Notes
    -----
    This function automatically adjusts the number if the category is "basal".
    The basal numbers are used as a list slice, and so are understood as 1 
    less than the name suggests etymologically (i.e. "tertial" = 2, so that 
    list[::2] can get every third note).

    Examples
    --------
    >>> encode_numeration(3, "polyad")
    'triad'
    >>> encode_numeration(2, "basal")
    'tertial'
    >>> encode_numeration(3, "cardinal")
    'three'
    >>> encode_numeration(3, "ordinal")
    'third'
    >>> encode_numeration(3, "uple")
    'triple'
    >>> encode_numeration(3, "tonal")
    'tritonic'
    >>> encode_numeration(5, "tonal")
    'pentatonic'
    >>> encode_numeration(7, "tonal")
    'heptatonic'
    '''
    file = "/data/numeration.csv"
    number = number if category == 'basal' else number - 1
    keyword = ""
    with open(__parent_dir__ + file, newline="", encoding="utf8") as numdata:
        reader = csv.DictReader(numdata)
        rows = list(reader)
        keyword = rows[number][category]
        numdata.close()
    return keyword


def decode_numeration(keyword: str) -> int:
    '''
    Decode a numeric keyword into the number it represents.

    Parameters
    ----------
    keyword : str
        A numeric keyword term, e.g. "tertial", "pentad".

    Returns
    -------
    int
        An integer between 1 and 15. If the keyword is a basal word, then its 
        number will be 1 lower than the name suggests. (This is so it can be 
        used to slice lists starting at 0)

    Raises
    ------
    errors.UnknownKeywordError
        If the term is not a known keyword.

    Notes
    -----
    This function automatically adjusts the number if the category is "basal".
    The basal numbers are used as a list slice, and so are returned 1 
    less than the name suggests etymologically (i.e. "tertial" = 2, so that 
    list[::2] can get every third note).

    Examples
    --------
    >>> decode_numeration("triad")
    3
    >>> decode_numeration("thirteenth")
    13
    >>> decode_numeration("sextuple")
    6
    >>> decode_numeration("tertial")
    2
    '''
    file = "/data/numeration.csv"
    with open(__parent_dir__ + file, newline="", encoding="utf8") as numdata:
        reader = csv.DictReader(numdata)
        for i, row in enumerate(reader):
            if keyword in row.values():
                if row["basal"] != keyword:
                    return i + 1
                return i
    raise errors.UnknownKeywordError(keyword)


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

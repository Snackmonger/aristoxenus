'''
This module contains functions that convert names in one format into a
different format.
'''

from typing import Iterable, Sequence

from aristoxenus.core.roman_numeral import encode_roman_numeral

from aristoxenus.core.annotations import (
    NoteNameData
)
from aristoxenus.core.constants import (
    EMPTY_STRING,
    FLAT_SYMBOL,
    NATURAL_NAMES,
    NOTE_NAME,
    NOTES,
    RELATIVE,
    ROMAN_NAME,
    SHARP_SYMBOL,
    TONES,
    ABSOLUTE,
    INTERVAL_NAME
)
from aristoxenus.core.heptatonic_spelling import get_heptatonic_note_names
from aristoxenus.core.interval import calculate_interval
from aristoxenus.core.errors import (
    StringValidationError
)
from aristoxenus.core.note_name import encode_note_name
from aristoxenus.core.validation import (
    validate_alphabetic_name,
    validate_interval_name,
    validate_roman_name
)


def convert_interval_names_to_roman_names(interval_names: Iterable[str] | str) -> tuple[str, ...]:
    '''
    Convert Indian numeral interval name(s) to Roman numeral interval name(s).

    Parameters
    ----------
    interval_names : Iterable[str] | str
        A string or array of strings representing interval symbols using Indian 
        numerals (e.g 'b3').

    Returns
    -------
    tuple[str, ...]
        A tuple containing the same interval symbol(s) expressed using Roman 
        numerals (e.g. 'bIII'). These numerals will always be uppercase.

    Raises
    ------
    StringValidationError
        If any of the interval names cannot be parsed.
    '''
    roman_intervals: list[str] = []
    if isinstance(interval_names, str):
        interval_names = [interval_names]
    for interval in interval_names:
        if not validate_interval_name(interval):
            raise StringValidationError(interval, INTERVAL_NAME)
        for number in range(1, 8):
            if (x := str(number)) in interval:
                r = encode_roman_numeral(number)
                roman_intervals.append(interval.replace(x, r))
    return tuple(roman_intervals)


def convert_roman_names_to_interval_names(roman_names: Iterable[str] | str) -> tuple[str, ...]:
    '''
    Convert Roman numeral interval name(s) to Indian numerals interval name(s).

    Parameters
    ----------
    roman_names : Iterable[str] | str
        A string or array of strings representing interval symbols using Roman
        numerals (e.g 'bIII', '#iv').

    Returns
    -------
    tuple[str, ...]
        A tuple containing the same interval symbol(s) expressed using Indian  
        numerals (e.g. 'b3').

    Raises
    ------
    StringValidationError
        If any of the Roman interval names cannot be parsed.
    '''
    indian_intervals: list[str] = []
    if isinstance(roman_names, str):
        roman_names = [roman_names]
    for roman_name in [x.lower() for x in roman_names]:
        if not validate_roman_name(roman_name):
            raise StringValidationError(roman_name, ROMAN_NAME)
        for number in reversed(range(1, 8)):
            numeral = (encode_roman_numeral(number).lower())
            base = (roman_name
                    .replace(SHARP_SYMBOL, EMPTY_STRING)
                    .replace(FLAT_SYMBOL, EMPTY_STRING))
            if base == numeral:
                n = str(number)
                indian_intervals.append(roman_name.replace(numeral, n))
                break
    return tuple(indian_intervals)


def convert_interval_names_to_note_names(root: NoteNameData, interval_names: Iterable[str] | str) -> tuple[str, ...]:
    '''
    Return the note names that correspond to the given interval symbols, from
    the perspective of the given root note name.

    Parameters
    ----------
    root : NoteData
        An alphabetic root note name.
    interval_symbols : Iterable[str]
        A collection of interval symbols.

    Returns
    -------
    tuple[str, ...]
        A collection of note names that represent the given intervals, from
        the perspective of the root note name.

    Raises
    ------
    StringValidationError
        If any of the interval names cannot be parsed.
    '''
    if isinstance(interval_names, str):
        interval_names = [interval_names]
    scale = get_heptatonic_note_names(root)
    start = scale.index(encode_note_name(root))
    sequence = scale[start:] + scale[:start]
    names: list[str] = []

    def __n(symbol: str) -> int:
        return int(''.join(c for c in symbol if c.isdigit()))
    for interval in interval_names:
        if not validate_interval_name(interval):
            raise StringValidationError(interval, INTERVAL_NAME)
        index = (__n(interval) % NOTES) - 1
        sh = SHARP_SYMBOL*interval.count(SHARP_SYMBOL)
        fl = FLAT_SYMBOL*interval.count(FLAT_SYMBOL)
        name = sequence[index] + sh + fl
        while True:
            if (s := SHARP_SYMBOL + FLAT_SYMBOL) in name:
                name = name.replace(s, '')
            elif (s := FLAT_SYMBOL + SHARP_SYMBOL) in name:
                name = name.replace(s, '')
            else:
                break
        names.append(name)
    return tuple(names)


def convert_interval_names_to_integers(interval_names: Sequence[str] | str) -> tuple[int, ...]:
    '''
    Turn interval names into their integer equivalents.

    This function operates with the assumptions that:

    1) the first interval will be considered the 'root'; if it is not 
    the tonic '1', then all other intervals will be recalculated to make it
    the tonic.
    2) each interval in sequence will be considered higher 
    than the one before it, so that '3', '5', '1', '3', '5' will be 
    represented as 0, 3, 10, 12, 15

    NOTE: Integers tell us the absolute values of intervals, but cannot 
    preserve the relative values of specific structures (e.g. a tritone is 6,
    but this could be expressed variously as different interval names like #4 
    or b5 or ##3 or bbb6, etc.). 

    Parameters
    ----------
    interval_names : Iterable[str] | str
        An interval name or collection of interval names.

    Returns
    -------
    tuple[int, ...]
        The integer representations of the given interval names.

    Raises
    ------
    StringValidationError
        If any of the interval names cannot be parsed.
    '''
    alpha: list[str] = []
    for interval in interval_names:
        digit = EMPTY_STRING.join(x for x in interval if x.isdigit())
        accidentals = interval.replace(digit, EMPTY_STRING)
        n = NATURAL_NAMES[(int(digit) - 1) % NOTES]
        alpha.append(n + accidentals)
    return convert_note_names_to_integers(alpha)


def convert_note_names_to_interval_names(note_names: Sequence[str]) -> tuple[str, ...]:
    '''
    Convert the given note names into relative interval names, assuming
    that the first note name in the collection is the keynote.

    # TODO: This func doesn't consider 9th, etc. Should it?

    Parameters
    ----------
    note_names : Sequence[str]
        A collection of note names.

    Returns
    -------
    tuple[str, ...]
        A collection of interval names representing the given note names.

    Raises
    ------
    StringValidationError
        If any of the note names cannot be parsed.
    '''
    root = note_names[0]
    if not validate_alphabetic_name(root):
        raise StringValidationError(root, NOTE_NAME)
    interval_names: list[str] = []
    for note_name in note_names:
        if not validate_alphabetic_name(note_name):
            raise StringValidationError(note_name, NOTE_NAME)
        interval_names.append(calculate_interval(root, note_name)[RELATIVE])
    return tuple(interval_names)


def convert_note_names_to_integers(note_names: Sequence[str]) -> tuple[int, ...]:
    '''
    Assess a sequence of note names, with the assumption that the first name
    is the unison, and every subsequent name must be higher than the one 
    preceding it (i.e. 'A', 'E', 'A', 'A' will be parsed as 0, 7, 12, 24).

    In order to get the notes as a single octave, simply apply modulus 12 
    to each integer.

    Parameters
    ----------
    note_names : Sequence[str]
        A sequence of note names that will be converted into integers.

    Returns
    -------
    tuple[int, ...]
        A tuple of integers representing the given note names.
    '''
    note_names = list(note_names)
    root = note_names.pop(0)
    intervals: list[int] = [0]
    modifier = 0
    highest = 0
    for name in note_names:
        interval = calculate_interval(root, name)[ABSOLUTE]
        if (highest >= interval + modifier):
            modifier += TONES
        interval += modifier
        highest = interval
        intervals.append(interval)
    return tuple(intervals)


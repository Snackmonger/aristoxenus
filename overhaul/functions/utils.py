from typing import Any, Sequence
from overhaul.data.constants import FREQUENCY_DECIMAL_LIMIT
from overhaul.data.constants import CENTRAL_REFERENCE_NOTE_FREQUENCY, OCTAVE_EQUIVALENCE_FACTOR, TONES


def rotate_array(array: Sequence[Any], new_first_idx: int) -> tuple[Any, ...]:
    '''
    Rotate a sequence of items so that the item at the given index is first
    in the new array.

    Parameters
    ----------
    array : Sequence[Any]
        An array of items.
    mode_idx : int
        The current index of the item that will be the new '0' index.

    Returns
    -------
    tuple[str, ...]
        A tuple of same items, but rotated so that the given index is now 
        first.
    '''
    new_array: list[Any] = []
    for i in range(len(array)):
        new_array.append(array[(i + new_first_idx) % len(array)])
    return tuple(new_array)


def order_interval_names(interval_names: Sequence[str]) -> tuple[str, ...]:
    '''
    Take an array of interval names and ensure that they follow the order
    of their numerals, regardless of the accidentals.

    Parameters
    ----------
    interval_names : Sequence[str]
        An array of strings representing interval symbols using Indian numerals 
        (e.g. "#4", 'b2', 'b7', '5').

    Returns
    -------
    tuple[str, ...]
        An array of the same, but ordered according to the numerals in the 
        strings.
    '''
    interval_names = list(interval_names)
    interval_names.sort(key=extract_number)
    return tuple(interval_names)


def extract_number(number_symbol: str) -> int:
    '''
    Take a string that contains numeric digits, and return an integer made 
    up of those digits. Intended for interval names, but can work with
    any string.

    Parameters
    ----------
    number_symbol : str
        A string containing numeric digits.

    Returns
    -------
    int
        An integer made up of all digits in sequence.

    Examples
    --------
    >>> extract_number("#11")
    11
    >>> extract_number("12oclockand54minutes")
    1254
    '''
    number = ""
    for char in number_symbol:
        if char.isdigit():
            number += char
    return int(number)


def calculate_frequency(semitones: int) -> float:
    '''
    Calculate the frequency that is the given number of semitones from the
    central starting frequency defined in the constants (by default 440).

    Parameters
    ----------
    semitones : int
        A +/- number of semitones away from the starting frequency.

    Returns
    -------
    float
        A frequency rounded to a number of decimal places defined in the 
        constants (by default 3 places)
    '''
    return round(CENTRAL_REFERENCE_NOTE_FREQUENCY * OCTAVE_EQUIVALENCE_FACTOR ** (semitones / TONES), FREQUENCY_DECIMAL_LIMIT)

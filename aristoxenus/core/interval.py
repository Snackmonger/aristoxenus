
from typing import Iterable

from aristoxenus.core.annotations import IntervalData
from aristoxenus.core.constants import (
    ACCIDENTALS, DIATONIC,
    EMPTY_STRING,
    FLAT_SYMBOL,
    HEPTATONIC_SCALES,
    NOTE_NAME_INDEX,
    NOTES,
    SHARP_SYMBOL,
    TONES
)
from aristoxenus.core.heptatonic_spelling import get_heptatonic_note_names
from aristoxenus.core.note_name import decode_note_name

__all__ = [
    "sort_interval_names",
    "calculate_formula",
    "calculate_interval",
    'get_double_octave'
]


def sort_interval_names(interval_names: Iterable[str]) -> tuple[str, ...]:
    '''Take an unordered iterable of interval names and order them according
    to their numerical digit.
    '''
    x = {
        "1": 0.0, 'b2': 0.11, '2': 0.12,
        'bb3': 0.13, '#2': 0.135, 'b3': 0.14,
        '3': 0.15, 'b4': 0.16, '#3': 0.17,
        '4': 0.18, 'bb5': 0.19, '#4': 0.2,
        'b5': 0.21, '5': 0.22, '#5': 0.23,
        'b6': 0.24, '##5': 0.25, '6': 0.26,
        'bb7': 0.27, '#6': 0.28, 'b7': 0.29,
        '7': 0.3, 'b9': 0.31, '9': 0.32,
        "#9": 0.33, '11': 0.34, '#11': 0.35,
        'b13': 0.36, '13': 0.37
    }
    # Not an elegant way to do it, but there aren't a huge number of
    # intervals we need to support, even with the very exotic scales,
    # and time is better spent elsewhere.
    return tuple(sorted(interval_names, key=lambda n: x[n]))


def calculate_interval(lower: str, higher: str) -> IntervalData:
    '''
    Describe the relationship between a lower note name and a higher 
    name. The output will respect the implicit enharmonic values of
    the input, so that e.g. #4 and b5 have the same integer value, but
    different interval names.

    Parameters
    ----------
    lower : str
        The name of the lower note in the interval.
    higher : str
        The name of the higher note in the interval.

    Returns
    -------
    IntervalData
        A pair consisting of the absolute integer value of the interval as 
        well as its name relative to the given lower note.
    '''
    low = decode_note_name(lower)
    high = decode_note_name(higher)
    diatonic_names = get_heptatonic_note_names(low)
    diatonic_pattern = HEPTATONIC_SCALES[DIATONIC]
    n = list(range(NOTES))
    order = n[low[NOTE_NAME_INDEX]:] + n[:low[NOTE_NAME_INDEX]]
    interval_base = order.index(high[NOTE_NAME_INDEX])
    diatonic_accidentals = decode_note_name(
        diatonic_names[interval_base])[ACCIDENTALS]
    actual_accidentals = high[ACCIDENTALS]

    accidentals = 0
    if diatonic_accidentals == actual_accidentals:
        accidentals = 0

    elif diatonic_accidentals == 0:
        accidentals = actual_accidentals

    elif diatonic_accidentals < 0:
        accidentals = -1 * diatonic_accidentals + actual_accidentals

    elif diatonic_accidentals > 0:
        accidentals = -1 * diatonic_accidentals + actual_accidentals

    sharps_flats = EMPTY_STRING
    if accidentals > 0:
        sharps_flats = SHARP_SYMBOL * accidentals
    elif accidentals < 0:
        sharps_flats = FLAT_SYMBOL * abs(accidentals)

    absolute_value = diatonic_pattern[interval_base] + accidentals
    if absolute_value > 11:
        absolute_value %= TONES
    if absolute_value < 0:
        absolute_value = TONES + absolute_value
    interval_name = sharps_flats + str(interval_base + 1)
    return IntervalData(absolute=absolute_value, relative=interval_name)


def calculate_formula(interval_structure: Iterable[int]) -> tuple[str, ...]:
    '''
    Calculate the semitone-tone step formula for the given interval structure.

    Parameters
    ----------
    interval_structure : Iterable[int]
        _description_

    Returns
    -------
    tuple[str, ...]
        _description_
    '''
    interval_structure = list(interval_structure) + [12]
    elements = {1: 'semitone', 2: 'tone', 3: 'hemiolion',
                4: 'ditone', 5: 'diatessaron', 6: 'tritone',
                7: 'diapente', 8: 'diapente + semitone',
                9: 'diapente + tone', 10: 'diapente + hemiolion',
                11: 'diapente + ditone', 12: 'diapason'}
    formula: list[str] = []
    prev = 0
    for num in sorted(interval_structure):
        diff = num - prev
        prev = num
        if num > 0:
            formula.append(elements[diff])
    return tuple(formula)


def get_double_octave(interval_structure: Iterable[int]) -> tuple[int, ...]:
    '''
    Extend the range of a scale pattern to two octaves.

    Parameters
    ----------
    interval_structure : Iterable[int]
        An array of integers representing the intervals of a heptatonic scale.

    Returns
    -------
    tuple[int, ...]
        An array with the original intervals, plus the same intervals an 
        octave higher.
    '''
    double_octave = list(interval_structure)
    interval_structure = tuple(interval_structure)
    for i in range(NOTES):
        double_octave.append(interval_structure[i] + TONES)
    return tuple(double_octave)


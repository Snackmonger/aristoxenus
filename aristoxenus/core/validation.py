
import re
from typing import Iterable

from aristoxenus.core.constants import (
    ACCIDENTALS,
    DIATONIC,
    HEPTATONIC_SCALES,
    NOTE_NAME_INDEX,
    NOTES,
    RE_PARSE_INTERVAL_NAME,
    RE_PARSE_NOTE_NAME,
    RE_PARSE_ROMAN_NAME
)
from aristoxenus.core.note_name import (
    simplify_note_name,
    decode_note_name
)


def validate_heptatonic_spelling(note_names: Iterable[str]) -> bool:
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
    '''
    new: list[int] = []
    for note in [simplify_note_name(decode_note_name(x)) for x in note_names]:
        i, a = note[NOTE_NAME_INDEX], note[ACCIDENTALS]
        new.append(HEPTATONIC_SCALES[DIATONIC][i] + a)
    return len(set(new)) == NOTES


def validate_heptatonic_structure(interval_structure: Iterable[int]) -> bool:
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
    '''
    return len(set(interval_structure)) == NOTES and 0 in interval_structure


def validate_alphabetic_name(string: str) -> bool:
    '''
    Check whether a string is a valid alphabetic note name.

    Valid is any of A-G plus any number of sharps or flats, 
    but not a mixture of both.

    Parameters
    ----------
    string : str
        The string to be tested.

    Returns
    -------
    bool
        True, if the string is a valid alphabetic note name.
    '''
    return re.match(RE_PARSE_NOTE_NAME, string) is not None


def validate_roman_name(string: str) -> bool:
    '''
    Check whether a string is a Roman interval name.

    Valid is any number of sharps or flats, but not a mixture of both, 
    plus any of I-VII, upper or lower case.


    Parameters
    ----------
    string : str
        The note name to be tested.

    Returns
    -------
    bool
        True, if the name is a valid Roman interval name.
    '''
    return re.match(RE_PARSE_ROMAN_NAME, string) is not None


def validate_interval_name(string: str) -> bool:
    '''
    Check whether a string is an Indian interval name.

    Valid is any number of sharps or flats, but not a mixture of both, 
    plus any of 1-7, 9, 11, or 13.


    Parameters
    ----------
    string : str
        The string to be tested.

    Returns
    -------
    bool
        True, if the name is a valid Indian interval name.
    '''
    return re.match(RE_PARSE_INTERVAL_NAME, string) is not None

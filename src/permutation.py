'''
Functions relating to permuting different types of interval structures.
'''
import loguru
import functools

from src import bitwise
from data import constants
from src import errors
from src import parsing
from src.models.interval_structures import LimitedIntervalStructure, Octave


logger = loguru.logger


def extend_structure(interval_structure: int,
                     extensions: int = constants.NUMBER_OF_OCTAVES) -> int:
    '''
    Extend a 12-bit interval structure to the range of n identical octaves.

    Parameters
    ----------
    interval_structure : int
        An integer of no more than 12 bits representing an interval structure.
    extensions : int, default=9
        A number of octaves to extend the structure over.

    Returns
    -------
    int
        An n*12-bit interval structure, with the original 12-bit structure 
        repeating every 12 bits.
    '''
    compound_structure: int = interval_structure
    for transposed_octave in range(1, extensions):
        compound_structure |= bitwise.transpose_interval(
            interval_structure, transposed_octave, echo=True)
    return compound_structure




def chordify(interval_structure: int, notes: int=3, step: int=2) -> list[int]:
    '''
    Return a dict of chords for the given scale and structural principles.

    Parameters
    ----------
    interval_structure : int
        A 12-bit representation of a scale-like interval structure.
    notes : int
        The number of notes to include each chord's structure.
    step : int
        The number of structural steps between chord intervals.        

    Returns
    -------
    dict[str, int]
    '''
    if interval_structure.bit_count() > constants.TONES:
        raise errors.OctaveRotationError
    
    all_chords: list[int] = []
    chord_intervals: list[int] = []
    octave: Octave = Octave(interval_structure)
    extended_mode: LimitedIntervalStructure

    # Use an extended range in case the user wants to make chords made out of
    # e.g. compound sevenths, where a tetrad would span nearly three octaves.
    for inversion in octave.inversions:
        full_range: int = extend_structure(inversion)
        extended_mode = LimitedIntervalStructure(full_range.bit_length(), full_range)
        chord_intervals = list(extended_mode.intervals[::step])[:notes]
        all_chords.append(functools.reduce(lambda a, b: a|b, chord_intervals))

    return all_chords

    



    


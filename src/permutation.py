'''
Functions relating to permuting different types of interval structures.
'''
import functools
import loguru
from typing import Callable


from data import constants
from data import keywords
from src import bitwise
from src import errors
from src import parsing
from src import nomenclature
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


def chordify(interval_structure: int, notes: int | str = 3, step: int | str = 2) -> list[int]:
    '''
    Return a dict of chords for the given scale and structural principles.

    Parameters
    ----------
    interval_structure : int
        A 12-bit representation of a scale-like interval structure.
    notes : int or str, default=3
        The number of notes to include each chord's structure, or a special 
        term denoting the number of notes in a structure (e.g. 'triad'). N.B.
        that the number of notes is the number of intervals + 1.
    step : int or str, default=2
        The number of structural steps between chord intervals, or a special
        term denoting the number of steps between notes in the structure,
        (e.g. 'tertial'). The step works like a list slice, starting on 0.

    Returns
    -------
    list[int]
        A list of chords build from each degree of the scale, according to the
        given structural principles. 

    Notes
    -----
    The function is robust enough to be able to create any type of simple 
    chord pattern from a given scale, as long as it does not exceed the 
    maximum range. This means that in addition to tertial & quartal triads 
    and tetrads, we can also create septimal triads, undecimal tetrads, etc.

    Importantly, the number of steps refers to the notes in the scale, not to
    specific intervals, so 'tertial' means 'every third note,' not 
    specifically 'major/minor thirds only.' This means that a 'tertial' chord 
    might be made up of 'major seconds' or 'perfect fourths' depending on 
    the actual interval structure that is given.

    If the number of notes in the scale is fewer than the number of 
    requested notes in the chord, then the upper octaves of the returned 
    structure will be mirrors of their lower counterparts. 
    
    The maximum extent of an interval structure is 108 bits. If the requested 
    structure would exceed this limit (for instance, building a 12-note chord
    out of octave intervals would yield a 144-bit structure) then we simply 
    omit the excessive intervals and return an incomplete structure of 108
    bits or less (depending on the specific structure).
    '''
    if interval_structure.bit_count() > constants.TONES:
        raise errors.OctaveRotationError
    
    # Convert keywords to ints
    if isinstance(notes, str):
        notes = nomenclature.translate_numeric_keyword(notes)
    if isinstance(step, str):
        step = nomenclature.translate_numeric_keyword(step) - 1

    chord_scale: list[int] = []
    chord_intervals: list[int] = []
    full_range: int
    clip: int
    extended_mode: LimitedIntervalStructure

    octave: Octave = Octave(interval_structure)
    for inversion in octave.inversions:
        full_range = extend_structure(inversion)
        extended_mode = LimitedIntervalStructure(
            full_range.bit_length(), full_range)
        all_intervals =list(extended_mode.intervals[::step])

        # Ensure that the requested number of notes does not exceed the
        # number of available notes.
        clip = notes
        if notes > len(all_intervals):
            clip = len(all_intervals)
        chord_intervals = all_intervals[:clip]

        # Collapse recognized intervals into discrete chords
        chord_scale.append(functools.reduce(lambda a, b: a | b, chord_intervals))

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
    '''
    # clean this up later
    if not bitwise.validate_interval_structure(chord_structure, 12, 3):
        raise ValueError
    
    octave: Octave = Octave(chord_structure)
    intervals_: list[int] = list(octave.intervals)
    intervals_[1] = bitwise.transpose_interval(intervals_[1])
    return functools.reduce(lambda a, b: a | b, intervals_)



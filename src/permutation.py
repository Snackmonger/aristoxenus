'''
Functions relating to permuting different types of interval structures.
'''
from data import constants
from src import (bitwise,
                 errors,
                 nomenclature)


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
    
    Examples
    --------
    >>> bin(extend_structure(0b101010110101, 2))
    '0b101010110101101010110101'
    >>> bin(extend_structure(0b101010110101, 3))
    '0b101010110101101010110101101010110101'
    '''
    if not bitwise.validate_interval_structure(interval_structure, 12):
        raise errors.IntervalOutOfBoundsError
    
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
        (e.g. 'tertial'). The step works like a list slice, starting on 0, so
        tertial is 2, quartal is 3, etc.

    Returns
    -------
    list[int]
        A list of chords built from each degree of the scale, according to the
        given structural principles. 

    Notes
    -----
    The function is able to create any type of simple chord pattern from a 
    given scale, as long as it does not exceed the maximum range. This means
    that in addition to tertial & quartal triads and tetrads, we can also 
    create septimal triads, undecimal tetrads, and other unusual structures.

    Importantly, the number of steps refers to the notes in the scale, not to
    specific intervals, so 'tertial' means 'every third note,' not 
    specifically 'major/minor thirds only.' This means that a 'tertial' chord 
    might be made up of 'major seconds' or 'perfect fourths' depending on 
    the actual interval structure that is given.

    If the number of notes in the scale is fewer than the number of 
    requested notes in the chord, then the upper octaves of the returned 
    structure will be copies of their lower counterparts. 
    
    The maximum extent of an interval structure is 108 bits. If the requested 
    structure would exceed this limit (for instance, building a 12-note chord
    out of octave intervals would yield a 144-bit structure) then we simply 
    omit the excessive intervals and return an incomplete structure of 108
    bits or less (depending on the specific structure).

    Examples
    --------
    >>> chordify(0b101010110101)
    [73, 137, 145, 145, 137, 137, 145]
    >>> chordify(0b101010110101, 4, 3)
    [33825, 33825, 66593, 67649, 33825, 33825, 67617]
    >>> chordify(0b101010110101, 'tetrad', 'quartal')
    [33825, 33825, 66593, 67649, 33825, 33825, 67617]
    '''
    if not bitwise.validate_interval_structure(interval_structure, 12):
        raise errors.IntervalOutOfBoundsError
    
    # Convert keywords to ints
    if isinstance(notes, str):
        notes = nomenclature.translate_numeric_keyword(notes)
    if isinstance(step, str):
        step = nomenclature.translate_numeric_keyword(step)

    chord_scale: list[int] = []
    chord_intervals: list[int] = []
    all_intervals: list
    full_range: int
    clip: int
    
    # Grab the intervals for each mode and use them to derive chords
    for inversion in bitwise.inversions(interval_structure, 12):
        full_range = extend_structure(inversion)
        all_intervals = list(bitwise.iterate_intervals(full_range))[::step]

        # Ensure that the requested number of notes in the chord
        # does not exceed the number of available notes.
        clip = len(all_intervals) if notes > len(all_intervals) else notes
        chord_intervals = all_intervals[:clip]

        # Collapse recognized intervals into discrete chords
        chord_scale.append(bitwise.reduce_(chord_intervals))

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
        raise errors.IntervalOutOfBoundsError
    
    return drop_voicing(chord_structure, constants.DROP_2)


def drop_voicing(chord_structure:int, drop_notes: tuple[int, ...] | list[int]) -> int:
    '''
    Adjust the intervals in a given chord structure to produce a 'drop' voicing.

    Parameters
    ----------
    chord_structure : int
        An integer representing the structure of a chord.
    drop_notes : tuple[int, ...] or list[int]
        The notes of the chord that will be shifted to produce the new voicing.
        Some common options are included in `data.constants` as `DROP_2`,
        `DROP_2_AND_4`, and `DROP_3`.

    Returns
    -------
    int
        The same chord, but with the given modifications to its intervals.

    Notes
    -----
    Although called 'drop' chords, the method by which we produce the voicing
    is actually the opposite of what the abstraction might suggest. The 'drop'
    logic often produces a voicing in the wrong inversion:

        C E G B -> G C E B (drop the G, results in a 2nd inversion major7)

    We prefer to express drop chords in terms of *raised* intervals. We do 
    this for two reasons:
        1. The least significant bit represents the lowest pitch. Dropping
        pitches below this requires a reconfiguration of the entire basic 
        range for every pitch that gets moved.
        2. The raised intervals still produce the correct drop voicing, but
        they now retain the same bass note as their same-named inversion in
        the parent form.

        C E G B -> C E B G (raise the G, results in a root position major7)

    This situation entails that a drop chord must **always** be generated from 
    the corresponding inversion of a close-voiced chord, e.g. first inversion
    close voice produces first inversion drop 2, drop 3, drop 2&4, etc.

    IMPORTANT: Although drop chords are called 'inversions' based on their 
    bass note, this is misleading. The actual rotational inversion of a drop 
    chord will produce several distict drop voicings:

        C E B G (starting point: 'root position' drop 2 Cmaj7)
        E B G C (first rotation: a '1st inversion' drop 2&4 Cmaj7)
        B G C E (second rotation: a '3rd inversion' drop 3 Cmaj7)
        G C E B (third rotation: a '2nd inversion' drop 2 Cmaj7)

    Therefore, if we want to make sure that a whole passage consists of 
    similarly-voiced drop chords, we must apply the inversion to the close 
    voicing and THEN apply the drop voicing modification.

    Although drop chords are typically 4-note voicings, the function can 
    accommodate larger structures as well. 

    Examples
    --------
    >>> bin(drop_voicing(0b100010010001, constants.DROP_2))
    '0b10000100010000001'
    >>> bin(drop_voicing(0b100010010001, constants.DROP_3))
    '0b10010000100000000001'
    >>> bin(drop_voicing(0b100010010001, constants.DROP_2_AND_4))
    '0b100000010000000010000001'
    '''
    intervals = list(bitwise.iterate_intervals(chord_structure))
    for interval in drop_notes:
        intervals[interval] = bitwise.transpose_interval(intervals[interval])
    return bitwise.reduce_(intervals)

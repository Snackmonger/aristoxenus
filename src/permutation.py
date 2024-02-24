'''
Functions relating to permuting different types of interval structures.
'''
from data import (annotations, 
                  constants,
                  errors,
                  intervallic_canon,
                  keywords)

from src import (bitwise,
                 nomenclature,
                 utils)


def extend_structure(interval_structure: int,
                     extensions: int = constants.NUMBER_OF_OCTAVES
                     ) -> int:
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
        raise errors.IntervalStructureError(interval_structure)

    compound_structure: int = interval_structure
    for transposed_octave in range(1, extensions):
        compound_structure |= bitwise.transpose_interval(
            interval_structure, transposed_octave, echo=True)
    return compound_structure


def chordify(interval_structure: int,
             notes: int | str = 3,
             step: int | str = 2
             ) -> list[int]:
    '''
    Return a dict of chords for the given scale and structural principles.

    Parameters
    ----------
    interval_structure : int
        An integer not exceeding 12 bits representing the interval structure 
        to be treated as the 'parent' scale. 
    notes : int or str, default=3
        The number of notes to include in each chord's structure, or a special
        term denoting the number of notes in a structure (e.g. 'triad'). 
        N.B. that the number of notes is the number of intervals + 1.
    step : int or str, default=2
        The number of structural steps between chord intervals, or a special
        term denoting the number of steps between notes in the structure,
        (e.g. 'tertial'). The step works like a list slice, starting on 0, so
        tertial is 2, quartal is 3, etc.

    Returns
    -------
    list[int]
        A list of chords built from each degree of the scale, according to the
        given structural principles, expressed as integers.

    Notes
    -----
    Importantly, the number of steps refers to the notes in the scale, not to
    specific intervals, so 'tertial' means 'every third note,' not 
    specifically 'major/minor thirds only.' This means that a 'tertial' chord 
    might be made up of 'major seconds' or 'perfect fourths' depending on 
    the actual interval structure of the parent scale.

    The maximum extent of an interval structure is 108 bits. If the requested 
    structure would exceed this limit (for instance, building a 12-note chord
    out of octave intervals would yield a 144-bit structure) then we simply 
    omit the excessive intervals and return an incomplete structure of 108
    bits or fewer (depending on the specific structure).

    Examples
    --------
    >>> chordify(0b101010110101)
    [145, 137, 137, 145, 145, 137, 73]

    This translates to the diatonic triads
    (dim, min, maj, maj, min, min, maj)

    >>> chordify(0b101010110101, 4, 3)
    [67617, 33825, 33825, 67649, 66593, 33825, 33825]
    >>> chordify(0b101010110101, 'tetrad', 'quartal')
    [67617, 33825, 33825, 67649, 66593, 33825, 33825]

    This translates to quartal voicings of the diatonic tetrads.
    '''
    # Convert keywords to ints
    if isinstance(notes, str):
        notes = nomenclature.decode_numeric_keyword(notes)
    if isinstance(step, str):
        step = nomenclature.decode_numeric_keyword(step) - 1

    if not bitwise.validate_interval_structure(interval_structure, 12):
        raise errors.IntervalStructureError(interval_structure)

    chord_scale: list[int] = []
    chord_intervals: list[int] = []
    all_intervals: list[int]
    full_range: int
    clip: int

    # Grab the intervals for each mode and use them to derive chords
    for inversion in bitwise.inversions(interval_structure, 12):
        full_range = extend_structure(inversion)
        all_intervals: list[int] = list(
            bitwise.iterate_intervals(full_range))[::step]

        # Ensure that the requested number of notes in the chord
        # does not exceed the number of available notes.
        clip = len(all_intervals) if notes > len(all_intervals) else notes
        chord_intervals = all_intervals[:clip]

        # Reduce recognized intervals into discrete chords
        chord_scale.append(bitwise.reduce_(chord_intervals))

    return chord_scale


def chordify_note_names(note_names: list[str] | tuple[str, ...],
                        notes: int | str = 3,
                        step: int | str = 2
                        ) -> dict[str, tuple[str, ...]]:
    '''
    Return a dict of chords for the given scale and structural principles.

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
    In order to accommodate the chordification of scales with both sharps
    and flats, this function does not attempt to validate that the notes are
    legal. Technically, 
    '''

    # Convert keywords to ints
    if isinstance(notes, str):
        notes = nomenclature.decode_numeric_keyword(notes)
    if isinstance(step, str):
        step = nomenclature.decode_numeric_keyword(step) - 1

    chord_scale: dict[str, tuple[str, ...]] = {}
    for index, note_name in enumerate(note_names):
        base: list[str] = utils.shift_list(note_names, note_name)
        full_range: list[str] = base * constants.NUMBER_OF_OCTAVES
        chord_form: list[str] = full_range[::step]
        degree: str = utils.roman_numeral(index+1)
        clip: int = len(chord_form) if notes > len(chord_form) else notes
        chord_form = chord_form[:clip]

        chord_scale.update({degree: tuple(chord_form)})

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

    return drop_voicing(chord_structure, constants.DROP_2)


def drop_voicing(chord_structure: int,
                 drop_notes: tuple[int, ...] | list[int]
                 ) -> int:
    '''
    Adjust the intervals in a given chord structure to produce a 'drop' 
    voicing.

    Parameters
    ----------
    chord_structure : int
        An integer representing the structure of a chord.
    drop_notes : tuple[int, ...] or list[int]
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
    Although called 'drop' chords, the method by which we produce the voicing
    is actually the opposite of what the abstraction might suggest. The 'drop'
    logic produces a voicing in a different inversion from the starting chord:

        C E G B -> G C E B (drop the G, results in a 2nd inversion major7)

    We prefer to express drop chords in terms of *raised* intervals:

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
    accommodate larger structures as well, as long as the indices are
    present in the given interval structure (0 is the lowest note).

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


def triad_variants(triads: dict[str, int] | None = None
                   ) -> annotations.ChordInventory:
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
    if triads is None:
        triads = intervallic_canon.triads

    variants: list[annotations.TriadConspectus] = []
    for name, triad in triads.items():
        open_triad = spread_triad(triad)
        close_inversions = bitwise.inversions(triad, constants.TONES)
        open_inversions = bitwise.inversions(open_triad, constants.TONES*2)
        inversion_names = [keywords.numbered_inversions[x] for x in range(3)]

        variants.append(annotations.TriadConspectus(canonical_name=name,
                                                    canonical_form=triad,
                                                    close=dict(
                                                        zip(inversion_names, close_inversions)),
                                                    open=dict(zip(inversion_names, open_inversions))))

    return tuple(variants)


def tetrad_variants(tetrads: dict[str, int] | None = None
                    ) -> annotations.ChordInventory:
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
    if tetrads is None:
        tetrads = intervallic_canon.tetrads

    variants: annotations.ChordInventory = []
    inversion_names = [keywords.numbered_inversions[x] for x in range(4)]
    
    for name, tetrad in tetrads.items():
        inversions: tuple[int, ...] = bitwise.inversions(
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
            drop2: int = drop_voicing(inversion, constants.DROP_2)
            drop3: int = drop_voicing(inversion, constants.DROP_3)
            drop24: int = drop_voicing(inversion, constants.DROP_2_AND_4)

            innerdict[keywords.CLOSE].update({inversion_name: inversion})
            innerdict[keywords.DROP_2].update({inversion_name: drop2})
            innerdict[keywords.DROP_3].update({inversion_name: drop3})
            innerdict[keywords.DROP_2_AND_4].update({inversion_name: drop24})

        variants.append(innerdict)

    return tuple(variants)



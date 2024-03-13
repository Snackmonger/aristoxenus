

from typing import Sequence
from data import (chord_symbols,
                  intervallic_canon as intervals,
                  constants,
                  errors,
                  keywords,
                  annotations)
from src import (nomenclature,
                 utils,
                 rendering,
                 permutation)


def remove_chord_prefix(chord_symbol: str) -> tuple[str, str]:
    '''For a given chord symbol, return a tuple containing: (root, all other symbols).'''
    root: str
    for note in sorted(constants.LEGAL_ROOT_NAMES, key=len, reverse=True):
        if note in chord_symbol:
            root = note
            chord_symbol = chord_symbol.removeprefix(note)
            return root, chord_symbol

    raise errors.ChordNameError('Unknown note name.')


def parse_chord_symbol(chord_symbol: str) -> int:
    '''
    Return an integer representing an interval map of a given chord symbol.

    Parameters
    ----------
    chord_symbol : str
        A chord symbol with note name, extensions, and modifiers.

    Returns
    -------
    int
        An integer representation of an interval structure derived from the 
        chord name.

    Raises
    ------
    ChordNameError
        Raised when the alphabetic chord name is not found in the list defined
        by `nomenclature.legal_chord_names`. (This error is actually generated
        by the auxiliary function `parsing.__remove_chord_prefix`).

    Notes
    -----
    A variety of standard forms are supported. Apart from the alphabetic chord
    name, any other unrecognized symbols are simply ignored. If the 
    function does not raise an error because of a malformed root note, it will
    always return, at minimum, a p5 (that is, 129 = 0b10000001). 

    The parser will treat all 'add' and 'no' notations last (even if they are 
    not written last in the chord symbol), so they can be used to make explicit 
    statements and corrections about a chord's structure.

        Em7add9 -> (int) ->  E, G, B, D, F#
        Em7maj9nob3 -> (int) -> E, G#, B, D, F#

    Examples
    --------
    >>> bin(parse_chord_symbol('Cmaj7'))
    '0b100010010001'
    >>> bin(parse_chord_symbol('CM7'))
    '0b100010010001'
    >>> bin(parse_chord_symbol('CΔ7'))
    '0b100010010001'
    >>> bin(parse_chord_symbol('Cmaj#5'))
    '0b100010001'
    >>> bin(parse_chord_symbol('Caug'))
    '0b100010001'
    >>> bin(parse_chord_symbol('C+'))
    '0b100010001'
    >>> bin(parse_chord_symbol('Ebm7b5'))
    '0b10001001001'
    >>> bin(parse_chord_symbol('Ebmin7b5'))
    '0b10001001001'
    >>> bin(parse_chord_symbol('Eb-7b5'))
    '0b10001001001'
    >>> bin(parse_chord_symbol('Ebdimb7'))
    '0b10001001001'
    >>> bin(parse_chord_symbol('C6/9'))
    '0b100001010010001'
    >>> bin(parse_chord_symbol('F#dim7'))
    '0b1001001001'
    >>> bin(parse_chord_symbol('Gm13'))
    '0b1000100100010010001001'
    >>> bin(parse_chord_symbol('Asus2add11'))
    '0b100000000010000101'
    >>> bin(parse_chord_symbol('Fmaj13no11'))
    '0b1000000100100010010001'
    >>> bin(parse_chord_symbol('G7b9'))
    '0b10010010010001'
    >>> bin(parse_chord_symbol('Fmajsus2'))
    '0b10000101'
    '''
    # Remove contradictory symbol usage of '/'
    # AFAIK, this is the only symbol to conflict with slash notation
    if '6/9' in chord_symbol:
        chord_symbol = chord_symbol.replace('6/9', '69')

    # Delegate special structures to auxiliary functions. These types of chord
    # symbols use explicit note names to identify structural features, and so
    # they cannot be parsed purely based on the chord suffix.
    if constants.POLYCHORD_DIVIDER_SYMBOL in chord_symbol:
        return parse_polychord_symbol(chord_symbol)
    if constants.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
        return parse_slash_chord_symbol(chord_symbol)

    # Root note is not needed beyond this point.
    chord_symbol = remove_chord_prefix(chord_symbol)[1]

    return parse_simple_chord_suffix(chord_symbol)


def parse_simple_chord_suffix(chord_symbol: str) -> int:
    """Generate an interval map from the parts of a chord symbol
    that do not refer to note names (e.g. "min7b5", "maj7", "7b5", etc.)
    """
    # Dummy structure is a P5. This gets removed if the chord has an
    # alteration or a 'no5' suffix. If no symbol gets recognized,
    # this P5 is returned as a default.
    structure: int = intervals.DIAPENTE

    # No suffix = major triad: C, D, E, etc.
    if len(chord_symbol) == 0:
        return structure | intervals.DITONE
    # Powerchord suffix: D5, E5, F5, etc.,
    # (implies a p5 and p8).
    if chord_symbol == chord_symbols.CHORD_5:
        return structure | intervals.DIAPASON

    # Remove all 'add'/'no' modifiers to see what the base symbol is.
    add_drop: list[str] = []
    for add in chord_symbols.additive:
        if add in chord_symbol:
            chord_symbol = chord_symbol.replace(add, '')
            add_drop.append(add)
    for drop in chord_symbols.subtractive:
        if drop in chord_symbol:
            chord_symbol = chord_symbol.replace(drop, '')
            add_drop.append(drop)

    parsed_symbols: list[str] = []

    # Parse prototypical prefixes, e.g. maj11, min9, 13, etc.,
    # and create an explicit list of implicit intervals.
    for extension, extended_structure in {
        chord_symbols.CHORD_7: ['1'],  # dummy value: 7 is idiomatic
        chord_symbols.CHORD_9: [chord_symbols.CHORD_9],

        chord_symbols.CHORD_11: [chord_symbols.CHORD_9,
                                 chord_symbols.CHORD_11],

        chord_symbols.CHORD_13: [chord_symbols.CHORD_9,
                                 chord_symbols.CHORD_11,
                                 chord_symbols.CHORD_13]
    }.items():

        for symbol in chord_symbols.CHORD_SYMBOL_LIST:
            if chord_symbol.startswith(symbol + extension):
                parsed_symbols += extended_structure

                # maj7 (or variant) -> maj, maj7, plus extensions
                if symbol in chord_symbols.CHORD_MAJOR_SYMBOL_LIST:
                    chord_symbol = chord_symbol.removeprefix(
                        symbol + extension)
                    parsed_symbols += [chord_symbols.CHORD_MAJ,
                                       chord_symbols.CHORD_MAJ_7]

                # dim7 (or variant) -> dim, bb7, plus extensions
                if symbol == chord_symbols.CHORD_DIM:
                    chord_symbol = chord_symbol.removeprefix(
                        symbol + extension)
                    parsed_symbols += [chord_symbols.CHORD_DIM,
                                       chord_symbols.CHORD_DOUBLE_FLAT_7]

                # min7 (or variant): ensure that b7 is present
                # if not explicit (e.g. Em11)
                if symbol in chord_symbols.CHORD_MINOR_SYMBOL_LIST:
                    parsed_symbols += [chord_symbols.CHORD_FLAT_7]

        # 7 (or variant) -> maj, b7, plus extensions
        if chord_symbol.startswith(extension):
            parsed_symbols += extended_structure + \
                [chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_MAJ]
            chord_symbol = chord_symbol.removeprefix(extension)

    # First element is another number: C2, C4, C6, etc.
    # implies major triad plus colour tone (different from sus2,
    # sus4, which have no 3rd)
    for symbol in [chord_symbols.CHORD_6,
                   chord_symbols.CHORD_2,
                   chord_symbols.CHORD_4]:
        if chord_symbol.startswith(symbol):
            parsed_symbols.append(chord_symbols.CHORD_MAJ)

    # By now, we should have an explicit list of all previously implicit
    # intervals, plus any explicit intervals remaining in the chord symbol.
    # (start with longest values to avoid misparsing a subsymbol)
    for symbol_element, interval in sorted(
        chord_symbols.symbol_elements.items(),
        key=lambda key: len(key[0]),
        reverse=True
    ):
        # Add intervals to structure
        if symbol_element in chord_symbol or symbol_element in parsed_symbols:
            structure |= interval
            chord_symbol = chord_symbol.replace(symbol_element, '')
            if symbol_element not in parsed_symbols:
                parsed_symbols.append(symbol_element)

    # Check if a symbol overrides the implicit p5 of a chord.
    for symbol in chord_symbols.CHORD_ALTERED_FIFTH_SYMBOL_LIST:
        if symbol in parsed_symbols:
            structure ^= (intervals.DIAPENTE - 1)  # 1 = tonic

    # If the chord indicated sus, assume that this symbol overrides any
    # symbol indicating a 3rd.
    for sus in [chord_symbols.CHORD_SUS_2, chord_symbols.CHORD_SUS_4]:
        if sus in parsed_symbols:
            structure &= (~intervals.DITONE & ~intervals.HEMIOLION) - 1

    # Handle add/no notation
    for symbol in add_drop:
        if symbol in chord_symbols.additive:
            structure |= chord_symbols.additive[symbol]

        elif symbol in chord_symbols.subtractive:
            structure &= (~chord_symbols.subtractive[symbol] - 1)  # 1 = tonic

    # if chord_symbol != '':
        # logger.info(f'Parsed: {parsed_symbols}, Unparsed: {chord_symbol}')

    return structure


def parse_slash_chord_symbol(chord_symbol: str) -> int:
    '''
    Parse a chord in 'slash' notation (e.g.: G/Bb, Cm7/Eb).   

    Parameters
    ----------
    chord_symbol : str
        A chord in slash notation

    Returns
    -------
    int
        An integer representation of an interval map.
    '''
    if chord_symbol.count('/') != 1:
        raise errors.ChordSymbolError(chord_symbol)

    # TODO: This is broken... Needs fix... you fix now?
    # We want to ensure that, if the bass note is a chord tone, we are using
    # the normal inversion of the chord, rather than transposing with an extra
    # bass note.

    bass: str = nomenclature.decode_enharmonic(chord_symbol.split('/')[1])
    root: str = nomenclature.decode_enharmonic(
        remove_chord_prefix(chord_symbol)[0])
    octave_from_bass: tuple[str, ...] = utils.shift_list(
        nomenclature.chromatic(), bass)
    octave_from_root: tuple[str, ...]  = utils.shift_list(
        nomenclature.chromatic(), root)
    main_chord_structure: int = parse_chord_symbol(chord_symbol.split('/')[0])
    chord = rendering.render_plain(main_chord_structure, octave_from_root)
    if bass in chord:
        bass_i = octave_from_root.index(bass) + 1
        main_chord_structure ^= (1 << bass_i)

    extra_semitones: int = octave_from_bass.index(root)

    return (main_chord_structure << extra_semitones) + 1


def parse_polychord_symbol(chord_symbol: str) -> int:
    '''
    Parse a chord in 'polychord' notation.

    Parameters
    ----------
    chord_symbol : str
        A compound symbol consisting of two or more chord symbols separated 
        by the '@' symbol. 

    Returns
    -------
    int
        An interval structure corresponding to the given polychord symbol.

    Notes
    -----
    A polychord is entered as a sequence of chord symbols separated by the '@' 
    symbol. Each successive note name in the polychord will be understood as 
    referring to the note name in the previous name's first octave. 

    The '^' symbol can be substituted for a chord symbol in the polychord, 
    indicating that the following chord is to be shifted an octave higher than
    normal. The symbol can also be compounded to indicate a shift of multiple 
    octaves (e.g. '^^^' means 'shift the next chord 3 octaves up').

    Examples
    --------
    >>> bin(parse_polychord_symbol('Cmaj7@Ebm7b5'))
    '0b10101011011001'

    This translates to : C0 Eb0 E0 Gb0 G0 Bbb0 B0 Db1

    This notation can also be used as a shorthand for scale names:

    >>> bin(parse_polychord_symbol('Cmaj7@Dm'))
    '0b101010110101'

    This translates to : C0 D0 E0 F0 G0 A0 B0 (C major scale)
    '''
    # TODO: Repair this shit

    compiled_structure: int = 1
    subchord_structure: int = 1
    current_bass: str = ''
    previous_bass: str = ''
    distance: int = 0
    octaves: int = 0
    octave: tuple[str, ...]
    if constants.POLYCHORD_DIVIDER_SYMBOL not in chord_symbol:
        raise errors.ChordSymbolError(chord_symbol)

    # Break up the symbol and parse each subchord. For every chord that isn't
    # the first chord, transpose the resulting structure into the range of the
    # previous one.
    for subchord_symbol in chord_symbol.split('@'):

        # The polychord octave symbol means 'transpose the next chord up 1
        # octave'. The symbol can also be compounded to transpose multiple
        # octaves.
        if constants.POLYCHORD_OCTAVE_SYMBOL in subchord_symbol:
            octaves = subchord_symbol.count(constants.POLYCHORD_OCTAVE_SYMBOL)
            distance += octaves * 12

        else:
            current_bass, chord_symbol = remove_chord_prefix(subchord_symbol)
            subchord_structure = parse_chord_symbol(subchord_symbol)
            if constants.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
                current_bass = chord_symbol.split(
                    constants.SLASH_CHORD_DIVIDER_SYMBOL)[-1]

            # First symbol
            if previous_bass == '':
                compiled_structure |= subchord_structure
                previous_bass = nomenclature.decode_enharmonic(current_bass)

            else:
                octave = utils.shift_list(nomenclature.chromatic(
                    constants.BINOMIALS), previous_bass)
                distance += octave.index(
                    nomenclature.decode_enharmonic(current_bass))
                previous_bass = nomenclature.decode_enharmonic(current_bass)
                compiled_structure |= (subchord_structure << distance)

    return compiled_structure


# def parse_heptatonic_scale_structure(interval_structure:int):
#     '''
#     Take an integer of no more than 12 bits, of which exactly 7 are flipped,
#     and attempt to assign a name to it.

#     Parameters
#     ----------
#     scale_structure : int
#         An integer

#     Returns
#     -------
#     _type_
#         _description_

#     Raises
#     ------
#     HeptatonicScaleError
#         _description_
#     '''

#     if interval_structure.bit_length() > 12 or interval_structure.bit_count() != 7:
#         raise errors.HeptatonicScaleError

#     scale: interval_structures.HeptatonicScale = interval_structures.HeptatonicScale(interval_structure)
#     inversions: tuple[int, ...] = scale.inversions
#     parent: str = ''
#     mode: int = 0
#     found_parent: bool = False

#     for heptatonic_supertype in intervals.HEPTATONIC_ORDER:
#         supertype_scale: interval_structures.HeptatonicScale = interval_structures.HeptatonicScale(heptatonic_supertype)
#         supertype_modes: tuple[int, ...] = supertype_scale.inversions

#         for inversion in inversions:
#             if inversion in supertype_modes:
#                 found_parent = True
#                 parent = intervals.HEPTATONIC_SYSTEM[heptatonic_supertype]
#                 mode = supertype_modes.index(inversion)

#     if found_parent is True:
#         return (parent, mode)

    # TODO: keep working here after you write the permutation
    # module to get all variants of a scale form.

    # Find nearest comparison... starting from the diatonic,
    # seek out scales that have same structure with X number
    # of mods, and return the scale with the fewest mods.

    # we can use the 'get heptatonic intervals' function to create
    # names like 'aeolian nat3 b5' if the scale is not a known form.


def identify_polyad():
    ...


def identify_triad(interval_structure: int) -> dict[str, str | dict[str, str]]:
    '''
    Return the canonical identity of a given triadic interval structure.

    Parameters
    ----------
    interval_structure  
        An integer of 24 bits or fewer, of which exactly 3 are flipped.

    Returns
    -------
    dict
        result : str or dict
            The result will either be 'no_match' or a dictionary with the
            following keys:

            chord_identity : str
                The canonical name of the chord structure.
            chord_symbol : str
                The canonical symbol for the chord type.
            inversion : str
                The name of the inversion, or root position.
            structure : str
                A description of the chord's structural makeup.

    Examples
    --------
    >>> identify_triad(0b10000000010000001) == {'result': {'canonical_name': 'major_triad', 'chord_symbol': 'maj', 'inversion': 'root_position', 'structure': 'open'}}
    True
    >>> identify_triad(0b100001001) == {'result': {'canonical_name': 'major_triad', 'chord_symbol': 'maj', 'inversion': 'first_inversion', 'structure': 'close'}}
    True
    >>> identify_triad(0b10001001) == {'result': {'canonical_name': 'minor_triad', 'chord_symbol': 'min', 'inversion': 'root_position', 'structure': 'close'}}
    True
    >>> identify_triad(0b111) == {'result': 'no_match'}
    True
    '''
    if interval_structure.bit_length() > (constants.TONES * 2):
        raise ValueError(interval_structure)

    triads: annotations.TriadInventory = permutation.triad_variants()

    for triad in triads:
        if triad[keywords.CANONICAL_FORM] == interval_structure:
            identity = triad[keywords.CANONICAL_NAME]
            symbol = chord_symbols.triads_symbols[identity]
            result = {keywords.CANONICAL_NAME: identity,
                      keywords.CHORD_SYMBOL: symbol,
                      keywords.INVERSION: keywords.ROOT_POSITION,
                      keywords.STRUCTURE: keywords.CLOSE}
            return {'result': result}

    for triad in triads:
        for voicing in (keywords.CLOSE,
                        keywords.OPEN):

            for inversion, int_structure in triad[voicing].items():
                if int_structure == interval_structure:
                    identity = triad[keywords.CANONICAL_NAME]
                    symbol = chord_symbols.triads_symbols[identity]
                    result = {keywords.CANONICAL_NAME: identity,
                              keywords.CHORD_SYMBOL: symbol,
                              keywords.INVERSION: inversion,
                              keywords.STRUCTURE: voicing}
                    return {'result': result}

    return {'result': 'no_match'}


def identify_tetrad(interval_structure: int) -> dict[str, str | dict[str, str]]:
    '''
    Return the canonical identity of a given tetradic interval structure.

    Parameters
    ----------
    interval_structure : int
        An integer of 24 bits or fewer, of which exactly 4 are flipped.

    Returns
    -------
    dict 
        result : str or dict
            The result will either be 'no_match' or a dictionary with the
            following keys:

            chord_identity : str
                The canonical name of the chord structure.
            chord_symbol : str
                The canonical symbol for the chord type.
            inversion : str
                The name of the inversion, or root position.
            structure : str
                A description of the chord's structural makeup.

    Examples
    --------

    '''
    if interval_structure.bit_length() > (constants.TONES * 2):
        raise ValueError(interval_structure)

    tetrads: annotations.TetradInventory = permutation.tetrad_variants()
    for tetrad in tetrads:
        if tetrad[keywords.CANONICAL_FORM] == interval_structure:
            identity = tetrad[keywords.CANONICAL_NAME]
            symbol = chord_symbols.tetrads_symbols[identity]
            result = {keywords.CANONICAL_NAME: identity,
                      keywords.CHORD_SYMBOL: symbol,
                      keywords.INVERSION: keywords.ROOT_POSITION,
                      keywords.STRUCTURE: keywords.CLOSE}
            return {'result': result}

    for tetrad in tetrads:
        for voicing in (keywords.CLOSE,
                        keywords.DROP_2,
                        keywords.DROP_3,
                        keywords.DROP_2_AND_4):

            for inversion, int_structure in tetrad[voicing].items():
                if int_structure == interval_structure:
                    identity = tetrad[keywords.CANONICAL_NAME]
                    symbol = chord_symbols.tetrads_symbols[identity]
                    result = {keywords.CANONICAL_NAME: identity,
                              keywords.CHORD_SYMBOL: symbol,
                              keywords.INVERSION: inversion,
                              keywords.STRUCTURE: voicing}
                    return {'result': result}

    return {'result': 'no_match'}


def parse_interval_structure_as_chord_symbol(interval_structure: int) -> str:
    '''
    Return a generic chord symbol for a given interval structure.

    The symbol returned by this function will refer to the general structure
    of the chord rather than a specific voicing. Thus, a drop2 maj7 and a
    drop3 maj7 will both return 'maj7', etc. 
    '''
    symbol_elements: list[str] = []
    canonical_form: int
    # Check against common structures before trying to generate
    # a symbol procedurally. This will cover 90% of chords.
    for number_of_notes, function in [(3, identify_triad),
                                      (4, identify_tetrad)]:
        if interval_structure.bit_count() == number_of_notes:
            attempt = function(interval_structure)
            if isinstance(result := attempt[keywords.RESULT], dict):
                return result[keywords.CHORD_SYMBOL]
    interval_12_tone = nomenclature.twelve_tone_scale_intervals(
        interval_structure)
    chord_intervals = rendering.render_plain(
        interval_structure, interval_12_tone)

    return parse_interval_names_as_chord_symbol(chord_intervals)


def parse_as_jazz_chord(chord_symbol: str, config: dict[str, str | int | bool | float]) -> int:
    '''
    Generates a simplified skeleton of a full chord from a chord symbol.

    Parameters
    ----------
    chord_symbol : str
        Any regular chord symbol (not a slash chord or polychord).

    Returns
    -------
    int
        An integer representing an interval structure.

    Notes
    -----
    A chord symbol frequently implies intervals, and the regular chord parser
    always infers implied intervals. Jazz music generally limits the scope of
    chord voicings to only the most important intervals. Intervals will be 
    selectively removed from the structure until an ideal form with 2 to 4 
    intervals can be found.

    The function assembles a number of candidates and evaluateds them 
    according to a hierarchy of constraints:

    The highest interval of any chord will be ranked 1 (PRESERVE MELODY)
    Any altered fifth will be ranked 2 (EXPRESS ALTERATION)
    A major or minor 3rd will be ranked 3 (DEFINE CHORD TYPE)
    A suspended 2 or 4 will be ranked 3 if there is no third, or 7 if there is a third (DEFINE CHORD TYPE)
    A major 7 or b7 will be ranked 4 (BRIDGE OCTAVE)
    A secondary altered extension will be ranked 5 (EXPRESS ALTERED COLOUR)
    The root will be ranked 6 (NAME CHORD)
    A secondary natural extension will be ranked 7 (EXPRESS NATURAL COLOUR)
    A perfect fifth will be ranked 7 (ANCHOR CHORD)

    Examples
    --------

    '''
    return 0


def condense_note_names(note_names: Sequence[str]) -> int:
    '''
    Return a 12-bit integer representing a given collection of note names.

    The first note of the given list will serve as the tonic or root of the 
    pitch map, and other notes will be considered sharper intervals from that
    note name. Unrecognizable note names will be ignored. Scientific note 
    names and all accidentals will be resolved into their simplest binomial 
    form.

    Parameters
    ----------
    note_names : list[str]
        A list of note names. 

    Returns
    -------
    int
        A 12-bit integer representing all the intervals transposed into a 
        single octave.

    See Also
    --------
    `condense_large_interval_structure` 
        : Does the same with integer interval structures instead of note names

    Examples
    --------
    >>> bin(condense_note_names(['C', 'D###4', 'Db', 'Fbbb5', 'Mb', 'G###6', 'F#####9', 'F#|Gb', 'F#|Gb5']))
    '0b10001100111'
    '''

    simplified_notes: list[str] = []
    for note_name in note_names:
        if note_name in nomenclature.chromatic():
            pass
        elif not note_name.isalpha():
            note_name = note_name[:-1]
        try:
            simplified_notes.append(nomenclature.decode_enharmonic(note_name))
        except errors.AristoxenusException:
            pass

    tonic: str = simplified_notes[0]
    chromatic_: tuple[str, ...] = nomenclature.chromatic(constants.BINOMIALS)
    chromatic_ = utils.shift_list(chromatic_, tonic)
    interval_map: int = 1
    for note_name in simplified_notes:
        interval_map |= (1 << chromatic_.index(note_name))
    return interval_map


def parse_literal_sequence(note_names: Sequence[str]) -> int:
    '''
    Return an integer interval structure based on the specific sequence of notes.

    This function ignores scientific names and simply assumes that all sequences
    read left to right, low to high, according to position in the binomial octave.

    Parameters
    ----------
    note_names : list[str]
        A list of note names from the naturals, sharps, flats, or binomials. 

    Returns
    -------
    int
        An interval map representing the structure indicated by the sequence
        of note names. 
    '''
    note_names = [nomenclature.decode_enharmonic(x) for x in note_names]
    rotandum: tuple[str, ...] = utils.shift_list(
        nomenclature.chromatic(), note_names[0])
    interval_structure: int = 1
    distance: int = 0

    # Each note defines the octave in which
    # the next note will be contextualized
    for number, note in enumerate(note_names):
        octave = utils.shift_list(rotandum, note)
        if number < len(note_names) - 1:
            next_note = note_names[number+1]
            distance += octave.index(next_note)
            interval_structure |= (1 << distance)

    return interval_structure


def parse_interval_names_as_chord_symbol(interval_names: Sequence[str]) -> str:
    """Attempt to generate a chord symbol from the given interval names.

    This function anticipates that interval names might be unusual enharmonic
    variants used to accommodate a few unusual scale structures (e.g. bb3, 
    bb7) and attempts to generate a nomenclaturally-consistent name.

    This function has a companion function designed to parse integer interval
    structures in the most main straightforward way possible. In that function
    a bb3 is not distinct from a 2, and so maj7bb3 will be rendered maj7sus2.
    """

    # The function does a pretty good job of naming the common chords in root
    # position, but in order to describe chords from weird heptatonic scales 
    # it is unable to recognize enharmonic variants, inversions, and reordered 
    # voice chords.
    interval_names_ = list(interval_names)
    parsed_symbols: list[str] = []
    is_dim: bool = False
    is_dom: bool = False
    normal3: str = ""
    primary_suffix: str = ""
    secondary_suffix: str = ""
    sus: str = ""
    alt3: str = ""
    alt5: str = ""
    add: str = ""
    no5: str = ""
    no3: str = ""
    extensions: str = ""

    interval_names_.pop(0)  # Unison is not relevant in this context
    diminished_symbols: list[str] = [chord_symbols.CHORD_FLAT_3,
                                     chord_symbols.CHORD_FLAT_5,
                                     chord_symbols.CHORD_DOUBLE_FLAT_7]
    primary_suffixes: list[str] = [chord_symbols.CHORD_FLAT_7,
                                   chord_symbols.CHORD_7,
                                   chord_symbols.CHORD_DOUBLE_FLAT_7]
    secondary_suffixes: list[str] = [chord_symbols.CHORD_6,
                                     chord_symbols.CHORD_FLAT_6,
                                     chord_symbols.CHORD_SHARP_6]
    altered_fifths: list[str] = [chord_symbols.CHORD_FLAT_5,
                                 chord_symbols.CHORD_SHARP_5]
    altered_thirds: list[str] = [chord_symbols.CHORD_DOUBLE_FLAT_3,
                                 chord_symbols.CHORD_SHARP_3]
    suspensions: list[str] = [chord_symbols.CHORD_2,
                              chord_symbols.CHORD_4]
    natural_extensions: list[str] = [chord_symbols.CHORD_9,
                                     chord_symbols.CHORD_11,
                                     chord_symbols.CHORD_13]

    def __finish(symbol: str) -> None:
        interval_names_.remove(symbol)
        parsed_symbols.append(symbol)

    # Does the chord have a primary/seconday suffix?
    # A primary suffix will incorporate the numeral of the highest sequential
    # natural extension, a secondary suffix will not.
    for symb in primary_suffixes:
        if symb in interval_names_:
            primary_suffix = symb
            __finish(symb)
    for symb in secondary_suffixes:
        if symb in interval_names_:
            secondary_suffix = symb
            __finish(symb)
    # If there's both suffixes, then the secondary suffix is a colour tone.
    if secondary_suffix and primary_suffix:
        add += chord_symbols.CHORD_ADD + secondary_suffix
        secondary_suffix = ""

    # Change 7s from literal to symbolic value
    # 7 => maj7, b7 => 7, bb7 => dim7 or bb7
    if chord_symbols.CHORD_DOUBLE_FLAT_7 in primary_suffix:
        if all(x in parsed_symbols + interval_names_ for x in diminished_symbols):
            primary_suffix = primary_suffix.replace(
                chord_symbols.CHORD_DOUBLE_FLAT_7,
                chord_symbols.CHORD_DIM_7)
            __finish(chord_symbols.CHORD_FLAT_5)
            __finish(chord_symbols.CHORD_FLAT_3)
            is_dim = True
    elif chord_symbols.CHORD_FLAT_7 in primary_suffix:
        primary_suffix = primary_suffix.replace(
            chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_7)
    elif chord_symbols.CHORD_7 in primary_suffix:
        primary_suffix = primary_suffix.replace(
            chord_symbols.CHORD_7, chord_symbols.CHORD_MAJ_7)

    # How is the 3rd of the chord expressed?
    if chord_symbols.CHORD_3 in interval_names_:
        __finish(chord_symbols.CHORD_3)
        # C,3,5,7 > Cmaj7 but C,3,5,b7 > C7
        if chord_symbols.CHORD_FLAT_7 not in parsed_symbols:
            normal3 = chord_symbols.CHORD_MAJ
        else:
            is_dom = True
    elif chord_symbols.CHORD_FLAT_3 in interval_names_:
        __finish(chord_symbols.CHORD_FLAT_3)
        # C,b3,b5,bb7 > Cdim7 but C,b3,b5,b7 > Cmin7b5
        if not is_dim:
            normal3 = chord_symbols.CHORD_MIN

    # Is there a colour tone or suspended tone?
    if not normal3:
        # Suspension: C,2,5 > Csus2
        for symb in suspensions:
            if symb in interval_names_:
                sus += chord_symbols.CHORD_SUS + symb
                __finish(symb)
    else:
        # Colour tone: C,2,3,5 > Cmajadd2
        for symb in suspensions:
            if symb in interval_names_:
                add += chord_symbols.CHORD_ADD + symb
                __finish(symb)

    # Does a series of extensions get condensed into a single symbol?
    # If not, does the extension get expressed as a plain symbol or as
    # an addition?
    largest_extension: str = ""
    if primary_suffix:
        for i, symb in enumerate(natural_extensions):
            # Check that the sequence was maintained, otherwise the interval
            # is characterized as an addition.
            previous = natural_extensions[i-1] if i > 0 else None
            if symb in interval_names_:
                if not previous:
                    largest_extension = symb
                    __finish(symb)
                elif previous in parsed_symbols:
                    largest_extension = symb
                    __finish(symb)
                else:
                    add += chord_symbols.CHORD_ADD + symb
                    __finish(symb)
    # C7,9,11,13 > C13, etc.
    if largest_extension:
        if chord_symbols.CHORD_7 in primary_suffix:
            primary_suffix = primary_suffix.replace(
                chord_symbols.CHORD_7, largest_extension)
    # C7,9,13 > C9add13, etc.
    for symb in natural_extensions:
        if symb in interval_names_:
            add += chord_symbols.CHORD_ADD + symb
            __finish(symb)

    # How does the chord express its fifth (if it has one)?
    for symb in altered_fifths:
        if symb in interval_names_:
            alt5 = symb
            __finish(symb)
    # C,3,7 > Cmaj7no5
    if not chord_symbols.CHORD_5 in interval_names_:
        if not alt5:
            alt5 = chord_symbols.CHORD_NO + chord_symbols.CHORD_5
    # Most chords don't mention the fifth: C,3,5,7 > Cmaj7
    else:
        interval_names_.remove(chord_symbols.CHORD_5)

    # Does the chord contain an altered 3rd?
    for symb in altered_thirds:
        if symb in interval_names_:
            alt3 = symb
            __finish(symb)

    # Is a 3rd accounted for at all?
    if not any([alt3, normal3, sus, is_dom, is_dim]):
        no3 = chord_symbols.CHORD_NO + chord_symbols.CHORD_3

    # Cbb3, etc. is ambiguous, convert to Cmajbb3, etc.
    if alt3 and not any([primary_suffix, secondary_suffix]):
        if alt5 and alt5 == chord_symbols.CHORD_FLAT_5:
            normal3 =  chord_symbols.CHORD_MIN
        else:
            normal3 = chord_symbols.CHORD_MAJ
        
    # Cbb7 etc. is ambiguous, convert to Cmajbb7
    if chord_symbols.CHORD_DOUBLE_FLAT_7 in parsed_symbols and not is_dim:
        if not normal3:
            if alt5 and alt5 == chord_symbols.CHORD_FLAT_5:
                normal3 = chord_symbols.CHORD_MIN
            else: 
                normal3 = chord_symbols.CHORD_MAJ

    # Does the chord symbol contain a redundant sub-symbol?
    if chord_symbols.CHORD_MAJ in primary_suffix and normal3 == chord_symbols.CHORD_MAJ:
        normal3 = ""
    if chord_symbols.CHORD_DIM in primary_suffix:
        alt5 = ""

    # An extension without an accidental is easier to read as an addition.
    # C7sus2#11 vs C7sus2add11
    for ex in extensions:
        if not any([constants.SHARP_SYMBOL in ex, constants.FLAT_SYMBOL in ex]):
            add += chord_symbols.CHORD_ADD + ex
            ex = ""

    extensions = "".join(interval_names_)
    symbols: list[str] = [normal3,
                          primary_suffix,
                          secondary_suffix,
                          sus,
                          alt5,
                          alt3,
                          add,
                          no3,
                          no5,
                          extensions]
    final_form = "".join(symbols)

    return final_form

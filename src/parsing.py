from loguru import logger
from typing import Sequence
from data import (
    chord_symbols,
    intervallic_canon as intervallic_canon,
    constants,
    errors,
    keywords,
    annotations
)
from src import (
    bitwise,
    nomenclature,
    utils,
    rendering,
    permutation
)


class UnfinishedFunctionError(Exception):
    """Error that reminds the programmer that a particular bit of logic hasn't
    been written completely.
    """


def remove_chord_prefix(chord_symbol: str) -> tuple[str, str]:
    '''For a given chord symbol, return a tuple containing: (root, all other symbols).'''
    root: str
    # Case 1: Radical is a note name (e.g. Gb, A#, F)
    for note in sorted(constants.LEGAL_ROOT_NAMES, key=len, reverse=True):
        if note in chord_symbol:
            root = note
            chord_symbol = chord_symbol.removeprefix(note)
            return root, chord_symbol

    # Case 2: Radical is an interval name (e.g. bIII, V, vii)
    roman_intervals = list(utils.romanize_intervals(
        [str(x) for x in range(1, 8)]))
    roman_intervals += [x.lower() for x in roman_intervals]
    roman_intervals.sort(key=len, reverse=True)
    for interval in roman_intervals:
        if interval in chord_symbol:
            root = chord_symbol[:chord_symbol.index(interval)+len(interval)]
            chord_symbol = chord_symbol.removeprefix(root)
            return root, chord_symbol

    raise errors.ChordNameError(f'Unknown note name: {chord_symbol}.')


def parse_chord_symbol(chord_symbol: str) -> tuple[int, tuple[str, ...]]:

    # TODO: update docstring for new return type, likewise the companion
    # functions.
    '''
    Return an integer representing an interval map of a given chord symbol.

    Parameters:
        chord_symbol : A chord symbol with note name, extensions, and 
        modifiers.

    Returns
        int : An integer representation of an interval structure derived 
        from the chord name.

    Raises:
        ChordNameError : If the root is not a recognized symbol.

    Notes:
        A variety of standard forms are supported. Apart from the chord's root
        name, any other unrecognized symbols are simply ignored. If the 
        function does not raise an error because of a malformed root note, it 
        will always return, at minimum, a p5 (that is, 129 = 0b10000001). 

        The parser will treat all 'add' and 'no' notations last (even if they 
        are not written last in the chord symbol), so they can be used to make 
        explicit statements and corrections about a chord's structure.

        Em7add9 -> (int) ->  E, G, B, D, F#
        Em7maj9nob3 -> (int) -> E, G#, B, D, F#

    Examples:
        >>> bin(parse_chord_symbol('Cmaj7')[0])
        '0b100010010001'
        >>> bin(parse_chord_symbol('CM7')[0])
        '0b100010010001'
        >>> bin(parse_chord_symbol('CΔ7')[0])
        '0b100010010001'
        >>> bin(parse_chord_symbol('Cmaj#5')[0])
        '0b100010001'
        >>> bin(parse_chord_symbol('Caug')[0])
        '0b100010001'
        >>> bin(parse_chord_symbol('C+')[0])
        '0b100010001'
        >>> bin(parse_chord_symbol('Ebm7b5')[0])
        '0b10001001001'
        >>> bin(parse_chord_symbol('Ebmin7b5')[0])
        '0b10001001001'
        >>> bin(parse_chord_symbol('Eb-7b5')[0])
        '0b10001001001'
        >>> bin(parse_chord_symbol('Ebdimb7')[0])
        '0b10001001001'
        >>> bin(parse_chord_symbol('C6/9')[0])
        '0b100001010010001'
        >>> bin(parse_chord_symbol('F#dim7')[0])
        '0b1001001001'
        >>> bin(parse_chord_symbol('Gm13')[0])
        '0b1000100100010010001001'
        >>> bin(parse_chord_symbol('Asus2add11')[0])
        '0b100000000010000101'
        >>> bin(parse_chord_symbol('Fmaj13no11')[0])
        '0b1000000100100010010001'
        >>> bin(parse_chord_symbol('G7b9')[0])
        '0b10010010010001'
        >>> bin(parse_chord_symbol('Fmajsus2')[0])
        '0b10000101'
        >>> bin(parse_chord_symbol('Gmaj7susbb3b5')[0])
        '0b100001000101'
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


def parse_simple_chord_suffix(chord_symbol: str) -> tuple[int, tuple[str, ...]]:
    """Generate an interval map from the parts of a chord symbol
    that do not refer to note names (e.g. "min7b5", "maj7", "7b5", etc.).

    This is an auxiliary function. Most requests are probably best directed
    towards ``parse_chord_symbol``.

    Args:
        chord_symbol : All chord suffixes except the root name.
    Returns:
        int : An integer representing an interval map.
    Notes:
        This function attempts to be able to parse most of the common ways of
        expressing chord structures, so that many different symbols will be
        able to generate the same integer result. For more information about
        the chord symbols generated by the program and the chord symbols that
        the program is able to recognize, see the /docs/style_guide.rst.
    """
    # NOTE: Rewrite this function.
    # ----------------------------
    # 1. The main function should just return a list of interval names. We can use this
    # to make the list of enharmonicaly-correct note names as well as the integer.

    # 2. The integer conversion part of the function is actually very basic and
    # should be its own function.

    # 3. We also need a function that can translate interval names into note names,
    # while respecting their alphabetic enharmonic values. Assume that every chord
    # comes from a heptatonic scale until we know otherwise, then just supplement
    # with notes from the twelve_tone_intervals/notes.

    # Chord parsing interface
    # -----------------------
    # parse_chord_symbol(chord_symbol: str)
    #   -   This function should be the top-level dispatcher, and it should
    #       return a typed mapping of the integer, the interval names, and
    #       the note names.
    #   -   This function therefore will consolidate the three types
    #       of information.
    # parse_slash_chord_symbol(ch)
    #   -   This function gets called by the dispatcher if the chord matches.
    #   -   It needs to be able to take a base chord and get an answer from
    #       the main dispatcher, then relate that chord to the inversion
    #       indicated in the notation, then return it to the dispatcher that
    #       originally called it.
    # parse_polychord_symbol(ch)
    #   -   This function is the hardest to conceptualize in the new framework.
    #   -   We need to be able to parse all the subchords in the symbol, but
    #       doing so means that they will each be contextualized as their own
    #       individual forms as they pass through the dispatcher. Thus, the second
    #       chord should be contextualized within the structure of the first, but it
    #       will have intervals that relate to itself, rather than its context
    #       within the structure of the first chord.
    #
    # Further concerns
    # ----------------
    # The polychord parser worked well when we were just returning an integer,
    # since we can basically just left shift it as much as we want to compound
    # structures together. But when we deal with interval names, do we really
    # want to be thinking in terms of major 22nds and so on?
    #
    # Possible solution: Simplify the polychord structure in general.
    # Instead of being able to compound infinitely many chords, just
    # limit it to two.
    # When we generate the note names and intervals for the chord, we can

    # Dummy structure is a P5. This gets removed if the chord has an
    # alteration or a 'no5' suffix. If no symbol gets recognized,
    # this P5 is returned as a default.
    structure: int = intervallic_canon.DIAPENTE
    parsed_symbols: list[str] = [chord_symbols.CHORD_5]

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

    # No suffix = major triad: C, D, E, etc.
    if len(chord_symbol) == 0:
        parsed_symbols += [chord_symbols.CHORD_3, chord_symbols.CHORD_5]

    # Powerchord suffix: D5, E5, F5, etc.,
    # (implies a p5 and p8).
    if chord_symbol == chord_symbols.CHORD_5:
        chord_symbol = ""
        parsed_symbols.append(chord_symbols.CHORD_8)

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
                    parsed_symbols.append(chord_symbols.CHORD_7)
                    if chord_symbols.CHORD_SUS not in chord_symbol:
                        parsed_symbols.append(chord_symbols.CHORD_3)

                # dim7 (or variant) -> dim, bb7, plus extensions
                if symbol == chord_symbols.CHORD_DIM:
                    chord_symbol = chord_symbol.removeprefix(
                        symbol + extension)
                    parsed_symbols += [chord_symbols.CHORD_FLAT_3,
                                       chord_symbols.CHORD_FLAT_5,
                                       chord_symbols.CHORD_DOUBLE_FLAT_7]

                # min7 (or variant): ensure that b7 is present
                # if not explicit (e.g. Em11). If symbol has a '7',
                # remove it so it doesn't get interpreted as natural.
                if symbol in chord_symbols.CHORD_MINOR_SYMBOL_LIST:
                    parsed_symbols += [chord_symbols.CHORD_FLAT_7]
                    chord_symbol = chord_symbol.replace(
                        chord_symbols.CHORD_7, "")

        # 7 (or variant) -> maj, b7, plus extensions
        if chord_symbol.startswith(extension):
            parsed_symbols += extended_structure + \
                [chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_3]
            chord_symbol = chord_symbol.removeprefix(extension)

    # First element is another number: C2, C4, C6, etc.
    # implies major triad plus colour tone (different from sus2,
    # sus4, which have no 3rd)
    for symbol in [chord_symbols.CHORD_6,
                   chord_symbols.CHORD_2,
                   chord_symbols.CHORD_4]:
        if chord_symbol.startswith(symbol):
            parsed_symbols.append(chord_symbols.CHORD_3)

    # By now, we should have an explicit list of all previously implicit
    # intervals, plus any explicit intervals remaining in the chord symbol.
    # (start with longest values to avoid misparsing a subsymbol).
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
            structure ^= (intervallic_canon.DIAPENTE - 1)  # 1 = tonic

    # If the chord indicated sus, assume that this symbol overrides any
    # symbol indicating a 3rd and remove any thirds.
    suspensions = [chord_symbols.CHORD_SUS_2,
                   chord_symbols.CHORD_SUS_4,
                   chord_symbols.CHORD_SUS_DOUBLE_FLAT_3,
                   chord_symbols.CHORD_SUS_SHARP_3]
    for sus in suspensions:
        if sus in parsed_symbols:
            structure &= (~intervallic_canon.DITONE & ~intervallic_canon.HEMIOLION) - 1

    # Handle add/no notation
    for symbol in add_drop:
        if symbol in chord_symbols.additive:
            structure |= chord_symbols.additive[symbol]

        elif symbol in chord_symbols.subtractive:
            structure &= (~chord_symbols.subtractive[symbol] - 1)  # 1 = tonic

    # Clean the list of parsed symbols so that every non-numeric symbol is
    # replaced with a valid interval name. We want to keep the contextual
    # information of the chord's nomenclature that gets lost in the conversion
    # to an integer expression. This helps us know which alphabetic names will
    # describe the collection. E.g. 100000101 could be sus2 or susbb3, therefore
    # C, D, G vs. C Ebb G.
    interval_names: set[str] = set("1")
    for symbol in parsed_symbols:
        if symbol in chord_symbols.CHORD_MAJOR_SYMBOL_LIST:
            interval_names |= {chord_symbols.CHORD_3, chord_symbols.CHORD_5}
        elif symbol == chord_symbols.CHORD_MAJ_7:
            interval_names.add(chord_symbols.CHORD_7)
        elif symbol in chord_symbols.CHORD_MINOR_SYMBOL_LIST:
            interval_names |= {
                chord_symbols.CHORD_FLAT_3, chord_symbols.CHORD_5}
        elif symbol in chord_symbols.CHORD_AUGMENTED_SYMBOL_LIST:
            interval_names |= {chord_symbols.CHORD_3,
                               chord_symbols.CHORD_SHARP_5}
        elif symbol in chord_symbols.CHORD_DIMINISHED_SYMBOL_LIST:
            interval_names |= {chord_symbols.CHORD_FLAT_5,
                               chord_symbols.CHORD_FLAT_3}
        elif symbol in suspensions:
            interval_names |= {symbol.replace(
                chord_symbols.CHORD_SUS, ""), chord_symbols.CHORD_5}
        else:
            interval_names.add(symbol)

    for add in add_drop:
        if add in chord_symbols.additive:
            interval_names |= {add.replace(chord_symbols.CHORD_ADD, "")}
        if add in chord_symbols.subtractive and (name := add.replace(chord_symbols.CHORD_NO, "")) in interval_names:
            interval_names.remove(name)

    for symbol in chord_symbols.CHORD_ALTERED_FIFTH_SYMBOL_LIST + [chord_symbols.CHORD_NO + chord_symbols.CHORD_5]:
        if symbol in interval_names and chord_symbols.CHORD_5 in interval_names:
            interval_names.remove(chord_symbols.CHORD_5)

    return (structure, utils.order_interval_names(list(interval_names)))


def parse_slash_chord_symbol(chord_symbol: str) -> tuple[int, tuple[str, ...]]:
    '''
    Parse a chord in 'slash' notation (e.g.: G/Bb, Cm7/Eb).   

    Parameters:
        chord_symbol : A chord in slash notation

    Returns:
        int : An integer representation of an interval map.

    Examples:
        >>> bin(parse_slash_chord_symbol("Gmaj/B")[0])
        '0b100001001'
        >>> bin(parse_slash_chord_symbol("Fmin7b5/Eb")[0])
        '0b100100101'
        >>> bin(parse_slash_chord_symbol("Ab7b5/A")[0])
        '0b101000101001'
    '''
    if chord_symbol.count('/') != 1:
        raise errors.ChordSymbolError(chord_symbol)
    main, bass = chord_symbol.split("/")
    chord_structure, interval_names = parse_chord_symbol(main)
    root, _ = remove_chord_prefix(main)
    root = nomenclature.decode_enharmonic(root)
    bass = nomenclature.decode_enharmonic(bass)
    ch_binomials = nomenclature.chromatic()
    octave = utils.shift_array(ch_binomials, root)
    bass_interval = nomenclature.twelve_tone_scale_intervals()[
        octave.index(bass)]
    chord_note_names = list(rendering.render_plain(chord_structure, octave))
    if bass_interval not in interval_names:
        interval_names = utils.order_interval_names(
            list(interval_names) + [bass_interval])
    if bass not in chord_note_names:
        octave = utils.shift_array(ch_binomials, bass)
        chord_note_names.append(bass)
        chord_note_names = [x for x in octave if x in chord_note_names]

    interval_names = utils.shift_array(interval_names, bass_interval)
    chord_note_names = utils.shift_array(chord_note_names, bass)
    return parse_literal_sequence(chord_note_names), interval_names


def parse_polychord_symbol(chord_symbol: str) -> tuple[int, tuple[str, ...]]:
    '''
    Parse a chord in 'polychord' notation.

    Parameters:
        chord_symbol : A compound symbol consisting of two or more chord 
        symbols separated by the '@' symbol. 

    Returns:
        int : An interval structure corresponding to the given polychord 
        symbol.

    Notes:
        A polychord is entered as a sequence of chord symbols separated by 
        the '@' symbol. Each successive note name in the polychord will be 
        understood as referring to the note name in the previous name's first 
        octave. 

        The '^' symbol can be substituted for a chord symbol in the polychord, 
        indicating that the following chord is to be shifted an octave higher 
        than normal. The symbol can also be compounded to indicate a shift of 
        multiple octaves, e.g. '^^^' means 'shift the next chord 3 octaves up'.

    Examples
        >>> chord = 'Cmaj7@Ebm7b5'
        >>> x = parse_polychord_symbol(chord)[0]
        >>> bin(x)
        '0b10101011011001'
        >>> rendering.render_plain(x)
        ('C', 'D#|Eb', 'E', 'F#|Gb', 'G', 'A', 'B', 'C#|Db')

        This notation can be useful as a shorthand for a scale configuration:
        >>> chord = 'Cmaj7@Dmin'
        >>> x = parse_polychord_symbol(chord)[0]
        >>> bin(x)
        '0b101010110101'
        >>> rendering.render_plain(x)
        ('C', 'D', 'E', 'F', 'G', 'A', 'B')

        The notation can use the "^" symbol to indicate that the next chord 
        should begin in the next octave, not the current octave. The symbol
        can be combined multiple times to increase the gap to the overnext
        octave or farther:
        >>> chord = "Cmaj7b13@Emin7b5@^^@Bbmin7#11"
        >>> x = parse_polychord_symbol(chord)[0]
        >>> bin(x)
        '0b10000000100100010010000000000000100000100110010010001'
        >>> rendering.render_plain(x)
        ('C', 'E', 'G', 'A#|Bb', 'B', 'D', 'G#|Ab', 'A#|Bb', 'C#|Db', 'F', 'G#|Ab', 'E')
    '''
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

        # The polychord octave symbol means 'transpose the next chord so that
        # it begins in the next octave instead of the current octave.'
        # The symbol can also be compounded to transpose multiple octaves.
        if constants.POLYCHORD_OCTAVE_SYMBOL in subchord_symbol:
            octaves = subchord_symbol.count(constants.POLYCHORD_OCTAVE_SYMBOL)
            distance += octaves * 12

        else:
            current_bass, chord_symbol = remove_chord_prefix(subchord_symbol)
            subchord_structure, interval_names = parse_chord_symbol(
                subchord_symbol)
            if constants.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
                current_bass = chord_symbol.split(
                    constants.SLASH_CHORD_DIVIDER_SYMBOL)[-1]

            # First symbol
            if previous_bass == '':
                compiled_structure |= subchord_structure
                previous_bass = nomenclature.decode_enharmonic(current_bass)

            else:
                octave = utils.shift_array(nomenclature.chromatic(
                    constants.BINOMIALS), previous_bass)
                distance += octave.index(
                    nomenclature.decode_enharmonic(current_bass))
                previous_bass = nomenclature.decode_enharmonic(current_bass)
                compiled_structure |= (subchord_structure << distance)
    interval_names = rendering.render_plain(
        compiled_structure, nomenclature.twelve_tone_scale_intervals())
    return compiled_structure, interval_names


def parse_heptatonic_scale_structure(interval_structure: int) -> tuple[str, str]:
    """
    Take an integer of no more than 12 bits, of which exactly 7 are flipped,
    and attempt to assign a name to it.

    Args:
        interval_structure: An integer representing an interval structure.

    Raises:
        errors.HeptatonicScaleError: If the interval structure is invalid.

    Returns:
        [TEMPORARY] - (scale name, mode name)
    """

    if not bitwise.validate_interval_structure(interval_structure, constants.TONES, constants.NOTES):
        raise errors.HeptatonicScaleError
    parent: str = ''
    mode_name: str = ""
    mode: int = 0

    # 9 scales in 7 modes = 63 forms that are easily identifiable with a
    # canonical name.
    for heptatonic_supertype in intervallic_canon.HEPTATONIC_ORDER:
        supertype_modes: tuple[int, ...] = bitwise.inversions(
            heptatonic_supertype, constants.TONES)
        if interval_structure in supertype_modes:
            parent = intervallic_canon.HEPTATONIC_SYSTEM_BY_NUMBER[heptatonic_supertype]
            mode = supertype_modes.index(interval_structure)
            mode_name = keywords.MODAL_SERIES[mode]

            # TODO: THis func should really be returning a more complete
            # report, but this is okay for testing.
            return (parent, mode_name)

    # TODO: Next section should look at scales that are 2 moves away from the
    # heptatonic series, without canonical names

    # Function would continue after this, but for testing, just abort anything
    # that doesn't pass.
    raise errors.HeptatonicScaleError(
        "Cannot find scale <REMOVE THIS ERROR LATER>")


def identify_polyad(interval_structure: int) -> dict[str, str | dict[str, str]]:
    """Attempt to identify an interval structure as a specific chord voicing.
    """
    if interval_structure.bit_count() == 3:
        return identify_triad(interval_structure)
    if interval_structure.bit_count() == 4:
        return identify_tetrad(interval_structure)
    raise UnfinishedFunctionError(interval_structure)


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

    # The first loop only checks the canonical form. This ensures that, if one
    # chord's canonical form could be expressed as an inversion of another
    # chord that comes earlier in the sequence, the canonical form is preferred.
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

    # The first loop only checks the canonical form. This ensures that, if one
    # chord's canonical form could be expressed as an inversion of another
    # chord that comes earlier in the sequence, the canonical form is preferred.
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
    Return a chord symbol for a given interval structure.

    Notes
        This function will understand the structure in the most neutral
        terms, so it cannot capture the enharmonic context of the chord's 
        parent scale.

    Examples:
        >>> parse_interval_structure_as_chord_symbol(0b10010001)
        'maj'
        >>> parse_interval_structure_as_chord_symbol(0b100010001)
        'maj#5'
        >>> parse_interval_structure_as_chord_symbol(0b10001001)
        'min'
        >>> parse_interval_structure_as_chord_symbol(0b100010010010001)
        '9'
        >>> parse_interval_structure_as_chord_symbol(0b100010010001)
        'maj7'
        >>> parse_interval_structure_as_chord_symbol(0b10001001001)
        'min7b5'
        >>> parse_interval_structure_as_chord_symbol(0b100000000010000101)
        'sus2add11'
        >>> parse_interval_structure_as_chord_symbol(0b1000100010010010001)
        '9#11'
    '''
    lower_octave: list[str] = list(nomenclature.twelve_tone_scale_intervals())
    upper_octave: list[str] = ['1', 'b9', '9', '#9',
                               '3', '11', '#11', '5', 'b13', '13', 'b7', '7']

    result = rendering.render_plain(
        interval_structure, lower_octave + upper_octave)
    return parse_interval_names_as_chord_symbol(result)


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
    raise UnfinishedFunctionError


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
    chromatic_ = utils.shift_array(chromatic_, tonic)
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
    rotandum: tuple[str, ...] = utils.shift_array(
        nomenclature.chromatic(), note_names[0])
    interval_structure: int = 1
    distance: int = 0

    # Each note defines the octave in which
    # the next note will be contextualized
    for number, note in enumerate(note_names):
        octave = utils.shift_array(rotandum, note)
        if number < len(note_names) - 1:
            next_note = note_names[number+1]
            distance += octave.index(next_note)
            interval_structure |= (1 << distance)

    return interval_structure


def parse_interval_names_as_chord_symbol(interval_names: Sequence[str]) -> str:
    """Attempt to generate a chord symbol from the given interval names.

    The interval names will be parsed 'as-is', and will neither be resolved 
    into their enharmonic equivalents nor relativized in inversions. We have
    anticipated names for every chord that can be generated by the internal
    canonical scales, but scales outside of our own canon may cause 
    nomenclatural errors. 

    Args:
        interval_names: An array of strings consisting of numbers from 1 to 15,
        possibly modified by the '#' or 'b' symbol.

    Examples:
        >>> parse_interval_names_as_chord_symbol(["1","3","5"])
        'maj'
        >>> parse_interval_names_as_chord_symbol(["1","b3","5"])
        'min'
        >>> parse_interval_names_as_chord_symbol(["1","b3","b5", "b7"])
        'min7b5'
        >>> parse_interval_names_as_chord_symbol(["1","b3","b5", "bb7"])
        'dim7'
        >>> parse_interval_names_as_chord_symbol(["1","3","5","7","9"])
        'maj9'
        >>> parse_interval_names_as_chord_symbol(["1","b3","b5", "bb7", "9", "11"])
        'dim11'
        >>> parse_interval_names_as_chord_symbol(["1","3","7","9"])
        'maj9no5'
        >>> parse_interval_names_as_chord_symbol(["1","bb3","5"])
        'susbb3'
        >>> parse_interval_names_as_chord_symbol(["1","bb3","#5","7"])
        'maj7susbb3#5'
    """
    ###########################################################################
    # March 24, 2024:
    # The function does a pretty good job of naming the common chords in root
    # position, but in order to spell chords from weird heptatonic scales
    # it is unable to recognize enharmonic variants, inversions, and reordered
    # voice chords. It will always parse a chord as if it were a root position
    # expression.
    #
    # The formal sequence of suffixes is taken to be:
    #
    # - root                A note name or Roman interval symbol.
    # - normal3             maj, min
    # - primary_suffix      7, maj7, bb7, dim7
    # - secondary_suffix    6, b6, #6
    # - sus                 sus2, sus4, susbb3, sus#3
    # - alt5                #5, b5
    # - add                 addX, where X is an interval name
    # - no3                 only appears if there is no 3 or sus
    # - no5                 only appears if there is no 5 or alt5
    # - extensions          intervals that can't be added to the primary suffix
    #
    # Examples:
    #
    # Amaj#5        [A]-[maj]-[#5]          [root]-[normal3]-[alt5]
    # Cmin7b5       [C]-[min]-[7]-[b5]      [root]-[normal3]-[primary]-[alt5]
    # G11b13        [G]-[11]-[b13]          [root]-[primary]-[extensions]
    # F#min11b5     [F#]-[min]-[11]-[b5]    [root]-[normal3]-[primary]-[alt5]
    # Abmaj9susbb3  [Ab]-[maj9]-[susbb3]    [root]-[primary]-[sus]
    #
    # In a few cases, the presence of a symbol in one slot triggers the
    # removal of another, so we don't wind up with 'majmaj7' and 'dim7b5'.
    # For a full account of the chord symbol prescription, see the notes at
    # aristoxenus/docs/style_guide.rst.
    ###########################################################################
    interval_names_ = list(interval_names)
    parsed_symbols: list[str] = []
    is_dim: bool = False
    is_dom: bool = False
    normal3: str = ""
    primary_suffix: str = ""
    secondary_suffix: str = ""
    sus: str = ""
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
    suspensions: list[str] = [chord_symbols.CHORD_2,
                              chord_symbols.CHORD_4,
                              chord_symbols.CHORD_DOUBLE_FLAT_3,
                              chord_symbols.CHORD_SHARP_3]
    natural_extensions: list[str] = [chord_symbols.CHORD_9,
                                     chord_symbols.CHORD_11,
                                     chord_symbols.CHORD_13]

    def __finish(symbol: str) -> None:
        interval_names_.remove(symbol)
        parsed_symbols.append(symbol)

    # PRIMARY SUFFIX
    # --------------
    # Does the chord have a primary suffix or a seconday suffix or no suffix?
    # A primary suffix will incorporate the numeral of the highest sequential
    # natural extension, a secondary suffix will not.
    # Primary: Cmaj7 > Cmaj9 > Cmaj11
    # Secondary: Cmaj6 > Cmaj6add9 > Cmaj6add9add11
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
    # Change 7s in the primary suffix from literal to idiomatic values.
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

    # THE MEDIAL
    # ----------
    # Medial is a third: How is the 3rd expressed?
    if chord_symbols.CHORD_3 in interval_names_:
        __finish(chord_symbols.CHORD_3)
        # Shorten symbol for major dominant, but not major 7.
        # C,3,5,7 > Cmaj7 but C,3,5,b7 > C7
        if chord_symbols.CHORD_FLAT_7 not in parsed_symbols:
            normal3 = chord_symbols.CHORD_MAJ
        else:
            is_dom = True
    elif chord_symbols.CHORD_FLAT_3 in interval_names_:
        __finish(chord_symbols.CHORD_FLAT_3)
        # Shorten symbol for diminished seventh, but not minor 7 flat 5.
        # C,b3,b5,bb7 > Cdim7 but C,b3,b5,b7 > Cmin7b5
        if not is_dim:
            normal3 = chord_symbols.CHORD_MIN
    # Are there medials aside from the third?
    if normal3:
        # Secondary medial: C,2,3,5 > Cmajadd2
        for symb in suspensions:
            if symb in interval_names_:
                add += chord_symbols.CHORD_ADD + symb
                __finish(symb)
    else:
        # Medial is a normal suspension: C,2,5 > Csus2
        # Note: This includes chords with altered 3rds, e.g. C,bb3,5 > Csusbb3
        for symb in suspensions:
            if symb in interval_names_:
                sus += chord_symbols.CHORD_SUS + symb
                __finish(symb)
    # Is there no medial at alL?
    if not any([normal3, sus, is_dom, is_dim]):
        no3 = chord_symbols.CHORD_NO + chord_symbols.CHORD_3

    # PRIMARY EXTENSIONS
    # ------------------
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
                if not previous or previous in parsed_symbols:
                    largest_extension = symb
                    __finish(symb)
                else:
                    add += chord_symbols.CHORD_ADD + symb
                    __finish(symb)
    # Update the primary suffix to the last extension in proper sequence.
    # C7,9,11,13 > C13, etc.
    if largest_extension:
        if chord_symbols.CHORD_7 in primary_suffix:
            primary_suffix = primary_suffix.replace(
                chord_symbols.CHORD_7, largest_extension)
    # Add any nonsequential natural extensions that were found.
    # C7,9,13 > C9add13, etc.
    for symb in natural_extensions:
        if symb in interval_names_:
            add += chord_symbols.CHORD_ADD + symb
            __finish(symb)

    # THE FIFTH
    # ---------
    # How is the fifth expressed, if there is one?
    # Altered fifth: C,3,b5,b7 > C7b5
    for symb in altered_fifths:
        if symb in interval_names_:
            alt5 = symb
            __finish(symb)
    # No fifth: C,3,7 > Cmaj7no5
    if chord_symbols.CHORD_5 not in interval_names_:
        if not alt5 and not is_dim:
            alt5 = chord_symbols.CHORD_NO + chord_symbols.CHORD_5
    # Implicit perfect fifth: C,3,5,7 > Cmaj7
    else:
        interval_names_.remove(chord_symbols.CHORD_5)

    # FINALIZE
    # --------
    # Condense symbol: Cmajmaj7 > Cmaj7
    if chord_symbols.CHORD_MAJ in primary_suffix and normal3 == chord_symbols.CHORD_MAJ:
        normal3 = ""
    # An extension without an accidental is easier to read as an addition.
    # C7sus2#11 but C7sus2add11
    # Fminb5b9 but Fminb5add9
    for ex in interval_names_:
        if not any([constants.SHARP_SYMBOL in ex, constants.FLAT_SYMBOL in ex]):
            add += chord_symbols.CHORD_ADD + ex
            ex = ""
    extensions = "".join(interval_names_)
    symbols: list[str] = [normal3,
                          primary_suffix,
                          secondary_suffix,
                          sus,
                          alt5,
                          add,
                          no3,
                          no5,
                          extensions]
    final_form = "".join(symbols)

    return final_form

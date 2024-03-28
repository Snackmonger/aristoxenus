from typing import Sequence
from loguru import logger
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


def split_chord_symbol(chord_symbol: str) -> tuple[str, str]:
    """Return the root and suffix of a chord symbol.

    This function only works on simple chords (i.e. not slash chords
    or polychords).
    """
    # NOTE: If the symbol radical is something other than a note name or Roman
    # numeral, then it is likely to be misunderstood and will probably lead to
    # a mis-parsed chord.
    # E.g. "Kmin7b5" > 1, b5, b7, because "i" counts as a Roman  numeral, so
    # the parser thinks that the radical is "Kmi" and the suffix is "n7b5".

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
            # Get from the beginning to the end of the numeral, in case it
            # is modified by accidental symbols.
            root = chord_symbol[:chord_symbol.index(interval)+len(interval)]
            chord_symbol = chord_symbol.removeprefix(root)
            return root, chord_symbol

    raise errors.ChordNameError(f'Unknown note name: {chord_symbol}.')


def parse_chord_symbol(chord_symbol: str) -> annotations.ChordData:
    """
    Return a set of data representing the information implied in a chord
    symbol.

    Args:
        chord_symbol: A chord symbol, expressed as a string.

    Returns:
        dict {
            chord_symbol: str
            interval_names: tuple[str, ...]
            note_names: tuple[str, ...]
            interval_structure: int
        }

    Examples:
        >>> x = parse_chord_symbol('Cmaj7')
        >>> bin(x["interval_structure"])
        '0b100010010001'
        >>> x["note_names"]
        ('C', 'E', 'G', 'B')
        >>> x["interval_names"]
        ('1', '3', '5', '7')
        >>> x = parse_chord_symbol('CM7')
        >>> bin(x["interval_structure"])
        '0b100010010001'
        >>> x = parse_chord_symbol('CΔ7')
        >>> bin(x["interval_structure"])
        '0b100010010001'
        >>> x = parse_chord_symbol('Cmaj#5')
        >>> bin(x["interval_structure"])
        '0b100010001'
        >>> x["note_names"]
        ('C', 'E', 'G#')
        >>> x["interval_names"]
        ('1', '3', '#5')
        >>> bin(parse_chord_symbol('Caug')["interval_structure"])
        '0b100010001'
        >>> bin(parse_chord_symbol('C+')["interval_structure"])
        '0b100010001'
        >>> bin(parse_chord_symbol('Ebm7b5')["interval_structure"])
        '0b10001001001'
        >>> bin(parse_chord_symbol('Ebmin7b5')["interval_structure"])
        '0b10001001001'
        >>> bin(parse_chord_symbol('Eb-7b5')["interval_structure"])
        '0b10001001001'
        >>> bin(parse_chord_symbol('Ebdimb7')["interval_structure"])
        '0b10001001001'
        >>> bin(parse_chord_symbol('C6/9')["interval_structure"])
        '0b100001010010001'
        >>> bin(parse_chord_symbol('F#dim7')["interval_structure"])
        '0b1001001001'
        >>> bin(parse_chord_symbol('Gm13')["interval_structure"])
        '0b1000100100010010001001'
        >>> bin(parse_chord_symbol('Asus2add11')["interval_structure"])
        '0b100000000010000101'
        >>> bin(parse_chord_symbol('Fmaj13no11')["interval_structure"])
        '0b1000000100100010010001'
        >>> bin(parse_chord_symbol('G7b9')["interval_structure"])
        '0b10010010010001'
        >>> bin(parse_chord_symbol('Fmajsus2')["interval_structure"])
        '0b10000101'
        >>> bin(parse_chord_symbol('Gmaj7susbb3b5')["interval_structure"])
        '0b100001000101'
    """
    # Pre-filter unorthodox symbols that could.
    chord_symbol = chord_symbol.replace("6/9", "69")

    if constants.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
        return parse_slash_chord_symbol(chord_symbol)

    root, suffix = split_chord_symbol(chord_symbol)
    interval_names = parse_chord_suffix(suffix)
    if root in constants.LEGAL_ROOT_NAMES:
        note_names = nomenclature.encode_intervals_as_notes(
            interval_names, root)
    else:
        note_names = utils.romanize_intervals(interval_names)
    interval_structure = convert_interval_names_to_integer(interval_names)

    return annotations.ChordData(
        chord_symbol=chord_symbol,
        interval_names=interval_names,
        note_names=note_names,
        interval_structure=interval_structure
    )


def parse_chord_suffix(chord_symbol: str) -> tuple[str, ...]:
    """Return a list of interval names implied in a chord suffix.

    The names will respect the enharmonic-equivalences implied in the chord
    symbol, so that #2 is distinct from b3, etc.
    """
    suspensions = [chord_symbols.CHORD_SUS_2,
                   chord_symbols.CHORD_SUS_4,
                   chord_symbols.CHORD_SUS_DOUBLE_FLAT_3,
                   chord_symbols.CHORD_SUS_SHARP_3]

    def __remove(affix: str) -> None:
        nonlocal chord_symbol
        chord_symbol = chord_symbol.replace(affix, "")
    parsed_symbols: set[str] = set(["1", "5"])
    subtractive: set[str] = set()

    # Remove all 'add'/'no' modifiers to see what the base symbol is.
    for add in chord_symbols.additive:
        if add in chord_symbol:
            interval = add.replace(chord_symbols.CHORD_ADD, "")
            parsed_symbols.add(interval)
            __remove(add)
    for no in chord_symbols.subtractive:
        if no in chord_symbol:
            subtractive.add(no)
            __remove(no)

    # No suffix = major triad: C, D, E, etc.
    if len(chord_symbol) == 0:
        parsed_symbols.add(chord_symbols.CHORD_3)

    # Powerchord suffix: D5, E5, F5, etc.,
    # (implies a p5 and p8).
    if chord_symbol == chord_symbols.CHORD_5:
        chord_symbol = ""
        parsed_symbols.add(chord_symbols.CHORD_8)

    prefix_modifiers = {
        chord_symbols.CHORD_7: {'1'},  # dummy value; 7 is idiomatic
        chord_symbols.CHORD_9: {chord_symbols.CHORD_9},
        chord_symbols.CHORD_11: {chord_symbols.CHORD_9,
                                 chord_symbols.CHORD_11},
        chord_symbols.CHORD_13: {chord_symbols.CHORD_9,
                                 chord_symbols.CHORD_11,
                                 chord_symbols.CHORD_13}}

    # Parse the implicit meanings in prototypical prefixes.
    for extension, extended_structure in prefix_modifiers.items():
        for symbol in chord_symbols.CHORD_SYMBOL_LIST:
            if chord_symbol.startswith(symbol + extension):
                parsed_symbols |= extended_structure

                # maj7 (or variant) -> maj, maj7, plus extensions
                if symbol in chord_symbols.CHORD_MAJOR_SYMBOL_LIST:
                    __remove(symbol + extension)
                    parsed_symbols.add(chord_symbols.CHORD_7)
                    if chord_symbols.CHORD_SUS not in chord_symbol:
                        parsed_symbols.add(chord_symbols.CHORD_3)

                # dim7 (or variant) -> dim, bb7, plus extensions
                if symbol == chord_symbols.CHORD_DIM:
                    __remove(symbol + extension)
                    parsed_symbols |= {chord_symbols.CHORD_FLAT_3,
                                       chord_symbols.CHORD_FLAT_5,
                                       chord_symbols.CHORD_DOUBLE_FLAT_7}

                # min7 (or variant): ensure that b7 is present
                # if not explicit (e.g. Em11). If symbol has a '7',
                # remove it so it doesn't get interpreted as natural.
                if symbol in chord_symbols.CHORD_MINOR_SYMBOL_LIST:
                    parsed_symbols.add(chord_symbols.CHORD_FLAT_7)
                    __remove(chord_symbols.CHORD_7)

        # 7 (or variant) -> maj, b7, plus extensions
        if chord_symbol.startswith(extension):
            parsed_symbols |= extended_structure | {
                chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_3}
            __remove(extension)

    # First element is another number: C2, C4, C6, etc.
    # implies major triad plus colour tone (different from sus2,
    # sus4, which have no 3rd)
    for symbol in [chord_symbols.CHORD_6,
                   chord_symbols.CHORD_2,
                   chord_symbols.CHORD_4]:
        if chord_symbol.startswith(symbol):
            parsed_symbols.add(chord_symbols.CHORD_3)

    # All remaining sub-symbols in the chord symbol should
    # be plain interval names. Anything that can't be reconciled
    # with the known interval names and aliases will be left out.
    pairs = chord_symbols.symbol_elements.items()
    pairs = sorted(pairs, key=lambda key: len(key[0]), reverse=True)
    for symbol_element, interval in pairs:
        if symbol_element in chord_symbol:
            parsed_symbols.add(symbol_element)
            __remove(symbol_element)

    # The only things that we should expect to remain in the chord symbol
    # are malformed symbols or symbols from systems that haven't been
    # incorporated to the Aristoxenus lists.
    # logger.info(f"Symbols parsed: {parsed_symbols}, remaining chord data: {chord_symbol}")
    # Filter all the parsed symbols to ensure that they are interval names
    # and not special symbols (e.g. "maj")
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

    # If there's any altered fifth, assume that it
    # overrides the implied perfect fifth.
    for symbol in chord_symbols.CHORD_ALTERED_FIFTH_SYMBOL_LIST + [chord_symbols.CHORD_NO + chord_symbols.CHORD_5]:
        if symbol in interval_names and chord_symbols.CHORD_5 in interval_names:
            interval_names.remove(chord_symbols.CHORD_5)

    # If the chord indicated sus, assume that this symbol overrides any
    # symbol indicating a 3rd and remove any thirds.
    for sus in suspensions:
        if sus in parsed_symbols:
            interval_names.discard(chord_symbols.CHORD_3)
            interval_names.discard(chord_symbols.CHORD_FLAT_3)

    # Clean up final result by applying "no" modifiers to remove
    # any unwanted intervals.
    for no in subtractive:
        if (interval := no.replace(chord_symbols.CHORD_NO, "")) in parsed_symbols:
            interval_names -= {interval}

    return utils.order_interval_names(list(interval_names))


def convert_interval_names_to_integer(interval_names: Sequence[str]) -> int:
    """Return an integer representing a binary mapping of the given interval
    names.
    """
    structure = 1
    elements = chord_symbols.symbol_elements.items()
    elements = sorted(elements, key=lambda x: len(x[0]), reverse=True)
    for symbol_element, interval in elements:
        if symbol_element in interval_names:
            structure |= interval
    return structure


def parse_slash_chord_symbol(chord_symbol: str) -> annotations.ChordData:
    """
    Return information parsed from a given slash chord symbol. 

    The slash chord will be rotated to the inversion implied by its bass note,
    rather than simply superimposed over that bass in its root form. If the
    bass note is not a chord tone, then it will be added to the chord in the 
    lower octave, and the chord will be rotated to an 'inversion' beginning
    with that note.

    Args:
        chord_symbol: _description_

    Returns:
        _description_
    """
    if chord_symbol.count('/') != 1:
        raise errors.ChordSymbolError(chord_symbol)

    main, bass = chord_symbol.split("/")
    main_chord_data: annotations.ChordData = parse_chord_symbol(main)
    root, _ = split_chord_symbol(main)
    root_enh = nomenclature.decode_enharmonic(root)
    bass_enh = nomenclature.decode_enharmonic(bass)
    ch_binomials = nomenclature.chromatic()
    octave = utils.shift_array(ch_binomials, root_enh)
    chord_note_names: list[str] = list(main_chord_data[keywords.NOTE_NAMES])
    if bass not in chord_note_names:
        if bass_enh not in [nomenclature.decode_enharmonic(x) for x in chord_note_names]:
            chord_note_names.append(bass)
            i = octave.index(bass_enh)
            bass_interval = nomenclature.twelve_tone_scale_intervals()[i]
        else:
            i = [nomenclature.decode_enharmonic(
                x) for x in chord_note_names].index(bass_enh)
            bass = chord_note_names[i]
            bass_interval = main_chord_data["interval_names"][i]
    else:
        i = chord_note_names.index(bass)
        bass_interval = main_chord_data["interval_names"][i]

    intervals = list(
        set(list(main_chord_data["interval_names"]) + [bass_interval]))
    intervals = utils.order_interval_names(intervals)
    chord_note_names = list(utils.shift_array(sorted(chord_note_names), bass))
    intervals = utils.shift_array(intervals, bass_interval)

    return annotations.ChordData(chord_symbol=chord_symbol,
                                 interval_names=intervals,
                                 note_names=tuple(chord_note_names),
                                 interval_structure=parse_literal_sequence(chord_note_names))


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

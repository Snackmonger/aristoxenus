import sys
import loguru

from data import (chord_symbols,
                  intervallic_canon as intervals,
                  constants,
                  errors,
                  keywords)

from src import (nomenclature,
                 utils,
                 rendering,
                 permutation)

from data.annotations import ChordConspectus


# ----------------------------------------------------------
logger = loguru.logger
logger.add(sys.stderr, format="{time} {level} {message}",
           filter="my_module", level="INFO")
logger.add("file_1.log", rotation="10 MB")
#-----------------------------------------------------------

def __remove_chord_prefix(chord_symbol: str) -> tuple[str, str]:
    '''For a given chord symbol, return a tuple containing: (root, all other symbols).'''
    root: str
    for note in sorted(nomenclature.legal_chord_names(), key=lambda x: len(x), reverse=True):
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
    function does not raise an error, it will always return, at minimum, a p5 
    (that is, 129 = 0b10000001). 

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
    '''
    structure: int = intervals.DIAPENTE

    # Remove contradictory symbol usage of '/'
    # AFAIK, this is the only symbol to conflict with slash notation
    if '6/9' in chord_symbol:
        chord_symbol = chord_symbol.replace('6/9', '69')

    # Delegate special structures to auxiliary functions.
    if constants.POLYCHORD_DIVIDER_SYMBOL in chord_symbol:
        return parse_polychord_symbol(chord_symbol)
    if constants.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
        return parse_slash_chord_symbol(chord_symbol)

    # Root note is not needed beyond this point.
    chord_symbol = __remove_chord_prefix(chord_symbol)[1]

    # Remove all 'add'/'no' modifiers
    # to see what the base symbol is.
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
        return structure | intervals.DITONE

    # Powerchord suffix: D5, E5, F5, etc.,
    # (implies a p5 and p8).
    if chord_symbol == chord_symbols.CHORD_5:
        return structure | intervals.DIAPASON

    parsed_symbols: list[str] = []

    # Parse prototypical prefix, e.g. maj11, min9, 13, etc., and create an
    # explicit list of implicit intervals. Most symbols correspond directly
    # to specific intervals, so it is only necessary to remove those symbols
    # that have positional meanings that get lost in the 1:1 parser below.
    for extension, extended_structure in {chord_symbols.CHORD_7: ['1'], # dummy value: 7 is idiomatic
                                          chord_symbols.CHORD_9: [chord_symbols.CHORD_9],

                                          chord_symbols.CHORD_11: [chord_symbols.CHORD_9,
                                                                   chord_symbols.CHORD_11],

                                          chord_symbols.CHORD_13: [chord_symbols.CHORD_9,
                                                                   chord_symbols.CHORD_11,
                                                                   chord_symbols.CHORD_13]}.items():
        for symbol in chord_symbols.CHORD_SYMBOL_LIST:
            if chord_symbol.startswith(symbol+extension):
                parsed_symbols += extended_structure

                # maj7 (or variant) -> maj, maj7, plus extensions
                if symbol in chord_symbols.CHORD_MAJOR_SYMBOL_LIST:
                    chord_symbol = chord_symbol.removeprefix(symbol+extension)
                    parsed_symbols += [chord_symbols.CHORD_MAJ, chord_symbols.CHORD_MAJ_7]

                # dim7 (or variant) -> dim, bb7, plus extensions
                if symbol == chord_symbols.CHORD_DIM:
                    chord_symbol = chord_symbol.removeprefix(symbol+extension)
                    parsed_symbols += [chord_symbols.CHORD_DIM, chord_symbols.CHORD_DOUBLE_FLAT_7]

                # m7 (or variant): ensure that b7 is present if not explicit (e.g. Em11)
                if symbol in chord_symbols.CHORD_MINOR_SYMBOL_LIST:
                    parsed_symbols += [chord_symbols.CHORD_FLAT_7]

        # 7 (or variant) -> maj, b7, plus extensions
        if chord_symbol.startswith(extension):
            parsed_symbols += extended_structure + [chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_MAJ]
            chord_symbol = chord_symbol.removeprefix(extension)

    # First element is another number: C2, C4, C6, etc.
    # implies major triad plus colour tone (different from sus2, sus4, which have no 3rd)
    for symbol in [chord_symbols.CHORD_6, chord_symbols.CHORD_2, chord_symbols.CHORD_4]:
        if chord_symbol.startswith(symbol):
            parsed_symbols.append(chord_symbols.CHORD_MAJ)

    # By now, we should have an explicit list of all previously implicit
    # intervals, plus any explicit intervals remaining in the chord symbol.
    # (start with longest values to avoid misparsing a subsymbol)
    for symbol_element, interval in sorted(chord_symbols.symbol_elements.items(),
                                           key=lambda key: len(key[0]),
                                           reverse=True):
        # Add intervals to structure
        if symbol_element in chord_symbol or symbol_element in parsed_symbols:
            structure |= interval
            chord_symbol = chord_symbol.replace(symbol_element, '')
            if symbol_element not in parsed_symbols:
                parsed_symbols.append(symbol_element)

    # Check if a symbol overrides the implicit p5 of a chord.
    for symbol in chord_symbols.CHORD_ALTERED_FIFTH_SYMBOL_LIST:
        if symbol in parsed_symbols:
            structure ^= (intervals.DIAPENTE - 1) # 1 = tonic

    # Handle add/no notation
    for symbol in add_drop:
        if symbol in chord_symbols.additive:
            structure |= chord_symbols.additive[symbol]

        elif symbol in chord_symbols.subtractive:
            structure ^= (chord_symbols.subtractive[symbol] - 1)  # 1 = tonic

    if chord_symbol != '':
        logger.info(f'Parsed: {parsed_symbols}, Unparsed: {chord_symbol}')
        
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

    Examples
    --------
    >>> bin(parse_slash_chord_symbol('G/Bb'))
    '''
    if chord_symbol.count('/') != 1:
        raise errors.ChordSymbolError(chord_symbol)

    # TODO: This is broken... Needs fix... you fix now?
    # We want to ensure that, if the bass note is a chord tone, we are using
    # the normal inversion of the chord, rather than transposing with an extra
    # bass note.

    bass: str = nomenclature.decode_enharmonic(chord_symbol.split('/')[1])
    root: str = nomenclature.decode_enharmonic(__remove_chord_prefix(chord_symbol)[0])
    octave_from_bass: list[str] = utils.shift_list(nomenclature.chromatic(), bass)
    octave_from_root: list[str] = utils.shift_list(nomenclature.chromatic(), root)
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
    compiled_structure: int = 1
    subchord_structure: int = 1
    current_bass: str = ''
    previous_bass: str = ''
    distance: int = 0
    octaves: int = 0
    octave: list[str] = []
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
            current_bass, chord_symbol = __remove_chord_prefix(subchord_symbol)
            subchord_structure = parse_chord_symbol(subchord_symbol)
            if constants.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
                current_bass = chord_symbol.split(
                    constants.SLASH_CHORD_DIVIDER_SYMBOL)[-1]
                
            # First symbol
            if previous_bass == '':
                compiled_structure |= subchord_structure
                previous_bass = nomenclature.decode_enharmonic(current_bass)
                
            else:
                octave = utils.shift_list(nomenclature.chromatic(constants.BINOMIALS), previous_bass)
                distance += octave.index(nomenclature.decode_enharmonic(current_bass))
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


def identify_triad(interval_structure: int
                   ) -> dict[str, str | dict[str, str]]:
    '''
    Return the canonical identity of a given triadic interval structure.

    Parameters
    ----------
    interval_structure : int
        An integer of no more than 24 bits, representing a maximum of two
        octaves.

    Returns
    -------
    dict 
        result : str or dict
            The result will either be 'no_match' or a dictionary with the
            following keys:

            chord_identity : str
                The canonical name of the chord structure.
            inversion : str
                The name of the inversion, or root position.
            structure : str
                A description of the chord's structural makeup.

    Examples
    --------
    >>> identify_triad(0b10000000010000001)
    {'result': {'canonical_name': 'major_triad', 'inversion': 'root_position', 'structure': 'open'}}
    >>> identify_triad(0b100001001)
    {'result': {'canonical_name': 'major_triad', 'inversion': 'first_inversion', 'structure': 'close'}} 
    >>> identify_triad(0b10001001)
    {'result': {'canonical_name': 'minor_triad', 'inversion': 'root_position', 'structure': 'close'}}  
    '''
    if interval_structure.bit_length() > (constants.TONES * 2):
        raise ValueError(interval_structure)
    triads: InventoryConspectus  = permutation.triad_variants()

    for triad in triads:
        for kind in [keywords.CLOSE, keywords.OPEN]:
            for inversion, int_structure in triad[kind].items():
                if int_structure == interval_structure:
                    identity = triad[keywords.CANONICAL_NAME]
                    result = {keywords.CANONICAL_NAME: identity,
                              keywords.INVERSION: inversion,
                              keywords.STRUCTURE: kind}
                    return {'result': result}
                
    return {'result': 'no_match'}






def generate_chord_symbol(interval_structure: int,
                          bass_note: str
                          ) -> str:
    '''
    Return a chord symbol for a given interval structure.

    Parameters
    ----------
    interval_structure : int
        An interval structure to be parsed.
    bass_note : str
        The lowest note of the structure (not necessarily the 'root')

    Returns
    -------
    str
        A chord symbol representing the interval structure.

    Notes
    -----
    The interval structure will be parsed *as a chord*, even if its form might
    more typically suggest a scalar structure. This entails that a colour tone
    is treated differently than an extension, and we only transpose intervals
    if they exceed the compass of two octaves.

    The parser will attempt to find the most reasonable name for a chord. In 
    some cases, this means articulating a structure as a slash chord or poly-
    chord so as to avoid an awkward or complicated symbol. 

    See Also
    --------
    `force_chord_symbol`
        Also parses interval structures, but also ensures that the given bass
        note will be considered the root, regardless of awkward nomenclature.

    ''' 

    
def parse_as_jazz_chord(chord_symbol: str, config: dict[str, str|int|bool|float]) -> int:
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
    

def name_heptatonic_intervals(note_names: list[str] | int, comparandum: int = intervals.DIATONIC_SCALE) -> list[str]:
    '''
    For a given collection of note names, return the Indian numerals describing
    the pattern's relation to a given scale.

    Parameters
    ----------
    note_names : list[str] | int
        A list of exactly 7 note names, from the naturals, sharps, flats, or
        binomials; or an integer representing an interval structure not 
        exceeding 12 bits.

    comparandum: int, default=2741
        A integer representing an interval structure to be used as a point 
        of comparison for the given collection. The default value represents
        a major scale.

    Returns
    -------
    list[str]
        A list of numbers modified by the sharp or flat symbol according to
        their relationship to the given scale. 

    Examples
    --------
    >>> name_heptatonic_intervals(['C', 'D', 'Eb', 'Fb', 'Gbb', 'Ab', 'Bb']) 
    ['1', '2', 'b3', 'b4', 'bb5', 'b6', 'b7']

    >>> name_heptatonic_intervals(['C', 'D#', 'E', 'F', 'G#', 'A#', 'B']) 
    ['1', '#2', '3', '4', '#5', '#6', '7']
    '''
    if isinstance(note_names, int):
        note_names = rendering.render_plain(note_names)

    tonic: str = note_names[0]
    binomial_names = list(map(nomenclature.decode_enharmonic, note_names))
    if len(binomial_names) != constants.NOTES:
        raise ValueError('Only works on heptatonic scales.')
    
    chromatic_names: list[str] = utils.shift_list(nomenclature.chromatic(constants.BINOMIALS), tonic)
    major_names: list[str] = rendering.render_plain(comparandum, chromatic_names)
    intervals_: list[str] = []
    for index in range(constants.NOTES):
        expected_note: str = major_names[index]
        given_note: str = binomial_names[index]
        difference: int = chromatic_names.index(given_note) - chromatic_names.index(expected_note)
        accidental: str = constants.SHARP_SYMBOL
        if difference < 0:
            accidental = constants.FLAT_SYMBOL
            difference *= constants.FLAT_VALUE

        intervals_.append((accidental * difference) + str(index + 1))

    return intervals_


def condense_note_names(note_names: list[str]) -> int:
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
        
        Legal names from the naturals, sharps, flats, and binomials (both 
        plain and scientific) will be parsed as binomials, and illegal names 
        will be ignored.

    Returns
    -------
    int
        A 12-bit integer representing all the intervals transposed into a 
        single octave.

    Notes
    -----
    This function is mostly useful when you want to analyse whether a whole
    section of music belongs to a single chord or scale system. Grab all the 
    named notes and reduce them to a single octave to see their simplest 
    structural expression. 

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
        except ValueError:
            pass
    
    tonic: str = simplified_notes[0]
    chromatic_: list[str] = nomenclature.chromatic(constants.BINOMIALS)
    chromatic_ = utils.shift_list(chromatic_, tonic)
    interval_map: int = 1
    for note_name in simplified_notes:
        interval_map |= (1 << chromatic_.index(note_name))
    return interval_map


def parse_literal_sequence(note_names: list[str] | tuple[str, ...]) -> int:
    '''
    Return an integer interval structure based on the specific sequence of notes.

    This function takes a list of notes of any accidental type and uses their
    literal sequence to create an interval structure. This entails that only 
    the enharmonic value and relative position are relevant; a note marked 
    C##3 wil be treated as a higher pitch than A5 if it comes later in the 
    sequence, since these are read as A ... C. Each note defines the octave in
    which the next note will be contextualized (except the last). 

    Parameters
    ----------
    note_names : list[str]
        A list of note names from the naturals, sharps, flats, binomials.
        Scientific variants of these categories will be reduced to their 
        non-scientific equivalents.

    Returns
    -------
    int
        An interval map representing the structure indicated by the sequence
        of note names. 
        
    Notes
    -----
        The structure generated by this function has no theoretical limit; 
        other functions expect limited structures, so check bit-length before 
        passing these structures to functions.
    '''
    note_names = list(map(nomenclature.decode_enharmonic, note_names))
    rotandum: list[str] = utils.shift_list(nomenclature.chromatic(), note_names[0])
    interval_structure: int = 1
    distance: int = 0

    # Each note defines the octave in which
    # the next note will be contextualized
    for number, note in enumerate(note_names):
        octave = utils.shift_list(rotandum, note)
        if number < len(note_names) -1:
            next_note = note_names[number+1]
            distance += octave.index(next_note)
            interval_structure |= (1 << distance)

    return interval_structure







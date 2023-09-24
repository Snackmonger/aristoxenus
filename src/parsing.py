import loguru
import sys

from . import chord_symbols
from . import intervallic_canon as intervals
from . import bitwise
from . import errors
from . import nomenclature
from . import constants
from . import utils
from .models import interval_structures


# ----------------------------------------------------------
logger = loguru.logger
logger.add(sys.stderr, format="{time} {level} {message}",
           filter="my_module", level="INFO")
logger.add("file_1.log", rotation="10 MB")
#-----------------------------------------------------------

def __remove_chord_prefix(chord_symbol: str) -> tuple[str, str]:
    '''For a given chord symbol, return a tuple containing: (root, all other symbols).'''
    root: str
    for note in nomenclature.legal_chord_names():
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
        An integer representation of an interval map.

    Raises
    ------
    ChordNameError
        Raised when the alphabetic chord name is not found in the list defined
        by `nomenclature.legal_chord_names`. This error is actually generated
        by the auxiliary function `parsing.__remove_chord_prefix`.

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
    '''
    structure: int = intervals.DIAPENTE

    # Remove contradictory symbol usage of '/'
    # AFAIK, this is the only symbol to conflict with slash notation
    if '6/9' in chord_symbol:
        chord_symbol = chord_symbol.replace('6/9', '69')

    # Delegate special structures to auxiliary functions.
    if chord_symbols.POLYCHORD_DIVIDER_SYMBOL in chord_symbol:
        return __parse_polychord(chord_symbol)
    if chord_symbols.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
        return __parse_slash_chord(chord_symbol)

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

    # First element is a prototypical prefix (maj11,
    # min9, 13, etc.) implying intervening intervals.
    for extension, extended_structure in {chord_symbols.CHORD_9: intervals.NINTH_CHORD_EXTENSIONS,
                                          chord_symbols.CHORD_11: intervals.ELEVENTH_CHORD_EXTENSIONS,
                                          chord_symbols.CHORD_13: intervals.THIRTEENTH_CHORD_EXTENSIONS}.items():
        for symbol in chord_symbols.CHORD_SYMBOL_LIST:

            # maj7, m7, dim9, aug11, etc.
            if chord_symbol.startswith(symbol+extension):
                structure |= extended_structure

                # maj7 implies natural 7, unless it's the
                # first symbol, which means also add3
                if symbol in chord_symbols.CHORD_MAJOR_SYMBOL_LIST:
                    structure |= intervals.DITONE

        # C7, D7, F#7, etc. implies b7 and 3
        if chord_symbol.startswith(extension):
            structure |= intervals.DITONE | extended_structure

    # First element is another number: C2, C4, C6, etc.
    # (implies major triad)
    for symbol in [chord_symbols.CHORD_6, chord_symbols.CHORD_2, chord_symbols.CHORD_4]:
        if chord_symbol.startswith(symbol):
            structure |= intervals.DITONE

    # Process all remaining recognisable elements
    parsed_symbols: list[str] = []
    for symbol_element, interval in sorted(chord_symbols.symbol_elements.items(),
                                           key=lambda key: len(key[0]),
                                           reverse=True):
        # Add intervals to structure
        if symbol_element in chord_symbol:
            structure |= interval

            # Check if a symbol overrides the implicit p5 of a chord.
            for symbol in ['dim', 'aug', '+', 'b5', '#5']:
                if symbol in chord_symbol:
                    structure ^= (intervals.DIAPENTE - 1)
            chord_symbol = chord_symbol.replace(symbol_element, '')
            parsed_symbols.append(symbol_element)

    # Handle add/no notation
    for symbol in add_drop:
        if symbol in chord_symbols.additive:
            structure |= chord_symbols.additive[symbol]
        elif symbol in chord_symbols.subtractive:
            structure ^= (chord_symbols.subtractive[symbol] - 1)  # 1 = tonic

    return structure


def __parse_slash_chord(chord_symbol: str) -> int:
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
    if chord_symbol.count('/') > 1:
        raise ValueError(
            f'Irregularly formatted chord structure: {chord_symbol}')

    bass: str = chord_symbol.split('/')[1]
    root: str = nomenclature.decode_enharmonic(__remove_chord_prefix(chord_symbol)[0])
    octave_from_bass: list[str] = utils.shift_list(nomenclature.chromatic(constants.BINOMIALS), bass)
    main_chord_structure: int = parse_chord_symbol(chord_symbol.split('/')[0])
    extra_semitones: int = octave_from_bass.index(root)

    return (main_chord_structure << extra_semitones) + 1


def __parse_polychord(chord_symbol: str) -> int:
    '''
    Parse a chord in 'polychord' notation.

    ...

    Notes
    -----
    A polychord is entered as a sequence of chord symbols
    separated by the @ symbol. Each successive chord symbol in 
    the polychord will be understood as referring to the note
    name in the previous symbol's first octave. 

    E.g. 

        Cmaj7@Ebm7b5    ->        0b10101011011001
                    (C0 Eb0 E0 Gb0 G0 Bbb0 B0 Db1)
    '''
    compiled_structure: int = 1
    previous_bass: str = ''
    distance: int = 0
    octave: list[str]
    octaves: int
    subchord_structure: int
    current_bass: str
    
    # Break up the symbol and parse each subchord. For every chord that isn't
    # the first chord, transpose the resulting structure into the range of the
    # previous one.
    for subchord_symbol in chord_symbol.split('@'):

        # The polychord octave symbol means 'transpose the next chord up 1
        # octave'. The symbol can also be compounded to transpose multiple
        # octaves.
        if chord_symbols.POLYCHORD_OCTAVE_SYMBOL in subchord_symbol:
            octaves = subchord_symbol.count(chord_symbols.POLYCHORD_OCTAVE_SYMBOL)
            distance += octaves * 12


        else:
            current_bass, chord_symbol = __remove_chord_prefix(subchord_symbol)
            subchord_structure = parse_chord_symbol(subchord_symbol)
            if chord_symbols.SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
                current_bass = chord_symbol.split(
                    chord_symbols.SLASH_CHORD_DIVIDER_SYMBOL)[-1]
                
            # First symbol
            if previous_bass == '':
                compiled_structure |= subchord_structure
                previous_bass = decode_enharmonic(current_bass)

            else:
                octave = nomenclature.shift_list(chromatic(), previous_bass)
                distance += octave.index(decode_enharmonic(current_bass))
                previous_bass = decode_enharmonic(current_bass)
                compiled_structure |= (subchord_structure << distance)

    return compiled_structure


def parse_heptatonic_scale_structure(interval_structure:int):
    '''
    Take an integer of no more than 12 bits, of which exactly 7 are flipped,
    and attempt to assign a name to it.

    Parameters
    ----------
    scale_structure : int
        _description_

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    HeptatonicScaleError
        _description_
    '''
    
    if interval_structure.bit_length() > 12 or interval_structure.bit_count() != 7:
        raise errors.HeptatonicScaleError
    
    scale: interval_structures.HeptatonicScale = interval_structures.HeptatonicScale(interval_structure)
    inversions: tuple[int, ...] = scale.inversions

    parent: str = ''
    mode: int = 0
    found_parent: bool = False
    for heptatonic_supertype in intervals.HEPTATONIC_ORDER:
        supertype_scale: interval_structures.HeptatonicScale = interval_structures.HeptatonicScale(heptatonic_supertype)
        supertype_modes: tuple[int, ...] = supertype_scale.inversions

        for inversion in inversions:
            if inversion in supertype_modes:
                found_parent = True
                parent = intervals.HEP_DICT[heptatonic_supertype]
                mode = supertype_modes.index(inversion)

    if found_parent is True:
        return (parent, mode)
        
    # Find nearest comparison... starting from the diatonic, 
    # seek out scales that have same structure with X number
    # of mods, and return the scale with the fewest mods.


def identify_triad(interval_structure: int) -> dict[str, int|str]:
    '''
    Return the canonical identity of a given triadic interval structure.

    The function searches through the canonical triads and permutes their
    inversions and spread forms to seek a match for the given structure. 

    Parameters
    ----------
    interval_structure : int
        An integer of no more than 24 bits, representing a maximum of two
        octaves.

    Returns
    -------
    dict 
        chord_identity : str
            The canonical name of the chord structure.
        inversion : int
            The number of rotations the given structure is from the canonical
            structure.
        canonical_form : int
            An integer representing the canonical form that was found.
        structural_mods : list of str
            A list containing any structural modifications that the parser
            identified during analysis. For the triad parser, this is limited
            to 'spread triad'.
    '''




def generate_chord_symbol(interval_structure: int, bass_note: str) -> str:
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
    # NOTE: this is the wrong approach. we should build a system to invert chords and 
    # identify them against canonical types before writing this function...


    symbols: list[str] = []

    # Check major third
    if bitwise.has_interval(interval_structure, intervals.DITONE):


        # Check 7
        if bitwise.has_interval(interval_structure, intervals.COMPOUND_HEMIOLION):

        # Check maj7
        elif bitwise.has_interval(interval_structure, intervals.COMPOUND_DITONE):


        # Check implicit fifth.
        if not bitwise.has_interval(interval_structure, intervals.DIAPENTE):



    # Check minor third
    if bitwise.has_interval(interval_structure, intervals.HEMIOLION):


        # Check 7
        if bitwise.has_interval(interval_structure, intervals.COMPOUND_HEMIOLION):


        # Check implicit fifth.
        if not bitwise.has_interval(interval_structure, intervals.DIAPENTE):

            

    
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

    The highest interval of any chord will be ranked 1
    Any altered fifth will be ranked 2
    A major or minor 3rd will be ranked 3
    A suspended 2 or 4 will be ranked 3 if there is no third, or 7 if there is a third
    A major or b7 will be ranked 4
    A secondary altered extension will be ranked 5
    The root will be ranked 6
    A secondary natural extension will be ranked 7
    A perfect fifth will be ranked 7

    Examples
    --------

    '''
    


    

    


    

        










import loguru
import sys

from .intervallic_canon import *
from .bitwise import has_interval
from .errors import HeptatonicScaleError
from .models.interval_structures import HeptatonicScale

from .vocabulary import (symbol_elements,
                         SLASH_CHORD_DIVIDER_SYMBOL,
                         POLYCHORD_OCTAVE_SYMBOL,
                         POLYCHORD_DIVIDER_SYMBOL,
                         CHORD_SYMBOL_LIST,
                         CHORD_MAJOR_SYMBOL_LIST,
                         CHORD_2,
                         CHORD_4,
                         CHORD_5,
                         CHORD_6,
                         CHORD_9,
                         CHORD_11,
                         CHORD_13)

from .nomenclature import (legal_chord_names,
                           decode_enharmonic,
                           chromatic,
                           shift_list)

# ----------------------------------------------------------
logger = loguru.logger
logger.add(sys.stderr, format="{time} {level} {message}",
           filter="my_module", level="INFO")
logger.add("file_1.log", rotation="10 MB")
#-----------------------------------------------------------

__additive: dict[str, int] = {
    'add' + symbol: interval for symbol, interval in symbol_elements.items()}
__subtractive: dict[str, int] = {
    'no' + symbol: interval for symbol, interval in symbol_elements.items()}


def __remove_chord_prefix(chord_symbol: str) -> tuple[str, str]:
    '''For a given chord symbol, return a tuple containing: (root, all other symbols).'''
    for note in legal_chord_names():
        if note in chord_symbol:
            root = note
            chord_symbol = chord_symbol.removeprefix(note)
            return root, chord_symbol
    raise ValueError('Unknown note name.')


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

    Notes
    -----
    A variety of standard forms are supported. If the parser encounters any
    unrecognized symbol, it simply ignores it, and always returns a result.

    The parser will treat all 'add' and 'no' notations last (even if they are 
    not written last in the chord symbol), so they can be used to make explicit 
    statements and corrections about a chord's structure:

        Em7add9 -> (int) ->  E, G, B, D, F#
        Em7maj9nob3 -> (int) -> E, G#, B, D, F#
    '''
    structure: int = DIAPENTE

    # Remove contradictory symbol usages
    if '6/9' in chord_symbol:
        chord_symbol = chord_symbol.replace('6/9', '69')

    if POLYCHORD_DIVIDER_SYMBOL in chord_symbol:
        return __parse_polychord(chord_symbol)
    if SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
        return __parse_slash_chord(chord_symbol)

    chord_symbol = __remove_chord_prefix(chord_symbol)[1]

    # Remove all 'add'/'no' modifiers
    # to see what the base symbol is.
    add_drop: list[str] = []
    for add in __additive:
        if add in chord_symbol:
            chord_symbol = chord_symbol.replace(add, '')
            add_drop.append(add)
    for drop in __subtractive:
        if drop in chord_symbol:
            chord_symbol = chord_symbol.replace(drop, '')
            add_drop.append(drop)

    # No suffix = major triad: C, D, E, etc.
    if len(chord_symbol) == 0:
        return structure | DITONE

    # Powerchord suffix: D5, E5, F5, etc.,
    # (implies a p5 and p8).
    if chord_symbol == CHORD_5:
        return structure | DIAPASON

    # First element is a prototypical prefix (maj11,
    # min9, 13, etc.) implying intervening intervals.
    for extension, extended_structure in {CHORD_9: NINTH_CHORD_EXTENSIONS,
                                          CHORD_11: ELEVENTH_CHORD_EXTENSIONS,
                                          CHORD_13: THIRTEENTH_CHORD_EXTENSIONS}.items():
        for symbol in CHORD_SYMBOL_LIST:

            # maj7, m7, dim9, aug11, etc.
            if chord_symbol.startswith(symbol+extension):
                structure |= extended_structure

                # maj7 implies natural 7, unless it's the
                # first symbol, which means also add3
                if symbol in CHORD_MAJOR_SYMBOL_LIST:
                    structure |= DITONE

        # C7, D7, F#7, etc. implies b7 and 3
        if chord_symbol.startswith(extension):
            structure |= DITONE | extended_structure

    # First element is another number: C2, C4, C6, etc.
    # (implies major triad)
    for symbol in [CHORD_6, CHORD_2, CHORD_4]:
        if chord_symbol.startswith(symbol):
            structure |= DITONE

    # Process all remaining recognisable elements
    parsed_symbols: list[str] = []
    for symbol_element, interval in sorted(symbol_elements.items(),
                                           key=lambda key: len(key[0]),
                                           reverse=True):
        # Add intervals to structure
        if symbol_element in chord_symbol:
            structure |= interval

            # Check if a symbol overrides the implicit p5 of a chord.
            for symbol in ['dim', 'aug', '+', 'b5', '#5']:
                if symbol in chord_symbol:
                    structure ^= (DIAPENTE - 1)
            chord_symbol = chord_symbol.replace(symbol_element, '')
            parsed_symbols.append(symbol_element)

    # Handle add/no notation
    for symbol in add_drop:
        if symbol in __additive:
            structure |= __additive[symbol]
        elif symbol in __subtractive:
            structure ^= (__subtractive[symbol] - 1)  # 1 = tonic

    return structure


def __parse_slash_chord(slash_chord_symbol: str) -> int:
    '''
    Parse a chord in 'slash' notation (e.g.: G/Bb, Cm7/Eb).   

    Parameters
    ----------
    slash_chord_symbol : str
        A chord in slash notation

    Returns
    -------
    int
        An integer representation of an interval map.
    '''
    if slash_chord_symbol.count('/') > 1:
        raise ValueError(
            f'Irregularly formatted chord structure: {slash_chord_symbol}')

    bass: str = slash_chord_symbol.split('/')[1]
    root: str = decode_enharmonic(__remove_chord_prefix(slash_chord_symbol)[0])
    octave_from_bass: list[str] = shift_list(chromatic(), bass)
    main_chord_structure: int = parse_chord_symbol(slash_chord_symbol.split('/')[0])
    extra_semitones: int = octave_from_bass.index(root)

    return (main_chord_structure << extra_semitones) + 1


def __parse_polychord(polychord_symbol: str) -> int:
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
    current_bass: str
    chord_symbol: str

    for subchord_symbol in polychord_symbol.split('@'):

        if POLYCHORD_OCTAVE_SYMBOL in subchord_symbol:
            octaves: int = subchord_symbol.count(POLYCHORD_OCTAVE_SYMBOL)
            distance += octaves * 12

        else:
            current_bass, chord_symbol = __remove_chord_prefix(subchord_symbol)
            subchord_structure: int = parse_chord_symbol(subchord_symbol)

            if SLASH_CHORD_DIVIDER_SYMBOL in chord_symbol:
                current_bass = chord_symbol.split(
                    SLASH_CHORD_DIVIDER_SYMBOL)[-1]

            # First symbol
            if previous_bass == '':
                compiled_structure |= subchord_structure
                previous_bass = decode_enharmonic(current_bass)

            else:
                octave: list[str] = shift_list(chromatic(), previous_bass)
                distance += octave.index(decode_enharmonic(current_bass))
                previous_bass = decode_enharmonic(current_bass)
                compiled_structure |= (subchord_structure << distance)

    return compiled_structure


def parse_heptatonic_scale_structure(scale_structure:int):
    '''
    Take an integer of no more than 12 bits, of which exactly 7 are flipped,
    and attempt to assign a name to it.    
    '''
    if scale_structure.bit_length() > 12 or scale_structure.bit_count() != 7:
        raise HeptatonicScaleError
    
    scale: HeptatonicScale = HeptatonicScale(scale_structure)
    inversions: tuple[int, ...] = scale.inversions

    parent: str = ''
    mode: int = 0
    found_parent: bool = False
    for heptatonic_supertype in HEPTATONIC_ORDER:
        supertype_scale: HeptatonicScale = HeptatonicScale(heptatonic_supertype)
        supertype_modes: tuple[int, ...] = supertype_scale.inversions

        for inversion in inversions:
            if inversion in supertype_modes:
                found_parent = True
                parent = HEP_DICT[heptatonic_supertype]
                mode = supertype_modes.index(inversion)

    if found_parent is True:
        return (parent, mode)
        
    # Find nearest comparison... starting from the diatonic, 
    # seek out scales that have same structure with X number
    # of mods, and return the scale with the fewest mods.






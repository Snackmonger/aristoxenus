import loguru
import sys

#from . import vocabulary as vcb
from .interval_structures import *
from .vocabulary import symbol_elements, SLASH_CHORD_DIVIDER_SYMBOL, POLYCHORD_OCTAVE_SYMBOL
from .bit_manipulation import has_interval
from .nomenclature import legal_chord_names, decode_enharmonic, chromatic, shift_list


logger = loguru.logger
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add("file_1.log", rotation="5 MB")

__additive: dict[str, int] = {'add' + symbol : interval for symbol, interval in symbol_elements.items()}
__subtractive: dict[str, int] = {'no' + symbol : interval for symbol, interval in symbol_elements.items()}


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
    Return an integer representing a pitch map of a given chord symbol.

    The system outlined here is meant to parse standard chord symbols and
    their variants. The parser will ignore any symbol it can't recognize.

    The parser can get also confused if nonstandard combinations of otherwise
    legal symbols are used:

        Em7maj9 >> (int) >> E, G, G#, B, D, D#, F#

    'maj9' usually appears like Emaj9, where we can safely assume that it
    refers to a chord with a major 3rd and 7th. Em7 refers to a chord with a minor
    3rd and 7th. The parser recognizes both symbols and attempts to supply the 
    intervals that it thinks are implied.

    Similarly, 

    The parser will treat all 'add' and 'no' notations last, so they can
    be used to make explicit statements about a chord's structure:

        Em7add9 >> (int) >>  E, G, B, D, F#
        Em7maj9nob3 >> (int) >> E, G#, B, D, F#
    '''
    structure: int = DIAPENTE
    chord_symbol = chord_symbol.replace('6/9', '69')
    
    if '@' in chord_symbol:
        return __parse_polychord(chord_symbol)
    if '/' in chord_symbol:
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

    # No suffix: C, D, E, etc.
    if len(chord_symbol) == 0:
        return structure | DITONE
    
    # Powerchord: D5, E5, F5, etc.,
    # (implies a p5 and p8).
    if chord_symbol == '5':
        return structure | DIAPASON
    
    # Major7: has natural 3 unless another
    # symbol explicitly contradicts this.
    for symbol in ['maj7', 'M7']:
        mod = DITONE
        if symbol in chord_symbol:
            for symbol_ in ['min', 'm', '-', 'dim']:
                if symbol_ in chord_symbol:
                    mod = HEMIOLION
            if 'sus' in chord_symbol:
                mod = 1
            structure |= mod

    # Major 7 simple extensions.
    # (implies intervening extensions)
    for symbol in ['M9', 'maj9']:
        if symbol in chord_symbol:
            structure = MAJOR_NINTH
    for symbol in ['M11', 'maj11']:
        if symbol in chord_symbol:
            structure = MAJOR_ELEVENTH
    for symbol in ['M13', 'maj13']:
        if symbol in chord_symbol:
            structure = MAJOR_THIRTEENTH
    
    # Minor 7 simple extensions.
    # (implies intervening extensions)
    for symbol in ['m9', 'min9', '-9']:
        if symbol in chord_symbol:
            structure = MINOR_NINTH
    for symbol in ['m11', 'min11', '-11']:
        if symbol in chord_symbol:
            structure = MINOR_ELEVENTH
    for symbol in ['m13', 'min13', '-13']:
        if symbol in chord_symbol:
            structure = MINOR_THIRTEENTH

    # Dominant 7 simple extensions.
    # (implies intervening extensions)
    if chord_symbol.startswith('7'):
        structure = DOMINANT_SEVENTH
    if chord_symbol.startswith('9'):
        structure = DOMINANT_NINTH
    if chord_symbol.startswith('11'):
        structure = DOMINANT_ELEVENTH
    if chord_symbol.startswith('13'):
        structure = DOMINANT_THIRTEENTH

    # Process all remaining recognisable elements
    parsed_symbols: list[str] = []
    for symbol_element, interval in sorted(symbol_elements.items(),
                                           key = lambda key : len(key[0]),
                                           reverse=True):
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
            structure ^= (__subtractive[symbol] - 1) # 1 = tonic

    return structure


def __parse_slash_chord(chord_symbol: str) -> int:
    '''
    Parse a chord in 'slash' notation (e.g.: G/Bb, Cm7/Eb).    
    '''
    if chord_symbol.count('/') > 1:
        raise ValueError(f'Irregularly formatted chord structure: {chord_symbol}')
    root, chord_symbol = __remove_chord_prefix(chord_symbol)
    bass_note: str = chord_symbol.split('/')[1]
    main_chord: str = (root + chord_symbol).split('/')[0]
    octave_from_bass: list[str] = shift_list(chromatic(), bass_note)
    root_binomial: str = decode_enharmonic(root)
    chord_structure: int = parse_chord_symbol(main_chord)
    extra_semitones: int = octave_from_bass.index(root_binomial)

    return (chord_structure << extra_semitones) + 1


def __parse_polychord(chord_symbol: str) -> int:
    '''
    Parse a chord in 'polychord' notation.

    A polychord is entered as a sequence of chord symbols
    separated by the @ symbol. Each successive chord symbol in 
    the polychord will be understood as referring to the note
    name in the previous symbol's first octave. 
    '''
    compiled_structure: int = 1
    previous_bass: str = ''
    distance: int = 0
    current_bass: str
    symbol: str
    
    for chord in chord_symbol.split('@'):
        if POLYCHORD_OCTAVE_SYMBOL in chord:
            octaves:int = chord.count(POLYCHORD_OCTAVE_SYMBOL)
            distance += octaves * 12

        else:
            current_bass, symbol = __remove_chord_prefix(chord)
            structure: int = parse_chord_symbol(chord)

            if SLASH_CHORD_DIVIDER_SYMBOL in symbol:
                current_bass = symbol.split(SLASH_CHORD_DIVIDER_SYMBOL)[-1]

            # First symbol
            if previous_bass == '':
                compiled_structure |= structure
                previous_bass = decode_enharmonic(current_bass)
            else:
                octave: list[str] = shift_list(chromatic(), previous_bass)
                distance += octave.index(decode_enharmonic(current_bass))
                previous_bass = decode_enharmonic(current_bass)
                compiled_structure |= (structure << distance)

    return compiled_structure

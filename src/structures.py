from src import vocabulary as vcb
from src.nomenclature import legal_chord_names

def __second_octave(interval: int) -> int:
    return ((interval - 1) << 12) + 1

# Intervals of an octave.
HEMITONE =              0b11
TONE =                  0b101
HEMIOLION =             0b1001
DITONE =                0b10001
DIATESSARON =           0b100001
TRITONE =               0b1000001
DIAPENTE =              0b10000001
COMPOUND_HEMITONE =     0b100000001
COMPOUND_TONE =         0b1000000001
COMPOUND_HEMIOLION =    0b10000000001
COMPOUND_DITONE =       0b100000000001
DIAPASON =              0b1000000000001

# Divisions of the single octave.
# -------------------------------

# Basic triads.
MAJOR_TRIAD = DITONE | DIAPENTE
MINOR_TRIAD = HEMIOLION | DIAPENTE
DIMINISHED_TRIAD = HEMIOLION | TRITONE
AUGMENTED_TRIAD = DITONE | COMPOUND_HEMITONE
MAJOR_FLAT_5 = DITONE | TRITONE
SUS2 = TONE | DIAPENTE
SUS4 = DIATESSARON | DIAPENTE

# Basic tetrads.
MAJOR_SIXTH = MAJOR_TRIAD | COMPOUND_TONE
MINOR_SIXTH = MINOR_TRIAD | COMPOUND_TONE
MAJOR_SEVENTH = MAJOR_TRIAD | COMPOUND_DITONE
MINOR_SEVENTH = MINOR_TRIAD | COMPOUND_HEMIOLION
DOMINANT_SEVENTH = MAJOR_TRIAD | COMPOUND_HEMIOLION
MINOR_SEVEN_FLAT_FIVE = DIMINISHED_TRIAD | COMPOUND_HEMIOLION
DIMINISHED_SEVENTH = DIMINISHED_TRIAD | COMPOUND_TONE
AUGMENTED_SEVENTH = AUGMENTED_TRIAD | COMPOUND_HEMIOLION
AUGMENTED_MAJOR_SEVENTH = AUGMENTED_TRIAD | COMPOUND_DITONE
DOMINANT_SEVENTH_FLAT_FIVE = MAJOR_FLAT_5 | COMPOUND_HEMIOLION

# Divisions of the double octave.
# -------------------------------

# Basic pentads, hexads, heptads.
MAJOR_NINTH = MAJOR_SEVENTH | __second_octave(TONE)
MINOR_NINTH = MINOR_SEVENTH | __second_octave(TONE)
DOMINANT_NINTH = DOMINANT_SEVENTH | __second_octave(TONE)
DOMINANT_SEVENTH_FLAT_NINE = DOMINANT_SEVENTH | __second_octave(HEMITONE)
DOMINANT_SEVENTH_SHARP_NINE = DOMINANT_SEVENTH | __second_octave(HEMIOLION)
MAJOR_ELEVENTH = MAJOR_NINTH | __second_octave(DIATESSARON)
MINOR_ELEVENTH = MINOR_NINTH | __second_octave(DIATESSARON)
DOMINANT_ELEVENTH = DOMINANT_NINTH | __second_octave(DIATESSARON)
MAJOR_THIRTEENTH = MAJOR_ELEVENTH | __second_octave(COMPOUND_TONE)
MINOR_THIRTEENTH = MINOR_ELEVENTH | __second_octave(COMPOUND_TONE)
DOMINANT_THIRTEENTH = DOMINANT_ELEVENTH | __second_octave(COMPOUND_TONE)

# TODO: Unicode symbols for diminished, half diminished, major triangle

symbol_elements: dict[str, int] = {
        'b2': HEMITONE,
        '2': TONE,
        'sus2': SUS2,
        'sus4': SUS4,
        'b3': HEMIOLION,
        '-': HEMIOLION,
        'm': HEMIOLION,
        'min': HEMIOLION,
        'M': DITONE,
        'maj': DITONE,
        'b4': DITONE,
        '4': DIATESSARON,
        '#4': TRITONE,
        'b5': TRITONE,
        '5': DIAPENTE,
        'dim': DIMINISHED_TRIAD,
        'dim7': DIMINISHED_SEVENTH,
        '#5': COMPOUND_HEMITONE,
        'aug5': COMPOUND_HEMITONE,
        'aug': COMPOUND_HEMITONE,
        '+': COMPOUND_HEMITONE,
        'b6': COMPOUND_HEMITONE,
        '6': COMPOUND_TONE,
        '#6': COMPOUND_HEMIOLION,
        'b7': COMPOUND_HEMIOLION,
        '7': COMPOUND_HEMIOLION,
        'maj7': COMPOUND_DITONE,
        'M7': COMPOUND_DITONE,
        '8': DIAPASON,
        'b9': __second_octave(HEMITONE),
        '9': __second_octave(TONE),
        'b10': __second_octave(HEMIOLION),
        '10': __second_octave(DITONE),
        'b11': __second_octave(DITONE),
        '11': __second_octave(DIATESSARON),
        '#11': __second_octave(TRITONE),
        'b12': __second_octave(TRITONE),
        '12': __second_octave(DIAPENTE),
        'b13': __second_octave(COMPOUND_HEMITONE),
        '13': __second_octave(COMPOUND_TONE),
        '#13': __second_octave(COMPOUND_HEMIOLION),
        'b14': __second_octave(COMPOUND_HEMIOLION),
        '14': __second_octave(COMPOUND_DITONE),
        '15': __second_octave(DIAPASON)
        }

__additive: dict[str, int] = {'add' + symbol : interval for symbol, interval in symbol_elements.items()}
__subtractive: dict[str, int] = {'no' + symbol : interval for symbol, interval in symbol_elements.items()}


def has_hemitone(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a hemitone above the tonic.
    '''
    return HEMITONE & pitch_collection == HEMITONE


def has_tone(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a tone above the tonic.
    '''
    return TONE & pitch_collection == TONE


def has_hemiolion(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a hemiolion above the tonic. 
    '''
    return HEMIOLION & pitch_collection == HEMIOLION


def has_ditone(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a ditone above the tonic.
    '''
    return DITONE & pitch_collection == DITONE


def has_diatessaron(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a diatessaron above the tonic.
    '''
    return DIATESSARON & pitch_collection == DIATESSARON


def has_tritone(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a tritone above the tonic.
    '''
    return TRITONE & pitch_collection == TRITONE


def has_diapente(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a diapente above the tonic.
    '''
    return DIAPENTE & pitch_collection == DIAPENTE


def has_compound_hemitone(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a compound hemitone above 
    the tonic.
    '''
    return COMPOUND_HEMITONE & pitch_collection == COMPOUND_HEMITONE


def has_compound_tone(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a compound tone above the 
    tonic.
    '''
    return COMPOUND_TONE & pitch_collection == COMPOUND_TONE


def has_compound_hemiolion(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a compound hemiolion above 
    the tonic.
    '''
    return COMPOUND_HEMIOLION & pitch_collection == COMPOUND_HEMIOLION


def has_compound_ditone(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a compound ditone above the 
    tonic.
    '''
    return COMPOUND_DITONE & pitch_collection == COMPOUND_DITONE


def has_diapason(pitch_collection: int):
    '''
    Return true if the pitch collection 
    contains a diapason above the 
    tonic.
    '''
    return COMPOUND_TONE & pitch_collection == COMPOUND_TONE



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
    # Remove letter name. If the chord symbol attempts to
    # use an ambiguous notation like Cb6, we assume that
    # this means Cb 6 chord, not C b6 chord.
    root: str = ''
    base: int = 1
    for note in legal_chord_names():
        if note in chord_symbol:
            root = note
            chord_symbol = chord_symbol.removeprefix(note)

    # Check slash & polychord notation
    if '@' in chord_symbol:
        return parse_polychord(root + chord_symbol)
    elif '/' in chord_symbol:
        return parse_slash_chord(root + chord_symbol)

    # Remove all add/no modifiers to see what the base chord is.
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
        return MAJOR_TRIAD
    
    # Powerchord: D5, E5, F5, etc.
    # (implies a p5 and p8)
    if chord_symbol == '5':
        return DIAPENTE | DIAPASON
    
    # Major 7 simple extensions.
    # (implies intervening extensions)
    for symbol in ['M9', 'maj9']:
        if symbol in chord_symbol:
            base = MAJOR_NINTH
    for symbol in ['M11', 'maj11']:
        if symbol in chord_symbol:
            base = MAJOR_ELEVENTH
    for symbol in ['M13', 'maj13']:
        if symbol in chord_symbol:
            base = MAJOR_THIRTEENTH
    
    # Minor 7 simple extensions.
    # (implies intervening extensions)
    for symbol in ['m9', 'min9', '-9']:
        if symbol in chord_symbol:
            base = MINOR_NINTH
    for symbol in ['m11', 'min11', '-11']:
        if symbol in chord_symbol:
            base = MINOR_ELEVENTH
    for symbol in ['m13', 'min13', '-13']:
        if symbol in chord_symbol:
            base = MINOR_THIRTEENTH

    # Dominant 7 and simple extensions
    # (implies intervening extensions)
    if chord_symbol.startswith('7'):
        base = DOMINANT_SEVENTH
    if chord_symbol.startswith('9'):
        base = DOMINANT_NINTH
    if chord_symbol.startswith('11'):
        base = DOMINANT_ELEVENTH
    if chord_symbol.startswith('13'):
        base = DOMINANT_THIRTEENTH

    parsed_symbols: list[str] = []
    explicit_fifth: bool = False

    # Process all remaining recognisable elements
    # (longest first, to avoid misidentifying)
    for symbol_element, interval in sorted(symbol_elements.items(),
                                           key = lambda key : len(key[0]),
                                           reverse=True):
        if symbol_element in chord_symbol:
            base |= interval
            for symbol in ['5', 'dim', 'aug', '+']:
                if symbol in chord_symbol:
                    explicit_fifth = True
            chord_symbol = chord_symbol.replace(symbol_element, '')
            parsed_symbols.append(symbol_element)

    # If the symbol could imply a p5 and
    # no 5th is indicated, infer a p5 now.
    if not has_diapente(base) and not explicit_fifth:
        base |= DIAPENTE

    # Handle add/no notation
    for symbol in add_drop:
        if symbol in __additive:
            base |= __additive[symbol]
        elif symbol in __subtractive:
            base &= (~__subtractive[symbol] - 1) # 1 = tonic

    return base


def parse_slash_chord(chord_symbol: str) -> int:
    '''
    Parse a chord in 'slash' notation (e.g.: G/Bb, Cm7/Eb). 

    Slash notation is used to indicate BASS NOTES, not (as is sometimes
    done) to indicate polychords. 
    
    A slash chord consists of a chord symbol separated from a note name by the '/' symbol.
    The chord symbol should be a simple recognizable symbol for the sake of the engine,
    but in theory it could be anything. Mostly the slash notation is meant to relieve 
    the necessity of spelling out an unusual structure explicitly (e.g.: G/B = Bmb6no5), 
    so we don't expect to have to parse stupid symbols like Bmb6no5/G. 

    If the chord symbol gives a colour or an extension that is enharmonic with
    the given slash note, it will be ignored.
    
    '''
    return 0

def parse_polychord(chord_symbol: str) -> int:
    '''
    A polychord is entered as a sequence of chord symbols
    separated by the @ symbol. Each successive chord symbol in 
    the polychord will be understood as referring to the note
    name in the previous symbol's first octave. 

    Therefore, a polychord can indicate a multi-octave voicing:

        C@B7@F#m7
        >> 0b1000100100010001001001001001 

    This translates to:
        C E G @ B D# F# A @ (F# A) C Eb

    C: The octave begins with a major chord (10001001)

    B7: The note name of the next chord symbol is located within the 
    octave in which the previous chord began. This is now defined
    as the starting note of the next chord: dominant 7 chord
    (10001001001). 

    F#m: the note name of the next chord symbol is located within the
    octave in which the previous chord began, but because these notes
    represent intervals that are already in the chord, they can't be 
    added again. Still, the note serves as a starting point for the 
    next chord: minor 7 chord (100100001001)

    The whole compass of the expression C@B7@F#m7 is a minor eighteenth,
    or 28 semitones. Polychords can be used to make theoretical pitch
    structures of any size (stored as integers), but the renderer may
    not be able to display them if they exceed B8 as the highest note.   

    Because of this flexibility, we can also indicate large voicings like
    those of a piano, in which the two hands are separated by an octave or more.
    For these situations, the ^ character means 'start the following chord
    an octave higher than usual':

        C5@^@Eno3no5
        >>  100000010000000001
    This translates to a root-position major spread triad (C, G, ^E) with
    the compass of a major tenth. Accurately rendering these structures
    requires a multi-octave style.
    '''
    return 0

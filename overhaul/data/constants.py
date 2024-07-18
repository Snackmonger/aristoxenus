'''Constants used in the program.'''
##############
# Raw Values #
##############

NOTES = 7
TONES = 12
NATURAL_NAMES = "CDEFGAB"
OCTAVE_EQUIVALENCE_FACTOR = 2
FREQUENCY_DECIMAL_LIMIT = 3
CENTRAL_REFERENCE_NOTE_NAME = 'A4'
CENTRAL_REFERENCE_NOTE_FREQUENCY = 440
FLAT_SYMBOL = "b"
SHARP_SYMBOL = '#'




############
# Keywords #
############
# Our Canon Heptatonic Scale Names
DIATONIC = 'diatonic'
ALTERED = 'altered'
HEMITONIC = 'hemitonic'
HEMIOLIC = 'hemiolic'
DIMINISHED = 'diminished'
AUGMENTED = 'augmented'
HARMONIC = 'harmonic'
BISEPTIMAL = 'biseptimal'
PALEOCHROMATIC = 'paleochromatic'
# Internal canonical order of scale types
HEPTATONIC_ORDER_KEYS = (
    DIATONIC,
    ALTERED,
    HEMITONIC,
    HEMIOLIC,
    DIMINISHED,
    AUGMENTED,
    HARMONIC,
    BISEPTIMAL,
    PALEOCHROMATIC
)
# Other Scale Names
ENIGMATIC = 'enigmatic'
NEAPOLITAN_MAJOR = 'neapolitan_major'
NEAPOLITAN_MINOR = 'neapolitan_minor'
HUNGARIAN = 'hungarian'
HARMONIC_MINOR = 'harmonic_minor'
# Internal scale processing terms
PREFERRED_NAME = 'preferred_name'
CANONICAL_NAME = 'canonical_name'
CANONICAL_FORM = 'canonical_form'
BINOMIAL_RENDERING = 'binomial_rendering'
TWELVE_TONE_INTERVALS = "twelve_tone_intervals"
FORCED_RENDERING = 'forced_rendering'
BEST_RENDERING = 'best_rendering'
BEST_KEYNOTE = 'best_keynote'
RECOGNIZED_NAMES = 'recognized_names'
# Modal names
IONIAN = 'ionian'
DORIAN = 'dorian'
PHRYGIAN = 'phrygian'
LYDIAN = 'lydian'
MIXOLYDIAN = 'mixolydian'
AEOLIAN = 'aeolian'
LOCRIAN = 'locrian'
# Modal names in order
MODAL_SERIES_KEYS = (
    IONIAN,
    DORIAN,
    PHRYGIAN,
    LYDIAN,
    MIXOLYDIAN,
    AEOLIAN,
    LOCRIAN
)
# Chord terms
ROOT = 'root'
POSITION = 'position'
ROOT_POSITION = 'root_position'
INVERSION = 'inversion'
OPEN = 'open'
CLOSE = 'close'
CHORD_SYMBOL = 'chord_symbol'
CHORD_NAME = 'chord_name'
DROP_2 = 'drop_2'
DROP_3 = 'drop_3'
DROP_2_AND_4 = 'drop_2_and_4'
# Triad types
MAJOR_TRIAD = 'major_triad'
MINOR_TRIAD = 'minor_triad'
MINOR_FLAT_5 = 'minor_flat_5_triad'
MAJOR_FLAT_5 = 'major_flat_5_triad'
MAJOR_SHARP_5 = 'major_sharp_5_triad'
SUS2_TRIAD = 'sus2_triad'
SUS4_TRIAD = 'sus4_triad'
# Tetrad types
MAJOR_SEVENTH = 'major_7'
MINOR_SEVENTH = 'minor_7'
MAJOR_SIXTH = 'major_6'
MINOR_SIXTH = 'minor_6'           
MINOR_MAJOR_SEVENTH = 'minor_major_7'
DOMINANT_SEVENTH = 'dominant_7'
MINOR_SEVEN_FLAT_FIVE = 'minor_7_flat_5'
DIMINISHED_SEVENTH = 'diminished_7'
AUGMENTED_SEVENTH = 'augmented_7'
AUGMENTED_MAJOR_SEVENTH = 'augmented_major_7'
DOMINANT_SEVENTH_FLAT_FIVE = 'dominant_7_flat_5'
# Numeration Terms
CARDINAL = 'cardinal'
ORDINAL = 'ordinal'
UPLE = 'uple'
POLYAD = 'polyad'
TONAL = 'tonal'
BASAL = 'basal'

# Chord Parsing Keywords
NOTE_NAME = 'note_name'
ACCIDENTALS = 'accidentals'
SUFFIX = 'suffix'
PRIMARY_SUFFIX = 'primary_suffix'
ADD_SUFFIX = 'add_suffix'
NO_SUFFIX = 'no_suffix'
SUS_SUFFIX = 'sus_suffix'




##############
# Scaleforms #
##############
HEPTATONIC_SCALES = {
    DIATONIC: [0, 2, 4, 5, 7, 9, 11],
    ALTERED: [0, 1, 3, 4, 6, 8, 10],
    HEMITONIC: [0, 1, 4, 5, 7, 9, 11],
    HEMIOLIC: [0, 3, 4, 5, 7, 9, 11],
    DIMINISHED: [0, 2, 4, 5, 6, 9, 11],
    AUGMENTED: [0, 2, 4, 6, 7, 9, 11],
    BISEPTIMAL: [0, 2, 4, 5, 7, 10, 11],
    PALEOCHROMATIC: [0, 1, 4, 5, 6, 9, 11]
}
HEPTATONIC_SUPPLEMENT = {
    ENIGMATIC: [0, 1, 4, 6, 8, 10, 11],
    NEAPOLITAN_MINOR: [0, 1, 3, 5, 7, 8, 11],
    NEAPOLITAN_MAJOR: [0, 1, 3, 5, 7, 9, 11],
    HUNGARIAN: [0, 2, 3, 6, 7, 8, 11],
    HARMONIC_MINOR: [0, 2, 3, 5, 7, 8, 11]
}
NATURAL_MAP = tuple(
    (HEPTATONIC_SCALES[DIATONIC][i], NATURAL_NAMES[i]) for i in range(7)
)

##############
# Chordforms #
##############
# Simple symbols
CHORD_DIM = 'dim'
CHORD_AUG = 'aug'
CHORD_MAJ = 'maj'
CHORD_MAJ_DELTA = 'Δ'
CHORD_HALFDIM_OE = 'ø'
CHORD_MIN = 'min'
CHORD_M_UPPER = 'M'
CHORD_M_LOWER = 'm'
CHORD_PLUS = '+'
CHORD_MINUS = '-'
CHORD_SUS = 'sus'
CHORD_ADD = 'add'
CHORD_NO = 'no'
CHORD_2 = '2'
CHORD_3 = '3'
CHORD_4 = '4'
CHORD_5 = '5'
CHORD_6 = '6'
CHORD_7 = '7'
CHORD_8 = '8'
CHORD_9 = '9'
CHORD_10 = '10'
CHORD_11 = '11'
CHORD_12 = '12'
CHORD_13 = '13'
CHORD_14 = '14'
CHORD_15 = '15'
# Compound Symbols
CHORD_FLAT_2 = FLAT_SYMBOL + CHORD_2
CHORD_SUS_2 = CHORD_SUS + CHORD_2
CHORD_DOUBLE_FLAT_3 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_3
CHORD_SUS_DOUBLE_FLAT_3 = CHORD_SUS + CHORD_DOUBLE_FLAT_3
CHORD_SHARP_2 = SHARP_SYMBOL + CHORD_2
CHORD_FLAT_3 = FLAT_SYMBOL + CHORD_3
CHORD_SHARP_3 = SHARP_SYMBOL + CHORD_3
CHORD_SUS_SHARP_3 = CHORD_SUS + CHORD_SHARP_3
CHORD_FLAT_4 = FLAT_SYMBOL + CHORD_4
CHORD_SUS_4 = CHORD_SUS + CHORD_4
CHORD_SHARP_4 = SHARP_SYMBOL + CHORD_4
CHORD_FLAT_5 = FLAT_SYMBOL + CHORD_5
CHORD_SHARP_5 = SHARP_SYMBOL + CHORD_5
CHORD_AUG_5 = CHORD_AUG + CHORD_5
CHORD_DIM_5 = CHORD_DIM + CHORD_5
CHORD_FLAT_6 = FLAT_SYMBOL + CHORD_6
CHORD_SHARP_6 = SHARP_SYMBOL + CHORD_6
CHORD_FLAT_7 = FLAT_SYMBOL + CHORD_7
CHORD_MAJ_7 = CHORD_MAJ + CHORD_7
CHORD_DIM_7 = CHORD_DIM + CHORD_7
CHORD_M7_UPPER = CHORD_M_UPPER + CHORD_7
CHORD_MAJ_DELTA7 = CHORD_MAJ_DELTA + CHORD_7
CHORD_DOUBLE_FLAT_7 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_7
CHORD_FLAT_9 = FLAT_SYMBOL + CHORD_9
CHORD_SHARP_9 = SHARP_SYMBOL + CHORD_9
CHORD_FLAT_10 = FLAT_SYMBOL + CHORD_10
CHORD_SHARP_10 = SHARP_SYMBOL + CHORD_10
CHORD_SHARP_11 = SHARP_SYMBOL + CHORD_11
CHORD_FLAT_11 = FLAT_SYMBOL + CHORD_11
CHORD_FLAT_12 = FLAT_SYMBOL + CHORD_12
CHORD_SHARP_12 = SHARP_SYMBOL + CHORD_12
CHORD_SHARP_13 = SHARP_SYMBOL + CHORD_13
CHORD_FLAT_13 = FLAT_SYMBOL + CHORD_13
CHORD_SHARP_14 = SHARP_SYMBOL + CHORD_14
CHORD_FLAT_14 = FLAT_SYMBOL + CHORD_14
# Groups of chord symbols that serve as bases for extended chords (maj9,
# dim11, etc.) that have non-explicit structures (e.g. maj13 also implies
# 9 and 11)
CHORD_MAJOR_SYMBOL_LIST = [
    CHORD_MAJ,
    CHORD_MAJ_DELTA,
    CHORD_M_UPPER
]
CHORD_MINOR_SYMBOL_LIST = [
    CHORD_MIN,
    CHORD_M_LOWER,
    CHORD_MINUS
]
CHORD_AUGMENTED_SYMBOL_LIST = [
    CHORD_AUG,
    CHORD_PLUS,
    CHORD_AUG_5
]
CHORD_DIMINISHED_SYMBOL_LIST = [
    CHORD_DIM,
    CHORD_DIM_5
]
CHORD_SYMBOL_LIST = CHORD_MAJOR_SYMBOL_LIST + \
    CHORD_MINOR_SYMBOL_LIST + \
    CHORD_AUGMENTED_SYMBOL_LIST + \
    CHORD_DIMINISHED_SYMBOL_LIST
# Chord symbols for which we normally expect NOT to have a p5
CHORD_ALTERED_FIFTH_SYMBOL_LIST = CHORD_AUGMENTED_SYMBOL_LIST + \
    CHORD_DIMINISHED_SYMBOL_LIST + \
    [
        CHORD_FLAT_5,
        CHORD_SHARP_5
    ]
# Mapping of interval values to interval names.
INTERVAL_TO_POSSIBLE_SYMBOLS_MAP = {
    1: [CHORD_FLAT_2],
    2: [CHORD_2, CHORD_SUS_2, CHORD_SUS_DOUBLE_FLAT_3, CHORD_DOUBLE_FLAT_3],
    3: [CHORD_SHARP_2, CHORD_FLAT_3] + CHORD_MINOR_SYMBOL_LIST,
    4: [CHORD_3, CHORD_FLAT_4] + CHORD_MAJOR_SYMBOL_LIST,
    5: [CHORD_SUS_4, CHORD_4, CHORD_SUS_SHARP_3, CHORD_SHARP_3],
    6: [CHORD_SHARP_4, CHORD_FLAT_5],
    7: [CHORD_5],
    8: [CHORD_SHARP_5, CHORD_FLAT_6],
    9: [CHORD_6, CHORD_DOUBLE_FLAT_7],
    10: [CHORD_FLAT_7, CHORD_SHARP_6],
    11: [CHORD_7, CHORD_MAJ_7, CHORD_M7_UPPER, CHORD_MAJ_DELTA7],
    12: [CHORD_8],
    13: [CHORD_FLAT_9],
    14: [CHORD_9],
    15: [CHORD_SHARP_9, CHORD_FLAT_10],
    16: [CHORD_10, CHORD_FLAT_11],
    17: [CHORD_11, CHORD_SHARP_10],
    18: [CHORD_SHARP_11, CHORD_FLAT_12],
    19: [CHORD_12],
    20: [CHORD_FLAT_13, CHORD_SHARP_12],
    21: [CHORD_13],
    22: [CHORD_SHARP_13, CHORD_FLAT_14],
    23: [CHORD_14],
    24: [CHORD_15]
}
# Mapping of interval names to interval values.
SYMBOL_TO_INTERVAL_MAP = {
    symbol: interval for interval, symbols in INTERVAL_TO_POSSIBLE_SYMBOLS_MAP.items() for symbol in symbols}
# Mapping of add2, add11, etc. keys to the indicated interval value.
ADD_SYMBOLS = {
    CHORD_ADD + symbol: interval for symbol, interval in SYMBOL_TO_INTERVAL_MAP.items()}
# Mapping of no3, no5, etc. keys to the indicated interval value.
DROP_SYMBOLS = {
    CHORD_NO + symbol: interval for symbol, interval in SYMBOL_TO_INTERVAL_MAP.items()}
# Chord name : chord symbol
TRIADS_KEY_TO_SYMBOL_MAP = {
    MAJOR_TRIAD: CHORD_MAJ,
    MINOR_TRIAD: CHORD_MIN,
    MINOR_FLAT_5: CHORD_MIN + CHORD_FLAT_5,
    MAJOR_FLAT_5: CHORD_MAJ + CHORD_FLAT_5,
    MAJOR_SHARP_5: CHORD_MAJ + CHORD_SHARP_5,
    SUS2_TRIAD: CHORD_SUS_2,
    SUS4_TRIAD: CHORD_SUS_4
}
TETRADS_KEY_TO_SYMBOL_MAP = {
    MAJOR_SEVENTH: CHORD_MAJ_7,
    MINOR_SEVENTH: CHORD_MIN + CHORD_7,
    MAJOR_SIXTH: CHORD_MAJ + CHORD_6,
    MINOR_SIXTH: CHORD_MIN + CHORD_6,
    MINOR_MAJOR_SEVENTH: CHORD_MIN + CHORD_MAJ_7,
    DOMINANT_SEVENTH: CHORD_7,
    DOMINANT_SEVENTH_FLAT_FIVE: CHORD_7 + CHORD_FLAT_5,
    DIMINISHED_SEVENTH: CHORD_DIM_7,
    AUGMENTED_MAJOR_SEVENTH: CHORD_MAJ_7 + CHORD_SHARP_5,
    AUGMENTED_SEVENTH: CHORD_7 + CHORD_SHARP_5,
    MINOR_SEVEN_FLAT_FIVE: CHORD_MIN + CHORD_7 + CHORD_FLAT_5
}

#######################
# Regular Expressions #
#######################
RE_VALIDATE_NOTE_NAME = '^[A-G](#|b)*$'
RE_VALIDATE_INTERVAL_SYMBOL = '^(#|b)*[1234567]$'
RE_SPLIT_NOTE_NAME = f"(?P<{NOTE_NAME}>[A-G])(?P<{ACCIDENTALS}>(#|b)*)"
# Chord Parsing
RE_SPLIT_CHORD_SYMBOL = f"(?P<{ROOT}>[A-G](#|b)*)(?P<{SUFFIX}>.*)"
RE_EXTRACT_CHORD_PRIMARY_SUFF = f"(?P<{PRIMARY_SUFFIX}>({CHORD_MAJ}|{CHORD_M_UPPER}|{CHORD_MAJ_DELTA})?(7|9|11|13))"
RE_EXTRACT_CHORD_ADD = f"(?P<{ADD_SUFFIX}>{CHORD_ADD}(#|b)*(2|4|6|9|11|13))"
RE_EXTRACT_CHORD_NO = f"(?P<{NO_SUFFIX}>{CHORD_NO}(#|b)*(3|5|7))"
RE_EXTRACT_CHORD_SUS = f"(?P<{SUS_SUFFIX}>{CHORD_SUS}(2|4|bb3|#3))"
RE_EXTRACT_CHORD_BASE = f"(?P<chord_base>({CHORD_MAJ}|{CHORD_MIN}|{CHORD_M_LOWER}|{CHORD_M_UPPER}|{CHORD_MAJ_DELTA}|{CHORD_DIM}|{CHORD_AUG}|{CHORD_HALFDIM_OE}|{CHORD_PLUS}|{CHORD_MINUS}))"


 # The formal sequence of suffixes is taken to be:
    #
    # - root                A note name or Roman interval symbol.
    # - normal3             maj, min
    # - primary_suffix      7, maj7, dim7
    # - secondary_suffix    6, b6, #6
    # - sus                 sus2, sus4, susbb3, sus#3
    # - alt5                #5, b5
    # - add                 addX, where X is an interval name
    # - no3                 only appears if there is no 3 and no sus
    # - no5                 only appears if there is no 5 and no alt5
    # - alt7                bb7; only appears if there is a sus or no3
    # - extensions          intervals that can't be added to the primary suffix




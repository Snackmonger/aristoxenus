'''
Collection of canonical strings used as decypherable symbols and dict keys.
'''

from .bitwise import transpose_interval
from . import intervallic_canon as interval


# Accidentals.
SHARP = 'sharp'
FLAT = 'flat'

# Symbols
SHARP_SYMBOL = '#'
FLAT_SYMBOL = 'b'
BINOMIAL_DIVIDER_SYMBOL = '|'
SLASH_CHORD_DIVIDER_SYMBOL = '/'
POLYCHORD_DIVIDER_SYMBOL = '@'
POLYCHORD_OCTAVE_SYMBOL = '^'
# Note: we want to use the real flat/sharp symbols, but
# we want to keep being able to recognize pound and b...

# Structure interface.
PREFERRED_NAME: str = 'preferred_name'
MODAL_NAME: str = 'modal_name'
RECOGNIZED_NAMES: str = 'recognized_names'
INTERVAL_MAP: str = 'interval_map'

# Interval qualities
MAJOR = 'major'
MINOR = 'minor'
DIMINISHED = 'diminished'
AUGMENTED = 'augmented'
PERFECT = 'perfect'

# Chord sub-symbols.
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

# Canonical references for basic compounds.
CHORD_FLAT_2 = FLAT_SYMBOL + CHORD_2
CHORD_SUS_2 = CHORD_SUS + CHORD_2
CHORD_SHARP_2 = SHARP_SYMBOL + CHORD_2
CHORD_FLAT_3 = FLAT_SYMBOL + CHORD_3
CHORD_SHARP_3 = SHARP_SYMBOL + CHORD_3
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
CHORD_M7_UPPER = CHORD_M_UPPER + CHORD_7
CHORD_MAJ_DELTA7 = CHORD_MAJ_DELTA + CHORD_7
CHORD_DOUBLE_FLAT_7 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_7
CHORD_FLAT_9 = FLAT_SYMBOL + CHORD_9
CHORD_SHARP_9 = SHARP_SYMBOL + CHORD_9
CHORD_FLAT_10 = FLAT_SYMBOL + CHORD_10
CHORD_SHARP_10 = SHARP + CHORD_10
CHORD_SHARP_11 = SHARP_SYMBOL + CHORD_11
CHORD_FLAT_11 = FLAT_SYMBOL + CHORD_11
CHORD_FLAT_12 = FLAT_SYMBOL + CHORD_12
CHORD_SHARP_12 = SHARP_SYMBOL + CHORD_12
CHORD_SHARP_13 = SHARP_SYMBOL + CHORD_13
CHORD_FLAT_13 = FLAT_SYMBOL + CHORD_13
CHORD_SHARP_14 = SHARP_SYMBOL + CHORD_14
CHORD_FLAT_14 = FLAT_SYMBOL + CHORD_14


# Symbols we use to build extension formats maj9, dim11, etc.
# The resulting chords have nonexplicit structures (e.g. 13 implies 9 and 11)
CHORD_MAJOR_SYMBOL_LIST = [CHORD_MAJ, CHORD_MAJ_DELTA, CHORD_M_UPPER]
CHORD_MINOR_SYMBOL_LIST = [CHORD_MIN, CHORD_M_LOWER, CHORD_MINUS]
CHORD_AUGMENTED_SYMBOL_LIST = [CHORD_AUG, CHORD_PLUS]
CHORD_DIMINISHED_SYMBOL_LIST = [CHORD_DIM]
CHORD_SYMBOL_LIST = CHORD_MAJOR_SYMBOL_LIST + CHORD_MINOR_SYMBOL_LIST + \
    CHORD_AUGMENTED_SYMBOL_LIST + CHORD_DIMINISHED_SYMBOL_LIST

# Symbols that correspond explicitly to given intervals.
basic_symbols = {interval.HEMITONE: [CHORD_FLAT_2],
                 interval.TONE: [CHORD_2, CHORD_SUS_2],
                 interval.HEMIOLION: [CHORD_SHARP_2, CHORD_FLAT_3, CHORD_MINUS, CHORD_M_LOWER, CHORD_MIN],
                 interval.DITONE: [CHORD_3, CHORD_FLAT_4, CHORD_MAJ, CHORD_M_UPPER, CHORD_MAJ_DELTA],
                 interval.DIATESSARON: [CHORD_SUS_4, CHORD_4, CHORD_SHARP_3],
                 interval.TRITONE: [CHORD_SHARP_4, CHORD_FLAT_5],
                 interval.DIAPENTE: [CHORD_5],
                 interval.COMPOUND_HEMITONE: [CHORD_AUG, CHORD_AUG_5, CHORD_SHARP_5, CHORD_FLAT_6, CHORD_PLUS],
                 interval.COMPOUND_TONE: [CHORD_6, CHORD_DOUBLE_FLAT_7],
                 interval.COMPOUND_HEMIOLION: [CHORD_7, CHORD_FLAT_7, CHORD_SHARP_6],
                 interval.COMPOUND_DITONE: [CHORD_MAJ_7, CHORD_M7_UPPER, CHORD_MAJ_DELTA7],
                 interval.DIAPASON: [CHORD_8],
                 transpose_interval(interval.HEMITONE): [CHORD_FLAT_9],
                 transpose_interval(interval.TONE): [CHORD_9],
                 transpose_interval(interval.HEMIOLION): [CHORD_SHARP_9, CHORD_FLAT_10],
                 transpose_interval(interval.DITONE): [CHORD_10, CHORD_FLAT_11],
                 transpose_interval(interval.DIATESSARON): [CHORD_11, CHORD_SHARP_10],
                 transpose_interval(interval.TRITONE): [CHORD_SHARP_11, CHORD_FLAT_12],
                 transpose_interval(interval.DIAPENTE): [CHORD_12],
                 transpose_interval(interval.COMPOUND_HEMITONE): [CHORD_FLAT_13, CHORD_SHARP_12],
                 transpose_interval(interval.COMPOUND_TONE): [CHORD_13],
                 transpose_interval(interval.COMPOUND_HEMIOLION): [CHORD_SHARP_13, CHORD_FLAT_14],
                 transpose_interval(interval.COMPOUND_DITONE): [CHORD_14],
                 transpose_interval(interval.DIAPASON): [CHORD_15],
                 }

symbol_elements: dict[str, int] = {
    symbol: interval for interval, symbols in basic_symbols.items() for symbol in symbols}


symbol_prescription: dict[int, str] = {interval.HEMITONE: CHORD_FLAT_2,
                                       interval.TONE: CHORD_2,
                                       interval.HEMIOLION: CHORD_MIN,
                                       interval.DITONE: CHORD_MAJ,
                                       interval.DIATESSARON: CHORD_4,
                                       interval.TRITONE: CHORD_FLAT_5,
                                       interval.DIAPENTE: CHORD_5,
                                       interval.COMPOUND_HEMITONE: CHORD_SHARP_5,
                                       interval.COMPOUND_TONE: CHORD_6,
                                       interval.COMPOUND_HEMIOLION: CHORD_7,
                                       interval.COMPOUND_DITONE: CHORD_MAJ_7,
                                       interval.DIAPASON: CHORD_8,
                                       transpose_interval(interval.HEMITONE): CHORD_FLAT_9,
                                       transpose_interval(interval.TONE): CHORD_9,
                                       transpose_interval(interval.HEMIOLION): CHORD_SHARP_9,
                                       transpose_interval(interval.DITONE): CHORD_10,
                                       transpose_interval(interval.DIATESSARON): CHORD_11,
                                       transpose_interval(interval.TRITONE): CHORD_SHARP_11,
                                       transpose_interval(interval.DIAPENTE): CHORD_12,
                                       transpose_interval(interval.COMPOUND_HEMITONE): CHORD_FLAT_13,
                                       transpose_interval(interval.COMPOUND_TONE): CHORD_13,
                                       transpose_interval(interval.COMPOUND_HEMIOLION): CHORD_FLAT_14,
                                       transpose_interval(interval.COMPOUND_DITONE): CHORD_14,
                                       transpose_interval(interval.DIAPASON): CHORD_15}

numberstrings = {
    '1': {'cardinal': 'one',
          'ordinal': 'first',
          'ordinal_suffix': 'st',
          'uple': 'single'},

    '2': {'cardinal': 'two',
          'ordinal': 'second',
          'ordinal_suffix': 'nd',
          'uple': 'double'},

    '3': {'cardinal': 'three',
          'ordinal': 'third',
          'ordinal_suffix': 'rd',
          'uple': 'triple'},

    '4': {'cardinal': 'four',
          'ordinal': 'fourth',
          'ordinal_suffix': 'th',
          'uple': 'quadruple'},

    '5': {'cardinal': 'five',
          'ordinal': 'fifth',
          'ordinal_suffix': 'th',
          'uple': 'quintuple'},

    '6': {'cardinal': 'six',
          'ordinal': 'sixth',
          'ordinal_suffix': 'th',
          'uple': 'sextuple'},

    '7': {'cardinal': 'seven',
          'ordinal': 'seventh',
          'ordinal_suffix': 'th',
          'uple': 'septuple'},

    '8': {'cardinal': 'eight',
          'ordinal': 'eighth',
          'ordinal_suffix': 'th',
          'uple': 'octuple'},

    '9': {'cardinal': 'nine',
          'ordinal': 'ninth',
          'ordinal_suffix': 'th',
          'uple': 'nonuple'},

    '10': {'cardinal': 'ten',
           'ordinal': 'tenth',
           'ordinal_suffix': 'th'},

    '11': {'cardinal': 'eleven',
           'ordinal': 'eleventh',
           'ordinal_suffix': 'th'},

    '12': {'cardinal': 'twelve',
           'ordinal': 'twelfth',
           'ordinal_suffix': 'th'},

    '13': {'cardinal': 'thirteen',
           'ordinal': 'thirteenth',
           'ordinal_suffix': 'th'},

    '14': {'cardinal': 'fourteen',
           'ordinal': 'fourteenth',
           'ordinal_suffix': 'th'}
}

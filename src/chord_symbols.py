'''
Collection of canonical strings used as decipherable chord symbols.
'''

from . import bitwise
from . import intervallic_canon as interval
from . import constants

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

# Symbols that are compounds of other symbols.
CHORD_FLAT_2 = constants.FLAT_SYMBOL + CHORD_2
CHORD_SUS_2 = CHORD_SUS + CHORD_2
CHORD_SHARP_2 = constants.SHARP_SYMBOL + CHORD_2
CHORD_FLAT_3 = constants.FLAT_SYMBOL + CHORD_3
CHORD_SHARP_3 = constants.SHARP_SYMBOL + CHORD_3
CHORD_FLAT_4 = constants.FLAT_SYMBOL + CHORD_4
CHORD_SUS_4 = CHORD_SUS + CHORD_4
CHORD_SHARP_4 = constants.SHARP_SYMBOL + CHORD_4
CHORD_FLAT_5 = constants.FLAT_SYMBOL + CHORD_5
CHORD_SHARP_5 = constants.SHARP_SYMBOL + CHORD_5
CHORD_AUG_5 = CHORD_AUG + CHORD_5
CHORD_DIM_5 = CHORD_DIM + CHORD_5
CHORD_FLAT_6 = constants.FLAT_SYMBOL + CHORD_6
CHORD_SHARP_6 = constants.SHARP_SYMBOL + CHORD_6
CHORD_FLAT_7 = constants.FLAT_SYMBOL + CHORD_7
CHORD_MAJ_7 = CHORD_MAJ + CHORD_7
CHORD_M7_UPPER = CHORD_M_UPPER + CHORD_7
CHORD_MAJ_DELTA7 = CHORD_MAJ_DELTA + CHORD_7
CHORD_DOUBLE_FLAT_7 = constants.FLAT_SYMBOL*2 + CHORD_7
CHORD_FLAT_9 = constants.FLAT_SYMBOL + CHORD_9
CHORD_SHARP_9 = constants.SHARP_SYMBOL + CHORD_9
CHORD_FLAT_10 = constants.FLAT_SYMBOL + CHORD_10
CHORD_SHARP_10 = constants.SHARP_SYMBOL + CHORD_10
CHORD_SHARP_11 = constants.SHARP_SYMBOL + CHORD_11
CHORD_FLAT_11 = constants.FLAT_SYMBOL + CHORD_11
CHORD_FLAT_12 = constants.FLAT_SYMBOL + CHORD_12
CHORD_SHARP_12 = constants.SHARP_SYMBOL + CHORD_12
CHORD_SHARP_13 = constants.SHARP_SYMBOL + CHORD_13
CHORD_FLAT_13 = constants.FLAT_SYMBOL + CHORD_13
CHORD_SHARP_14 = constants.SHARP_SYMBOL + CHORD_14
CHORD_FLAT_14 = constants.FLAT_SYMBOL + CHORD_14

# Symbols we use to build extension formats maj9, dim11, etc.
# The resulting chords have nonexplicit structures (e.g. 13 implies 9 and 11)
CHORD_MAJOR_SYMBOL_LIST = [CHORD_MAJ, CHORD_MAJ_DELTA, CHORD_M_UPPER]
CHORD_MINOR_SYMBOL_LIST = [CHORD_MIN, CHORD_M_LOWER, CHORD_MINUS]
CHORD_AUGMENTED_SYMBOL_LIST = [CHORD_AUG, CHORD_PLUS]
CHORD_DIMINISHED_SYMBOL_LIST = [CHORD_DIM]
CHORD_SYMBOL_LIST = CHORD_MAJOR_SYMBOL_LIST + CHORD_MINOR_SYMBOL_LIST + \
    CHORD_AUGMENTED_SYMBOL_LIST + CHORD_DIMINISHED_SYMBOL_LIST

# Symbols that correspond explicitly to given intervals.
basic_symbols: dict[int, list[str]] = {interval.HEMITONE: [CHORD_FLAT_2],
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
                 bitwise.transpose_interval(interval.HEMITONE): [CHORD_FLAT_9],
                 bitwise.transpose_interval(interval.TONE): [CHORD_9],
                 bitwise.transpose_interval(interval.HEMIOLION): [CHORD_SHARP_9, CHORD_FLAT_10],
                 bitwise.transpose_interval(interval.DITONE): [CHORD_10, CHORD_FLAT_11],
                 bitwise.transpose_interval(interval.DIATESSARON): [CHORD_11, CHORD_SHARP_10],
                 bitwise.transpose_interval(interval.TRITONE): [CHORD_SHARP_11, CHORD_FLAT_12],
                 bitwise.transpose_interval(interval.DIAPENTE): [CHORD_12],
                 bitwise.transpose_interval(interval.COMPOUND_HEMITONE): [CHORD_FLAT_13, CHORD_SHARP_12],
                 bitwise.transpose_interval(interval.COMPOUND_TONE): [CHORD_13],
                 bitwise.transpose_interval(interval.COMPOUND_HEMIOLION): [CHORD_SHARP_13, CHORD_FLAT_14],
                 bitwise.transpose_interval(interval.COMPOUND_DITONE): [CHORD_14],
                 bitwise.transpose_interval(interval.DIAPASON): [CHORD_15],
                 }
symbol_elements: dict[str, int] = {
    symbol: interval for interval, symbols in basic_symbols.items() for symbol in symbols}
additive: dict[str, int] = {
    'add' + symbol: interval for symbol, interval in symbol_elements.items()}
subtractive: dict[str, int] = {
    'no' + symbol: interval for symbol, interval in symbol_elements.items()}

# The prescribed symbol for each interval, used by the parser
# to generate a complete chord symbol
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
                                       bitwise.transpose_interval(interval.HEMITONE): CHORD_FLAT_9,
                                       bitwise.transpose_interval(interval.TONE): CHORD_9,
                                       bitwise.transpose_interval(interval.HEMIOLION): CHORD_SHARP_9,
                                       bitwise.transpose_interval(interval.DITONE): CHORD_10,
                                       bitwise.transpose_interval(interval.DIATESSARON): CHORD_11,
                                       bitwise.transpose_interval(interval.TRITONE): CHORD_SHARP_11,
                                       bitwise.transpose_interval(interval.DIAPENTE): CHORD_12,
                                       bitwise.transpose_interval(interval.COMPOUND_HEMITONE): CHORD_FLAT_13,
                                       bitwise.transpose_interval(interval.COMPOUND_TONE): CHORD_13,
                                       bitwise.transpose_interval(interval.COMPOUND_HEMIOLION): CHORD_FLAT_14,
                                       bitwise.transpose_interval(interval.COMPOUND_DITONE): CHORD_14,
                                       bitwise.transpose_interval(interval.DIAPASON): CHORD_15}

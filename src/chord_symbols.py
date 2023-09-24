'''
Collection of canonical strings used as decipherable chord symbols.
'''

from . import bitwise
from . import intervallic_canon as interval
from . import constants

# Chord sub-symbols.
CHORD_DIM: str = 'dim'
CHORD_AUG: str = 'aug'
CHORD_MAJ: str = 'maj'
CHORD_MAJ_DELTA: str = 'Δ'
CHORD_HALFDIM_OE: str = 'ø'
CHORD_MIN: str = 'min'
CHORD_M_UPPER: str = 'M'
CHORD_M_LOWER: str = 'm'
CHORD_PLUS: str = '+'
CHORD_MINUS: str = '-'
CHORD_SUS: str = 'sus'
CHORD_ADD: str = 'add'
CHORD_NO: str = 'no'
CHORD_2: str = '2'
CHORD_3: str = '3'
CHORD_4: str = '4'
CHORD_5: str = '5'
CHORD_6: str = '6'
CHORD_7: str = '7'
CHORD_8: str = '8'
CHORD_9: str = '9'
CHORD_10: str = '10'
CHORD_11: str = '11'
CHORD_12: str = '12'
CHORD_13: str = '13'
CHORD_14: str = '14'
CHORD_15: str = '15'

# Symbols that are compounds of other symbols.
CHORD_FLAT_2: str = constants.FLAT_SYMBOL + CHORD_2
CHORD_SUS_2: str = CHORD_SUS + CHORD_2
CHORD_SHARP_2: str = constants.SHARP_SYMBOL + CHORD_2
CHORD_FLAT_3: str = constants.FLAT_SYMBOL + CHORD_3
CHORD_SHARP_3: str = constants.SHARP_SYMBOL + CHORD_3
CHORD_FLAT_4: str = constants.FLAT_SYMBOL + CHORD_4
CHORD_SUS_4: str = CHORD_SUS + CHORD_4
CHORD_SHARP_4: str = constants.SHARP_SYMBOL + CHORD_4
CHORD_FLAT_5: str = constants.FLAT_SYMBOL + CHORD_5
CHORD_SHARP_5: str = constants.SHARP_SYMBOL + CHORD_5
CHORD_AUG_5: str = CHORD_AUG + CHORD_5
CHORD_DIM_5: str = CHORD_DIM + CHORD_5
CHORD_FLAT_6: str = constants.FLAT_SYMBOL + CHORD_6
CHORD_SHARP_6: str = constants.SHARP_SYMBOL + CHORD_6
CHORD_FLAT_7: str = constants.FLAT_SYMBOL + CHORD_7
CHORD_MAJ_7: str = CHORD_MAJ + CHORD_7
CHORD_M7_UPPER: str = CHORD_M_UPPER + CHORD_7
CHORD_MAJ_DELTA7: str = CHORD_MAJ_DELTA + CHORD_7
CHORD_DOUBLE_FLAT_7: str = constants.FLAT_SYMBOL*2 + CHORD_7
CHORD_FLAT_9: str = constants.FLAT_SYMBOL + CHORD_9
CHORD_SHARP_9: str = constants.SHARP_SYMBOL + CHORD_9
CHORD_FLAT_10: str = constants.FLAT_SYMBOL + CHORD_10
CHORD_SHARP_10: str = constants.SHARP_SYMBOL + CHORD_10
CHORD_SHARP_11: str = constants.SHARP_SYMBOL + CHORD_11
CHORD_FLAT_11: str = constants.FLAT_SYMBOL + CHORD_11
CHORD_FLAT_12: str = constants.FLAT_SYMBOL + CHORD_12
CHORD_SHARP_12: str = constants.SHARP_SYMBOL + CHORD_12
CHORD_SHARP_13: str = constants.SHARP_SYMBOL + CHORD_13
CHORD_FLAT_13: str = constants.FLAT_SYMBOL + CHORD_13
CHORD_SHARP_14: str = constants.SHARP_SYMBOL + CHORD_14
CHORD_FLAT_14: str = constants.FLAT_SYMBOL + CHORD_14

# Symbols we use to build extension formats maj9, dim11, etc.
# The resulting chords have nonexplicit structures (e.g. 13 implies 9 and 11)
CHORD_MAJOR_SYMBOL_LIST: list[str] = [CHORD_MAJ, CHORD_MAJ_DELTA, CHORD_M_UPPER]
CHORD_MINOR_SYMBOL_LIST: list[str] = [CHORD_MIN, CHORD_M_LOWER, CHORD_MINUS]
CHORD_AUGMENTED_SYMBOL_LIST: list[str] = [CHORD_AUG, CHORD_PLUS]
CHORD_DIMINISHED_SYMBOL_LIST: list[str] = [CHORD_DIM]
CHORD_SYMBOL_LIST: list[str] = CHORD_MAJOR_SYMBOL_LIST + CHORD_MINOR_SYMBOL_LIST + \
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

'''Collection of canonical strings used as decypherable symbols and dict keys.'''
from .interval_structures import *

# Accidentals.
DOUBLE = 'double'
TRIPLE = 'triple'
SHARP = 'sharp'
FLAT = 'flat'

# Symbols
SHARP_SYMBOL = '#'
FLAT_SYMBOL = 'b'
BINOMIAL_DIVIDER_SYMBOL = '|'
SLASH_CHORD_DIVIDER_SYMBOL = '/'
# Note: we want to use the real flat/sharp symbols, but
# we want to keep being able to recognize pound and b...

# Structure interface.
PREFERRED_NAME: str = 'preferred_name'
RECOGNIZED_NAMES: str = 'recognized_names'
PITCH_MAP: str = 'pitch_map'

# Interval qualities
MAJOR = 'major'
MINOR = 'minor'
DIMINISHED = 'diminished'
AUGMENTED = 'augmented'

# Chord symbols.
CHORD_DIM = 'dim'
CHORD_AUG = 'aug'
CHORD_MAJ = 'maj'
CHORD_MIN = 'min'
CHORD_M_UPPER = 'M'
CHORD_M_LOWER = 'm'

CHORD_PLUS = '+'
CHORD_MINUS = '-'
CHORD_SUS = 'sus'
ADD = 'add'
NO = 'no'

CHORD_2 = '2'
CHORD_FLAT_2 = FLAT_SYMBOL + CHORD_2
CHORD_SUS_2 = CHORD_SUS + CHORD_2
CHORD_SHARP_2 = SHARP_SYMBOL + CHORD_2
CHORD_3 = '3'
CHORD_FLAT_3 = FLAT_SYMBOL + CHORD_3
CHORD_SHARP_3 = SHARP_SYMBOL + CHORD_3
CHORD_4 = '4'
CHORD_FLAT_4 = FLAT_SYMBOL + CHORD_4
CHORD_SUS_4 = CHORD_SUS + CHORD_4
CHORD_SHARP_4 = SHARP_SYMBOL + CHORD_4
CHORD_5 = '5'
CHORD_FLAT_5 = FLAT_SYMBOL + CHORD_5
CHORD_SHARP_5 = SHARP_SYMBOL + CHORD_5
CHORD_AUG_5 = CHORD_AUG + CHORD_5
CHORD_DIM_5 = CHORD_DIM + CHORD_5
CHORD_6 = '6'
CHORD_FLAT_6 = FLAT_SYMBOL + CHORD_6
CHORD_SHARP_6 = SHARP_SYMBOL + CHORD_6
CHORD_7 = '7'
CHORD_FLAT_7 = FLAT_SYMBOL + CHORD_7
CHORD_MAJ_7 = CHORD_MAJ + CHORD_7
CHORD_M7_UPPER = CHORD_M_UPPER + CHORD_7
CHORD_DOUBLE_FLAT_7 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_7
CHORD_8 = '8'
CHORD_9 = '9'
CHORD_FLAT_9 = FLAT_SYMBOL + CHORD_9
CHORD_SHARP_9 = SHARP_SYMBOL + CHORD_9
CHORD_10 = '10'
CHORD_FLAT_10 = FLAT_SYMBOL + CHORD_10
CHORD_SHARP_10 = SHARP + CHORD_10
CHORD_11 = '11'
CHORD_SHARP_11 = SHARP_SYMBOL + CHORD_11
CHORD_FLAT_11 = FLAT_SYMBOL + CHORD_11
CHORD_12 = '12'
CHORD_FLAT_12 = FLAT_SYMBOL + CHORD_12
CHORD_SHARP_12 = SHARP_SYMBOL + CHORD_12
CHORD_13 = '13'
CHORD_SHARP_13 = SHARP_SYMBOL + CHORD_13
CHORD_FLAT_13 = FLAT_SYMBOL + CHORD_13
CHORD_14 = '14'
CHORD_SHARP_14 = SHARP_SYMBOL + CHORD_14
CHORD_FLAT_14 = FLAT_SYMBOL + CHORD_14
CHORD_15 = '15'

symbols = {HEMITONE: [CHORD_FLAT_2],
           TONE: [CHORD_2, CHORD_SUS_2],
           HEMIOLION: [CHORD_SHARP_2, CHORD_FLAT_3, CHORD_MINUS, CHORD_M_LOWER, CHORD_MIN],
           DITONE: [CHORD_3, CHORD_FLAT_4],
           DIATESSARON: [CHORD_SUS_4, CHORD_4, CHORD_SHARP_3],
           TRITONE: [CHORD_SHARP_4, CHORD_FLAT_5],
           DIAPENTE: [CHORD_5],
           COMPOUND_HEMITONE: [CHORD_AUG, CHORD_AUG_5, CHORD_SHARP_5, CHORD_FLAT_6, CHORD_PLUS],
           COMPOUND_TONE: [CHORD_6, CHORD_DOUBLE_FLAT_7],
           COMPOUND_HEMIOLION: [CHORD_7, CHORD_FLAT_7, CHORD_SHARP_6],
           COMPOUND_DITONE: [CHORD_MAJ_7, CHORD_M7_UPPER],
           DIAPASON: [CHORD_8],
           transpose_interval(HEMITONE): [CHORD_FLAT_9],
           transpose_interval(TONE): [CHORD_9],
           transpose_interval(HEMIOLION): [CHORD_SHARP_9, CHORD_FLAT_10],
           transpose_interval(DITONE): [CHORD_10, CHORD_FLAT_11],
           transpose_interval(DIATESSARON): [CHORD_11, CHORD_SHARP_10],
           transpose_interval(TRITONE): [CHORD_SHARP_11, CHORD_FLAT_12],
           transpose_interval(DIAPENTE): [CHORD_12],
           transpose_interval(COMPOUND_HEMITONE): [CHORD_FLAT_13, CHORD_SHARP_12],
           transpose_interval(COMPOUND_TONE): [CHORD_13],
           transpose_interval(COMPOUND_HEMIOLION): [CHORD_SHARP_13, CHORD_FLAT_14],
           transpose_interval(COMPOUND_DITONE): [CHORD_14],
           transpose_interval(DIAPASON): [CHORD_15]
           }

el: dict[str, int] = {
    symbol: interval for interval in symbols for symbol in symbols[interval]}

# TODO: Unicode symbols for diminished, half diminished, major triangle
symbol_elements: dict[str, int] = {
    CHORD_FLAT_2: HEMITONE,
    CHORD_2: TONE,
    CHORD_SUS_2: TONE,
    'b3': HEMIOLION,
    '3': DITONE,
    '-': HEMIOLION,
    'm': HEMIOLION,
    'min': HEMIOLION,
    'M': DITONE,
    'maj': DITONE,
    'b4': DITONE,
    'sus4': DIATESSARON,
    '4': DIATESSARON,
    '#4': TRITONE,
    'b5': TRITONE,
    '5': DIAPENTE,
    'dim': DIMINISHED_TRIAD,
    'dim5': DIMINISHED_TRIAD,
    'dim7': DIMINISHED_SEVENTH,
    '#5': COMPOUND_HEMITONE,
    'aug5': COMPOUND_HEMITONE,
    'aug': COMPOUND_HEMITONE,
    '+': COMPOUND_HEMITONE,
    'b6': COMPOUND_HEMITONE,
    '6': COMPOUND_TONE,
    'bb7': COMPOUND_TONE,
    '#6': COMPOUND_HEMIOLION,
    'b7': COMPOUND_HEMIOLION,
    '7': COMPOUND_HEMIOLION,
    'maj7': COMPOUND_DITONE,
    'M7': COMPOUND_DITONE,
    '8': DIAPASON,
    'b9': transpose_interval(HEMITONE),
    '9': transpose_interval(TONE),
    '#9': transpose_interval(HEMIOLION),
    'b10': transpose_interval(HEMIOLION),
    '10': transpose_interval(DITONE),
    'b11': transpose_interval(DITONE),
    '11': transpose_interval(DIATESSARON),
    '#11': transpose_interval(TRITONE),
    'b12': transpose_interval(TRITONE),
    '12': transpose_interval(DIAPENTE),
    'b13': transpose_interval(COMPOUND_HEMITONE),
    '13': transpose_interval(COMPOUND_TONE),
    '#13': transpose_interval(COMPOUND_HEMIOLION),
    'b14': transpose_interval(COMPOUND_HEMIOLION),
    '14': transpose_interval(COMPOUND_DITONE),
    '15': transpose_interval(DIAPASON)
}

POLYCHORD_OCTAVE_SYMBOL = '^'
numberdata = {
    '1': {'cardinal': 'one',
          'ordinal': 'first',
          'ordinal_suffix': 'st'},

    '2': {'cardinal': 'two',
          'ordinal': 'second',
          'ordinal_suffix': 'nd'},

    '3': {'cardinal': 'three',
          'ordinal': 'third',
          'ordinal_suffix': 'rd'},

    '4': {'cardinal': 'four',
          'ordinal': 'fourth',
          'ordinal_suffix': 'th'},

    '5': {'cardinal': 'five',
          'ordinal': 'fifth',
          'ordinal_suffix': 'th'},

    '6': {'cardinal': 'six',
          'ordinal': 'sixth',
          'ordinal_suffix': 'th'},

    '7': {'cardinal': 'seven',
          'ordinal': 'seventh',
          'ordinal_suffix': 'th'},

    '8': {'cardinal': 'eight',
          'ordinal': 'eighth',
          'ordinal_suffix': 'th'},

    '9': {'cardinal': 'nine',
          'ordinal': 'ninth',
          'ordinal_suffix': 'th'},

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




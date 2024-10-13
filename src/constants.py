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
SLASH_SYMBOL = "/"

############
# Keywords #
############
# Internal heptatonic scale names
DIATONIC = 'diatonic'
ALTERED = 'altered'
HEMITONIC = 'hemitonic'
HEMIOLIC = 'hemiolic'
DIMINISHED = 'diminished'
AUGMENTED = 'augmented'
HARMONIC = 'harmonic'
BISEPTIMAL = 'biseptimal'
PALEOCHROMATIC = 'paleochromatic'

# Internal search order for heptatonic scale types.
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

# Other heptatonic scale names
ENIGMATIC = 'enigmatic'
NEAPOLITAN_MAJOR = 'neapolitan_major'
NEAPOLITAN_MINOR = 'neapolitan_minor'
HUNGARIAN = 'hungarian'
HARMONIC_MINOR = 'harmonic_minor'

# Octatonic scale names
# Barry Harris Scales
MAJ_6_DIMINISHED = 'maj_6_diminished'
MIN_6_DIMINISHED = 'min_6_diminished'
DOM_7_DIMINISHED = 'dom_7_diminished'
DOM_7_FLAT_5_DIMINISHED = 'dom_7_flat_5_diminished'

# Modal names
IONIAN = 'ionian'
DORIAN = 'dorian'
PHRYGIAN = 'phrygian'
LYDIAN = 'lydian'
MIXOLYDIAN = 'mixolydian'
AEOLIAN = 'aeolian'
LOCRIAN = 'locrian'

# Internal search order for modal names
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

# Chord Parsing Keywords
NOTE_NAME = 'note_name'
ACCIDENTALS = 'accidentals'
EXTENSION = 'extension'
MODIFICATION = 'modification'
MAIN = 'main'

##############
# Scaleforms #
##############
HEPTATONIC_SCALES = {
    DIATONIC: (0, 2, 4, 5, 7, 9, 11),
    ALTERED: (0, 1, 3, 4, 6, 8, 10),
    HEMITONIC: (0, 1, 4, 5, 7, 9, 11),
    HEMIOLIC: (0, 3, 4, 5, 7, 9, 11),
    DIMINISHED: (0, 2, 4, 5, 6, 9, 11),
    AUGMENTED: (0, 2, 4, 6, 7, 9, 11),
    BISEPTIMAL: (0, 2, 4, 5, 7, 10, 11),
    PALEOCHROMATIC: (0, 1, 4, 5, 6, 9, 11)
}
HEPTATONIC_SUPPLEMENT = {
    ENIGMATIC: (0, 1, 4, 6, 8, 10, 11),
    NEAPOLITAN_MINOR: (0, 1, 3, 5, 7, 8, 11),
    NEAPOLITAN_MAJOR: (0, 1, 3, 5, 7, 9, 11),
    HUNGARIAN: (0, 2, 3, 6, 7, 8, 11),
    HARMONIC_MINOR: (0, 2, 3, 5, 7, 8, 11)
}
NATURAL_MAP = tuple(
    (HEPTATONIC_SCALES[DIATONIC][i], NATURAL_NAMES[i]) for i in range(7)
)

BARRY_HARRIS_SCALES = {
    MAJ_6_DIMINISHED: (0, 2, 4, 5, 7, 8, 9, 11),
}

#######################
# Chord Voicing Forms #
#######################
DROP_2_VOICING: tuple[int, ...] = (1,)           # 1573 c e g b -> c g b e
DROP_2_AND_4_VOICING: tuple[int, ...] = (1, 3)   # 1537 c e g b -> c g e b
DROP_2_AND_3_VOICING: tuple[int, ...] = (2,)     # 1375 c e g b -> c e b g
DROP_3_VOICING: tuple[int, ...] = (1, 2)         # 1735 c e g b -> c b e g

#################
# Chord Symbols #
#################
CHORD_DIM = 'dim'
CHORD_O = 'o'
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
CHORD_2 = str(2)
CHORD_3 = str(3)
CHORD_4 = str(4)
CHORD_5 = str(5)
CHORD_6 = str(6)
CHORD_7 = str(7)
CHORD_9 = str(9)
CHORD_11 = str(11)
CHORD_13 = str(13)
CHORD_DOUBLE_FLAT_3 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_3
CHORD_FLAT_3 = FLAT_SYMBOL + CHORD_3
CHORD_SHARP_3 = SHARP_SYMBOL + CHORD_3
CHORD_FLAT_5 = FLAT_SYMBOL + CHORD_5
CHORD_SHARP_5 =  SHARP_SYMBOL + CHORD_5
CHORD_DOUBLE_FLAT_7 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_7
CHORD_FLAT_7 = FLAT_SYMBOL + CHORD_7
CHORD_MAJOR_SYMBOLS = [CHORD_MAJ, CHORD_M_UPPER, CHORD_MAJ_DELTA]
CHORD_MINOR_SYMBOLS = [CHORD_MIN, CHORD_M_LOWER, CHORD_MINUS]
CHORD_DIM_SYMBOLS = [CHORD_DIM, CHORD_O]
CHORD_AUGMENTED_SYMBOLS = [CHORD_AUG, CHORD_PLUS]
CHORD_HALFDIM_SYMBOLS = [CHORD_HALFDIM_OE]

#######################
# Regular Expressions #
#######################
RE_VALIDATE_NOTE_NAME = "[A-G](#|b)*"
RE_SPLIT_NOTE_NAME = f"(?P<{NOTE_NAME}>[A-G])(?P<{ACCIDENTALS}>(#|b)*)"
RE_PARSE_CHORD_SYMBOL = f"(?P<{NOTE_NAME}>[A-G](#|b)*|((#|b)*(VII|VI|V|IV|III|II|I)))(?P<{MAIN}>(maj|M|min|m|-|\\+|dim|aug|o|ø|Δ))?(?P<{EXTENSION}>((maj|M|Δ))?(13|11|9|7))?(?P<{MODIFICATION}>.*)"

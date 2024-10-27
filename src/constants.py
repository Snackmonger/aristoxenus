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

# Scale names: We use one scale name as the absolute 'canonical' name for
# identifying scale structures.

# Primary
# The ancient Greek scale comprised of two diatonic tetrachords.
DIATONIC = 'diatonic'
# The ancient Greek scale comprised of two chromatic tetrachords,
# which should be called 'chromatic', but renamed to avoid conflict
# with the modern sense of the name.
PALEOCHROMATIC = 'paleochromatic'
# Since the program just deals with 12-TET, we don't include the ancient
# Greek enharmonic scale.


# Synthetic scales: derived by moving each note of the primary scale into
# any available neighbouring empty slot. The names are derived, when possible,
# from some characteristic in the scale, or from a common name.

# Diatonic synthetics
ALTERED = 'altered' # common name "altered"
HEMITONIC = 'hemitonic' # first interval is hemitone
HEMIOLIC = 'hemiolic' # first interval is hemiolion
DIMINISHED = 'diminished' # fifth note is diminished
AUGMENTED = 'augmented' # fifth note is augmented
HARMONIC = 'harmonic'   # common name "harmonic major"
BISEPTIMAL = 'biseptimal' # sixth note sounds like extra seventh

# Other heptatonic scale names
ENIGMATIC = 'enigmatic'
NEAPOLITAN = 'neapolitan'
HUNGARIAN_MINOR = 'hungarian_minor'
HUNGARIAN_MAJOR = 'hungarian_major'
HARMONIC_MINOR = 'harmonic_minor'
DOUBLE_HARMONIC = 'double_harmonic'
PERSIAN = 'persian'

# Heptatonic modal names: for all heptatonic scales, modal names are
# considered as if the scale's canonical form is 'ionian'. Mode names
# are treated as aliases for numbers of rotations, without any specific
# intervals implied in the name (the mode names do not correspond to the
# ancient Greek mode names anyay).
IONIAN = 'ionian'
DORIAN = 'dorian'
PHRYGIAN = 'phrygian'
LYDIAN = 'lydian'
MIXOLYDIAN = 'mixolydian'
AEOLIAN = 'aeolian'
LOCRIAN = 'locrian'

# Octatonic scale names
HALF_WHOLE_DIMINISHED = 'half_whole_diminished'
# Barry Harris Scales
MAJ_6_DIMINISHED = 'maj_6_diminished'
MIN_6_DIMINISHED = 'min_6_diminished'
DOM_7_DIMINISHED = 'dom_7_diminished'
DOM_7_FLAT_5_DIMINISHED = 'dom_7_flat_5_diminished'

# Pentatonic scale names
MINOR_PENTATONIC = 'minor_pentatonic'
IN = 'in'
INSEN = 'insen'
IWATO = 'iwato'

# Hexatonic scale names
ISTRIAN = 'istrian'
WHOLE_TONE = 'whole_tone'

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
MAIN = 'main'
INVERSION = 'inversion'
EXTENSION = 'extension'
MODIFICATION = 'modification'
SLASH = 'slash'
CLOSE = 'close'

# General music terms
INTERVAL_STRUCTURE = 'interval_structure'
NOTE_NAME = 'note_name'
ROMAN_NAME = 'roman_name'
ACCIDENTALS = 'accidentals'

##############
# Scaleforms #
##############
HEPTATONIC_SCALES = {
    DIATONIC: (0, 2, 4, 5, 7, 9, 11),
    ALTERED: (0, 1, 3, 4, 6, 8, 10),
    HEMITONIC: (0, 1, 4, 5, 7, 9, 11),
    HEMIOLIC: (0, 3, 4, 5, 7, 9, 11),
    DIMINISHED: (0, 2, 4, 5, 6, 9, 11),
    AUGMENTED: (0, 2, 4, 5, 8, 9, 11),
    HARMONIC: (0, 2, 4, 5, 7, 8, 11),
    BISEPTIMAL: (0, 2, 4, 5, 7, 10, 11),
    PALEOCHROMATIC: (0, 1, 4, 5, 6, 9, 11)
}
HEPTATONIC_SUPPLEMENT = {
    ENIGMATIC: (0, 1, 4, 6, 8, 10, 11),
    DOUBLE_HARMONIC: (0,1,4,5,7,8,11),
    NEAPOLITAN: (0, 1, 3, 5, 7, 9, 11),
    HUNGARIAN_MAJOR: (0,3,4,6,7,9,10),
    PERSIAN: (0,1,4,5,6,8,11)
}
NATURAL_MAP = tuple(
    (HEPTATONIC_SCALES[DIATONIC][i], NATURAL_NAMES[i]) for i in range(7)
)

BARRY_HARRIS_SCALES = {
    MAJ_6_DIMINISHED: (0, 2, 4, 5, 7, 8, 9, 11),
}

PENTATONIC_SUPPLEMENT = {
    IN: (0,1,5,7,8),
    INSEN: (0,1,5,7,10),
    IWATO: (0,1,5,6,10)
}
HEXATONIC_SUPPLEMENT = {
    ISTRIAN: (0,1,3,4,6,7)
}


SCALE_ALIASES = { # or 'scaliases' :-)
    'ionian #1': (ALTERED, IONIAN),
    'super locrian': (ALTERED, IONIAN),
    'melodic minor': (ALTERED, DORIAN),
    'dorian natural 7': (ALTERED, DORIAN),
    'phrygian natural 6': (ALTERED, PHRYGIAN),
    'lydian #5': (ALTERED, LYDIAN),
    'lydian augmented': (ALTERED, LYDIAN),
    'lydian dominant': (ALTERED, MIXOLYDIAN),
    'mixolydian #4': (ALTERED, MIXOLYDIAN),
    'aeolian natural 3': (ALTERED, AEOLIAN),
    'locrian natural 2': (ALTERED, LOCRIAN),
    'half diminished': (ALTERED, LOCRIAN),

    'ionian b2': (HEMITONIC, IONIAN),
    'dorian b1': (HEMITONIC, DORIAN),
    'phrygian bb7': (HEMITONIC, PHRYGIAN),
    'lydian b6': (HEMITONIC, LYDIAN),
    'mixolydian b5': (HEMITONIC, MIXOLYDIAN),
    'aeolian b4': (HEMITONIC, AEOLIAN),
    'locrian bb3': (HEMITONIC, LOCRIAN),

    'ionian #2': (HEMIOLIC, IONIAN),
    'major #2': (HEMIOLIC, IONIAN),
    'ultralocrian': (HEMIOLIC, DORIAN),
    'dorian #1': (HEMIOLIC, DORIAN),
    'altered diminished': (HEMIOLIC, DORIAN),
    'neapolitan minor': (HEMIOLIC, PHRYGIAN),
    'phrygian natural 7': (HEMIOLIC, PHRYGIAN),
    'lydian natural 6': (HEMIOLIC, LYDIAN),
    'mixolydian augmented': (HEMIOLIC, MIXOLYDIAN),
    'mixolydian #5': (HEMIOLIC, MIXOLYDIAN),
    'romani minor': (HEMIOLIC, AEOLIAN),
    'gypsy minor': (HEMIOLIC, AEOLIAN),
    'aeolian #4': (HEMIOLIC, AEOLIAN),
    'minor #4': (HEMIOLIC, AEOLIAN),
    'locrian dominant': (HEMIOLIC, LOCRIAN),
    'locrian natural 3': (HEMIOLIC, LOCRIAN),

    'ionian b5': (DIMINISHED, IONIAN),
    'dorian b4': (DIMINISHED, DORIAN),
    'phrygian bb3': (DIMINISHED, PHRYGIAN),
    'lydian b2': (DIMINISHED, LYDIAN),
    'mixolydian b1': (DIMINISHED, MIXOLYDIAN),
    'aeolian bb7': (DIMINISHED, AEOLIAN),
    'locrian bb6': (DIMINISHED, LOCRIAN),

    'ionian #5': (AUGMENTED, IONIAN),
    'dorian #4': (AUGMENTED, DORIAN),
    'ukrainian dorian': (AUGMENTED, DORIAN),
    'phrygian natural 3': (AUGMENTED, PHRYGIAN),
    'phrygian dominant': (AUGMENTED, PHRYGIAN),
    'lydian #2': (AUGMENTED, LYDIAN),
    'mixolydian #1': (AUGMENTED, MIXOLYDIAN),
    'aeolian natural 7': (AUGMENTED, AEOLIAN),
    'harmonic minor': (AUGMENTED, AEOLIAN),
    'locrian natural 6': (AUGMENTED, LOCRIAN),

    'ionian b6': (HARMONIC, IONIAN),
    'harmonic major': (HARMONIC, IONIAN),
    'dorian b5': (HARMONIC, DORIAN),
    'phrygian b4': (HARMONIC, PHRYGIAN),
    'lydian b3': (HARMONIC, LYDIAN),
    'mixolydian b2': (HARMONIC, MIXOLYDIAN),
    'aeolian b1': (HARMONIC, AEOLIAN),
    'locrian bb7': (HARMONIC, LOCRIAN),

    'ionian #6': (BISEPTIMAL, IONIAN),
    'dorian #5': (BISEPTIMAL, DORIAN),
    'phrygian #4': (BISEPTIMAL, PHRYGIAN),
    'lydian #3': (BISEPTIMAL, LYDIAN),
    'mixolydian #2': (BISEPTIMAL, MIXOLYDIAN),
    'aeolian #1': (BISEPTIMAL, AEOLIAN),
    'locrian natural 7': (BISEPTIMAL, LOCRIAN),

    'neapolitan major': (NEAPOLITAN, IONIAN),
    'leading whole tone': (NEAPOLITAN, DORIAN),
    'lydian augmented #6': (NEAPOLITAN, DORIAN),
    'lydian augmented dominant': (NEAPOLITAN, PHRYGIAN),
    'lydian dominant b6': (NEAPOLITAN, LYDIAN),
    'major locrian': (NEAPOLITAN, MIXOLYDIAN),
    'half diminished b4': (NEAPOLITAN, AEOLIAN),
    'altered dominant #2': (NEAPOLITAN, AEOLIAN),
    'altered dominant bb3': (NEAPOLITAN, LOCRIAN),
 
    'byzantine': (DOUBLE_HARMONIC, IONIAN),
    'gypsy major': (DOUBLE_HARMONIC, IONIAN),
    'hungarian minor': (DOUBLE_HARMONIC, LYDIAN),
    'ultra phrygian': (DOUBLE_HARMONIC, PHRYGIAN),
}

#######################
# Chord Voicing Forms #
#######################
DROP_2_VOICING: tuple[int, ...] = (1,)           # 1573 c e g b -> c g b e
DROP_2_AND_4_VOICING: tuple[int, ...] = (1, 3)   # 1537 c e g b -> c g e b
DROP_2_AND_3_VOICING: tuple[int, ...] = (2,)     # 1375 c e g b -> c e b g
DROP_3_VOICING: tuple[int, ...] = (1, 2)         # 1735 c e g b -> c b e g
SPREAD_TRIAD = DROP_2_VOICING                    # 153  c e g   -> c g e

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
# RE_VALIDATE_NOTE_NAME = "^([A-G](?:#|b)*)$"
# RE_VALIDATE_ROMAN_NAME = "^((?:#|b)*(?:VII|vii|VI|vi|V|v|IV|iv|III|iii|II|ii|I|i))$"
RE_PARSE_NOTE_NAME = f"^(?P<{NOTE_NAME}>[A-G])(?P<{ACCIDENTALS}>(#|b)*)$"
RE_PARSE_ROMAN_NAME = f"^(?P<{ACCIDENTALS}>(#|b)*)(?P<{ROMAN_NAME}>(VII|vii|VI|vi|V|v|IV|iv|III|iii|II|ii|I|i))$"
RE_PARSE_CHORD_SYMBOL = f"^(?P<{NOTE_NAME}>([A-G](?:#|b)*|(?:#|b)*(?:VII|vii|VI|vi|V|v|IV|iv|III|iii|II|ii|I|i)))(?P<{MAIN}>(?:maj|M|min|m|-|\\+|dim|aug|o|ø|Δ))?(?P<{EXTENSION}>(?:maj|M|Δ)?(?:13|11|9|7))?(?P<{MODIFICATION}>(?:[\\w\\d+#]+))?(?:\\/(?P<{SLASH}>([A-G](?:#|b)*|(?:#|b)*(?:VII|vii|VI|vi|V|v|IV|iv|III|iii|II|ii|I|i))))?$"
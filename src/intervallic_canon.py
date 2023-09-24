'''
The integer expressions of some of the most common intervallic structures.
'''
from .bitwise import transpose_interval

# Divisions of the single octave.
# -------------------------------

# Intervals of the 12 tone octave.
HEMITONE = 0b11
TONE = 0b101
HEMIOLION = 0b1001
DITONE = 0b10001
DIATESSARON = 0b100001
TRITONE = 0b1000001
DIAPENTE = 0b10000001
COMPOUND_HEMITONE = 0b100000001
COMPOUND_TONE = 0b1000000001
COMPOUND_HEMIOLION = 0b10000000001
COMPOUND_DITONE = 0b100000000001
DIAPASON = 0b1000000000001

# Common triads: structures that are compounds of 2 intervals.
MAJOR_TRIAD = DITONE | DIAPENTE
MINOR_TRIAD = HEMIOLION | DIAPENTE
DIMINISHED_TRIAD = HEMIOLION | TRITONE
AUGMENTED_TRIAD = DITONE | COMPOUND_HEMITONE
MAJOR_FLAT_5 = DITONE | TRITONE
SUS = TONE | DIAPENTE

primary_structure: dict[str, int] = {'major_triad': MAJOR_TRIAD,
                                     'minor_triad': MINOR_TRIAD}

# Common tetrads: structures that are compounds of 3 intervals, which can be
# expressed as a triad and another interval, or as compounds of 2 triads.
# Some of the named tetrads are actually inversions of the others (Am7 = C6,
# etc.), but it's often nomenclaturally conventient to treat them separately.

MAJOR_SIXTH = MAJOR_TRIAD | COMPOUND_TONE                       # Cmaj@Amin
MINOR_SIXTH = MINOR_TRIAD | COMPOUND_TONE                       # Cmin@Adim
MAJOR_SEVENTH = MAJOR_TRIAD | COMPOUND_DITONE                   # Cmaj@Emin
MINOR_SEVENTH = MINOR_TRIAD | COMPOUND_HEMIOLION                # Cmin@Ebmaj
DOMINANT_SEVENTH = MAJOR_TRIAD | COMPOUND_HEMIOLION             # Cmaj@Edim
MINOR_SEVEN_FLAT_FIVE = DIMINISHED_TRIAD | COMPOUND_HEMIOLION   # Cdim@Ebmin
DIMINISHED_SEVENTH = DIMINISHED_TRIAD | COMPOUND_TONE           # Cdim@Ebdim
AUGMENTED_SEVENTH = AUGMENTED_TRIAD | COMPOUND_HEMIOLION        # Caug@Emajb5
AUGMENTED_MAJOR_SEVENTH = AUGMENTED_TRIAD | COMPOUND_DITONE     # Caug@Emaj
DOMINANT_SEVENTH_FLAT_FIVE = MAJOR_FLAT_5 | COMPOUND_HEMIOLION  # Cmajb5@Gbmajb5

# Heptatonic scale forms: these serve as the canonical interval structures that
# heptatonic modes will be considered to be inversions of. Heptatonic scales can be
# expressed as a polychord consisting of a tetrad and a triad (or vice-versa) separated
# by a b2, 2, or #2.
DIATONIC_SCALE = TONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_TONE | COMPOUND_DITONE
ALTERED_SCALE = HEMITONE | HEMIOLION | DITONE | TRITONE | COMPOUND_HEMITONE | COMPOUND_HEMIOLION
HEMITONIC_SCALE = HEMITONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_TONE | COMPOUND_DITONE
HEMIOLIC_SCALE = HEMIOLION | DITONE | DIATESSARON | DIAPENTE | COMPOUND_TONE | COMPOUND_DITONE
DIMINISHED_SCALE = TONE | DITONE | DIATESSARON | TRITONE | COMPOUND_TONE | COMPOUND_DITONE
AUGMENTED_SCALE = TONE | DITONE | DIATESSARON | COMPOUND_HEMITONE | COMPOUND_TONE | COMPOUND_DITONE
HARMONIC_SCALE = TONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_HEMITONE | COMPOUND_DITONE
BISEPTIMAL_SCALE = TONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_HEMIOLION | COMPOUND_DITONE
PALEOCHROMATIC_SCALE = HEMITONE | DITONE | DIATESSARON | TRITONE | COMPOUND_TONE | COMPOUND_DITONE

# This is the order scales will be compared. Scales that arent simply rotations of one of these
# will be expressed as a variant of one of these, with this order being the preference. Thus, if
# a scale can be expressed as diatonic +1 modification (or a mode of same), it will be, otherwise,
# we check if it can be expressed as altered +1, and so on until a suitable match is found.
HEPTATONIC_ORDER = [DIATONIC_SCALE,
                    ALTERED_SCALE,
                    HEMITONIC_SCALE,
                    HEMIOLIC_SCALE,
                    DIMINISHED_SCALE,
                    AUGMENTED_SCALE,
                    HARMONIC_SCALE,
                    BISEPTIMAL_SCALE]

DIATONIC_LABEL = 'diatonic'
ALTERED_LABEL = 'altered'
HEMITONIC_LABEL = 'hemitonic'
HEMIOLIC_LABEL = 'hemiolic'
DIMINISHED_LABEL = 'diminished'
AUGMENTED_LABEL = 'augmented'
HARMONIC_LABEL = 'harmonic'
BISEPTIMAL_LABEL = 'biseptimal'
PALEOCHROMATIC_LABEL = 'paleochromatic'

HEP_DICT = {DIATONIC_SCALE: DIATONIC_LABEL,
            ALTERED_SCALE: ALTERED_LABEL,
            HEMITONIC_SCALE: HEMITONIC_LABEL,
            HEMIOLIC_SCALE: HEMIOLIC_LABEL,
            DIMINISHED_SCALE: DIMINISHED_LABEL,
            AUGMENTED_SCALE: AUGMENTED_LABEL,
            HARMONIC_SCALE: HARMONIC_LABEL,
            BISEPTIMAL_SCALE: BISEPTIMAL_LABEL,
            PALEOCHROMATIC_SCALE: PALEOCHROMATIC_LABEL}


# Divisions of the double octave.
# -------------------------------

# Western extensions
FLAT_NINTH = transpose_interval(HEMITONE)
NINTH = transpose_interval(TONE)
SHARP_NINTH = transpose_interval(HEMIOLION)
ELEVENTH = transpose_interval(DIATESSARON)
SHARP_ELEVENTH = transpose_interval(TRITONE)
THIRTEENTH = transpose_interval(COMPOUND_TONE)
FLAT_THIRTEENTH = transpose_interval(COMPOUND_HEMITONE)

# Shortcuts to fill in the implicit extensions in
# e.g. Am11 (has a 9) G13 (has a 9 and 11)
NINTH_CHORD_EXTENSIONS = NINTH
ELEVENTH_CHORD_EXTENSIONS = NINTH | ELEVENTH
THIRTEENTH_CHORD_EXTENSIONS = NINTH | ELEVENTH | THIRTEENTH

'''
The integer expressions of some of the most common intervallic structures.
'''
from .bit_manipulation import transpose_interval

# def transpose_interval(interval: int) -> int:
#     '''
#     Displace an interval into the second octave.
#     '''
#     return ((interval - 1) << 12) + 1


# Divisions of the single octave.
# -------------------------------

# Intervals of the 12 tone octave.
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

# Common triads: structures that are compounds of 2 intervals.
MAJOR_TRIAD = DITONE | DIAPENTE
MINOR_TRIAD = HEMIOLION | DIAPENTE
DIMINISHED_TRIAD = HEMIOLION | TRITONE
AUGMENTED_TRIAD = DITONE | COMPOUND_HEMITONE
MAJOR_FLAT_5 = DITONE | TRITONE
SUS = TONE | DIAPENTE

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

# Divisions of the double octave.
# -------------------------------

# Basic pentads, hexads, heptads. Structures that are compounds of the
# previous levels of structures, and so on...
MAJOR_NINTH = MAJOR_SEVENTH | transpose_interval(TONE)
MINOR_NINTH = MINOR_SEVENTH | transpose_interval(TONE)
DOMINANT_NINTH = DOMINANT_SEVENTH | transpose_interval(TONE)
DOMINANT_SEVENTH_FLAT_NINE = DOMINANT_SEVENTH | transpose_interval(HEMITONE)
DOMINANT_SEVENTH_SHARP_NINE = DOMINANT_SEVENTH | transpose_interval(HEMIOLION)

MAJOR_ELEVENTH = MAJOR_NINTH | transpose_interval(DIATESSARON)
MINOR_ELEVENTH = MINOR_NINTH | transpose_interval(DIATESSARON)
DOMINANT_ELEVENTH = DOMINANT_NINTH | transpose_interval(DIATESSARON)

MAJOR_THIRTEENTH = MAJOR_ELEVENTH | transpose_interval(COMPOUND_TONE)
MINOR_THIRTEENTH = MINOR_ELEVENTH | transpose_interval(COMPOUND_TONE)
DOMINANT_THIRTEENTH = DOMINANT_ELEVENTH | transpose_interval(COMPOUND_TONE)

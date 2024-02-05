'''
The integer expressions of some of the most common intervallic structures.
'''
from data import keywords

# Intervals of the 12 tone octave.
UNISON: int = 0b1
HEMITONE: int = 0b11
TONE: int = 0b101
HEMIOLION: int = 0b1001
DITONE: int = 0b10001
DIATESSARON: int = 0b100001
TRITONE: int = 0b1000001
DIAPENTE: int = 0b10000001
COMPOUND_HEMITONE: int = 0b100000001
COMPOUND_TONE: int = 0b1000000001
COMPOUND_HEMIOLION: int = 0b10000000001
COMPOUND_DITONE: int = 0b100000000001
DIAPASON: int = 0b1000000000001

# Common triads: structures that are compounds of 2 intervals.
MAJOR_TRIAD: int = DITONE | DIAPENTE
MINOR_TRIAD: int = HEMIOLION | DIAPENTE
MINOR_FLAT_5: int = HEMIOLION | TRITONE
MAJOR_SHARP_5: int = DITONE | COMPOUND_HEMITONE
# minor # 5 is an inversion of major triad
MAJOR_FLAT_5: int = DITONE | TRITONE
SUS2_TRIAD: int = TONE | DIAPENTE
# sus2 and sus4 are inversions of each other,
# but we want to try to recognize them as separate chords,
# depending on the bass.
SUS4_TRIAD: int = DIATESSARON | DIAPENTE

triads: dict[str, int] = {keywords.MAJOR_TRIAD: MAJOR_TRIAD,
                          keywords.MINOR_TRIAD: MINOR_TRIAD,
                          keywords.MINOR_FLAT_5: MINOR_FLAT_5,
                          keywords.MAJOR_FLAT_5: MAJOR_FLAT_5,
                          keywords.MAJOR_SHARP_5: MAJOR_SHARP_5,
                          keywords.SUS2_TRIAD: SUS2_TRIAD,
                          keywords.SUS4_TRIAD: SUS4_TRIAD
                          }

# Common tetrads: structures that are compounds of 3 intervals, which can be
# expressed as a triad and another interval, or as compounds of 2 triads.
# Some of the named tetrads are actually inversions of the others (Am7 = C6,
# etc.), but it's often nomenclaturally conventient to treat them separately.

# augmented triad + major 6 is an inversion of minmaj7
MAJOR_SEVENTH: int = MAJOR_TRIAD | COMPOUND_DITONE                          # Cmaj@Emin
MINOR_SEVENTH: int = MINOR_TRIAD | COMPOUND_HEMIOLION                       # Cmin@Ebmaj
MAJOR_SIXTH: int = MAJOR_TRIAD | COMPOUND_TONE                              # Cmaj@Am
MINOR_SIXTH: int = MINOR_TRIAD | COMPOUND_TONE                              # Cm@Amb5
MINOR_MAJOR_SEVENTH: int = MINOR_TRIAD | COMPOUND_DITONE                    # Cmin@Ebmaj#5
DOMINANT_SEVENTH: int = MAJOR_TRIAD | COMPOUND_HEMIOLION                    # Cmaj@Emb5
MINOR_SEVEN_FLAT_FIVE: int = MINOR_FLAT_5 | COMPOUND_HEMIOLION              # Cdim@Ebmin
DIMINISHED_SEVENTH: int = MINOR_FLAT_5 | COMPOUND_TONE                      # Cdim@Ebmb5
AUGMENTED_SEVENTH: int = MAJOR_SHARP_5 | COMPOUND_HEMIOLION                 # Caug@Emajb5
AUGMENTED_MAJOR_SEVENTH: int = MAJOR_SHARP_5 | COMPOUND_DITONE              # Caug@Emaj
DOMINANT_SEVENTH_FLAT_FIVE: int = MAJOR_FLAT_5 | COMPOUND_HEMIOLION         # Cmajb5@Gbmajb5

tetrads: dict[str, int] = {keywords.MAJOR_SEVENTH: MAJOR_SEVENTH,
                           keywords.MINOR_SEVENTH: MINOR_SEVENTH,
                           keywords.MAJOR_SIXTH: MAJOR_SIXTH,
                           keywords.MINOR_SIXTH: MINOR_SIXTH,
                           keywords.MINOR_MAJOR_SEVENTH: MINOR_MAJOR_SEVENTH,
                           keywords.DOMINANT_SEVENTH: DOMINANT_SEVENTH,
                           keywords.DOMINANT_SEVENTH_FLAT_FIVE: DOMINANT_SEVENTH_FLAT_FIVE,
                           keywords.DIMINISHED_SEVENTH: DIMINISHED_SEVENTH,
                           keywords.AUGMENTED_MAJOR_SEVENTH: AUGMENTED_MAJOR_SEVENTH,
                           keywords.AUGMENTED_SEVENTH: AUGMENTED_SEVENTH,
                           keywords.MINOR_SEVEN_FLAT_FIVE: MINOR_SEVEN_FLAT_FIVE
                           }

# Heptatonic scale forms: these serve as the canonical interval structures that
# heptatonic modes will be considered to be inversions of. Heptatonic scales can be
# expressed as a polychord consisting of a tetrad and a triad (or vice-versa) separated
# by a b2, 2, or #2.
DIATONIC_SCALE: int = TONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_TONE | COMPOUND_DITONE
ALTERED_SCALE: int = HEMITONE | HEMIOLION | DITONE | TRITONE | COMPOUND_HEMITONE | COMPOUND_HEMIOLION
HEMITONIC_SCALE: int = HEMITONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_TONE | COMPOUND_DITONE
HEMIOLIC_SCALE: int = HEMIOLION | DITONE | DIATESSARON | DIAPENTE | COMPOUND_TONE | COMPOUND_DITONE
DIMINISHED_SCALE: int = TONE | DITONE | DIATESSARON | TRITONE | COMPOUND_TONE | COMPOUND_DITONE
AUGMENTED_SCALE: int = TONE | DITONE | DIATESSARON | COMPOUND_HEMITONE | COMPOUND_TONE | COMPOUND_DITONE
HARMONIC_SCALE: int = TONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_HEMITONE | COMPOUND_DITONE
BISEPTIMAL_SCALE: int = TONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_HEMIOLION | COMPOUND_DITONE
PALEOCHROMATIC_SCALE: int = HEMITONE | DITONE | DIATESSARON | TRITONE | COMPOUND_TONE | COMPOUND_DITONE

# This is the order scales will be compared. Scales that arent simply rotations of one of these
# will be expressed as a variant of one of these, with this order being the preference. Thus, if
# a scale can be expressed as diatonic +1 modification (or a mode of same), it will be, otherwise,
# we check if it can be expressed as altered +1, and so on until a suitable match is found.
HEPTATONIC_ORDER: tuple[int, ...] = (DIATONIC_SCALE,
                                     ALTERED_SCALE,
                                     HEMITONIC_SCALE,
                                     HEMIOLIC_SCALE,
                                     DIMINISHED_SCALE,
                                     AUGMENTED_SCALE,
                                     HARMONIC_SCALE,
                                     BISEPTIMAL_SCALE,
                                     PALEOCHROMATIC_SCALE)


HEPTATONIC_SYSTEM_BY_NUMBER: dict[int, str] = dict(
    zip(HEPTATONIC_ORDER, keywords.HEPTATONIC_ORDER))

HEPTATONIC_SYSTEM_BY_NAME: dict[str, int] = dict(
    zip(keywords.HEPTATONIC_ORDER, HEPTATONIC_ORDER))

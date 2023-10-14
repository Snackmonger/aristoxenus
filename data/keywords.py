'''Strings used as dictionary keywords in the program.'''

# Basic interface terms
NOTE_NAME: str = 'note_name'
FREQUENCY: str = 'frequency'
SHARP: str = 'sharp'
FLAT: str = 'flat'
ACCIDENTAL_NOTES: str = 'accidental_notes'
OCTAVE: str = 'octave'
CHROMATIC: str = 'chromatic'
SCIENTIFIC: str = 'scientific'
PLAIN: str = 'plain'
INTERVAL_STRUCTURE: str = 'interval_structure'
INTERVAL_SCALE: str = 'interval_scale'
INTERVAL: str = 'interval'
PREFERRED_NAME: str = 'preferred_name'
CHROMATIC_RENDERING: str = 'chromatic_rendering'
KEYNOTE: str = 'keynote'
ALPHABETIC_RENDERING: str = 'alphabetic_rendering'
OPTIMAL_RENDERING: str = 'optimal_rendering'
OPTIMAL_KEYNOTE: str = 'optimal_keynote'
MODAL_NAME: str = 'modal_name'
SCALE_NAME: str = 'scale_name'
RECOGNIZED_NAMES: str = 'recognized_names'
CHORD_SYMBOL: str = 'chord_symbol'
CHORD_NAME: str = 'chord_name'
ABOVE: str = 'above'
BELOW: str = 'below'

# Interval qualities
MAJOR: str = 'major'
MINOR: str = 'minor'
DIMINISHED: str = 'diminished'
AUGMENTED: str = 'augmented'
PERFECT: str = 'perfect'

# Modal names
IONIAN: str = 'ionian'
DORIAN: str = 'dorian'
PHRYGIAN: str = 'phrygian'
LYDIAN: str = 'lydian'
MIXOLYDIAN: str = 'mixolydian'
AEOLIAN: str = 'aeolian'
LOCRIAN: str = 'locrian'

# We use modal names as a fixed series, not
# as representative of any specific structures
MODAL_NAME_SERIES: tuple[str, ...] = (IONIAN,
                                      DORIAN,
                                      PHRYGIAN,
                                      LYDIAN,
                                      MIXOLYDIAN,
                                      AEOLIAN,
                                      LOCRIAN)

# Numeration 
CARDINAL: str = 'cardinal'
ORDINAL: str = 'ordinal'
UPLE: str = 'uple'
POLYAD: str = 'polyad'
TONAL: str = 'tonal'
BASAL: str = 'basal'

# Cardinal
ONE: str = 'one'
TWO: str = 'two'
THREE: str = 'three'
FOUR: str = 'four'
FIVE: str = 'five'
SIX: str = 'six'
SEVEN: str = 'seven'
EIGHT: str = 'eight'
NINE: str = 'nine'
TEN: str = 'ten'
ELEVEN: str = 'eleven'
TWELVE: str = 'twelve'
THIRTEEN: str = 'thirteen'
FOURTEEN: str = 'fourteen'
FIFTEEN: str = 'fifteen'

# Ordinal
FIRST: str = 'first'
SECOND: str = 'second'
THIRD: str = 'third'
FOURTH: str = 'fourth'
FIFTH: str = 'fifth'
SIXTH: str = 'sixth'
SEVENTH: str = 'seventh'
EIGHTH: str = 'eighth'
NINTH: str = 'ninth'
TENTH: str = 'tenth'
ELEVENTH: str = 'eleventh'
TWELFTH: str = 'twelfth'
THIRTEENTH: str = 'thirteenth'
FOURTEENTH: str = 'fourteenth'
FIFTEENTH: str = 'fifteenth'

# Uples
SINGLE: str = 'single'
DOUBLE: str = 'double'
TRIPLE: str = 'triple'
QUADRUPLE: str = 'quadruple'
QUINTUPLE: str = 'quintuple'
SEXTUPLE: str = 'sextuple'
SEPTUPLE: str = 'septuple'
OCTUPLE: str = 'octuple'
NONUPLE: str = 'nonuple'
DECUPLE: str = 'decuple'
UNDECUPLE: str = 'undecuple'
DUODECUPLE: str = 'duopdecuple'
TREDECUPLE: str = 'tredecuple'
QUATTUORDECUPLE: str = 'quattuordecuple'
QUINDECUPLE: str = 'quindecuple'

# Polyads
MONAD: str = 'monad'
DYAD: str = 'dyad'
TRIAD: str = 'triad'
TETRAD: str = 'tetrad'
PENTAD: str = 'pentad'
HEXAD: str = 'hexad'
HEPTAD: str = 'heptad'
OCTAD: str = 'octad'
ENNEAD: str = 'nonad'
DECAD: str = 'decad'
HENDECAD: str = 'undecad'
DUODECAD: str = 'duodecad'

# Tonal numbers
MONOTONIC: str = 'monotonic'
DITONIC: str = 'ditonic'
TRITONIC: str = 'tritonic'
TETRATONIC: str = 'tetratonic'
PENTATONIC: str = 'pentatonic'
HEXATONIC: str = 'hexatonic'
HEPTATONIC: str = 'heptatonic'
OCTATONIC: str = 'octatonic'
ENNEATONIC: str = 'enneatonic'
DECATONIC: str = 'decatonic'
HENDECATONIC: str = 'hendecatonic'
DUODECATONIC: str = 'duodecatonic'

# Basal structures
PRIMAL: str = 'primal'
SECUNDAL: str = 'secundal'
TERTIAL: str = 'tertial'
QUARTAL: str = 'quartal'
QUINTAL: str = 'quintal'
SEXTAL: str = 'sextal'
SEPTIMAL: str = 'septimal'
OCTONAL: str = 'octonal'
NONAL: str = 'nonal'
DECIMAL: str = 'decimal'
UNDECIMAL: str = 'undecimal'
DUODECIMAL: str = 'duodecimal'


# Scale identifiers
DIATONIC: str = 'diatonic'
ALTERED: str = 'altered'
HEMITONIC: str = 'hemitonic'
HEMIOLIC: str = 'hemiolic'
# diminished
# augmented
HARMONIC: str = 'harmonic'
BISEPTIMAL: str = 'biseptimal'
PALEOCHROMATIC: str = 'paleochromatic'

# Groups of scales
HEPTATONIC_ORDER: tuple[str, ...] = (DIATONIC,
                                     ALTERED,
                                     HEMITONIC,
                                     HEMIOLIC,
                                     DIMINISHED,
                                     AUGMENTED,
                                     HARMONIC,
                                     BISEPTIMAL,
                                     PALEOCHROMATIC)

# Groups of number words
# polyad, tonal, basal
NUMERATION: tuple[tuple[str|None, ...], ...] = (
    (MONAD, MONOTONIC, PRIMAL, ONE, FIRST, SINGLE),
    (DYAD, DITONIC, SECUNDAL, TWO, SECOND, DOUBLE),
    (TRIAD, TRITONIC, TERTIAL, THREE, THIRD, TRIPLE),
    (TETRAD, TETRATONIC, QUARTAL, FOUR, FOURTH, QUADRUPLE),
    (PENTAD, PENTATONIC, QUINTAL, FIVE, FIFTH, QUINTUPLE),
    (HEXAD, HEXATONIC, SEXTAL, SIX, SIXTH, SEXTUPLE),
    (HEPTAD, HEPTATONIC, SEPTIMAL, SEVEN, SEVENTH, SEPTUPLE),
    (OCTAD, OCTATONIC, OCTONAL, EIGHT, EIGHTH, OCTUPLE),
    (ENNEAD, ENNEATONIC, NONAL, NINE, NINTH, NONUPLE),
    (DECAD, DECATONIC, DECIMAL, TEN, TENTH, DECUPLE),
    (HENDECAD, HENDECATONIC, UNDECIMAL, ELEVEN, ELEVENTH, UNDECUPLE),
    (DUODECAD, DUODECATONIC, DUODECIMAL, TWELVE, TWELFTH, DUODECUPLE),
    (None, None, None, THIRTEEN, THIRTEENTH, TREDECUPLE),
    (None, None, None, FOURTEEN, FOURTEENTH, QUATTUORDECUPLE),
    (None, None, None, FIFTEEN, FIFTEENTH, QUINDECUPLE)
)

NUMERATION_INDICES: tuple[str, ...] = (POLYAD, TONAL, BASAL, CARDINAL, ORDINAL, UPLE)

# Chord Names
MAJOR_TRIAD: str = 'major_triad'
MINOR_TRIAD: str = 'minor_triad'
MINOR_FLAT_5: str = 'minor_flat_5_triad'
MAJOR_FLAT_5: str = 'major_flat_5_triad'
MAJOR_SHARP_5: str = 'major_sharp_5_triad'
SUS_TRIAD: str = 'sus_triad'

# Guitar Tunings
STANDARD: str = 'standard'
DROP_D: str = 'drop_d'
STANDARD_7_STRING: str = 'standard_7_string'
OPEN_D: str
OPEN_G: str


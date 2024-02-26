'''String literals used as dictionary or interface keywords in the program.'''

# General musical terms
NOTE_NAME = 'note_name'
FREQUENCY = 'frequency'
SHARP = 'sharp'
FLAT = 'flat'
BINOMIAL = "binomial"
ACCIDENTAL_NOTES = 'accidental_notes'
OCTAVE = 'octave'
CHROMATIC = 'chromatic'
SCIENTIFIC = 'scientific'
PLAIN = 'plain'
INTERVAL_STRUCTURE = 'interval_structure'
INTERVAL_SCALE = 'interval_scale'
INTERVAL_MAP = "interval_map"
INTERVAL = 'interval'
KEYNOTE = 'keynote'
MODAL_NAME = 'modal_name'
SCALE_NAME = 'scale_name'
MODE = "mode"
SCALE = "scale"
ARPEGGIO = "arpeggio"
ABOVE = 'above'
BELOW = 'below'
STRUCTURE = 'structure'
SCALE_DEGREE = "scale_degree"

# Interval qualities
MAJOR = 'major'
MINOR = 'minor'
DIMINISHED = 'diminished'
AUGMENTED = 'augmented'
PERFECT = 'perfect'

# Modal names
IONIAN = 'ionian'
DORIAN = 'dorian'
PHRYGIAN = 'phrygian'
LYDIAN = 'lydian'
MIXOLYDIAN = 'mixolydian'
AEOLIAN = 'aeolian'
LOCRIAN = 'locrian'

# Canonical order of mode names
MODAL_NAME_SERIES = (
    IONIAN,
    DORIAN,
    PHRYGIAN,
    LYDIAN,
    MIXOLYDIAN,
    AEOLIAN,
    LOCRIAN)

# Internal scale names
DIATONIC = 'diatonic'
ALTERED = 'altered'
HEMITONIC = 'hemitonic'
HEMIOLIC = 'hemiolic'
# diminished
# augmented
HARMONIC = 'harmonic'
BISEPTIMAL = 'biseptimal'
PALEOCHROMATIC = 'paleochromatic'

# Internal canonical order of scale types
HEPTATONIC_ORDER = (
    DIATONIC,
    ALTERED,
    HEMITONIC,
    HEMIOLIC,
    DIMINISHED,
    AUGMENTED,
    HARMONIC,
    BISEPTIMAL,
    PALEOCHROMATIC)

# Internal scale processing terms
PREFERRED_NAME = 'preferred_name'
CANONICAL_NAME = 'canonical_name'
CANONICAL_FORM = 'canonical_form'
CHROMATIC_RENDERING = 'chromatic_rendering'
TWELVE_TONE_INTERVALS = "twelve_tone_intervals"
ALPHABETIC_RENDERING = 'alphabetic_rendering'
OPTIMAL_RENDERING = 'optimal_rendering'
OPTIMAL_KEYNOTE = 'optimal_keynote'
RECOGNIZED_NAMES = 'recognized_names'

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

# Triad terms
MAJOR_TRIAD = 'major_triad'
MINOR_TRIAD = 'minor_triad'
MINOR_FLAT_5 = 'minor_flat_5_triad'
MAJOR_FLAT_5 = 'major_flat_5_triad'
MAJOR_SHARP_5 = 'major_sharp_5_triad'
SUS2_TRIAD = 'sus2_triad'
SUS4_TRIAD = 'sus4_triad'

# Tetrad terms
MAJOR_SEVENTH = 'major_7'
MINOR_SEVENTH = 'minor_7'
MAJOR_SIXTH = 'major_6'
MINOR_SIXTH = 'minor_6'           
MINOR_MAJOR_SEVENTH = 'minor_major_7'
DOMINANT_SEVENTH = 'dominant_7'
MINOR_SEVEN_FLAT_FIVE = 'minor_7_flat_5'
DIMINISHED_SEVENTH = 'diminished_7'
AUGMENTED_SEVENTH = 'augmented_7'
AUGMENTED_MAJOR_SEVENTH = 'augmented_major_7'
DOMINANT_SEVENTH_FLAT_FIVE = 'dominant_7_flat_5'

# Fingering terms
FINGERING = "fingering"
CURRENT_FINGERING = "current_fingering"
FINGER = "finger"
INDEX = "index"
MIDDLE = "middle"
RING = "ring"
PINKY = "pinky"
MIXED = "mixed"

# Instrument terms
FRET = "fret"
FRETBOARD = "fretboard"
STRING = "string"
TUNING = "tuning"
STANDARD = 'standard'
STANDARD_7_STRING = 'standard_7_string'
STANDARD_8_STRING = 'standard_8_string'
DROP_D = 'drop_d'
OPEN_D = "open_d"
OPEN_G = "open_g"

# Graphics display options
# ------------------------
# Diagram node control options
SHAPE = "shape"
SHAPE_SIZE = "size"
TEXT_SIZE = "text_size"
COLOUR = "colour"
SHAPE_COLOUR = "shape_colour"
TEXT_COLOUR = "text_colour"
RENDERING_MODE = "rendering_mode"
# Shape terms
CIRCLE = "circle"
TRIANGLE = "triangle"
INVERSE_TRIANGLE = "inverse_triangle"
SQUARE = "square"
DIAMOND = "diamond"
# Colour terms
BLACK = "black"
RED = "red"
BLUE = "blue"
GREEN = "green"
ORANGE = "orange"
PURPLE = "purple"
YELLOW = "yellow"
WHITE = "white"

# API terms
# ---------
RESULT = 'result'
RESPONSE = 'response'
NO_MATCH = 'no_match'

# Numeration terms
# ----------------
CARDINAL = 'cardinal'
ORDINAL = 'ordinal'
UPLE = 'uple'
POLYAD = 'polyad'
TONAL = 'tonal'
BASAL = 'basal'

# Cardinal numbers
ONE = 'one'
TWO = 'two'
THREE = 'three'
FOUR = 'four'
FIVE = 'five'
SIX = 'six'
SEVEN = 'seven'
EIGHT = 'eight'
NINE = 'nine'
TEN = 'ten'
ELEVEN = 'eleven'
TWELVE = 'twelve'
THIRTEEN = 'thirteen'
FOURTEEN = 'fourteen'
FIFTEEN = 'fifteen'

# Ordinal numbers
FIRST = 'first'
SECOND = 'second'
THIRD = 'third'
FOURTH = 'fourth'
FIFTH = 'fifth'
SIXTH = 'sixth'
SEVENTH = 'seventh'
EIGHTH = 'eighth'
NINTH = 'ninth'
TENTH = 'tenth'
ELEVENTH = 'eleventh'
TWELFTH = 'twelfth'
THIRTEENTH = 'thirteenth'
FOURTEENTH = 'fourteenth'
FIFTEENTH = 'fifteenth'

# -Uples
SINGLE = 'single'
DOUBLE = 'double'
TRIPLE = 'triple'
QUADRUPLE = 'quadruple'
QUINTUPLE = 'quintuple'
SEXTUPLE = 'sextuple'
SEPTUPLE = 'septuple'
OCTUPLE = 'octuple'
NONUPLE = 'nonuple'
DECUPLE = 'decuple'
HENDECUPLE = 'undecuple'
DUODECUPLE = 'duopdecuple'
TREDECUPLE = 'tredecuple'
QUATTUORDECUPLE = 'quattuordecuple'
QUINDECUPLE = 'quindecuple'

# Polyads
MONAD = 'monad'
DYAD = 'dyad'
TRIAD = 'triad'
TETRAD = 'tetrad'
PENTAD = 'pentad'
HEXAD = 'hexad'
HEPTAD = 'heptad'
OCTAD = 'octad'
ENNEAD = 'nonad'
DECAD = 'decad'
HENDECAD = 'undecad'
DUODECAD = 'duodecad'

# Tonal numbers
MONOTONIC = 'monotonic'
DITONIC = 'ditonic'
TRITONIC = 'tritonic'
TETRATONIC = 'tetratonic'
PENTATONIC = 'pentatonic'
HEXATONIC = 'hexatonic'
HEPTATONIC = 'heptatonic'
OCTATONIC = 'octatonic'
ENNEATONIC = 'enneatonic'
DECATONIC = 'decatonic'
HENDECATONIC = 'hendecatonic'
DUODECATONIC = 'duodecatonic'

# Basal structures
PRIMAL = 'primal'
SECUNDAL = 'secundal'
TERTIAL = 'tertial'
QUARTAL = 'quartal'
QUINTAL = 'quintal'
SEXTAL = 'sextal'
SEPTIMAL = 'septimal'
OCTONAL = 'octonal'
NONAL = 'nonal'
DECIMAL = 'decimal'
UNDECIMAL = 'undecimal'
DUODECIMAL = 'duodecimal'

# Groups of number words
# polyad, tonal, basal, cardinal, ordinal, -uple
NUMERATION = (
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
    (HENDECAD, HENDECATONIC, UNDECIMAL, ELEVEN, ELEVENTH, HENDECUPLE),
    (DUODECAD, DUODECATONIC, DUODECIMAL, TWELVE, TWELFTH, DUODECUPLE),
    (None, None, None, THIRTEEN, THIRTEENTH, TREDECUPLE),
    (None, None, None, FOURTEEN, FOURTEENTH, QUATTUORDECUPLE),
    (None, None, None, FIFTEEN, FIFTEENTH, QUINDECUPLE)
)

# Column names for the numeration matrix above
NUMERATION_INDICES = (POLYAD, TONAL, BASAL, CARDINAL, ORDINAL, UPLE)

# List of chord inversion terms
numbered_inversions = tuple([ROOT+'_'+POSITION] + [NUMERATION[
    x][4]+'_'+INVERSION for x in range(11)])






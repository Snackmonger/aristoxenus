'''Strings used as dictionary or interface keywords in the program.'''

# General musical terms
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
KEYNOTE: str = 'keynote'
MODAL_NAME: str = 'modal_name'
SCALE_NAME: str = 'scale_name'
MODE: str = "mode"
SCALE: str = "scale"
ABOVE: str = 'above'
BELOW: str = 'below'
STRUCTURE: str = 'structure'
SCALE_DEGREE: str = "scale_degree"

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

# Canonical order of mode names
MODAL_NAME_SERIES: tuple[str, ...] = (
    IONIAN,
    DORIAN,
    PHRYGIAN,
    LYDIAN,
    MIXOLYDIAN,
    AEOLIAN,
    LOCRIAN)

# Internal scale names
DIATONIC: str = 'diatonic'
ALTERED: str = 'altered'
HEMITONIC: str = 'hemitonic'
HEMIOLIC: str = 'hemiolic'
# diminished
# augmented
HARMONIC: str = 'harmonic'
BISEPTIMAL: str = 'biseptimal'
PALEOCHROMATIC: str = 'paleochromatic'

# Internal canonical order of scale types
HEPTATONIC_ORDER: tuple[str, ...] = (
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
PREFERRED_NAME: str = 'preferred_name'
CANONICAL_NAME: str = 'canonical_name'
CANONICAL_FORM: str = 'canonical_form'
CHROMATIC_RENDERING: str = 'chromatic_rendering'
TWELVE_TONE_INTERVALS: str = "twelve_tone_intervals"
ALPHABETIC_RENDERING: str = 'alphabetic_rendering'
OPTIMAL_RENDERING: str = 'optimal_rendering'
OPTIMAL_KEYNOTE: str = 'optimal_keynote'
RECOGNIZED_NAMES: str = 'recognized_names'

# Chord terms
ROOT: str = 'root'
POSITION: str = 'position'
INVERSION: str = 'inversion'
OPEN: str = 'open'
CLOSE: str = 'close'
CHORD_SYMBOL: str = 'chord_symbol'
CHORD_NAME: str = 'chord_name'
DROP_2: str = 'drop_2'
DROP_3: str = 'drop_3'
DROP_2_and_4: str = 'drop_2_and_4'

# Triad terms
MAJOR_TRIAD: str = 'major_triad'
MINOR_TRIAD: str = 'minor_triad'
MINOR_FLAT_5: str = 'minor_flat_5_triad'
MAJOR_FLAT_5: str = 'major_flat_5_triad'
MAJOR_SHARP_5: str = 'major_sharp_5_triad'
SUS2_TRIAD: str = 'sus2_triad'
SUS4_TRIAD: str = 'sus4_triad'

# Tetrad terms
MAJOR_SEVENTH: str = 'major_7'
MINOR_SEVENTH: str = 'minor_7'
MAJOR_SIXTH: str = 'major_6'
MINOR_SIXTH: str = 'minor_6'           
MINOR_MAJOR_SEVENTH: str = 'minor_major_7'
DOMINANT_SEVENTH:str = 'dominant_7'
MINOR_SEVEN_FLAT_FIVE: str = 'minor_7_flat_5'
DIMINISHED_SEVENTH: str = 'diminished_7'
AUGMENTED_SEVENTH: str = 'augmented_7'
AUGMENTED_MAJOR_SEVENTH: str = 'augmented_major_7'
DOMINANT_SEVENTH_FLAT_FIVE: str = 'dominant_7_flat_5'

# Fingering terms
FINGERING: str = "fingering"
CURRENT_FINGERING: str = "current_fingering"
FINGER: str = "finger"
INDEX: str = "index"
MIDDLE: str = "middle"
RING: str = "ring"
PINKY: str = "pinky"
MIXED: str = "mixed"

# Instrument terms
FRET: str = "fret"
FRETBOARD: str = "fretboard"
STRING: str = "string"
TUNING: str = "tuning"
STANDARD: str = 'standard'
STANDARD_7_STRING: str = 'standard_7_string'
STANDARD_8_STRING: str = 'standard_8_string'
DROP_D: str = 'drop_d'
OPEN_D: str = "open_d"
OPEN_G: str = "open_g"

# Graphics display options
# ------------------------
SHAPE: str = "shape"
SHAPE_SIZE: str = "size"
TEXT_SIZE: str = "text_size"
COLOUR: str = "colour"
SHAPE_COLOUR: str = "shape_colour"
TEXT_COLOUR: str = "text_colour"
RENDERING_MODE: str = "rendering_mode"
# Shape terms
CIRCLE: str = "circle"
TRIANGLE: str = "triangle"
INVERSE_TRIANGLE: str = "inverse_triangle"
SQUARE: str = "square"
DIAMOND: str = "diamond"
# Colour terms
BLACK: str = "black"
RED: str = "red"
BLUE: str = "blue"
GREEN: str = "green"
ORANGE: str = "orange"
PURPLE: str = "purple"
YELLOW: str = "yellow"
WHITE: str = "white"

# Numeration terms
# ----------------
CARDINAL: str = 'cardinal'
ORDINAL: str = 'ordinal'
UPLE: str = 'uple'
POLYAD: str = 'polyad'
TONAL: str = 'tonal'
BASAL: str = 'basal'

# Cardinal numbers
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

# Ordinal numbers
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

# -Uples
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
HENDECUPLE: str = 'undecuple'
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

# Groups of number words
# polyad, tonal, basal, cardinal, ordinal, -uple
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
    (HENDECAD, HENDECATONIC, UNDECIMAL, ELEVEN, ELEVENTH, HENDECUPLE),
    (DUODECAD, DUODECATONIC, DUODECIMAL, TWELVE, TWELFTH, DUODECUPLE),
    (None, None, None, THIRTEEN, THIRTEENTH, TREDECUPLE),
    (None, None, None, FOURTEEN, FOURTEENTH, QUATTUORDECUPLE),
    (None, None, None, FIFTEEN, FIFTEENTH, QUINDECUPLE)
)

# Column names for the numeration matrix above
NUMERATION_INDICES: tuple[str, ...] = (POLYAD, TONAL, BASAL, CARDINAL, ORDINAL, UPLE)

# List of chord inversion terms
numbered_inversions: tuple[str, ...] = tuple([ROOT+'_'+POSITION] + [NUMERATION[
    x][4]+'_'+INVERSION for x in range(11)])






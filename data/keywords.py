'''String literals used as dictionary or interface keywords in the program.'''

# General musical terms
from src import utils


NOTE_NAME = 'note_name'
NOTE_NAMES = "note_names"
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
MODAL_SERIES = (
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
HEPTATONIC_SERIES = (
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

# Numeration terms
# ----------------
CARDINAL = 'cardinal'
ORDINAL = 'ordinal'
UPLE = 'uple'
POLYAD = 'polyad'
TONAL = 'tonal'
BASAL = 'basal'

# List of chord inversion terms
NUMBERED_INVERSIONS = tuple([ROOT+'_'+POSITION] + [
    utils.encode_numeration(x, ORDINAL) + '_' + INVERSION for x in range(1, 12)])



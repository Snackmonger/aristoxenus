
# Accidentals.
DOUBLE = 'double'
TRIPLE = 'triple'
SHARP = 'sharp'
FLAT = 'flat'

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
CHORD_M7_UPPER = 'M7'
CHORD_M7_LOWER = 'm7'
CHORD_M_LOWER = 'm'
CHORD_PLUS = '+'
CHORD_MINUS = '-'
ADD = 'add'
NO = 'no'

# Chord symbol parsing lists.
# Handle irregular symbols first (e.g. 7 means b7, but in major
# chords it means natural 7, and in diminished chords it means
# bb7). 
# We should parse from largest recognizable symbol to smallest,
# so that e.g. 'maj7' gets resolved before considering whether
# 'm' should register a minor triad.

# Recognizable chord symbol modifiers
CHORD_MODIFIERS = ['b9', '9', '#9', '11', '#11', 'b13', '13', 'b5', '#5']

# Misc chord structures.
POWERCHORD = ['5']

# Triad symbols
MAJOR_SYMBOLS = [CHORD_MAJ, CHORD_M_UPPER]
MINOR_SYMBOLS = [CHORD_MIN, CHORD_MINUS, CHORD_M_LOWER]
AUGMENTED_SYMBOLS = [CHORD_PLUS, CHORD_AUG, 'M#5', 'maj#5', '+5', 'M+5', 'maj+5']
DIMINISHED_SYMBOLS = [CHORD_DIM, 'mb5', '-b5']
SUS2_SYMBOLS = ['sus2']
SUS4_SYMBOL = ['sus4']

# Tetrad symbols
MAJ7_SYMBOLS = [symbol + '7' for symbol in MAJOR_SYMBOLS]
MIN7_SYMBOLS = [symbol + '7' for symbol in MINOR_SYMBOLS]
DOM7_SYMBOLS = ['7', 'dom7', 'b7']
MAJ6_SYMBOLS = [symbol + '6' for symbol in MAJOR_SYMBOLS]
MIN6_SYMBOLS = [symbol + '6' for symbol in MINOR_SYMBOLS]
MIN7_FLAT5_SYMBOLS = ['m7b5', 'ø', 'ø7', '-7b5']
DIM7_SYMBOLS = ['dim7', '°', '°7']
AUGMAJ7_SYMBOLS = ['+M7', '+maj7', 'augmaj7', 'aug5maj7', '+5M7', '#5M7', 'M7+5', 'M7+', 'M#5', 'maj7+5', 'maj7+5', 'majaug5', 'maj7#5']
DOM7AUG_SYMBOLS = ['7#5', '7+', '+7', 'aug7']
MINMAJ7_SYMBOLS = ['mM7', 'minmaj7', 'minM7', '-M7', '-maj7', 'm#7']

# Pentad symbols lists
MAJ9_SYMBOLS = [symbol + '9' for symbol in MAJOR_SYMBOLS]
MIN9_SYMBOLS = [symbol + '9' for symbol in MINOR_SYMBOLS]
DOM9_SYMBOLS = ['9', 'dom9']
DOM_FLAT9_SYMBOLS = ['7b9', 'dom7b9']
DOM_SHARP9_SYMBOLS = ['7#9', 'dom7#9']


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



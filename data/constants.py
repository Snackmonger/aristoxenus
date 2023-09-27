'''
Constants used in the program.
'''
NATURALS: list[str] = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
HALFSTEPS: dict[str, str] = {'E': 'F', 'B': 'C'}
TONES: int = 12
NOTES: int = 7
SHARP_VALUE: int = 1
FLAT_VALUE: int = -1
NUMBER_OF_OCTAVES: int = 9
OCTAVE_EQUIVALENCE_FACTOR: int = 2
FREQUENCY_DECIMAL_LIMIT: int = 3
CENTRAL_REFERENCE_NOTE_NAME: str = 'A4'
CENTRAL_REFERENCE_NOTE_FREQUENCY: int = 440

# Qualities
SHARP_LABEL = 'sharp'
FLAT_LABEL = 'flat'
MAJOR = 'major'
MINOR = 'minor'
DIMINISHED = 'diminished'
AUGMENTED = 'augmented'
PERFECT = 'perfect'

# Symbols
SHARP_SYMBOL = '#'
FLAT_SYMBOL = 'b'
BINOMIAL_DIVIDER_SYMBOL = '|'
SLASH_CHORD_DIVIDER_SYMBOL = '/'
POLYCHORD_DIVIDER_SYMBOL = '@'
POLYCHORD_OCTAVE_SYMBOL = '^'
ACCIDENTAL_SYMBOLS = [SHARP_SYMBOL, FLAT_SYMBOL]
# Note: we want to use the real flat/sharp symbols, but
# we want to keep being able to recognize pound and b...


SHARPS: list[str] = [note + SHARP_SYMBOL for note in NATURALS
                       if note not in HALFSTEPS]

FLATS: list[str] = [note + FLAT_SYMBOL for note in NATURALS
                      if note not in HALFSTEPS.values()]

BINOMIALS: list[str] = [sharp + BINOMIAL_DIVIDER_SYMBOL + flat
                          for flat in FLATS for sharp in SHARPS
                          if FLATS.index(flat) == SHARPS.index(sharp)]

ACCIDENTAL_NOTES: list[str] = SHARPS + FLATS

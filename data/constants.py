'''
Constants used in the program.
'''
NATURALS = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
HALFSTEPS = {'E': 'F', 'B': 'C'}
TONES = 12
NOTES = 7
SHARP_VALUE = 1
FLAT_VALUE = -1
NUMBER_OF_OCTAVES = 9
OCTAVE_EQUIVALENCE_FACTOR = 2
FREQUENCY_DECIMAL_LIMIT = 3
CENTRAL_REFERENCE_NOTE_NAME = 'A4'
CENTRAL_REFERENCE_NOTE_FREQUENCY = 440

# Symbols
SHARP_SYMBOL = '#'
FLAT_SYMBOL = 'b'
BINOMIAL_DIVIDER_SYMBOL = '|'
SLASH_CHORD_DIVIDER_SYMBOL = '/'
POLYCHORD_DIVIDER_SYMBOL = '@'
POLYCHORD_OCTAVE_SYMBOL = '^'
ACCIDENTAL_SYMBOLS = [SHARP_SYMBOL, FLAT_SYMBOL]
# Note: we want to use the real flat/sharp symbols, but
# we want to keep being able to recognize pound sign and lowercase b...


SHARPS = tuple(note + SHARP_SYMBOL for note in NATURALS
               if note not in HALFSTEPS)

FLATS = tuple(note + FLAT_SYMBOL for note in NATURALS
              if note not in HALFSTEPS.values())

BINOMIALS = tuple(sharp + BINOMIAL_DIVIDER_SYMBOL + flat
                  for flat in FLATS for sharp in SHARPS
                  if FLATS.index(flat) == SHARPS.index(sharp))

ACCIDENTAL_NOTES = tuple(SHARPS + FLATS)

ACCIDENTAL_TYPES = [SHARPS, FLATS, BINOMIALS]

LEGAL_ROOT_NAMES = tuple([n for c in [NATURALS, SHARPS, FLATS] for n in c]
                          + [n + SHARP_SYMBOL for n in HALFSTEPS]
                          + [n + FLAT_SYMBOL for n in HALFSTEPS.values()])

# Chord voicings
DROP_2 = (1,)  # c e g b -> c g b e
DROP_3 = (1, 2)  # c e g b -> c b e g
DROP_2_AND_4 = (1, 3)  # c e g b -> c g e b

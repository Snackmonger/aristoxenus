'''
Constants used in the program.
'''
NATURALS: tuple[str, ...] = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
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
SHARP_LABEL:str = 'sharp'
FLAT_LABEL:str = 'flat'
MAJOR:str = 'major'
MINOR:str = 'minor'
DIMINISHED:str = 'diminished'
AUGMENTED:str = 'augmented'
PERFECT:str = 'perfect'
DROP_2: tuple[int] = (1,)
DROP_3: tuple[int, int] = (1, 2)
DROP_2_AND_4: tuple[int, int] = (1, 3)

# Symbols
SHARP_SYMBOL:str = '#'
FLAT_SYMBOL:str = 'b'
BINOMIAL_DIVIDER_SYMBOL:str = '|'
SLASH_CHORD_DIVIDER_SYMBOL:str = '/'
POLYCHORD_DIVIDER_SYMBOL:str = '@'
POLYCHORD_OCTAVE_SYMBOL:str = '^'
ACCIDENTAL_SYMBOLS: list[str] = [SHARP_SYMBOL, FLAT_SYMBOL]
# Note: we want to use the real flat/sharp symbols, but
# we want to keep being able to recognize pound sign and lowercase b...


SHARPS: tuple[str, ...] = tuple(note + SHARP_SYMBOL for note in NATURALS
                       if note not in HALFSTEPS)

FLATS: tuple[str, ...] = tuple(note + FLAT_SYMBOL for note in NATURALS
                      if note not in HALFSTEPS.values())

BINOMIALS: tuple[str, ...] = tuple(sharp + BINOMIAL_DIVIDER_SYMBOL + flat
                          for flat in FLATS for sharp in SHARPS
                          if FLATS.index(flat) == SHARPS.index(sharp))

ACCIDENTAL_NOTES: tuple[str, ...] = tuple(SHARPS + FLATS)


ACCIDENTAL_TYPES: list[tuple[str, ...]] = [SHARPS, FLATS, BINOMIALS]
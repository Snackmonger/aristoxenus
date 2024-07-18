'''
Constants used in permuting harmonic and rhythmic structures.
'''
# Basic directional patterns
RISING_RISING = (False, False)
FALLING_FALLING = (True, True)
RISING_FALLING = (False, True)
FALLING_RISING = (True, False)

# Basic beat patterns
ON_BEAT_SCHEMA = {"metre": "4/4",
           "rhythm": [4, 4, 4, 4],
           "accents": [True, False, True, False]}
OFF_BEAT_SCHEMA = {"metre": "4/4",
            "rhythm": [4, 4, 4, 4],
            "accents": [False, True, False, True]}

# Tetrad chord voicings
DROP_2_VOICING = (1,)           # c e g b -> c g b e
DROP_3_VOICING = (1, 2)         # c e g b -> c b e g
DROP_2_AND_4_VOICING = (1, 3)   # c e g b -> c g e b

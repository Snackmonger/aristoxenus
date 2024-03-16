
# Basic directional patterns
RISING_RISING = (False, False)
FALLING_FALLING = (True, True)
RISING_FALLING = (False, True)
FALLING_RISING = (True, False)

# Basic beat patterns
ON_BEAT = {"metre": "4/4",
           "rhythm": [4, 4, 4, 4],
           "accents": [True, False, True, False]}
OFF_BEAT = {"metre": "4/4",
            "rhythm": [4, 4, 4, 4],
            "accents": [False, True, False, True]}

# Chord voicings
DROP_2 = (1,)           # c e g b -> c g b e
DROP_3 = (1, 2)         # c e g b -> c b e g
DROP_2_AND_4 = (1, 3)   # c e g b -> c g e b

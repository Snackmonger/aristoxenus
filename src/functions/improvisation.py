'''
Step 1: Describe the improvisational context.
    This means things like the chord of a bar, the tempo, the basic up.down
    beats of the metrical system.

    The computer will use this to define the limits within which the 
    improvisation can take place.

    I suppose this also entails that we must define things like tolerance for
    deviation from established limits (so that chord substitutions, metrical
    variations, etc. can be contextualized).

Step 2: Define pitch, rhythm, dynamic contours.
    This will give the computer a general guideline for the melody, so that
    it doesn't have to sort through millions of variants


Step 3: Permute solutions to fill contours in context.
    As the permutations take place and the metre is filled out, the tolerances
    for certain features need to change. 

    For example the computer will value repeating a phrase more when the
    phrase has been played once than when it has been played twice, and even
    less when it has been played thrice. This ensures that repetition, which
    is a valuable compositional principle, does not become monotonous, which
    ruins a melody.

Step 4: Evaluate solutions
    The function needs to take some parameters that define what constitutes
    a good result. Not quite sure about the process here...
'''
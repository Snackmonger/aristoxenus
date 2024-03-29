from typing import Sequence
from data import constants


def format_note_names(note_names: Sequence[str]) -> tuple[str, ...]:
    """Convert note names generated by Aristoxenus into note names that can
    be recognized by LilyPond.
    
    Any Aristoxenus binomials will be converted into sharps by default.
    """
    note_names_ = list(note_names)
    for i, note_name in enumerate(note_names_):
        if note_name in constants.BINOMIALS or len(note_name) > 3:
            j = constants.BINOMIALS.index(note_name)
            note_names_[i] = constants.SHARPS[j]
        for k, v in {constants.SHARP_SYMBOL: "es", constants.FLAT_SYMBOL: "is"}.items():

            note_names_[i] = note_names_[i].replace(k, v)
        note_names_[i] = note_names_[i].lower()
    return tuple(note_names_)



notes = """


Structure: triad, tetrad, octave triad, scale segment
    The basic structure of the material that fills the bar. 
    We will keep this simple for now and get the basic system working first.

This is modified by: 

    Pickup
        The basic structure is preceded by a pick-up note.
    Octave displacement
        One or more notes of the basic structure is altered by an octave. Usually, the first or last note of the basic structure.
    Fill
        One or more of the spaces between structural steps is replaced by a scale or chromatic note.

Therefore, we need to define:

Pickup rules
    Which notes are eligible to be chosen to serve as a pick-up? This could be determined by contextual cues, but that's for the controller to decide; we just need a way
    to communicate how the pickup note fits into the rhythmic structure.
Fill rules
    Do we fill with a scale tone or a chromatic tone?
    This would be a good place to know a bit about how we're going to connect the up/down beat with the pitches.
    

"""

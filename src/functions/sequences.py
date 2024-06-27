
from dataclasses import dataclass
from typing import Any, Sequence



@dataclass
class Chroneme:
    """Chroneme is a length of time during which there is a sound or no sound
    (i.e. a rest). 

    The content of a chroneme might be a pitch (or note name representing a 
    pitch), or a rest, or a percussive sound, or an effect, etc. Maybe the 
    content can be a simple code contained in a string:
        <plain_note_name="G#">
        <frequency=440.0>
        <percussive_sound="conga_drum3">
        <rest=True>

    For the sake of this prototype, assume that a chroneme might have multiple
    sounds in it simultaneously (e.g. notes & percussion) but that it will 
    never intersect another chroneme. In other words, all chronemes MUST end 
    before the next one can start, and we WON'T allow a note to be held while 
    other shorter notes are allowed to come and go.

    The chroneme can also have annotations to indicate stress, volume, timbre,
    and instrument-specific features.

    {"stress": "play hard", "volume": "high", "bowing": "screech"}

    Typing with Any without knowing the keys of the dictionary will mean that
    the number of possible annotations will cause type hint problems later.
    We can add keys to the dict at runtime with dict.__setitem__ though.
    """
    duration: float
    content: str
    annotations: dict[str, Any]


class Movement:
    """Movement is a sequence of chronemes.
    
    The sequence might be expected to adhere to certain rhythmic qualities, and
    maybe the class can have some ways to check against these expectations...
    - Total => make sure that the chronemes add up to the expected duration.
    - Parse => take a rhymic profile and parse the movement into bars 
                represented as lists of lists of chronemes.
    - Find accents => take an accent profile and apply it to the parsed form
                        of the sequence; return a dict outlining the context
                        that surrounds each beat (e.g. whether it contains
                        a chord tone, chromatic, rest, tied note from offbeat,
                        etc.)
    
    """
    def __init__(self) -> None:
        self.chronemes: list[Chroneme]

    @property
    def total(self) -> float:
        """Return the total of all chronemes."""
        return sum(x.duration for x in self.chronemes)
    






whole_note = 1
half_note = 1/2
quarter_note = 1/4
eighth_note = 1/8
sixteenth_note = 1/16
quarter_note_triplet = 3/12 # = 1/4
eighth_note_triplet = 3/24 # = 1/8
sixteenth_note_triplet = 3/48 # = 1/16

def find_strong_beat(rhythm: Sequence[int], accent_pattern: Sequence[bool]) -> tuple[bool, ...]:
    ...
    # 0 = beat 1, 0.25 = beat 2, 0.5 = beat 3, 0.75 = beat 4
    # 1-e-and-a == 0, 0.0625, 0.125, 0.1875

    # The beats in 4/4 will get 4 1/4ths
    # If all the durations in the sequence up to now add up to x, we
    # know whether the next note is a strong beat or not.

    



def build_cluster_contour(sequence: Sequence[Sequence[str]], pattern: Sequence[bool]) -> list[list[str]]:
    """Take a sequence of note clusters and apply the given reversal pattern.

    Examples
    --------
    >>> from src.data.permutation_data import RISING_FALLING, FALLING_FALLING, RISING_RISING, FALLING_RISING
    >>> x = [["C", "E", "G"], ["D", "F", "A"], ["E", "G", "B"], ["F", "A", "C"], ["G", "B", "D"], ["A", "C", "E"], ["B", "D", "F"]]
    >>> for y in [RISING_FALLING, FALLING_FALLING, RISING_RISING, FALLING_RISING]:
    ...     print(build_cluster_contour(x, y))
    [['C', 'E', 'G'], ['A', 'F', 'D'], ['E', 'G', 'B'], ['C', 'A', 'F'], ['G', 'B', 'D'], ['E', 'C', 'A'], ['B', 'D', 'F']]
    [['G', 'E', 'C'], ['A', 'F', 'D'], ['B', 'G', 'E'], ['C', 'A', 'F'], ['D', 'B', 'G'], ['E', 'C', 'A'], ['F', 'D', 'B']]
    [['C', 'E', 'G'], ['D', 'F', 'A'], ['E', 'G', 'B'], ['F', 'A', 'C'], ['G', 'B', 'D'], ['A', 'C', 'E'], ['B', 'D', 'F']]
    [['G', 'E', 'C'], ['D', 'F', 'A'], ['B', 'G', 'E'], ['F', 'A', 'C'], ['D', 'B', 'G'], ['A', 'C', 'E'], ['F', 'D', 'B']]
    """
    pattern_ = list(pattern)
    while len(pattern_) < len(sequence):
        pattern_ += pattern_

    new_sequence: list[list[str]] = []
    for i, cluster in enumerate(sequence):
        new_cluster = list(cluster)
        if pattern_[i]:
            new_cluster = list(reversed(cluster))
        new_sequence.append(new_cluster)
    return new_sequence



def analyse_adherence(seq) -> None:
    """

    PSEUDO
    ------

    Assumptions
    +++++++++++

    Beats are tracked by calculating the total duration up to now.
    If there is no duration, we must be on beat 1.
    Example in DOWNBEAT:

    0, 0.25, 0.5, 0.75 are the four quarter note beats.
    0 and 0.5 are the beats 1 and 3 (ON BEAT)
    0.25 and 0.75 are the beats 2 and 4 (OFF BEAT)


    Process
    +++++++

    Step 1) 
    
    Create a dictionary of "normal" beats with their duration-indices:

    beat1: 0, beat2: 0.25, beat3: 0.5, beat4: 0.75

    Bar 1 starts at 0, where beat1 is 0.0, beat2 is 0.25
    Bar 2 starts at 1, where beat1 is 1.0, beat2 is 1.25
    Bar 3 starts at 2, where beat1 is 2.0, beat2 is 2.25

    This extends for the expected length of the composition.

    Step 2)

    Analyze the Movement. 
        1. crawl through the movement and keep track of the total duration
        at each step.
        2. if the current duration is equal to one of the normal beats, 
        then we know that the chroneme is in a "normal" position.
        3. a rhythm can be entered as a series of indices where strong beats occur:
            (0, 0.5) => this tells us that index 0 and index 0.5 of each bar will
            contain strong beats. (DOWN BEAT MUSIC)
            (0.25, 0.75) => this tells us that index 0.25 and index 0.75 of each
            bar will contain strong beats. (UP BEAT MUSIC)
            (0, 0.1875, 0.6875, 0.875, 0.75) => the more complex example shows
            how we can mark more sophisticated rhythms like the rumba clave.
            This represents beat 1, beat 1+3/16, beat 2+3/16, beat 3+1/2, beat 4.
        
            
    Notes
    -----
        
    NOTE: We should allow the user to enter rhythms in shorthand: 1, 1e, 2&, 3&, 4a
    But in order to do this accurately, we need to know how many beats to subdivide...
    Beat 3 is halfway in 4/4 but only a quarter in 12/8.
    
    """
    ...
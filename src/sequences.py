
from dataclasses import dataclass
from typing import Any, Sequence


@dataclass
class Chroneme:
    """Chroneme is a length of time during which there is a sound or no sound
    (i.e. a rest). 
    
    The content of a chroneme might be a pitch (or note name representing a 
    pitch), or a rest, or a percussive sound, or an effect, etc.

    The chroneme can also have annotations to indicate stress, volume, timbre,
    and instrument-specific features.


    """
    duration: float
    content: str
    annotations: dict[str, Any]


@dataclass
class Movement:
    """Movement is a sequence of chronemes.
    
    The sequence might be expected to adhere to certain rhythmic qualities
    
    """

    chronemes: list[Chroneme]

    @property
    def duration(self) -> float:
        return sum(x.duration for x in self.chronemes)

whole_note = 1
half_note = 1/2
quarter_note = 1/4
eighth_note = 1/8
sixteenth_note = 1/16
quarter_note_triplet = 3/12 # = 1/4
eighth_note_triplet = 3/24 # = 1/8
sixteenth_note_triplet = 3/48 # = 1/16

from data.permutation_data import ON_BEAT, OFF_BEAT

def find_strong_beat(rhythm: Sequence[int], accent_pattern: Sequence[bool]) -> tuple[bool, ...]:
    
    # 0 = beat 1, 0.25 = beat 2, 0.5 = beat 3, 0.75 = beat 4
    # 1-e-and-a == 0, 0.0625, 0.125, 0.1875

    # The beats in 4/4 will get 4 1/4ths
    # If all the durations in the sequence up to now add up to x, we
    # know whether the next note is a strong beat or not.
    ...


def build_cluster_contour(sequence: Sequence[Sequence[str]], pattern: Sequence[bool]) -> list[list[str]]:
    """Take a sequence of note clusters and apply the given reversal pattern.

    Examples
    --------
    >>> from data.permutation_data import RISING_FALLING, FALLING_FALLING, RISING_RISING, FALLING_RISING
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

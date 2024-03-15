
from typing import Sequence

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
        

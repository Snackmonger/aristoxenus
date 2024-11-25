from typing import Sequence, cast
import pytest

from aristoxenus.core.annotations import ChordData
from aristoxenus.core import rotate
from aristoxenus.core.constants import CHORD_SYMBOL, INTERVAL_NAMES, INTERVAL_STRUCTURE, NOTE_NAMES

params = pytest.mark.parametrize


@params(
    'interval_structure, mode_idx, expected', [
        ([0, 2, 4, 5, 7, 9, 11], 2, (0, 1, 3, 5, 7, 8, 10)),
        ([0, 2, 3, 5, 7, 9, 11], 4, (0, 2, 4, 5, 7, 8, 10)),
        ([0, 2, 4, 5, 7, 9, 11], 5, (0, 2, 3, 5, 7, 8, 10)),
        ([0, 2, 3, 5, 7, 9, 11], 6, (0, 1, 3, 4, 6, 8, 10)),
        ([0, 2, 3, 5, 7, 9, 11], 2, (0, 2, 4, 6, 8, 9, 11))
    ]
)
def test_rotate_interval_structure(interval_structure: Sequence[int], mode_idx: int, expected: tuple[int]) -> None:
    assert rotate.rotate_interval_structure(
        interval_structure, mode_idx) == expected


@params(
    'chord, new_bass_idx, expected', [
        (cast(ChordData, {CHORD_SYMBOL: 'Cmaj', NOTE_NAMES: ('C', 'E', 'G'), INTERVAL_NAMES: ('1', '3', '5'), INTERVAL_STRUCTURE: (0, 4, 7)}), 1, cast(ChordData, {CHORD_SYMBOL: 'Cmaj', NOTE_NAMES: ('E', 'G', 'C'), INTERVAL_NAMES: ('3', '5', '1'), INTERVAL_STRUCTURE: (0, 3, 8)})),
        (cast(ChordData, {CHORD_SYMBOL: 'Cmaj', NOTE_NAMES: ('C', 'E', 'G'), INTERVAL_NAMES: ('1', '3', '5'), INTERVAL_STRUCTURE: (0, 4, 7)}), 2, cast(ChordData, {CHORD_SYMBOL: 'Cmaj', NOTE_NAMES: ('G', 'C', 'E'), INTERVAL_NAMES: ('5', '1', '3'), INTERVAL_STRUCTURE: (0, 5, 9)})),
        (cast(ChordData, {CHORD_SYMBOL: 'Fmin7', NOTE_NAMES: ('F', 'Ab', 'C', 'Eb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}), 1, cast(ChordData, {CHORD_SYMBOL: 'Fmin7', NOTE_NAMES: ('Ab', 'C', 'Eb', 'F'), INTERVAL_NAMES: ('b3', '5', 'b7', '1'), INTERVAL_STRUCTURE: (0, 4, 7, 9)})),
        (cast(ChordData, {CHORD_SYMBOL: 'Fmin7', NOTE_NAMES: ('F', 'Ab', 'C', 'Eb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}), 2, cast(ChordData, {CHORD_SYMBOL: 'Fmin7', NOTE_NAMES: ('C', 'Eb', 'F', 'Ab'), INTERVAL_NAMES: ('5', 'b7', '1', 'b3'), INTERVAL_STRUCTURE: (0, 3, 5, 8)})),
        (cast(ChordData, {CHORD_SYMBOL: 'Fmin7', NOTE_NAMES: ('F', 'Ab', 'C', 'Eb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}), 3, cast(ChordData, {CHORD_SYMBOL: 'Fmin7', NOTE_NAMES: ('Eb', 'F', 'Ab', 'C'), INTERVAL_NAMES: ('b7', '1', 'b3', '5'), INTERVAL_STRUCTURE: (0, 2, 5, 9)}))
    
    ]
)
def test_rotate_chord(chord: ChordData, new_bass_idx: int, expected: ChordData) -> None:
    assert rotate.rotate_chord(chord, new_bass_idx) == expected


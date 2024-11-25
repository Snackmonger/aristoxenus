from typing import Iterable, cast
import pytest

from aristoxenus.core.annotations import ChordData
from aristoxenus.core import (
    voicing
)
from aristoxenus.core.constants import CHORD_SYMBOL, NOTE_NAMES, INTERVAL_NAMES, INTERVAL_STRUCTURE, DROP_2_VOICING, DROP_2_AND_4_VOICING, DROP_3_VOICING, DROP_2_AND_3_VOICING

params = pytest.mark.parametrize


@pytest.fixture
def Cmajor7() -> ChordData:
    return cast(ChordData, {CHORD_SYMBOL:  'Cmaj7', NOTE_NAMES: ('C', 'E', 'G', 'B'), INTERVAL_NAMES:  ("1", "3", "5", "7"), INTERVAL_STRUCTURE:  (1, 4, 7, 11)})


@params(
    "drop_notes, expected", [
        (DROP_2_VOICING, cast(ChordData, {CHORD_SYMBOL:  'Cmaj7', NOTE_NAMES: ('C', 'G', 'B', 'E'), INTERVAL_NAMES:  ('1', '5', '7', '3'), INTERVAL_STRUCTURE:  (1, 7, 11, 16)})),
        (DROP_3_VOICING, cast(ChordData, {CHORD_SYMBOL:  'Cmaj7', NOTE_NAMES: ('C', 'B', 'E', 'G'), INTERVAL_NAMES:  ('1', '7', '3', '5'), INTERVAL_STRUCTURE:  (1, 11, 16, 19)})),
        (DROP_2_AND_4_VOICING, cast(ChordData, {CHORD_SYMBOL:  'Cmaj7', NOTE_NAMES: ('C', 'G', 'E', 'B'), INTERVAL_NAMES:  ('1', '5', '3', '7'), INTERVAL_STRUCTURE:  (1, 7, 16, 23)})),
        (DROP_2_AND_3_VOICING, cast(ChordData, {CHORD_SYMBOL:  'Cmaj7', NOTE_NAMES: ('C', 'E', 'B', 'G'), INTERVAL_NAMES:  ('1', '3', '7', '5'), INTERVAL_STRUCTURE:  (1, 4, 11, 19)})),
        # If no voicing data is received, expect no change from input.
        ([], cast(ChordData, {CHORD_SYMBOL:  'Cmaj7', NOTE_NAMES: ('C', 'E', 'G', 'B'), INTERVAL_NAMES:  ("1", "3", "5", "7"), INTERVAL_STRUCTURE:  (1, 4, 7, 11)}))
    ]
)
def test_apply_drop_voicing(Cmajor7: ChordData, drop_notes: Iterable[int], expected: ChordData) -> None:
    assert voicing.apply_drop_voicing(Cmajor7, drop_notes) == expected


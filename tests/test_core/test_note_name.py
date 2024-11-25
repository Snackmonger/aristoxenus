
from typing import cast
import pytest

from aristoxenus.core.annotations import NoteNameData
from aristoxenus.core import note_name as n_n
from aristoxenus.core.constants import ACCIDENTALS, NOTE_NAME_INDEX

params = pytest.mark.parametrize

@params(
    'note_data, expected', [
        (cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  1}), True),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  1}), False),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS:  2}), True),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS:  3}), False),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  3}), True),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  1}), False),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  2}), True),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  -1}), False),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  1}), True),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS:  1}), False)
    ]
)
def test_is_enharmonically_natural(note_data: NoteNameData, expected: bool) -> None:
    assert n_n.is_enharmonically_natural(note_data) == expected


@params(
    'note_data, expected',
    [
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS:  0}), 'C'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  1}), 'D#'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  -1}), 'Eb'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  1}), 'B#'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS:  4}), 'F####'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  -1}), 'Ab'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  1}), 'E#'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  -1}), 'Gb'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  -1}), 'Bb'),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  2}), 'D##')
    ]
)
def test_encode_note_name(note_data: NoteNameData, expected: str):
    assert n_n.encode_note_name(note_data) == expected


@params(
    'note_name, expected', [
        ('B#', cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  1})),
        ('C', cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS:  0})),
        ('D#', cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  1})),
        ('Eb', cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  -1})),
        ('E####', cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  4})),
        ('E#', cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  1})),
        ('Fb', cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS:  -1})),
        ('G#', cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  1})),
        ('Gb', cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  -1})),
        ('Abb', cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  -2}))
    ]
)
def test_decode_note_name(note_name: str, expected: NoteNameData) -> None:
    assert n_n.decode_note_name(note_name) == expected


@params(
    'note_data, expected', [
        (cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  4}), cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  1})),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS:  4}), cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  0})),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  4}), cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  1})),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS:  -1}), cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  0})),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  2}), cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS:  0}))
    ]
)
def test_simplify_note_name(note_data: NoteNameData, expected: NoteNameData) -> None:
    assert n_n.simplify_note_name(note_data) == expected


@params(
    'keynote, expected', [
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS:  1}), (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS:  1}), cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  -1}))),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  1}), (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS:  1}), cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS:  -1}))),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS:  1}), (cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS:  1}), cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  -1}))),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  -1}), (cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  -1}), cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS:  1}))),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  -1}), (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS:  -1}), cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS:  1})))
    ]
)
def test_split_binomial_note(keynote: NoteNameData, expected: tuple[NoteNameData, NoteNameData]) -> None:
    assert n_n.split_binomial_note(keynote) == expected

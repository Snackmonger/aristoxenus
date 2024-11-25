from typing import Iterable, Optional
import pytest

from aristoxenus.core.annotations import NoteNameData
from aristoxenus.core import heptatonic_spelling

params = pytest.mark.parametrize


@params(
    'keynote, interval_structure, expected', [
        (NoteNameData(note_name_index=0, accidentals=0), [0, 2, 4, 5, 7, 9, 11],
         ('C', 'D', 'E', 'F', 'G', 'A', 'B')),
        (NoteNameData(note_name_index=1, accidentals=1), [0, 2, 4, 5, 7, 9, 11],
         ('D#', 'E#', 'F##', 'G#', 'A#', 'B#', 'C##')),
        (NoteNameData(note_name_index=1, accidentals=0), [0, 2, 3, 5, 7, 9, 10],
         ('D', 'E', 'F', 'G', 'A', 'B', 'C')),
        (NoteNameData(note_name_index=0, accidentals=0), [0, 2, 3, 5, 7, 9, 10],
         ('C', 'D', 'Eb', 'F', 'G', 'A', 'Bb')),
        (NoteNameData(note_name_index=0, accidentals=1), [0, 1, 3, 4, 6, 8, 10],
         ('C#', 'D', 'E', 'F', 'G', 'A', 'B')),
        (NoteNameData(note_name_index=5, accidentals=-1), [0, 2, 4, 5, 7, 9, 11],
         ('Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G')),
        (NoteNameData(note_name_index=4, accidentals=0), [0, 2, 3, 5, 7, 9, 11],
         ('G', 'A', 'Bb', 'C', 'D', 'E', 'F#')),
        (NoteNameData(note_name_index=3, accidentals=-1), [0, 2, 4, 5, 7, 9, 11],
         ('Fb', 'Gb', 'Ab', 'Bbb', 'Cb', 'Db', 'Eb')),
        (NoteNameData(note_name_index=6, accidentals=1), [0, 2, 4, 5, 7, 9, 11],
         ('B#', 'C##', 'D##', 'E#', 'F##', 'G##', 'A##')),
        (NoteNameData(note_name_index=3, accidentals=0), [0, 2, 3, 5, 7, 9, 11],
         ('F', 'G', 'Ab', 'Bb', 'C', 'D', 'E')),
    ]
)
def test_get_heptatonic_scale_notes(keynote: Optional[NoteNameData], interval_structure: Iterable[int], expected: tuple[str, ...]) -> None:
    assert heptatonic_spelling.get_heptatonic_note_names(
        keynote, interval_structure) == expected


@params(
    'keynote, interval_structure, expected', [
        (NoteNameData(note_name_index=5, accidentals=1), [0, 2, 4, 5, 7, 9, 11],
         ('Bb', 'C', 'D', 'Eb', 'F', 'G', 'A')),
        (NoteNameData(note_name_index=6, accidentals=-1), [0, 2, 4, 5, 7, 9, 11],
         ('Bb', 'C', 'D', 'Eb', 'F', 'G', 'A')),
        (NoteNameData(note_name_index=5, accidentals=2), [0, 2, 4, 5, 7, 9, 11],
         ('B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#')),
        (NoteNameData(note_name_index=3, accidentals=2), [0, 2, 4, 5, 7, 9, 11],
         ('G', 'A', 'B', 'C', 'D', 'E', 'F#')),
        (NoteNameData(note_name_index=3, accidentals=0), [0, 2, 4, 5, 7, 9, 11],
         ('F', 'G', 'A', 'Bb', 'C', 'D', 'E')),
        (NoteNameData(note_name_index=3, accidentals=1), [0, 2, 4, 5, 7, 9, 11],
         ('F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#')),
        (NoteNameData(note_name_index=1, accidentals=1), [0, 2, 4, 5, 7, 9, 11],
         ('Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D')),
        (NoteNameData(note_name_index=2, accidentals=-1), [0, 2, 4, 5, 7, 9, 11],
         ('Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D')),
        (NoteNameData(note_name_index=1, accidentals=0), [0, 2, 4, 5, 7, 9, 11],
         ('D', 'E', 'F#', 'G', 'A', 'B', 'C#'))
    ]
)
def test_get_best_heptatonic_spelling(keynote: NoteNameData, interval_structure: Iterable[int], expected: tuple[str, ...]) -> None:
    assert heptatonic_spelling.get_best_heptatonic_names(
        keynote, interval_structure) == expected


@params(
    'interval_structure, expected', [
        ([0, 1, 4, 5, 6, 8, 9], ('1', 'b2', '3', '4', 'b5', 'b6', 'bb7')),
        ([0, 2, 4, 6, 7, 9, 11], ('1', '2', '3', '#4', '5', '6', '7')),
        ([0, 2, 4, 5, 7, 8, 9], ('1', '2', '3', '4', '5', 'b6', 'bb7')),
        ([0, 2, 4, 5, 8, 9, 11], ('1', '2', '3', '4', '#5', '6', '7')),
        ([0, 2, 3, 5, 6, 9, 11], ('1', '2', 'b3', '4', 'b5', '6', '7')),
        ([0, 1, 4, 5, 7, 8, 10], ('1', 'b2', '3', '4', '5', 'b6', 'b7')),
        ([0, 2, 3, 5, 7, 9, 10], ('1', '2', 'b3', '4', '5', '6', 'b7')),
        ([0, 2, 4, 5, 6, 9, 10], ('1', '2', '3', '4', 'b5', '6', 'b7')),
        ([0, 1, 3, 4, 6, 8, 10], ('1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7')),
        ([0, 2, 4, 6, 7, 8, 11], ('1', '2', '3', '#4', '5', 'b6', '7'))
    ]
)
def test_get_heptatonic_interval_symbols(interval_structure: Iterable[int], expected: tuple[str, ...]) -> None:
    assert heptatonic_spelling.get_heptatonic_interval_names(interval_structure) == expected


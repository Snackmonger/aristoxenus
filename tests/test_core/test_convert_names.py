from typing import Iterable, Sequence, cast
import pytest

from aristoxenus.core import convert_names
from aristoxenus.core.annotations import NoteNameData
from aristoxenus.core.constants import ACCIDENTALS, NOTE_NAME_INDEX


params = pytest.mark.parametrize



@params(
    'interval_names, expected', [
        ('b3', ('bIII',)),
        (['#5', 'b6'], ('#V', 'bVI')),
        ('#3', ('#III',)),
        ('bb7', ('bbVII',)),
        ('b6', ('bVI',)),
        ('#2', ('#II',)),
        ('b5', ('bV',)),
        (['1', 'b3', 'b5'], ('I', 'bIII', 'bV')),
        (['1', '2', '#5'], ('I', 'II', '#V')),
        (['1', '4', '#6', 'b7'], ('I', 'IV', '#VI', 'bVII'))
    ]
)
def test_convert_interval_names_to_roman_names(interval_names: Iterable[str] | str, expected: tuple[str, ...]) -> None:
    assert convert_names.convert_interval_names_to_roman_names(
        interval_names) == expected


@params(
    'roman_names, expected', [
        ('bIII', ('b3',)),
        (['#V', 'bvi'], ('#5', 'b6')),
        ('#III', ('#3',)),
        ('bbVII', ('bb7',)),
        ('bVI', ('b6',)),
        ('vii', ('7',)),
        (['ii', 'iii', '#IV'], ('2', '3', '#4')),
        (['ii', 'iii', '#IV'], ('2', '3', '#4')),
        (['vii', 'bVI', 'bv'], ('7', 'b6', 'b5')),
        ('#vii', ('#7',))
    ]
)
def test_convert_roman_names_to_interval_names(roman_names: Iterable[str] | str, expected: tuple[str, ...]) -> None:
    assert convert_names.convert_roman_names_to_interval_names(roman_names) == expected


@params(
    'root, interval_names, expected', [
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS: -1}), ('1', '3', '#5', 'b7', '9'), ('Ab', 'C', 'E', 'Gb', 'Bb')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS: 2}), ('1', 'b3', '5', 'bb7', '11'), ('G##', 'B#', 'D##', 'F#', 'C##')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS: -1}), ('1', '3', '5', '7', '13'), ('Bb', 'D', 'F', 'A', 'G')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 2, ACCIDENTALS: -1}), ('1', '3', '5', 'b7'), ('Eb', 'G', 'Bb', 'Db')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS: -1}), ('1', '4', '6', '7'), ('Ab', 'Db', 'F', 'G')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS: 0}), ('1', 'b3', '5', '7'), ('D', 'F', 'A', 'C#')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS: -2}), ('5', '1', 'b7', '2'), ('Gbb', 'Cbb', 'Bbbb', 'Dbb')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS: 1}), ('1', '2', 'b7', '11'), ('F#', 'G#', 'E', 'B')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 4, ACCIDENTALS: -1}), ('1', 'b3', 'b5', 'bb7', '9'), ('Gb', 'Bbb', 'Dbb', 'Fbb', 'Ab')),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS: 1}), ('4', '1', '2', '5'), ('D#', 'A#', 'B#', 'E#')),
    ]
)
def test_convert_interval_names_to_note_names(root: NoteNameData, interval_names: Iterable[str], expected: tuple[str, ...]) -> None:
    assert convert_names.convert_interval_names_to_note_names(
        root, interval_names) == expected


@params(
    'interval_names, expected', [
        (('1', '3', '#5', 'b7', '9', 'b13'), (0, 4, 8, 10, 14, 20)),
        (('1', '3', '5', '7', '#9', '#11'),  (0, 4, 7, 11, 15, 18)),
        (('1', '3', '#4', '5', '#6'), (0, 4, 6, 7, 10)),
        (('3', '5', '7'), (0, 3, 7)),
        (('b3', 'b5', 'bb7'), (0, 3, 6)),
        (('2', '5', '1'), (0, 5, 10)),
        (('5', '1', 'b3'), (0, 5, 8)),
        (('b3', '#5', 'b7', '9', '1'), (0, 5, 7, 11, 21)),
        (('5', 'b7', '1', '4', '6'), (0, 3, 5, 10, 14)),
        (('b7', '1', '4', '6'), (0, 2, 7, 11))

    ]
)
def test_convert_interval_names_to_integers(interval_names: Sequence[str], expected: tuple[int, ...]) -> None:
    assert convert_names.convert_interval_names_to_integers(interval_names) == expected


@params(
    'note_names, expected', [
        (('A', 'C#', 'E', 'A', 'C#', 'E', 'A'), (0, 4, 7, 12, 16, 19, 24)),
        (('C', 'Eb', 'Gb', 'Bbb', 'D', 'C', 'D'), (0, 3, 6, 9, 14, 24, 26)),
        (('Ab', 'C', 'Eb', 'G', 'Db', 'Eb', 'C'), (0, 4, 7, 11, 17, 19, 28)),
        (('F', 'G', 'A', 'C', 'E', 'G', 'A'), (0, 2, 4, 7, 11, 14, 16)),
        (('Bb', 'G', 'A#', 'F', 'C'), (0, 9, 12, 19, 26)),
        (('A', 'C#', 'E', 'F', 'G', 'B', 'D', 'G', 'Bb'), (0, 4, 7, 8, 10, 14, 17, 22, 25)),
        (('B', 'B', 'B', 'B'), (0, 12, 24, 36)),
        (('G', 'Bb', 'D', 'F#'), (0, 3, 7, 11)),
        (('C', 'D#', 'F#', 'G#', 'A', 'B'), (0, 3, 6, 8, 9, 11)),
        (('D', 'F', 'Ab', 'Cb', 'E', 'G', 'Bb'), (0, 3, 6, 9, 14, 17, 20))
    ]
)
def test_convert_note_names_to_integers(note_names: Sequence[str], expected: tuple[int, ...]) -> None:
    assert convert_names.convert_note_names_to_integers(note_names) == expected


@params(
    'note_names, expected', [
        (('A', 'C#', 'E', 'G'), ('1', '3', '5', 'b7')),
        (('C#', 'E', 'G', 'Bb'), ('1', 'b3', 'b5', 'bb7')),
        (('E', 'G#', 'A#', 'F#'), ('1', '3', '#4', '2')),
        (('Db', 'F', 'Ab', 'C'), ('1', '3', '5', '7')),
        (('F', 'A', 'C', 'Eb'), ('1', '3', '5', 'b7')),
        (('Bb', 'Db', 'Fb', 'Abb', 'Cb'), ('1', 'b3', 'b5', 'bb7', 'b2')),
        (('D', 'F#', 'A#', 'C'), ('1', '3', '#5', 'b7')),
        (('B', 'Db', 'Fb', 'Ab'), ('1', 'bb3', 'bb5', 'bb7')),
        (('E', 'F#', 'B#', 'Db', 'G', 'B'), ('1', '2', '#5', 'bb7', 'b3', '5')),
        (('F', 'Ab', 'G', 'D', 'B'), ('1', 'b3', '2', '6', '#4'))
    ]
)
def test_convert_note_names_to_interval_names(note_names: Sequence[str], expected: tuple[str, ...]) -> None:
    assert convert_names.convert_note_names_to_interval_names(note_names) == expected


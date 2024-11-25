from typing import Iterable, cast
import pytest

from aristoxenus.core.annotations import IntervalData
from aristoxenus.core import interval
from aristoxenus.core.constants import ABSOLUTE, RELATIVE

params = pytest.mark.parametrize


# TODO: More test cases
@params(
    'interval_names, expected', [
        (["1", "b5", "7", "b3"], ('1', 'b3', 'b5', '7')),
        (["b7", "1", "5", "#11", "3"], ('1', '3', '5', 'b7', '#11')),
        (('2', 'b2', '#2', '1', '5', '7'), ('1', 'b2', '2', '#2', '5', '7'))
    ]
)
def test_sort_interval_names(interval_names: Iterable[str], expected: tuple[str, ...]) -> None:
    assert interval.sort_interval_names(interval_names) == expected



@params(
    'lower,higher, expected', [
        ('C', 'Db', cast(IntervalData, {ABSOLUTE: 1, RELATIVE: 'b2'})),
        ('C', 'D', cast(IntervalData, {ABSOLUTE: 2, RELATIVE: '2'})),
        ('C', 'Ebb', cast(IntervalData, {ABSOLUTE: 2, RELATIVE:  'bb3'})),
        ('C', 'D#', cast(IntervalData, {ABSOLUTE: 3,RELATIVE:  '#2'})),
        ('C', 'Eb', cast(IntervalData, {ABSOLUTE: 3, RELATIVE: 'b3'})),
        ('C', 'E', cast(IntervalData, {ABSOLUTE: 4, RELATIVE: '3'})),
        ('C', 'Fb', cast(IntervalData, {ABSOLUTE: 4, RELATIVE: 'b4'})),
        ('C', 'E#', cast(IntervalData, {ABSOLUTE: 5,RELATIVE:  '#3'})),
        ('C', 'F', cast(IntervalData, {ABSOLUTE: 5, RELATIVE: '4'})),
        ('C', 'F#', cast(IntervalData, {ABSOLUTE: 6,RELATIVE:  '#4'})),
        ('C', 'Gb', cast(IntervalData, {ABSOLUTE: 6, RELATIVE: 'b5'})),
        ('C', 'G', cast(IntervalData, {ABSOLUTE: 7, RELATIVE: '5'})),
        ('C', 'G#', cast(IntervalData, {ABSOLUTE: 8,RELATIVE:  '#5'})),
        ('C', 'Ab', cast(IntervalData, {ABSOLUTE: 8, RELATIVE: 'b6'})),
        ('C', 'A', cast(IntervalData, {ABSOLUTE: 9, RELATIVE: '6'})),
        ('C', 'A#', cast(IntervalData, {ABSOLUTE: 10,RELATIVE:  '#6'})),
        ('C', 'Bbb', cast(IntervalData, {ABSOLUTE: 9, RELATIVE: 'bb7'})),
        ('C', 'Bb', cast(IntervalData, {ABSOLUTE: 10, RELATIVE: 'b7'})),
        ('C', 'B', cast(IntervalData, {ABSOLUTE: 11, RELATIVE: '7'})),
        ('C', 'Cb', cast(IntervalData, {ABSOLUTE: 11, RELATIVE: 'b1'})),
        ('C', 'B#', cast(IntervalData, {ABSOLUTE: 0,RELATIVE:  '#7'})),
        ('A', 'G', cast(IntervalData, {ABSOLUTE: 10, RELATIVE: 'b7'})),
        ('Ab', 'Gb', cast(IntervalData, {ABSOLUTE: 10, RELATIVE: 'b7'})),
        ('A#', 'G#', cast(IntervalData, {ABSOLUTE: 10, RELATIVE: 'b7'})),
        ('A#', 'G', cast(IntervalData, {ABSOLUTE: 9, RELATIVE: 'bb7'})),
        ('A#', 'B#', cast(IntervalData, {ABSOLUTE: 2, RELATIVE: '2'})),
        ('A#', 'C##', cast(IntervalData, {ABSOLUTE: 4, RELATIVE: '3'})),
        ('A', "G#", cast(IntervalData, {ABSOLUTE: 11, RELATIVE: '7'})),
        ('Eb', 'G', cast(IntervalData,{ ABSOLUTE: 4, RELATIVE: '3'})),
        ('Gb', 'C', cast(IntervalData, {ABSOLUTE: 6,RELATIVE:  '#4'})),
        ('Gb', 'D', cast(IntervalData, {ABSOLUTE: 8,RELATIVE:  '#5'})),
        ('Gb', 'Db', cast(IntervalData, {ABSOLUTE: 7, RELATIVE: '5'})),
        ('Gb', 'D#', cast(IntervalData, {ABSOLUTE: 9,RELATIVE:  '##5'})),
        ('Gb', 'B', cast(IntervalData, {ABSOLUTE: 5,RELATIVE:  '#3'})),
        ('Gb', 'Bb', cast(IntervalData, {ABSOLUTE: 4, RELATIVE: '3'})),
        ('A#', 'F', cast(IntervalData, {ABSOLUTE: 7, RELATIVE: 'bb6'})),
        ('F', 'A', cast(IntervalData, {ABSOLUTE: 4, RELATIVE: '3'})),
        ('Gb', 'Bbb', cast(IntervalData, {ABSOLUTE: 3, RELATIVE: 'b3'})),
        ('Gb', 'Fbb', cast(IntervalData, {ABSOLUTE: 9, RELATIVE: 'bb7'})),
        ('Bb', 'Db', cast(IntervalData, {ABSOLUTE: 3, RELATIVE: 'b3'}))
    ]
)
def test_calculate_interval(lower: str, higher: str, expected: IntervalData) -> None:
    assert interval.calculate_interval(lower, higher) == expected



@params(
    'interval_structure, expected', [
        ((0, 2, 4, 5, 7, 9, 11), (0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23)),
        ((0, 1, 3, 4, 6, 9, 10), (0, 1, 3, 4, 6, 9, 10, 12, 13, 15, 16, 18, 21, 22)),
        ((0, 1, 3, 4, 5, 7, 10), (0, 1, 3, 4, 5, 7, 10, 12, 13, 15, 16, 17, 19, 22)),
        ((0, 3, 4, 5, 7, 8, 9), (0, 3, 4, 5, 7, 8, 9, 12, 15, 16, 17, 19, 20, 21)),
        ((0, 2, 4, 5, 6, 9, 11), (0, 2, 4, 5, 6, 9, 11, 12, 14, 16, 17, 18, 21, 23))
    ]
)
def test_get_double_octave(interval_structure: Iterable[int], expected: tuple[int, ...]) -> None:
    assert interval.get_double_octave(interval_structure) == expected


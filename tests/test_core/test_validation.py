from typing import Iterable
import pytest

from aristoxenus.core import validation

params = pytest.mark.parametrize

@params(
    'string, expected', [
        ("Mb", False),
        ("Bbb", True),
        ("Abbbbb", True),
        ("Emin7#11", False),
        ("G", True),
        
        ("F#", True),
        ("Qb#", False),
        ("Eb", True),
        ("A#", True),
        ('C#', True)
    ]
)
def test_is_valid_alphabetic_name(string: str, expected: bool) -> None:
    assert validation.validate_alphabetic_name(string) == expected


@params(
    'string, expected', [
        ("Mb", False),
        ("bVII", True),
        ("i", True),
        ("ii", True),
        ("biii", True),
        
        ("IV", True),
        ("#VI", True),
        ("bbVII", True),
        ("F#", False),
        ('Amin7', False)
    ]
)
def test_is_valid_roman_name(string: str, expected: bool) -> None:
    assert validation.validate_roman_name(string) == expected


@params(
    'string, expected', [
        ("#4", True),
        ("7", True),
        ("b9", True),
        ("11", True),
        ("#4", True),
        
        ("b13", True),
        ("#4", True),
        ("14", False),
        ("bM", False),
        ('Gb', False)
    ]
)
def test_is_valid_interval_name(string: str, expected: bool) -> None:
    assert validation.validate_interval_name(string) == expected


@params(
    'note_names, expected', [
        (['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'], True),
        (['C', 'D#', 'E', 'F', 'G', 'Ab', 'Bb'], True),
        (['C#', 'D#', 'E#', 'F', 'G#', 'A#', 'B#'], False),
        (['C', 'D#', 'Eb', 'F', 'G', 'Ab', 'Bb'], False),
        (['Ab', 'B', 'C#', 'D#', 'E', 'F', 'G#'], False),
        
        (['Ab', 'B', 'C#', 'D#', 'E', 'F', 'G'], True),
        (['Ab', 'B', 'C#', 'D#', 'E#', 'F#', 'G'], True),
        (['Ab', 'B', 'C#', 'D#', 'E#', 'F', 'G'], False),
        (['F', 'G', 'Ab', 'Bb', 'C', 'D#', 'E'], True),
        (['F', 'G', 'Ab', 'B', 'Cb', 'D#', 'E'], False),
    ]
)
def test_is_heptatonic_spelling(note_names: Iterable[str], expected: bool) -> None:
    assert validation.validate_heptatonic_spelling(note_names) == expected


@params(
    'interval_structure, expected', [
        ([0, 2, 3, 4, 5, 6, 7], True),
        ([1, 3, 3, 4, 5, 6, 7], False),
        ([0, 2, 4, 5, 7, 9, 11], True),
        ([1, 3, 3, 4, 5, 6, 7], False),
        ([1, 2, 4, 5, 6, 7], False),
        
        ([0, 1, 4, 5, 7, 8, 10], True),
        ([0, 0, 1, 2, 5, 7, 8], False),
        ([0, 2, 5, 5, 7, 2, 3], False),
        ([0, 3, 9, 4, 5, 6, 7], True),
        ([11, 9, 3, 5, 7, 2, 0], True)
    ]
)
def test_is_heptatonic_structure(interval_structure: Iterable[int], expected: bool) -> None:
    assert validation.validate_heptatonic_structure(interval_structure) == expected


from typing import Iterable
import pytest

from aristoxenus.core import chord_symbol as c_s

params = pytest.mark.parametrize


@params(
    'interval_names, expected', [
        (["1", "3", "5"], 'maj'),
        (["1", "3", "5", "7"], 'maj7'),
        (["1", "3", "5", "7", "9"], 'maj9'),
        (["1", "3", "5", "9"], 'majadd9'),
        (["1", "3", "5", "7", "9", "11"], 'maj11'),
        
        (["1", "3", "5", "7", "9", "11", "13"], 'maj13'),
        (["1", "3", "5", "7", "11"], 'maj7add11'),
        (["1", "3", "5", "7", "9", "13"], 'maj9add13'),
        (["1", "3", "5", "b7"], '7'),
        (["1", "3", "5", "b7", "9"], '9'),
        
        (["1", "3", "5", "b7", "9", "13"], '9add13'),
        (["1", "b3", "5"], 'min'),
        (["1", "b3", "5", "b7", "9"], 'min9'),
        (["1", "b3", "5", "9"], 'minadd9'),
        (["1", "b3", "5", "7"], 'minmaj7'),
        
        (["1", "b3", "5", "7", "9"], 'minmaj9'),
        (["1", "b3", "5", "7", "11"], 'minmaj7add11'),
        (["1", "b3", "5", "7", "9", "11", "13"], 'minmaj13'),
        (["1", "b3", "b5", "b7"], 'min7b5'),
        (["1", "b3", "b5", "b7", "9"], 'min9b5'),
        
        (["1", "b3", "b5", "b7", "9", "11", "13"], 'min13b5'),
        (["1", "b3", "b5", "bb7"], 'dim7'),
        (["1", "b3", "b5", "bb7", "9"], 'dim9'),
        (["1", "b3", "b5", "bb7", "9", "11"], 'dim11'),
        (["1", "3", "7", "9"], 'maj9no5'),
        
        (["1", "2", "5"], 'sus2'),
        (["1", "bb3", "5"], 'susbb3'),
        (["1", "#3", "5"], 'sus#3'),
        (["1", "4", "5"], 'sus4'),
        (["1", "2", "5", "7"], 'maj7sus2'),
        
        (["1", "2", "5", "b7"], '7sus2'),
        (["1", "2", "5", "bb7"], 'sus2bb7'),
        (["1", "3", "5", "bb7"], 'majbb7'),
        (["1", "bb3", "#5", "7"], 'maj7susbb3#5'),
        (["1", "bb3", "b5", "bb7", "9"], 'susbb3b5bb7add9'),
        
        (["1", "5", "bb7", "9"], 'no3bb7add9'),
        (["1", "3", "##5", "7"], 'maj7##5'),
        (["1", "3", "bb5", "7"], 'maj7bb5'),
        (["1", "3", "##5", "bb7"], 'maj##5bb7'),
        (['1', '4', '5', 'b7'], '7sus4')
    ]
)
def test_encode_chord_symbol(interval_names: Iterable[str], expected: str) -> None:
    assert c_s.encode_chord_symbol(interval_names) == expected


@params(
    'chord_symbol, expected', [
        ('C', ('1', '3', '5')),
        ('Cmaj7', ('1', '3', '5', '7')),
        ('CM7', ('1', '3', '5', '7')),
        ('Cm7', ('1', 'b3', '5', 'b7')),
        ('Cmin7', ('1', 'b3', '5', 'b7')),
        
        ('CmΔ7', ('1', 'b3', '5', '7')),
        ('CmM7', ('1', 'b3', '5', '7')),
        ('Cminmaj7', ('1', 'b3', '5', '7')),
        ('CminM7', ('1', 'b3', '5', '7')),
        ('CmM7', ('1', 'b3', '5', '7')),
        
        ('C7aug', ('1', '3', '#5', 'b7')),
        ('Caug7', ('1', '3', '#5', 'b7')),
        ('C+7', ('1', '3', '#5', 'b7')),
        ('C7+', ('1', '3', '#5', 'b7')),
        ('Cmin11b5', ('1', 'b3', 'b5', 'b7', '9', '11')),
        
        ('Co7', ('1', 'b3', 'b5', 'bb7')),
        ('Cmin7b5add11', ('1', 'b3', 'b5', 'b7', '11')),
        ('Cmaj7#5', ('1', '3', '#5', '7')),
        ('Cmaj7sus2', ('1', '2', '5', '7')),
        ('Csus4', ('1', '4', '5')),
        
        ('Csus2', ('1', '2', '5')),
        ('C7sus4', ('1', '4', '5', 'b7')),
        ('Csusbb3bb7', ('1', 'bb3', '5', 'bb7')),
        ('Cmin11', ('1', 'b3', '5', 'b7', '9', '11')),
        ('Cmin11b5', ('1', 'b3', 'b5', 'b7', '9', '11')),
        
        ('Cdim11nobb7', ('1', 'b3', 'b5', '9', '11')),
        ('Abbdim7nob5', ('1', 'b3', 'bb7')),
        ('C9no3', ('1', '5', 'b7', '9')),
        ('Amin7/G', ('b7', '1', 'b3', '5')),
        ('C/G', ('5', '1', '3')),
        
        ('G/C', ('4', '1', '3', '5')),
        ('Amin7/B', ('2', '1', 'b3', '5', 'b7')),
        ('iimin7b5', ('1', 'b3', 'b5', 'b7')),
        ('V7sus4add9', ('1', '4', '5', 'b7', '9')),
        ('viidim9', ('1', 'b3', 'b5', 'bb7', '9'))
    ]
)
def test_decode_chord_symbol(chord_symbol: str, expected: tuple[str, ...]) -> None:
    assert c_s.decode_chord_symbol(chord_symbol) == expected


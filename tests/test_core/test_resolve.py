from typing import Optional
import pytest

from aristoxenus.core.annotations import ChordData
from aristoxenus.core import resolve

params = pytest.mark.parametrize

@params(
    'modal_name, expected', (
        ('ionian b3 b6', ('1', '2', 'b3', '4', '5', 'b6', '7')),
        ('lydian #2 add b6', ('1', '#2', '3', '#4', '5', 'b6', 'b6', '7') ),
        ('phrygian natural 6', ('1', 'b2', 'b3', '4', '5', '6', 'b7')),
        ('aeolian natural 3', ('1', '2', '3', '4', '5', 'b6', 'b7')),
        ('ionian no 5', ('1', '2', '3', '4', '6', '7')),

        ('phrygian no b6 no 5', ('1', 'b2', 'b3', '4', 'b7')),
        ('ion_b3_b6', ('1', '2', 'b3', '4', '5', 'b6', '7')),
        ('lyd_#2_add_b6', ('1', '#2', '3', '#4', '5', 'b6', 'b6', '7')),
        ('phrygianNat6', ('1', 'b2', 'b3', '4', '5', '6', 'b7')),
        ('aeolian_n_3', ('1', '2', '3', '4', '5', 'b6', 'b7')),

        ('ionian no_5', ('1', '2', '3', '4', '6', '7')),
        ('phrygian no_b6_no 5', ('1', 'b2', 'b3', '4', 'b7')),
        ('dorian natural 7', ('1', '2', 'b3', '4', '5', '6', '7')),
        ('dorian nat 7', ('1', '2', 'b3', '4', '5', '6', '7')),
        ('dorian_nat_7', ('1', '2', 'b3', '4', '5', '6', '7')),

        ('dorian_natural_7', ('1', '2', 'b3', '4', '5', '6', '7')),
        ('doriannat7', ('1', '2', 'b3', '4', '5', '6', '7')),
        ('dorianNat7', ('1', '2', 'b3', '4', '5', '6', '7')),
        ('dorianNatural7', ('1', '2', 'b3', '4', '5', '6', '7')),
        ('DorianNat7', ('1', '2', 'b3', '4', '5', '6', '7')),
    )
)
def test_resolve_modal_name(modal_name: str, expected: tuple[str]) -> None:
    assert resolve.resolve_modal_name(modal_name) == expected

@params(
    'scale_name, mode_name, expected', [
        ('altered', 'dorian', (0, 2, 3, 5, 7, 9, 11)),
        ('hemiolic', 'dorian', (0, 1, 2, 4, 6, 8, 9)),
        ('augmented', 'mixolydian', (0, 1, 3, 4, 6, 8, 9)),
        ('hemitonic', 'lydian', (0, 2, 4, 6, 7, 8, 11)),
        ('diminished', 'aeolian', (0, 2, 3, 5, 7, 8, 9)),

        ('harmonic', 'phrygian', (0, 1, 3, 4, 7, 8, 10)),
        ('biseptimal', 'ionian', (0, 2, 4, 5, 7, 10, 11)),
        ('paleochromatic', 'mixolydian', (0, 3, 5, 6, 7, 10, 11)),
        ('augmented', 'lydian', (0, 3, 4, 6, 7, 9, 11)),
        ('hemitonic', 'aeolian', (0, 2, 3, 4, 7, 8, 10)),
    ]
)
def test_resolve_scale_name(scale_name: str, mode_name: Optional[str], expected: tuple[int, ...]) -> None:
    assert resolve.resolve_heptatonic_scale(scale_name, mode_name) == expected


@params(
    'scale_name, expected', [
        # This function should be able to parse any type of scale request:
        # a canon scale + mode, a regular alias, a constructive alias.

        # Canon combinations
        ('diatonic ionian', ('C', 'diatonic', 'ionian')),
        ('hemitonic phrygian', ('C', 'hemitonic', 'phrygian')), 
        ('altered dorian', ('C', 'altered', 'dorian')), 
        ('biseptimal locrian', ('C', 'biseptimal', 'locrian')),
        ('augmented lydian', ('C', 'augmented', 'lydian')),
        
        ('harmonic aeolian', ('C', 'harmonic', 'aeolian')),
        ('D diatonic ionian', ('D', 'diatonic', 'ionian')),
        ('Bb hemitonic phrygian', ('Bb', 'hemitonic', 'phrygian')),
        ('F# altered dorian', ('F#', 'altered', 'dorian')),
        ('Ab biseptimal locrian', ('Ab', 'biseptimal', 'locrian')),
        
        ('E augmented lydian', ('E', 'augmented', 'lydian')),
        ('G## harmonic aeolian', ('G##', 'harmonic', 'aeolian')),
        ('D dia ion', ('D', 'diatonic', 'ionian')),
        (' Bb_hemitonPhrygian', ('Bb', 'hemitonic', 'phrygian')),
        ('F#altDorian ', ('F#', 'altered', 'dorian')),
        
        ('F#altDorian ', ('F#', 'altered', 'dorian')),
        (' Ab Biseptimal Locrian', ('Ab', 'biseptimal', 'locrian')),
        ('_Eauglyd_', ('E', 'augmented', 'lydian')),
        ('_G##_harm_aeol', ('G##', 'harmonic', 'aeolian')),
        ('F# hemiol dor', ('F#', 'hemiolic', 'dorian')),

        # Regular aliases
        ('ionian', ('C', 'diatonic', 'ionian')),
        ('dorian', ('C', 'diatonic', 'dorian')),
        ('phrygian', ('C', 'diatonic', 'phrygian')),
        ('lydian', ('C', 'diatonic', 'lydian')),
        ('mixolydian', ('C', 'diatonic', 'mixolydian')),

        ('aeolian', ('C', 'diatonic', 'aeolian')),
        ('locrian', ('C', 'diatonic', 'locrian')),
        ('C ionian', ('C', 'diatonic', 'ionian')),
        ('D dorian', ('D', 'diatonic', 'dorian')),
        ('E phrygian', ('E', 'diatonic', 'phrygian')),

        ('F lydian', ('F', 'diatonic', 'lydian')),
        ('G mixolydian', ('G', 'diatonic', 'mixolydian')),
        ('A aeolian', ('A', 'diatonic', 'aeolian')),
        ('B locrian', ('B', 'diatonic', 'locrian')),
        ('Cb major', ('Cb', 'diatonic', 'ionian')),

        ('Db dominant', ('Db', 'diatonic', 'mixolydian')),
        ('Eb minor', ('Eb', 'diatonic', 'aeolian')),
        ('Fb major pentatonic', ('Fb', 'minor_pentatonic', '1')),
        ('Gb super locrian', ('Gb', 'altered', 'ionian')),
        ('Ab melodic minor', ('Ab', 'altered', 'dorian')),

        ('Bb lydian augmented', ('Bb', 'altered', 'lydian')),
        ('C lydian dominant', ('C', 'altered', 'mixolydian')),
        ('D half diminished', ('D', 'altered', 'locrian')),
        ('E ultra locrian', ('E', 'hemiolic', 'dorian')),
        ('F altered diminished', ('F', 'hemiolic', 'dorian')),

        ('G neapolitan minor', ('G', 'hemiolic', 'phrygian')),
        ('A mixolydian augmented', ('A', 'hemiolic', 'mixolydian')),
        ('B gypsy minor', ('B', 'hemiolic', 'aeolian')),
        ('C# locrian dominant', ('C#', 'hemiolic', 'locrian')),
        ('D# ukranian dorian', ('D#', 'augmented', 'dorian')),
        
        ('E# phrygian dominant', ('E#', 'augmented', 'phrygian')),
        ('F# harmonic minor', ('F#', 'diatonic', 'ionian')),
        ('G# neapolitan major', ('G#', 'neapolitan', 'ionian')),
        ('A# leading whole tone', ('A#', 'neapolitan', 'dorian')),
        ('B# lydian augmented #6', ('B#', 'neapolitan', 'dorian')),

        ('Cbb lydian augmented dominant', ('Cbb', 'diatonic', 'lydian')),
        ('Dbb lydian dominant b6', ('Dbb', 'neapolitan', 'lydian')),
        ('Ebb major locrian', ('Ebb', 'diatonic', 'locrian')),
        ('Fbb half diminished b4', ('Fbb', 'neapolitan', 'aeolian')),
        ('Gbb altered dominant #2', ('Gbb', 'neapolitan', 'aeolian')),

        ('Abb altered dominant bb3', ('Abb', 'neapolitan', 'locrian')),
        ('Bbb byzantine', ('Bbb', 'double_harmonic', 'ionian')),
        ('C## gypsy minor', ('C##', 'hemiolic', 'aeolian')),
        ('D## hungarian minor', ('D##', 'double_harmonic', 'lydian')),
        ('E## ultra phrygian', ('E##', 'double_harmonic', 'phrygian')),

        # Constructive aliases
        ('ionian b2', ('C', 'hemitonic', 'ionian')),
        ('dorian b2', ('C', 'altered', 'phrygian')),
        ('phrygian b5', ('C', 'diatonic', 'locrian')),
        ('lydian b7', ('C', 'altered', 'mixolydian')),
        ('mixolydian b6', ('C', 'altered', 'aeolian')),

        ('aeolian b2', ('C', 'diatonic', 'phrygian')),
        ('locrian b4', ('C', 'altered', 'ionian')),
        ('C ionian b2', ('C', 'hemitonic', 'ionian')),
        ('D dorian b2', ('D', 'altered', 'phrygian')),
        ('E phrygian b5', ('E', 'diatonic', 'locrian')),

        ('F lydian b7', ('F', 'altered', 'mixolydian')),
        ('G mixolydian b6', ('G', 'altered', 'aeolian')),
        ('A aeolian b2', ('A', 'diatonic', 'phrygian')),
        ('B locrian b4', ('B', 'altered', 'ionian')),
        ('b3, b5', ('C', 'romanian', 'mixolydian')),

        ('b6, b7', ('C', 'altered', 'aeolian')),
        ('b2', ('C', 'hemitonic', 'ionian')),
        ('1, 2, 3, 4, b5, 6, b7b3', ('C', 'harmonic', 'dorian')),
        ('b6 b2 #4', ('C', 'paleochromatic', 'lydian')),
        ('#5', ('C', 'augmented', 'ionian')),

        ('aeolian no 2 no b6', ('C', 'minor_pentatonic', '1')),
        ('G b3, b5', ('G', 'romanian', 'mixolydian')),
        ('G b6, b7', ('G', 'altered', 'aeolian')),
        ('G b2', ('G', 'hemitonic', 'ionian')),
        ('G 1, 2, 3, 4, b5, 6, b7G b3', ('G', 'harmonic', 'dorian')),

        ('G b6 b2 #4', ('G', 'paleochromatic', 'lydian')),
        ('G #5', ('G', 'augmented', 'ionian')),
        ('G aeolian no 2 no b6', ('G', 'minor_pentatonic', '1')),
        ('G## b3, b5', ('G##', 'romanian', 'mixolydian')),
        ('G## b6, b7', ('G##', 'altered', 'aeolian')),

        ('G## b2', ('G##', 'hemitonic', 'ionian')),
        ('G## 1, 2, 3, 4, b5, 6, b7G## b3', ('G##', 'harmonic', 'dorian')),
        ('G## b6 b2 #4', ('G##', 'paleochromatic', 'lydian')),
        ('G## #5', ('G##', 'augmented', 'ionian')),
        ('G## aeolian no 2 no b6Gb3, b5', ('G##', 'insen', '4')),

        # In cases where the accidental of the scale name collides with
        # that of the interval name, the note name is expected to take
        # precedence
        ('Gb6, b7', ('Gb', 'diatonic', 'mixolydian')),
        ('Gb2', ('Gb', 'diatonic', 'ionian')),
        ('G1, 2, 3, 4, b5, 6, b7Gb3', ('G', 'harmonic', 'dorian')),
        ('Gb6 b2 #4', ('Gb', 'diminished', 'lydian')),
        ('G#5', ('G#', 'diatonic', 'ionian')),
    ]
)
def test_resolve_generic_scale_request(scale_name: str, expected: tuple[str, str, str]) -> None:
    assert resolve.resolve_generic_scale_request(scale_name) == expected

@params(
    'chord_symbol, expected', [
    ('Amin7/F#', ChordData(chord_symbol='Amin7/F#', note_names=('F#', 'A', 'C', 'E', 'G'), interval_names=('6', '1', 'b3', '5', 'b7'), interval_structure=(0, 3, 6, 10, 13))),
    ('Gb/F#', ChordData(chord_symbol='Gb/F#', note_names=('F#', 'Gb', 'Bb', 'Db'), interval_names=('#7', '1', '3', '5'), interval_structure=(0, 12, 16, 19))),
    ('Gdim9/Bb', ChordData(chord_symbol='Gdim9/Bb', note_names=('Bb', 'Db', 'Fb', 'A', 'G'), interval_names=('b3', 'b5', 'bb7', '9', '1'), interval_structure=(0, 3, 6, 11, 21))),
    ('A#minmaj7/E#', ChordData(chord_symbol='A#minmaj7/E#', note_names=('E#', 'G##', 'A#', 'C#'), interval_names=('5', '7', '1', 'b3'), interval_structure=(0, 4, 5, 8))),
    ('iim7', ChordData(chord_symbol='iim7', note_names=('I', 'bIII', 'V', 'bVII'), interval_names=('1', 'b3', '5', 'b7'), interval_structure=(0, 3, 7, 10))),
    
    ('viidim7', ChordData(chord_symbol='viidim7', note_names=('I', 'bIII', 'bV', 'bbVII'), interval_names=('1', 'b3', 'b5', 'bb7'), interval_structure=(0, 3, 6, 9))),
    ('G/B', ChordData(chord_symbol='G/B', note_names=('B', 'D', 'G'), interval_names=('3', '5', '1'), interval_structure=(0, 3, 8))),
    ('F#min7#11', ChordData(chord_symbol='F#min7#11', note_names=('F#', 'A', 'C#', 'E', 'B#'), interval_names=('1', 'b3', '5', 'b7', '#11'), interval_structure=(0, 3, 7, 10, 18))),
    ('Gb7b9', ChordData(chord_symbol='Gb7b9', note_names=('Gb', 'Bb', 'Db', 'Fb', 'Abb'), interval_names=('1', '3', '5', 'b7', 'b9'), interval_structure=(0, 4, 7, 10, 13))),
    ('C/E', ChordData(chord_symbol='C/E', note_names=('E', 'G', 'C'), interval_names=('3', '5', '1'), interval_structure=(0, 3, 8))),
    
    ('Dbminmaj9', ChordData(chord_symbol='Dbminmaj9', note_names=('Db', 'Fb', 'Ab', 'C', 'Eb'), interval_names=('1', 'b3', '5', '7', '9'), interval_structure=(0, 3, 7, 11, 14))),
    ('Emin7/D', ChordData(chord_symbol='Emin7/D', note_names=('D', 'E', 'G', 'B'), interval_names=('b7', '1', 'b3', '5'), interval_structure=(0, 2, 5, 9))),
    ('Bbmaj/D', ChordData(chord_symbol='Bbmaj/D', note_names=('D', 'F', 'Bb'), interval_names=('3', '5', '1'), interval_structure=(0, 3, 8))),
    ('C#sus2/D#', ChordData(chord_symbol='C#sus2/D#', note_names=('D#', 'G#', 'C#'), interval_names=('2', '5', '1'), interval_structure=(0, 5, 10))),
    ('ivm7b5', ChordData(chord_symbol='ivm7b5', note_names=('I', 'bIII', 'bV', 'bVII'), interval_names=('1', 'b3', 'b5', 'b7'), interval_structure=(0, 3, 6, 10))),
    ]
)
def test_resolve_chord_symbol(chord_symbol: str, expected: ChordData) -> None:
    assert resolve.resolve_chord_symbol(chord_symbol) == expected

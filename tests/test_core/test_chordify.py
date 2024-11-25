from typing import Iterable, cast
import pytest

from aristoxenus.core import chordify
from aristoxenus.core.annotations import (
    ChordData,
    NoteNameData
)
from aristoxenus.core.constants import (
    ACCIDENTALS,
    NOTE_NAME_INDEX,
    NOTE_NAMES,
    INTERVAL_NAMES,
    INTERVAL_STRUCTURE,
    CHORD_SYMBOL
)

params = pytest.mark.parametrize

@params(
    "keynote, interval_structure, number_of_notes, expected", 
    [
        (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS: 0}), (0, 2, 4, 5, 7, 9, 11), 3,
            (
            cast(ChordData, {CHORD_SYMBOL: 'Dmaj', NOTE_NAMES: ('D', 'F#', 'A'), INTERVAL_NAMES: ('1', '3', '5'), INTERVAL_STRUCTURE: (0, 4, 7)}),
            cast(ChordData, {CHORD_SYMBOL: 'Emin', NOTE_NAMES: ('E', 'G', 'B'), INTERVAL_NAMES: ('1', 'b3', '5'), INTERVAL_STRUCTURE: (0, 3, 7)}),
            cast(ChordData, {CHORD_SYMBOL: 'F#min', NOTE_NAMES: ('F#', 'A', 'C#'), INTERVAL_NAMES: ('1', 'b3', '5'), INTERVAL_STRUCTURE: (0, 3, 7)}),
            cast(ChordData, {CHORD_SYMBOL: 'Gmaj', NOTE_NAMES: ('G', 'B', 'D'), INTERVAL_NAMES: ('1', '3', '5'), INTERVAL_STRUCTURE: (0, 4, 7)}),
            cast(ChordData, {CHORD_SYMBOL: 'Amaj', NOTE_NAMES: ('A', 'C#', 'E'), INTERVAL_NAMES: ('1', '3', '5'), INTERVAL_STRUCTURE: (0, 4, 7)}),
            cast(ChordData, {CHORD_SYMBOL: 'Bmin', NOTE_NAMES: ('B', 'D', 'F#'), INTERVAL_NAMES: ('1', 'b3', '5'), INTERVAL_STRUCTURE: (0, 3, 7)}),
            cast(ChordData, {CHORD_SYMBOL: 'C#minb5', NOTE_NAMES: ('C#', 'E', 'G'), INTERVAL_NAMES: ('1', 'b3', 'b5'), INTERVAL_STRUCTURE: (0, 3, 6)})
            )
        ),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS: -1}), (0, 2, 3, 5, 7, 9, 11), 4,
            (
            cast(ChordData, {CHORD_SYMBOL: 'Abminmaj7', NOTE_NAMES: ('Ab', 'Cb', 'Eb', 'G'), INTERVAL_NAMES: ('1', 'b3', '5', '7'), INTERVAL_STRUCTURE: (0, 3, 7, 11)}),
            cast(ChordData, {CHORD_SYMBOL: 'Bbmin7', NOTE_NAMES: ('Bb', 'Db', 'F', 'Ab'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Cbmaj7#5', NOTE_NAMES: ('Cb', 'Eb', 'G', 'Bb'), INTERVAL_NAMES: ('1', '3', '#5', '7'), INTERVAL_STRUCTURE: (0, 4, 8, 11)}),
            cast(ChordData, {CHORD_SYMBOL: 'Db7', NOTE_NAMES: ('Db', 'F', 'Ab', 'Cb'), INTERVAL_NAMES: ('1', '3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 4, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Eb7', NOTE_NAMES: ('Eb', 'G', 'Bb', 'Db'), INTERVAL_NAMES: ('1', '3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 4, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Fmin7b5', NOTE_NAMES: ('F', 'Ab', 'Cb', 'Eb'), INTERVAL_NAMES: ('1', 'b3', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 6, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Gmin7b5', NOTE_NAMES: ('G', 'Bb', 'Db', 'F'), INTERVAL_NAMES: ('1', 'b3', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 6, 10)})
            )
        ),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 3, ACCIDENTALS: -1}), (0, 2, 3, 5, 7, 9, 10), 4,
         (
            cast(ChordData, {CHORD_SYMBOL: 'Fbmin7', NOTE_NAMES: ('Fb', 'Abb', 'Cb', 'Ebb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Gbmin7', NOTE_NAMES: ('Gb', 'Bbb', 'Db', 'Fb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Abbmaj7', NOTE_NAMES: ('Abb', 'Cb', 'Ebb', 'Gb'), INTERVAL_NAMES: ('1', '3', '5', '7'), INTERVAL_STRUCTURE: (0, 4, 7, 11)}),
            cast(ChordData, {CHORD_SYMBOL: 'Bbb7', NOTE_NAMES: ('Bbb', 'Db', 'Fb', 'Abb'), INTERVAL_NAMES: ('1', '3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 4, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Cbmin7', NOTE_NAMES: ('Cb', 'Ebb', 'Gb', 'Bbb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Dbmin7b5', NOTE_NAMES: ('Db', 'Fb', 'Abb', 'Cb'), INTERVAL_NAMES: ('1', 'b3', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 6, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Ebbmaj7', NOTE_NAMES: ('Ebb', 'Gb', 'Bbb', 'Db'), INTERVAL_NAMES: ('1', '3', '5', '7'), INTERVAL_STRUCTURE: (0, 4, 7, 11)})
        )
        ),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS: -2}), (0, 2, 4, 5, 6, 9, 11), 4,
            (
            cast(ChordData, {CHORD_SYMBOL: 'Bbbmaj7b5', NOTE_NAMES: ('Bbb', 'Db', 'Fbb', 'Ab'), INTERVAL_NAMES: ('1', '3', 'b5', '7'), INTERVAL_STRUCTURE: (0, 4, 6, 11)}),
            cast(ChordData, {CHORD_SYMBOL: 'Cbmin7', NOTE_NAMES: ('Cb', 'Ebb', 'Gb', 'Bbb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Db7susbb3', NOTE_NAMES: ('Db', 'Fbb', 'Ab', 'Cb'), INTERVAL_NAMES: ('1', 'bb3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 2, 7, 10)}),
            cast(ChordData, {CHORD_SYMBOL: 'Ebbmaj7', NOTE_NAMES: ('Ebb', 'Gb', 'Bbb', 'Db'), INTERVAL_NAMES: ('1', '3', '5', '7'), INTERVAL_STRUCTURE: (0, 4, 7, 11)}),
            cast(ChordData, {CHORD_SYMBOL: 'Fbbmaj7sus#3#5', NOTE_NAMES: ('Fbb', 'Ab', 'Cb', 'Ebb'), INTERVAL_NAMES: ('1', '#3', '#5', '7'), INTERVAL_STRUCTURE: (0, 5, 8, 11)}),
            cast(ChordData, {CHORD_SYMBOL: 'Gbminbb7', NOTE_NAMES: ('Gb', 'Bbb', 'Db', 'Fbb'), INTERVAL_NAMES: ('1', 'b3', '5', 'bb7'), INTERVAL_STRUCTURE: (0, 3, 7, 9)}),
            cast(ChordData, {CHORD_SYMBOL: 'Abmin7b5', NOTE_NAMES: ('Ab', 'Cb', 'Ebb', 'Gb'), INTERVAL_NAMES: ('1', 'b3', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 6, 10)})
            )
        ),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 6, ACCIDENTALS: -2}), (0, 2, 3, 5, 6, 9, 11), 4,
        
            (
            cast(ChordData, {CHORD_SYMBOL: 'Bbbminmaj7b5', NOTE_NAMES: ('Bbb', 'Dbb', 'Fbb', 'Ab'), INTERVAL_NAMES: ('1', 'b3', 'b5', '7'), INTERVAL_STRUCTURE: (0, 3, 6, 11)}), 
            cast(ChordData, {CHORD_SYMBOL: 'Cbmin7', NOTE_NAMES: ('Cb', 'Ebb', 'Gb', 'Bbb'), INTERVAL_NAMES: ('1', 'b3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 7, 10)}), 
            cast(ChordData, {CHORD_SYMBOL: 'Dbbminmaj7#5', NOTE_NAMES: ('Dbb', 'Fbb', 'Ab', 'Cb'), INTERVAL_NAMES: ('1', 'b3', '#5', '7'), INTERVAL_STRUCTURE: (0, 3, 8, 11)}), 
            cast(ChordData, {CHORD_SYMBOL: 'Ebb7', NOTE_NAMES: ('Ebb', 'Gb', 'Bbb', 'Dbb'), INTERVAL_NAMES: ('1', '3', '5', 'b7'), INTERVAL_STRUCTURE: (0, 4, 7, 10)}), 
            cast(ChordData, {CHORD_SYMBOL: 'Fbbmaj7sus#3#5', NOTE_NAMES: ('Fbb', 'Ab', 'Cb', 'Ebb'), INTERVAL_NAMES: ('1', '#3', '#5', '7'), INTERVAL_STRUCTURE: (0, 5, 8, 11)}), 
            cast(ChordData, {CHORD_SYMBOL: 'Gbdim7', NOTE_NAMES: ('Gb', 'Bbb', 'Dbb', 'Fbb'), INTERVAL_NAMES: ('1', 'b3', 'b5', 'bb7'), INTERVAL_STRUCTURE: (0, 3, 6, 9)}), 
            cast(ChordData, {CHORD_SYMBOL: 'Abmin7b5', NOTE_NAMES: ('Ab', 'Cb', 'Ebb', 'Gb'), INTERVAL_NAMES: ('1', 'b3', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 3, 6, 10)})
            )
        )
    ]
)
def test_chordify_heptatonic_tertial(keynote: NoteNameData, interval_structure: tuple[int], number_of_notes: int, expected: tuple[ChordData, ...]) -> None:
    assert chordify.chordify_heptatonic_tertial(keynote, interval_structure, number_of_notes) == expected



@params(
    'keynote, interval_structure, number_of_notes, sus, expected', [
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS: 0}), (0, 2, 4, 5, 7, 9, 11), 3, 2, 
            (  
                cast(ChordData, {CHORD_SYMBOL: 'Csus2', NOTE_NAMES: ('C', 'D', 'G'), INTERVAL_NAMES: ('1', '2', '5'), INTERVAL_STRUCTURE: (0, 2, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Dsus2', NOTE_NAMES: ('D', 'E', 'A'), INTERVAL_NAMES: ('1', '2', '5'), INTERVAL_STRUCTURE: (0, 2, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Esusb2', NOTE_NAMES: ('E', 'F', 'B'), INTERVAL_NAMES: ('1', 'b2', '5'), INTERVAL_STRUCTURE: (0, 1, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Fsus2', NOTE_NAMES: ('F', 'G', 'C'), INTERVAL_NAMES: ('1', '2', '5'), INTERVAL_STRUCTURE: (0, 2, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Gsus2', NOTE_NAMES: ('G', 'A', 'D'), INTERVAL_NAMES: ('1', '2', '5'), INTERVAL_STRUCTURE: (0, 2, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Asus2', NOTE_NAMES: ('A', 'B', 'E'), INTERVAL_NAMES: ('1', '2', '5'), INTERVAL_STRUCTURE: (0, 2, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Bsusb2b5', NOTE_NAMES: ('B', 'C', 'F'), INTERVAL_NAMES: ('1', 'b2', 'b5'), INTERVAL_STRUCTURE: (0, 1, 6)})
            )
        ),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS: -1}), (0, 2, 3, 5, 6, 9, 11), 3, 4, 
            (
                cast(ChordData, {CHORD_SYMBOL: 'Absus4b5', NOTE_NAMES: ('Ab', 'Db', 'Ebb'), INTERVAL_NAMES: ('1', '4', 'b5'), INTERVAL_STRUCTURE: (0, 5, 6)}),
                cast(ChordData, {CHORD_SYMBOL: 'Bbsusb4', NOTE_NAMES: ('Bb', 'Ebb', 'F'), INTERVAL_NAMES: ('1', 'b4', '5'), INTERVAL_STRUCTURE: (0, 4, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Cbsus#4#5', NOTE_NAMES: ('Cb', 'F', 'G'), INTERVAL_NAMES: ('1', '#4', '#5'), INTERVAL_STRUCTURE: (0, 6, 8)}),
                cast(ChordData, {CHORD_SYMBOL: 'Dbsus#4', NOTE_NAMES: ('Db', 'G', 'Ab'), INTERVAL_NAMES: ('1', '#4', '5'), INTERVAL_STRUCTURE: (0, 6, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'Ebbsus#4#5', NOTE_NAMES: ('Ebb', 'Ab', 'Bb'), INTERVAL_NAMES: ('1', '#4', '#5'), INTERVAL_STRUCTURE: (0, 6, 8)}),
                cast(ChordData, {CHORD_SYMBOL: 'Fsus4b5', NOTE_NAMES: ('F', 'Bb', 'Cb'), INTERVAL_NAMES: ('1', '4', 'b5'), INTERVAL_STRUCTURE: (0, 5, 6)}),
                cast(ChordData, {CHORD_SYMBOL: 'Gsusb4b5', NOTE_NAMES: ('G', 'Cb', 'Db'), INTERVAL_NAMES: ('1', 'b4', 'b5'), INTERVAL_STRUCTURE: (0, 4, 6)})
            )
         ),
         (cast(NoteNameData, {NOTE_NAME_INDEX: 1, ACCIDENTALS: 1}), (0, 1, 3, 5, 7, 9, 10), 4, 2, 
            (
                cast(ChordData, {CHORD_SYMBOL: 'D#7susb2', NOTE_NAMES: ('D#', 'E', 'A#', 'C#'), INTERVAL_NAMES: ('1', 'b2', '5', 'b7'), INTERVAL_STRUCTURE: (0, 1, 7, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'Emaj7sus2#5', NOTE_NAMES: ('E', 'F#', 'B#', 'D#'), INTERVAL_NAMES: ('1', '2', '#5', '7'), INTERVAL_STRUCTURE: (0, 2, 8, 11)}),
                cast(ChordData, {CHORD_SYMBOL: 'F#7sus2', NOTE_NAMES: ('F#', 'G#', 'C#', 'E'), INTERVAL_NAMES: ('1', '2', '5', 'b7'), INTERVAL_STRUCTURE: (0, 2, 7, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'G#7sus2', NOTE_NAMES: ('G#', 'A#', 'D#', 'F#'), INTERVAL_NAMES: ('1', '2', '5', 'b7'), INTERVAL_STRUCTURE: (0, 2, 7, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'A#7sus2b5', NOTE_NAMES: ('A#', 'B#', 'E', 'G#'), INTERVAL_NAMES: ('1', '2', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 2, 6, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'B#7susb2b5', NOTE_NAMES: ('B#', 'C#', 'F#', 'A#'), INTERVAL_NAMES: ('1', 'b2', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 1, 6, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'C#maj7sus2', NOTE_NAMES: ('C#', 'D#', 'G#', 'B#'), INTERVAL_NAMES: ('1', '2', '5', '7'), INTERVAL_STRUCTURE: (0, 2, 7, 11)})
            )
        ),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 0, ACCIDENTALS: 0}), (0, 2, 4, 5, 7, 9, 10), 4, 2,
            (
                cast(ChordData, {CHORD_SYMBOL: 'C7sus2', NOTE_NAMES: ('C', 'D', 'G', 'Bb'), INTERVAL_NAMES: ('1', '2', '5', 'b7'), INTERVAL_STRUCTURE: (0, 2, 7, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'D7sus2', NOTE_NAMES: ('D', 'E', 'A', 'C'), INTERVAL_NAMES: ('1', '2', '5', 'b7'), INTERVAL_STRUCTURE: (0, 2, 7, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'E7susb2b5', NOTE_NAMES: ('E', 'F', 'Bb', 'D'), INTERVAL_NAMES: ('1', 'b2', 'b5', 'b7'), INTERVAL_STRUCTURE: (0, 1, 6, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'Fmaj7sus2', NOTE_NAMES: ('F', 'G', 'C', 'E'), INTERVAL_NAMES: ('1', '2', '5', '7'), INTERVAL_STRUCTURE: (0, 2, 7, 11)}),
                cast(ChordData, {CHORD_SYMBOL: 'G7sus2', NOTE_NAMES: ('G', 'A', 'D', 'F'), INTERVAL_NAMES: ('1', '2', '5', 'b7'), INTERVAL_STRUCTURE: (0, 2, 7, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'A7susb2', NOTE_NAMES: ('A', 'Bb', 'E', 'G'), INTERVAL_NAMES: ('1', 'b2', '5', 'b7'), INTERVAL_STRUCTURE: (0, 1, 7, 10)}),
                cast(ChordData, {CHORD_SYMBOL: 'Bbmaj7sus2', NOTE_NAMES: ('Bb', 'C', 'F', 'A'), INTERVAL_NAMES: ('1', '2', '5', '7'), INTERVAL_STRUCTURE: (0, 2, 7, 11)})
            )
        ),
        (cast(NoteNameData, {NOTE_NAME_INDEX: 5, ACCIDENTALS: 1}), (0, 2, 3, 5, 7, 8, 11), 3, 4,
            (
                cast(ChordData, {CHORD_SYMBOL: 'A#sus4', NOTE_NAMES: ('A#', 'D#', 'E#'), INTERVAL_NAMES: ('1', '4', '5'), INTERVAL_STRUCTURE: (0, 5, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'B#sus4b5', NOTE_NAMES: ('B#', 'E#', 'F#'), INTERVAL_NAMES: ('1', '4', 'b5'), INTERVAL_STRUCTURE: (0, 5, 6)}),
                cast(ChordData, {CHORD_SYMBOL: 'C#sus4#5', NOTE_NAMES: ('C#', 'F#', 'G##'), INTERVAL_NAMES: ('1', '4', '#5'), INTERVAL_STRUCTURE: (0, 5, 8)}),
                cast(ChordData, {CHORD_SYMBOL: 'D#sus#4', NOTE_NAMES: ('D#', 'G##', 'A#'), INTERVAL_NAMES: ('1', '#4', '5'), INTERVAL_STRUCTURE: (0, 6, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'E#sus4', NOTE_NAMES: ('E#', 'A#', 'B#'), INTERVAL_NAMES: ('1', '4', '5'), INTERVAL_STRUCTURE: (0, 5, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'F#sus#4', NOTE_NAMES: ('F#', 'B#', 'C#'), INTERVAL_NAMES: ('1', '#4', '5'), INTERVAL_STRUCTURE: (0, 6, 7)}),
                cast(ChordData, {CHORD_SYMBOL: 'G##susb4b5', NOTE_NAMES: ('G##', 'C#', 'D#'), INTERVAL_NAMES: ('1', 'b4', 'b5'), INTERVAL_STRUCTURE: (0, 4, 6)})
            )
        )
    ]
)
def test_cordify_heptatonic_sus(keynote: NoteNameData, interval_structure: Iterable[int], number_of_notes: int, sus: int, expected: tuple[ChordData, ...]) -> None:
    assert chordify.chordify_heptatonic_sus(keynote, interval_structure, number_of_notes, sus) == expected
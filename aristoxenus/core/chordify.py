'''
This module contains functions that generate chord scales from scale
and note precursors.
'''

from typing import Iterable, Optional

from aristoxenus.core.annotations import (
    ChordData,
    ChordStyle,
    NoteNameData
)
from aristoxenus.core.chord_symbol import encode_chord_symbol
from aristoxenus.core.heptatonic_spelling import (
    get_heptatonic_interval_names,
    get_heptatonic_note_names
)
from aristoxenus.core.constants import NOTES
from aristoxenus.core.errors import ArgumentError
from aristoxenus.core.interval import get_double_octave
from aristoxenus.core.note_name import decode_note_name
from aristoxenus.core.rotate import rotate_interval_structure


def chordify_heptatonic_tertial(keynote: NoteNameData, interval_structure: Iterable[int], number_of_notes: int, chord_style: Optional[ChordStyle] = None) -> tuple[ChordData, ...]:
    '''
    Create a scale of tertial chords in root position with the given 
    parameters.

    Parameters
    ----------
    interval_structure : Iterable[int]
        A list of intervals representing the scale from which the chords
        will be derived.
    keynote : NoteData
        Data about the keynote
    number_of_notes : int
        How many notes to take in sequence.
    chord_style : ChordStyle
        A dictionary with configurations for the chords' symbol.

    Returns
    -------
    tuple[ChordData, ...]
        A tuple of ChordData representing the requested chord scale.
    '''
    # TODO: write tests
    octave_fold = 4
    step = 2
    if number_of_notes > NOTES:
        raise ArgumentError(
            f"Chords can be generated with a maximum of 7 notes ({number_of_notes=}).")
    chords: list[ChordData] = []
    note_names = get_heptatonic_note_names(keynote, interval_structure)
    interval_structure = tuple(interval_structure)
    for i in range(NOTES):
        root = note_names[i]
        chord_interval_structure = rotate_interval_structure(
            interval_structure, i)
        root_data = decode_note_name(root)
        modal_names = get_heptatonic_note_names(root_data,
                                                 chord_interval_structure)
        interval_symbols = get_heptatonic_interval_names(
            chord_interval_structure)
        if number_of_notes > octave_fold:
            modal_names += modal_names
            interval_symbols = get_heptatonic_interval_names(
                chord_interval_structure, octave=True)
            chord_interval_structure = get_double_octave(
                chord_interval_structure)

        chord_symbol = root + encode_chord_symbol(
            interval_symbols[::step][:number_of_notes],
            chord_style)
        chords.append(
            ChordData(
                chord_symbol=chord_symbol,
                note_names=modal_names[::step][:number_of_notes],
                interval_names=interval_symbols[::step][:number_of_notes],
                interval_structure=chord_interval_structure[::step][:number_of_notes]
            )
        )
    return tuple(chords)


def chordify_heptatonic_sus(keynote: NoteNameData, interval_structure: Iterable[int], number_of_notes: int, sus: int, chord_style: Optional[ChordStyle] = None) -> tuple[ChordData, ...]:
    '''
    Create a scale of sus chords in root position with the 
    given parameters.

    Parameters
    ----------
    interval_structure : Iterable[int]
        A list of intervals representing the scale from which the chords
        will be derived.
    keynote : NoteData
        Data about the keynote.
    number_of_notes : int
        How many notes to take in sequence.
    sus : int
        Which scale degree will be suspended (2 or 4). Note that this refers
        to absolute degrees and not the specific interval names of the actual 
        scale, so e.g. a scale with a '#4' will still simply submit 4.
    chord_style : ChordStyle
        A dictionary with configurations for the chords' symbol.

    Returns
    -------
    tuple[ChordData, ...]
        A tuple of ChordData representing the requested chord scale.
    '''
    octave_fold = 4
    step = 2
    if number_of_notes > NOTES:
        raise ArgumentError(
            f"Chords can be generated with a maximum of 7 notes ({number_of_notes=}).")
    if not sus in (2, 4):
        raise ArgumentError(f"Suspended scale degree must be 2 or 4 ({sus=}).")

    chords: list[ChordData] = []
    note_names = get_heptatonic_note_names(keynote, interval_structure)
    pattern = list(range(13))[::step]
    if sus == 2:
        pattern[1] -= 1
        # pattern = [0, 1, 4, 6, 8, 10, 12]
    else:
        pattern[1] += 1
        # pattern = [0, 3, 4, 6, 8, 10, 12]
    interval_structure = tuple(interval_structure)
    for i in range(NOTES):
        root = note_names[i]
        chord_interval_structure = rotate_interval_structure(
            interval_structure, i)
        root_data = decode_note_name(root)
        modal_names = get_heptatonic_note_names(
            root_data, chord_interval_structure)
        interval_symbols = get_heptatonic_interval_names(
            chord_interval_structure)
        if number_of_notes > octave_fold:
            modal_names += modal_names
            interval_symbols = get_heptatonic_interval_names(
                chord_interval_structure, octave=True)
            chord_interval_structure = get_double_octave(
                chord_interval_structure)

        _pattern = pattern[:number_of_notes]
        ch_note_names = [modal_names[i] for i in _pattern]
        ch_interval_symbols = [interval_symbols[i] for i in _pattern]
        ch_interval_structure = [chord_interval_structure[i] for i in _pattern]
        ch_symbol = root + encode_chord_symbol(ch_interval_symbols, chord_style)
        chords.append(
            ChordData(
                chord_symbol=ch_symbol,
                note_names=tuple(ch_note_names),
                interval_names=tuple(ch_interval_symbols),
                interval_structure=tuple(ch_interval_structure)
            )
        )
    return tuple(chords)

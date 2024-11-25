

from typing import Sequence

from aristoxenus.core.annotations import ChordData
from aristoxenus.core.constants import (
    CHORD_SYMBOL,
    INTERVAL_NAMES,
    INTERVAL_STRUCTURE,
    NOTE_NAMES,
    TONES
)


def rotate_interval_structure(interval_structure: Sequence[int], mode_idx: int) -> tuple[int, ...]:
    '''
    Rotate an interval structure so as to rephrase the intervals from the
    perspective of the new modal starting index.

    Parameters
    ----------
    interval_structure : Sequence[int]
        A sequence of integers representing intervals in semitones.
    mode_idx : int
        The index that will serve as the new '0' of the resulting scale form.

    Returns
    -------
    tuple[int, ...]
        A tuple of integers representing the original scale pattern from 
        the new modal perspective.
    '''
    modal_semitones_offset = interval_structure[mode_idx]
    pitches: list[int] = []
    for i in range(len(interval_structure)):
        new_note_idx = (i + mode_idx) % len(interval_structure)
        original_value = interval_structure[new_note_idx]
        tones_offset = ((i + mode_idx) // len(interval_structure)) * TONES
        new_value = original_value - modal_semitones_offset + tones_offset
        if new_value < 0:
            new_value *= -1
        pitches.append(new_value)
    return tuple(pitches)


def rotate_chord(chord: ChordData, new_bass_idx: int) -> ChordData:
    '''
    Rotate the elements in a chord so that it has a new starting point.

    NOTE: The chord symbol is returned unchanged from this function. Slash
    notation must be added after this step.

    Parameters
    ----------
    chord : ChordData
        A collection of chord information.
    new_bass_idx : int
        The index that will be first in the rotated form.

    Returns
    -------
    ChordData
        The input chord information, but rotated so that the elements at
        the given index are now first.
    '''
    if not new_bass_idx in range(len(chord[INTERVAL_STRUCTURE])):
        new_bass_idx %= len(chord[INTERVAL_STRUCTURE])
    names = list(chord[NOTE_NAMES][new_bass_idx:]) + \
        list(chord[NOTE_NAMES][:new_bass_idx])
    symbols = list(chord[INTERVAL_NAMES][new_bass_idx:]) + \
        list(chord[INTERVAL_NAMES][:new_bass_idx])
    intervals = rotate_interval_structure(
        chord[INTERVAL_STRUCTURE], new_bass_idx)
    return ChordData(
        chord_symbol=chord[CHORD_SYMBOL],
        note_names=tuple(names),
        interval_names=tuple(symbols),
        interval_structure=intervals)

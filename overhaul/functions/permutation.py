
from typing import Sequence
from overhaul.data.constants import TONES, NOTES
from overhaul.functions.nomenclature import decode_note_name, get_heptatonic_interval_symbols, get_heptatonic_scale_notes


def rotate_heptatonic_scale_pattern(interval_structure: Sequence[int], mode_idx: int) -> tuple[int, ...]:
    '''
    Rotate a heptatonic scale pattern so as to rephrase the intervals from the
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
    for i in range(NOTES):
        new_note_idx = (i + mode_idx) % NOTES
        original_value = interval_structure[new_note_idx]
        tones_offset = ((i + mode_idx) // NOTES) * TONES
        new_value = original_value - modal_semitones_offset + tones_offset
        pitches.append(new_value)
    return tuple(pitches)

def get_heptatonic_double_octave(interval_structure: Sequence[int]) -> tuple[int, ...]:
    '''
    Extend the range of a scale pattern to two octaves.

    Parameters
    ----------
    interval_structure : Sequence[int]
        An array of integers representing the intervals of a heptatonic scale.

    Returns
    -------
    tuple[int, ...]
        An array with the original intervals, plus the same intervals an 
        octave higher.
    '''
    double_octave = list(interval_structure)
    for i in range(NOTES):
        double_octave.append(interval_structure[i] + 12)
    return tuple(double_octave)


def get_heptatonic_chord_scale_tertial(interval_structure: Sequence[int], keynote: tuple[int, int], notes: int):
    chords: list[tuple[tuple[str, ...], tuple[str, ...], tuple[int, ...]]] = []
    octave = False
    note_names = get_heptatonic_scale_notes(interval_structure, *keynote)
    for i in range(7):
        root = note_names[i]
        modal_pattern = rotate_heptatonic_scale_pattern(interval_structure, i)
        modal_names = get_heptatonic_scale_notes(modal_pattern, *decode_note_name(root))
        interval_pattern = get_heptatonic_interval_symbols(modal_pattern)
        if notes > 4:
            modal_pattern = get_heptatonic_double_octave(modal_pattern)
            modal_names += modal_names
            octave = True
            interval_pattern = get_heptatonic_interval_symbols(modal_pattern, octave)
        chords.append((modal_names[::2][:notes], 
                       interval_pattern[::2][:notes], 
                       modal_pattern[::2][:notes]))
        
    return chords
        
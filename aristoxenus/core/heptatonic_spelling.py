'''
This module takes precursors and uses them to create new forms.
'''
from typing import Iterable, Optional

from aristoxenus.core.annotations import (
    NoteNameData
)
from aristoxenus.core.constants import (
    ACCIDENTALS,
    DIATONIC,
    FLAT_SYMBOL,
    HEPTATONIC_SCALES,
    NOTE_NAME_INDEX,
    NOTES,
    SHARP_SYMBOL,
    TONES
)
from aristoxenus.core.errors import (
    ArgumentError
)
from aristoxenus.core.note_name import (
    encode_note_name,
    simplify_note_name,
    split_binomial_note,
    is_enharmonically_natural
)
from aristoxenus.core.validation import validate_heptatonic_structure


def get_heptatonic_note_names(keynote: Optional[NoteNameData] = None, interval_structure: Iterable[int] = HEPTATONIC_SCALES[DIATONIC]) -> tuple[str, ...]:
    '''
    Return the note names for the given scale form, root note, and root accidentals.

    Parameters
    ----------
    keynote : NoteData, optional, by default None
        Data about the keynote; None defaults to 'C' (=0, 0).
    interval_structure : Sequence[int], default [0, 2, 4, 5, 7, 9, 11]
        A sequence of integers representing the intervals of a scale form.

    Returns
    -------
    tuple[str, ...]
        A tuple of the seven alphabetic names in the appropriate order and 
        with the appropriate number of accidentals.
    '''
    if keynote is None:
        keynote = NoteNameData(note_name_index=0, accidentals=0)
    interval_structure = tuple(interval_structure)
    result: list[str] = []
    root_pitch: int = HEPTATONIC_SCALES[DIATONIC][keynote[NOTE_NAME_INDEX]] + \
        keynote[ACCIDENTALS]
    for i in range(NOTES):
        new_note_idx = (i + keynote[NOTE_NAME_INDEX]) % NOTES
        tones_offset = ((i + keynote[NOTE_NAME_INDEX]) // NOTES) * TONES
        original_value = HEPTATONIC_SCALES[DIATONIC][new_note_idx]
        relative_value = root_pitch + interval_structure[i]
        accidentals = relative_value - (original_value + tones_offset)
        note_name = encode_note_name(
            NoteNameData(note_name_index=new_note_idx, accidentals=accidentals))
        result.append(note_name)
    return tuple(result)


def get_best_heptatonic_names(keynote: NoteNameData, interval_structure: Iterable[int]) -> tuple[str, ...]:
    '''
    Choose the best set of alphabetic note names for a given heptatonic scale
    and keynote. 

    Parameters
    ----------
    keynote : str
        An alphabetic keynote (not a Roman numeral).
    interval_structure : Sequence[int]
        A collection of integers representing the intervals of a heptatonic
        scale.

    Returns
    -------
    tuple[str, ...]
        A collection of the optimal note names for this scale and keynote.

    Raises
    ------
    ArgumentError
        If the structure is not heptatonic.
    '''
    if not validate_heptatonic_structure(interval_structure):
        raise ArgumentError(
            'This function is intended only for heptatonic scale forms.')

    note = simplify_note_name(keynote)
    # Naturals' default name is always the best.
    if is_enharmonically_natural(note):
        return get_heptatonic_note_names(note, interval_structure)

    # Check both spelling variants of a binomial (black key) note.
    k1, k2 = split_binomial_note(note)
    s1 = get_heptatonic_note_names(k1, interval_structure)
    s2 = get_heptatonic_note_names(k2, interval_structure)
    s1_s = sum(n.count(SHARP_SYMBOL) for n in s1)
    s1_f = sum(n.count(FLAT_SYMBOL) for n in s1)
    s2_s = sum(n.count(SHARP_SYMBOL) for n in s2)
    s2_f = sum(n.count(FLAT_SYMBOL) for n in s2)
    t1, t2 = (s1_s + s1_f), (s2_s + s2_f)
    m1, m2 = (s1_s > 0 and s1_f > 0), (s2_s > 0 and s2_f > 0)
    # Best key is usually as simple as fewest total accidentals.
    if t1 < t2:
        return s1
    if t2 < t1:
        return s2
    # If the accidentals are equal, the best key is the one that does not
    # mix sharps and flats.
    if t1 == t2:
        if m1 and not m2:
            return s2
        if m2 and not m1:
            return s1
    # If both keys have the same number of sharps and flats, and they both
    # mix both types of accidentals, fall back arbitrarily to sharps.
    if SHARP_SYMBOL in encode_note_name(k1):
        return s1
    return s2


def get_heptatonic_interval_names(interval_structure: Iterable[int] = HEPTATONIC_SCALES[DIATONIC], octave: bool = False) -> tuple[str, ...]:
    '''
    Return the numeric interval symbols for the given scale form.

    Parameters
    ----------
    interval_structure : Sequence[int], default [0, 2, 4, 5, 7, 9, 11]
        A sequence of integers representing the intervals of a scale form.
    octave : bool
        Flag whether to extend the structure into the second octave, by 
        default False.

    Returns
    -------
    tuple[str, ...]
        A tuple of the digits 1-7 with the appropriate accidentals.

    Raises
    ------
    ArgumentError
        If the structure is not heptatonic.
    '''
    if not validate_heptatonic_structure(interval_structure):
        raise ArgumentError(
            f'Interval structure must be heptatonic ({interval_structure=}).')
    interval_structure = tuple(interval_structure)
    result: list[str] = []
    for i in range(NOTES if not octave else NOTES * 2):
        degree_name = (i % (TONES if not octave else TONES * 2)) + 1
        normal_value = HEPTATONIC_SCALES[DIATONIC][i % NOTES]
        actual_value = interval_structure[i % len(interval_structure)] % TONES
        accidentals = actual_value - normal_value
        if accidentals > 0:
            interval_name = SHARP_SYMBOL * (accidentals) + str(degree_name)
        else:
            interval_name = FLAT_SYMBOL * (-accidentals) + str(degree_name)
        result.append(interval_name)
    return tuple(result)


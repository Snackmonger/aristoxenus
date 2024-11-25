
from typing import Iterable
from aristoxenus.core.annotations import ChordData
from aristoxenus.core.constants import CHORD_SYMBOL, INTERVAL_NAMES, INTERVAL_STRUCTURE, NOTE_NAMES, TONES
from aristoxenus.core.errors import ArgumentError


def apply_drop_voicing(chord_data: ChordData, drop_notes: Iterable[int]) -> ChordData:
    '''
    Create a drop voicing for the given chord.

    Parameters
    ----------
    chord_data : ChordData
        The chord that will be modified.
    drop_notes : Iterable[int]
        The indices of the intervals to be modified. These are actually
        raised rather than dropped, in order that the new voicing will have
        the same inversion as the old one.
        E.g. (0, 4, 7, 11), [1] -> (0, 7, 11, 16)
             (C, E, G, B),  [1] -> (C, G, B, E)
        The indicies are not the same as the 'drop' notes, so this function
        should be used with the provided constants (DROP_2_VOICING &c.).

    Returns
    -------
    ChordData
        A chord with the original intervals modified according to the given

    Raises
    ------
    ArgumentError
        If one of the drop notes is already the bass (= 0). We do this to 
        ensure that the output is in the same inversion as the input.
    '''
    interval_structure = list(chord_data[INTERVAL_STRUCTURE])
    note_names = list(chord_data[NOTE_NAMES])
    interval_symbols = list(chord_data[INTERVAL_NAMES])
    for i in drop_notes:
        if i == 0:
            raise ArgumentError(
                f"Interval 0 cannot be modified ({drop_notes=}).")
        if i >= len(note_names):
            continue

        interval = chord_data[INTERVAL_STRUCTURE][i]
        interval_structure.remove(interval)
        interval_structure.append(interval + TONES)

        name = chord_data[NOTE_NAMES][i]
        note_names.remove(name)
        note_names.append(name)

        symbol = chord_data[INTERVAL_NAMES][i]
        interval_symbols.remove(symbol)
        interval_symbols.append(symbol)

    return ChordData(
        chord_symbol=chord_data[CHORD_SYMBOL],
        note_names=tuple(note_names),
        interval_names=tuple(interval_symbols),
        interval_structure=tuple(interval_structure)
    )

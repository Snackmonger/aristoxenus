

from data import constants, intervallic_canon, keywords
from data import annotations 
from src import bitwise, nomenclature
from src.permutation import chordify
from src.utils import shift_list


def render_chord_scale(scale: annotations.HeptatonicScales, 
                       mode: annotations.ModalNames, 
                       keynote: str,
                       number_of_notes: int = 3, 
                       base_step: int = 2):

    interval_structure: int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale]
    rotations: int = keywords.MODAL_NAME_SERIES.index(mode)
    interval_structure = bitwise.get_modal_form(interval_structure, rotations)

    note_names = nomenclature.best_heptatonic(keynote, interval_structure)

    chords: dict[str, int] = chordify(interval_structure, number_of_notes, base_step)
    collection: list[dict[str, int|str|list[int]]|list[str]] = []

    # Generate correct note names based on parent scale.
    for i, note in enumerate(note_names):
        new_notes = shift_list(note_names, note)
        new_notes *= constants.NUMBER_OF_OCTAVES
        chord = new_notes[::base_step][:number_of_notes]
        collection.append({"root": note, "notes": chord, "structure": list(chords.values())[i]})

    return collection


from src.parsing import generate_chord_symbol
from data.intervallic_canon import DOMINANT_SEVENTH, DOMINANT_SEVENTH_FLAT_FIVE, MAJOR_SEVENTH, AUGMENTED_MAJOR_SEVENTH


for chord in (DOMINANT_SEVENTH, DOMINANT_SEVENTH_FLAT_FIVE, MAJOR_SEVENTH, AUGMENTED_MAJOR_SEVENTH):
    print (generate_chord_symbol(chord))
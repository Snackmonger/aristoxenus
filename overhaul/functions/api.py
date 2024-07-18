from overhaul.data import annotations
from overhaul.data.constants import DIATONIC, IONIAN

def heptatonic_scale_form(
        keynote: str = "C",
        scale_name: annotations.HeptatonicScales = DIATONIC,
        modal_name: annotations.ModalNames = IONIAN
) -> annotations.APIScaleFormResponse:
    ...



def heptatonic_chord_scale(
        keynote: str = "C",
        scale_name: annotations.HeptatonicScales = DIATONIC,
        modal_name: annotations.ModalNames = IONIAN,
        number_of_notes: int | str = 3,
        base_step: int | str = 2,
        roman_lower: bool = False
) -> annotations.APIChordScaleResponse:
    ...
"""Dataclasses that correspond to API responses, or segments thereof."""

from dataclasses import dataclass

from src.data import annotations
from src.functions import interface

__all__ = ["HeptatonicRendering",
           "ChordScaleRendering",
           "HeptatonicChordRendering"]

@dataclass
class HeptatonicRendering:
    """Simple structure with the same keys as 
    ``annotations.APIScaleFormResponse``.
    """
    scale_name: str
    modal_name: str
    interval_structure: int
    interval_scale: tuple[str, ...]
    interval_map: dict[str, str]
    keynote: str
    binomial_rendering: tuple[str, ...]
    forced_rendering: tuple[str, ...]
    best_keynote: str
    best_rendering: tuple[str, ...]
    

    @classmethod
    def from_names(cls, 
                   scale: annotations.HeptatonicScales, 
                   mode: annotations.ModalNames, 
                   note_name: str) -> "HeptatonicRendering":
        """Alternate constructor to mirror interface parameters."""
        data = interface.heptatonic_form(note_name, scale, mode)
        return cls(**data)
    

@dataclass
class ChordScaleRendering:
    """Simple structure with the same keys as  
    ``annotations.APIChordScaleResponse``.
    """
    scale: str
    mode: str
    keynote: str
    notes: int
    step: int
    chord_scale: list[annotations.HeptatonicChord]
    

    @classmethod
    def from_names(cls, 
                   scale: annotations.HeptatonicScales, 
                   mode: annotations.ModalNames, 
                   note_name: str,
                   notes: int = 3,
                   step: int = 2) -> "ChordScaleRendering":
        """Alternate constructor to mirror interface parameters."""
        data = interface.heptatonic_chord_scale(scale, mode, note_name, notes, step)
        return cls(**data)
    

@dataclass
class HeptatonicChordRendering:
    numeric_degree: str
    root: str
    notes: list[str]
    interval_structure: int
    interval_names: list[str]
    chord_symbol: str
    roman_degree: str
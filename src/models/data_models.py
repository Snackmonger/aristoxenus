"""Dataclasses that correspond to API responses, or segments thereof."""

from dataclasses import dataclass

from data import annotations
from functions import api

__all__ = ["HeptatonicRendering",
           "ChordScaleRendering",
           "HeptatonicChordRendering"]

@dataclass
class HeptatonicRendering:
    """
    Dataclass that matches the dict ``data.annotations.APIScaleFormResponse``,
    which is returned from ``src.functions.api.heptatonic_form``.

    scale_name: str
        The canonical scale base.
    modal_name: str
        The canonical modal rotation from the base.
    interval_structure: int
        The unique integer expression of this scale form.
    interval_scale: tuple[str, ...]
        An array of interval names using Indian numerals.
    interval_map: dict[str, str]
        A chromatic scale that respects the scaleform's unique interval 
        names.
    keynote: str
        The real keynote of the scaleform.
    binomial_rendering: tuple[str, ...]
        The binomial names of the scaleform's notes.
    forced_rendering: tuple[str, ...]
        The names for the scale notes, using the real keynote.
    best_keynote: str
        The best name for the given keynote.
    best_rendering: tuple[str, ...]
        The best names for the scale notes, using the best keynote.
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
        data = api.heptatonic_scale_form(note_name, scale, mode)
        return cls(**data)
    

@dataclass
class ChordScaleRendering:
    """Simple structure with the same keys as  
    ``data.annotations.APIChordScaleResponse``.
    """
    scale_name: str
    modal_name: str
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
        data = api.heptatonic_chord_scale(note_name, scale, mode,  notes, step)
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
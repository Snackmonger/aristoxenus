"""Dataclasses and similar things for modelling data in easy ways."""

from dataclasses import dataclass
from typing import Mapping, Sequence

from data import annotations
from src import interface


@dataclass
class HeptatonicRendering:
    """Simple structure with the same keys as  
    ``annotations.APIScaleFormResponse``.
    """
    scale_name: str
    modal_name: str
    interval_structure: int
    interval_scale: list[str]
    interval_map: dict[str, str]
    keynote: str
    chromatic_rendering: list[str]
    alphabetic_rendering: list[str]
    optimal_keynote: str
    optimal_rendering: list[str]
    

    @classmethod
    def from_names(cls, 
                   scale: annotations.HeptatonicScales, 
                   mode: annotations.ModalNames, 
                   note_name: str) -> "HeptatonicRendering":
        """Alternate constructor to mirror interface parameters."""
        data = interface.render_heptatonic_form(scale, mode, note_name)
        return cls(**data)
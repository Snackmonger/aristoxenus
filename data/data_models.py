"""Dataclasses and similar things for modelling data in easy ways."""

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass
class HeptatonicRendering:
    """Simple structure with the same keys as  
    ``annotations.APIScaleFormResponse``.
    """
    scale_name: str
    modal_name: str
    interval_structure: int
    interval_scale: Sequence[str]
    interval_map: Mapping[str, str]
    keynote: str
    chromatic_rendering: Sequence[str]
    alphabetic_rendering: Sequence[str]
    optimal_keynote: str
    optimal_rendering: Sequence[str]
    
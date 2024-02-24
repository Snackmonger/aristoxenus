

from dataclasses import dataclass


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
    
from typing import Sequence

from src.api import heptatonic_scale_form
from src.constants import (
    HEPTATONIC_ORDER_KEYS,
    HEPTATONIC_SUPPLEMENT,
    INTERVAL_STRUCTURE,
    MODAL_SERIES_KEYS
)

def find_pattern(interval_structure: Sequence[int]) -> tuple[str, str]:
    # this func should become part of the api module, but it needs 
    # a bit more searchitude... have it not only return the canonical
    # names, but also any aliases that exist in the dictionary.
    for scale in HEPTATONIC_ORDER_KEYS:
        for mode in MODAL_SERIES_KEYS:
            data = heptatonic_scale_form(scale_name=scale, modal_name=mode)
            if data[INTERVAL_STRUCTURE] == interval_structure:
                return (scale, mode)
    for scale in HEPTATONIC_SUPPLEMENT:
        for mode in MODAL_SERIES_KEYS:
            data = heptatonic_scale_form(scale_name=scale, modal_name=mode)
            if data[INTERVAL_STRUCTURE] == interval_structure:
                return (scale, mode)
    raise ValueError("Unable to locate sequence.")


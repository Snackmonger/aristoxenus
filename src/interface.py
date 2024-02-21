"""Functions that represent the end-points of an API."""


from typing import Any, Optional

from src import (nomenclature,
                 rendering,
                 bitwise,
                 utils)

from data import (constants,
                  keywords,
                  intervallic_canon)


def chromatic(keynote: str = "C", accidental_type: Optional[str] = None) -> list[str]:
    """Return a chromatic scale in the given accidental style 
    (default=binomial) and starting at the given keynote (default=C).
    """
    if not accidental_type:
        accidental_type = nomenclature.get_accidental_keyword(keynote)
    
    # Catch fuzzy keyword
    keys = [keywords.BINOMIAL, keywords.FLAT, keywords.SHARP]
    for k in keys:
        if accidental_type == k + "s":
            accidental_type = accidental_type[:-1]

    notes: list[str]
    match accidental_type:
        case keywords.BINOMIAL:
            notes = nomenclature.chromatic(constants.BINOMIALS)
        case keywords.SHARP:
            notes = nomenclature.chromatic(constants.SHARPS)
        case keywords.FLAT:
            notes = nomenclature.chromatic(constants.FLATS)
        case _:
            notes = nomenclature.chromatic(constants.BINOMIALS)

    if keynote not in notes:
        raise ValueError(f"Unknown keynote: {keynote}")

    return utils.shift_list(notes, keynote)




def render_heptatonic_form(
        scale_name: str,
        modal_name: str,
        keynote: str
) -> dict[str, Any]: 
    # replace return with a typedDict once we have standardized the output
    '''
    Return a collection of data about a given scaleform configuration.

    Parameters
    ----------
    scale_name : str
        A recognized scale name.
    modal_name : str
        A recognized modal name.
    keynote : str
        A recognized note name (any natural, sharp, flat, or binomial with no 
        more than 1 accidental)

    Returns
    -------
    dict[str, str|tuple[str, ...]|list[str]]
        A dictionary containing information about the rendering under the 
        following keys:
        - modal_name
        - scale_name
        - interval_scale
        - interval_structure
        - chromatic_rendering
        - alphabetic_rendering
        - recognized_names
        - keynote
        - twelve_tone_intervals
        - optimal_rendering
        - optimal_keynote
    '''
    base_scale:int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale_name]
    modal_rotations: int = keywords.MODAL_NAME_SERIES.index(modal_name)
    for _ in range(modal_rotations):
        base_scale = bitwise.previous_inversion(base_scale, 12)
    render_base: list[str] = chromatic(keynote)

    chromatic_rendering: tuple[str, ...] = tuple(
        rendering.render_plain(base_scale, render_base))
    best_rendering: tuple[str, ...] = tuple(
        nomenclature.best_heptatonic(keynote, base_scale))
    forced_rendering: tuple[str, ...] = best_rendering
    if not keynote in constants.BINOMIALS:
        forced_rendering: tuple[str, ...] = tuple(
            nomenclature.force_heptatonic(keynote, base_scale))
        
    numeric_rendering: tuple[str, ...] = tuple(
        nomenclature.name_heptatonic_intervals(base_scale))
    twelve_tone_intervals: dict[str, str] = dict(
        zip(utils.shift_list(nomenclature.chromatic(), keynote),
            nomenclature.twelve_tone_scale_intervals(base_scale)))
    
    interval_map = nomenclature.get_interval_map(keynote, base_scale)

    # this is fine for now, this should be a typeddict once the final
    # form is known
    return {keywords.SCALE_NAME: scale_name,
            keywords.MODAL_NAME: modal_name,
            keywords.INTERVAL_STRUCTURE: base_scale,
            keywords.INTERVAL_SCALE: numeric_rendering,
            keywords.INTERVAL_MAP: interval_map,
            keywords.KEYNOTE: keynote,
            keywords.CHROMATIC_RENDERING: chromatic_rendering,
            keywords.ALPHABETIC_RENDERING: forced_rendering,
            keywords.OPTIMAL_KEYNOTE: best_rendering[0],
            keywords.OPTIMAL_RENDERING: best_rendering,
            keywords.TWELVE_TONE_INTERVALS: twelve_tone_intervals}


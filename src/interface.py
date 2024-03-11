"""Functions that represent the end-points of an API."""


from typing import Optional

from src import (nomenclature,
                 rendering,
                 bitwise,
                 utils)

from data import (annotations,
                  constants,
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
        scale_name: annotations.HeptatonicScales,
        modal_name: annotations.ModalNames,
        keynote: str
) -> annotations.APIScaleFormResponse:
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
    '''
    scale_base: int = intervallic_canon.HEPTATONIC_SYSTEM_BY_NAME[scale_name]
    modal_rotations: int = keywords.MODAL_NAME_SERIES.index(modal_name)
    scale_base = bitwise.get_modal_form(scale_base, modal_rotations)
    binomial_base: list[str] = chromatic(
        nomenclature.decode_enharmonic(keynote))

    # Chromatic rendering will use binomials (the 'absolute' spelling)
    chromatic_rendering: list[str] = rendering.render_plain(scale_base, binomial_base)

    # Optimal rendering is that which has the fewest accidentals, while
    # still maintaining the alphabetic order (the 'correct' spelling).
    optimal_rendering: list[str] = nomenclature.best_heptatonic(keynote, scale_base)

    # Alphabetic rendering forces the nomenclature to follow the given
    # keynote, even if it makes an awkward spelling. If the keynote was
    # a binomial, use the optimal rendering instead.
    alphabetic_rendering: list[str] = optimal_rendering
    if not keynote in constants.BINOMIALS:
        alphabetic_rendering = nomenclature.force_heptatonic(keynote, scale_base)

    # Interval scale is a list of intervals in the scale, spelled correctly so
    # that there is exactly one each of 12334567, plus any accidentals.
    interval_scale: list[str] = nomenclature.name_heptatonic_intervals(scale_base)
    
    # Interval map is a dictionary of the chromatic binomials to the
    # 7 correct interval names, plus 5 supplementary names, which can be used
    # to supply chromatic accidentals to the scale intervals. The interval map
    # for just the scale notes could be dict(zip(optimal_rendering, interval_scale))
    interval_map: dict[str, str] = nomenclature.get_interval_map(keynote, scale_base, True)

    return annotations.APIScaleFormResponse(scale_name=scale_name,
                                            modal_name=modal_name,
                                            interval_structure=scale_base,
                                            interval_scale=interval_scale,
                                            interval_map=interval_map,
                                            keynote=keynote,
                                            chromatic_rendering=chromatic_rendering,
                                            alphabetic_rendering=alphabetic_rendering,
                                            optimal_keynote=optimal_rendering[0],
                                            optimal_rendering=optimal_rendering)

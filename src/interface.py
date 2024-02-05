"""Functions that process and supply the larger chunks of data requested by the API."""


from typing import Any

from src import (nomenclature,
                 rendering,
                 bitwise,
                 parsing,
                 utils,
                 permutation)

from data import (constants,
                  keywords,
                  intervallic_canon)


def render_heptatonic_form(scale_name: str, modal_name: str, keynote: str) -> dict[str, Any]:
    '''
    Render the given heptatonic scale according to the given modal name and keynote.

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
        - recognized_names
        - keynote
        - rendering
        - optimal_rendering
        - optimal_keynote
    '''
    
    base_scale: int = {value: key for key, value in intervallic_canon.HEPTATONIC_SYSTEM_BY_NUMBER.items()}[scale_name]
    modal_rotations: int = keywords.MODAL_NAME_SERIES.index(modal_name)
    for _ in range(modal_rotations):
        base_scale = bitwise.previous_inversion(base_scale, 12)

    render_base: list[str] = nomenclature.chromatic()
    if keynote in constants.SHARPS:
        render_base = nomenclature.chromatic(constants.SHARPS)
    elif keynote in constants.FLATS:
        render_base = nomenclature.chromatic(constants.FLATS)

    render_base = utils.shift_list(render_base, keynote)

    chromatic_rendering: tuple[str, ...] = tuple(rendering.render_plain(base_scale, render_base))
    forced_rendering: tuple[str, ...]  = tuple(nomenclature.force_heptatonic(keynote, base_scale))
    best_rendering: tuple[str, ...]  = tuple(nomenclature.best_heptatonic(keynote, base_scale))
    numeric_rendering: tuple[str, ...]  = tuple(parsing.name_heptatonic_intervals(base_scale))
    

    return {keywords.SCALE_NAME: scale_name,
            keywords.MODAL_NAME: modal_name,
            keywords.INTERVAL_STRUCTURE: base_scale,
            keywords.INTERVAL_SCALE: numeric_rendering,
            keywords.KEYNOTE: keynote,
            keywords.CHROMATIC_RENDERING: chromatic_rendering,
            keywords.ALPHABETIC_RENDERING: forced_rendering,
            keywords.OPTIMAL_KEYNOTE: best_rendering[0],
            keywords.OPTIMAL_RENDERING: best_rendering}



def render_heptatonic_chord_scale(optimal_rendering: tuple[str, ...], 
                       notes: str|int):
    
    # Because the optimal form might use a mix of accidentals
    # in order to maintain alphabetic order, we can't generate
    # chords from the integer interval maps...

    # EDIT: actually, it might be easier just to render the scale as
    # if it were pure, then write a function to mask a specific spelling.
    
    
    base_form = parsing.parse_literal_sequence(optimal_rendering)
    chords = permutation.chordify(base_form, notes)

    

    series = [utils.roman_numeral(i+1).upper() for i in range(len(keywords.MODAL_NAME_SERIES))]


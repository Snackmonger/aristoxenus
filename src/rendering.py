
from data import constants
from src import nomenclature


def render(interval_structure: int, 
           chromatic_scale: list[str] | None = None
           ) -> list[str]:
    '''
    Return a human-readable list of strings representing the pitch collection
    in the given accidental style.

    Params:
            
    '''
    # TODO: The rendering should involve a little bit more decision resolution:

    # 2) If the range of the interval map exceeds the chromatic scale, we should
    #    automatically switch to scientific rendering mode, so we can distinguish
    #    between the octaves of the multi-octave structure. No more of making the user
    #    check for exact lengths.

    # 3) We should add a function that raises or lowers the range of a whole scientific
    #    rendering, so that if the renderer is forced to use scientific notation starting
    #    from C0, we can easily shift it into the range of C3 (e.g.).

    # MOve rendering logic to separate module

    if chromatic_scale is None:
        chromatic_scale = nomenclature.chromatic(constants.BINOMIALS)
    if interval_structure.bit_length() > len(chromatic_scale):
        chromatic_scale *= 8

    rendering: list[str] = []
    for interval in range(0, interval_structure.bit_length()):
        binary_column: int = 1 << interval # tonic is least significant bit
        if (interval_structure & binary_column) == binary_column:
            rendering.append(chromatic_scale[interval])
    return rendering




def render_multi_octave():
    ...



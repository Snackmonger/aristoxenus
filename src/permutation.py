'''
Functions relating to permuting different types of interval structures.
'''
from .models.interval_structures import Scale
from .errors import OctaveRotationError


def triads(interval_structure: int, step: int=2) -> dict[str, int]:
    '''
    Return a dict of triads for the given scale and structural principle.

    Parameters
    ----------
    interval_structure : int
        A 12-bit representation of a scale-like interval structure.
    step : int
        The number of structural steps between chord intervals.        

    Returns
    -------
    dict[str, int]
        
    '''
    if not interval_structure.bit_length() <= 12:
        raise OctaveRotationError()
    scale: Scale = Scale(interval_structure)
    scale_modes: list[int] = scale.inversions
    extra_octaves: int = steps * 12
    chord_scale: list[int] = []
    for mode in scale_modes:
        ...


'''
Functions relating to permuting different types of interval structures.
'''

import loguru

from .models.interval_structures import Scale
from . import bitwise
from .errors import OctaveRotationError

logger = loguru.logger


def triads(interval_structure: int, step: int=2) -> list[int]:
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
    chord: list[int] = []
    for interval in list(bitwise.iterate_intervals(interval_structure))[::step]:
            logger.debug(bin(interval), interval)
            chord.append(interval)
    return chord[:3]

    



    


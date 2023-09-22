'''
Decorators that are used in the program.
'''

from typing import Callable, Any, TYPE_CHECKING

from .errors import IntervalOOBError
from .enums import OOBOptions

if TYPE_CHECKING:
    from .models.interval_structures import IntervalStructure, LimitedIntervalStructure

# Note: decorators are basically magic to me, so I'm sure these
# are absolutely terrible ways of achieving the desired goal,
# but that's part of the learning process...


# ----------------------- models.interval_structures ----------------------- #

def pos_only(function: Callable[..., Any]) -> Callable[..., Any]:
    '''
    Make sure the interval is not a negative number.
    '''
    def wrapper(self: 'IntervalStructure',
                interval: 'int | IntervalStructure',
                *args: tuple[Any, ...]) -> 'int | IntervalStructure':
        interval = int(interval)
        if interval < 0:
            interval *= -1
        return function(self, interval, *args)
    return wrapper


def check_oob(func: Callable[..., 'int | LimitedIntervalStructure']
              ) -> Callable[..., 'LimitedIntervalStructure']:
    '''
    Check whether an interval is beyond the limit of the structure,
    and perform a designated action if so.
    '''
    def wrapper(self: 'LimitedIntervalStructure',
                interval: int) -> 'LimitedIntervalStructure':
        
        if interval.bit_length() > self.bits:
            match self.oob:
                case OOBOptions.INTEGRATE:
                    interval >>= self.bits
                case OOBOptions.OCT_INTEGRATE:
                    interval >>= 12
                case OOBOptions.ERROR:
                    raise IntervalOOBError(bin(interval))
                case OOBOptions.IGNORE:
                    interval = 1
                case _:
                    pass
        return func(self, interval)
    return wrapper

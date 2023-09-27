'''
Decorators that are used in the program.
'''
from typing import Callable, TYPE_CHECKING, TypeVar, ParamSpec
import loguru

from .errors import IntervalOutOfBoundsError
from .enums import OOBOptions

if TYPE_CHECKING:
    from .models.interval_structures import IntervalStructure, LimitedIntervalStructure

T = TypeVar('T')
P = ParamSpec('P')

logger = loguru.logger

# Note: decorators are basically magic to me, so I'm sure these
# are absolutely terrible ways of achieving the desired goal,
# but that's part of the learning process...


# ----------------------- models.interval_structures ----------------------- #

def pos_only(function: Callable[P, T]) -> Callable[P, T]:
    '''
    Make sure the interval is not a negative number.
    '''
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        for arg in args:
            if isinstance(arg, int) and arg < 0:
                arg *= -1
        return function(*args, **kwargs)
    return wrapper


def check_oob(func: Callable[P, T]) -> Callable[P, T]:
    '''
    Check whether an interval is beyond the limit of the structure,
    and perform a designated action if so.
    '''
    def wrapper(self: 'LimitedIntervalStructure',
                interval: int,
                *args: P.args,
                **kwargs: P.kwargs) -> T:
        if interval.bit_length() > self.bits:
            match self.oob:
                case OOBOptions.INTEGRATE:
                    interval >>= self.bits
                case OOBOptions.OCT_INTEGRATE:
                    interval >>= 12
                case OOBOptions.ERROR:
                    raise IntervalOutOfBoundsError(f'Max bits: {self.bits} Current bits: {interval.bit_length()} (={bin(interval)})')
                case OOBOptions.IGNORE:
                    interval = 1
                case _:
                    interval = 1
        return func(self, interval, *args, **kwargs)
    return wrapper





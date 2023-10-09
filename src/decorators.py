'''
Decorators that are used in the program.
'''
from typing import Callable, TYPE_CHECKING, TypeVar, ParamSpec, Concatenate

from data import constants
from data.errors import IntervalOutOfBoundsError
from data.enums import OOBOptions

if TYPE_CHECKING:
    from .models.interval_structures import LimitedIntervalStructure

T = TypeVar('T')
P = ParamSpec('P')

# Note: decorators are basically magic to me, so I'm sure these
# are absolutely terrible ways of achieving the desired goal,
# but that's part of the learning process...

# Second note: why in the efferucking heck do these dramn decorators
# play so poorly with type hints? Ths seems to fix the errors in pylint,
# bit it's kind of ugly...


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


def check_oob(func: Callable[Concatenate[..., int, P], T]) -> Callable[Concatenate[..., int, P], T]:
    '''
    Perform the action designated in the subclass' `oob` attribute if the given 
    interval is out of bounds of the interval structure's limits.
    '''
    def wrapper(self: 'LimitedIntervalStructure',
                interval: int,
                *args: P.args,
                **kwargs: P.kwargs) -> T:
        if self.oob not in OOBOptions:
            self.oob = OOBOptions.IGNORE
        if interval.bit_length() > self.bits:
            match self.oob:
                case OOBOptions.INTEGRATE_LOW:
                    interval >>= self.bits
                case OOBOptions.INTEGRATE_HIGH:
                    interval >>= constants.TONES
                case OOBOptions.ERROR:
                    raise IntervalOutOfBoundsError(f'Max bits: {self.bits} Current bits: {interval.bit_length()} (={bin(interval)})')
                case OOBOptions.IGNORE:
                    interval = 1
        return func(self, interval, *args, **kwargs)
    return wrapper


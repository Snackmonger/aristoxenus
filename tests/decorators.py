import time
from typing import TypeVar, ParamSpec, Callable


P = ParamSpec("P")
T = TypeVar("T")

def test_perf(on: bool = False) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Measure how long the function takes to run."""
    def inner(func: Callable[P, T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            p1 = time.perf_counter()
            v = func(*args, **kwargs)
            p2 = time.perf_counter()
            if on:
                print(f"Operation for {func.__name__} took {p2-p1} seconds.")
            return v
        return wrapper
    return inner


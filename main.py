from functools import partial
from typing import Any, Callable


# def partial(func: Callable[..., Any],
#             /,
#             *args: tuple[Any, ...],
#             **keywords: dict[str, Any]) -> Callable[..., Any]:
#     """Return a partial application of the given function and arguments."""

#     def newfunc(*fargs: tuple[Any, ...], **fkeywords: dict[str, Any]):
#         newkeywords = {**keywords, **fkeywords}
#         return func(*args, *fargs, **newkeywords)
#     return newfunc


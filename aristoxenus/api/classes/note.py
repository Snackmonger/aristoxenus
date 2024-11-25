

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Note:
    note_name: Optional[str] = None
    interval_name: Optional[str] = None
    octave: Optional[int] = None
    duration: Optional[float] = None
    dynamics: Optional[Iterable[str]] = None
    annotation: Optional[str] = None

    def __repr__(self):
        field_values = {k: v for k, v in self.__dict__.items() if v is not None}
        field_str = ', '.join(f'{k}={repr(v)}' for k, v in field_values.items())
        return f'{self.__class__.__name__}({field_str})'
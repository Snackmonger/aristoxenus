
from typing import Optional, Sequence

from src import rendering






class Chord:
    def __init__(self, /, chord_name: Optional[str] = None, keynote: Optional[str] = None, structure: Optional[int] = None, note_names: Optional[Sequence[str]] = None) -> None:
        self.base_structure: int
        self.base_note_names: list[str]
        self.inversion: int
        self.voicing: tuple[int, ...]

        if structure:
            if keynote:
                self.base_structure = structure
                self.base_note_names = rendering.render_plain(structure)
                


# x = Chord("G#maj7").invert(3).voicing("drop2")
                
from src.utils import encode_numeration




print(encode_numeration(3, "polyad"))
from typing import Optional
from src import (nomenclature, 
                 utils, 
                 rendering)



class IntervalStructure:

    def __init__(self, value: int, keynote: Optional[str]) -> None:
        self.value = value
        self.keynote = keynote

    def __repr__(self) -> str:
        return str(self.render_binomial())

    def render_binomial(self, keynote: Optional[str]) -> list[str]:
        if keynote is None:
            if self.keynote:
                keynote = self.keynote
            else:
                keynote = "C"
        keynote = nomenclature.decode_enharmonic(keynote)
        chromatic = utils.shift_list(nomenclature.chromatic(), keynote)
        return rendering.render_plain(self.value, chromatic)

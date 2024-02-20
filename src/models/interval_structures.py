from src import (nomenclature,
                 utils,
                 rendering)


class IntervalStructure:

    def __init__(self, value: int) -> None:
        self.value = value

    def render_binomial(self, keynote: str) -> list[str]:
        keynote = nomenclature.decode_enharmonic(keynote)
        chromatic = utils.shift_list(nomenclature.chromatic(), keynote)
        return rendering.render_plain(self.value, chromatic)

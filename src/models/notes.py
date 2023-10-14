from typing import Callable

from src import (nomenclature)

from data import (constants,
                  keywords)


class Note():

    def __init__(self):
        self.frequency: float
        self.sharp: str
        self.flat: str
        self.binomial: str
        self.enharmonics: tuple[str, ...]
        self.preferred: str
        self.dynamics: float
        self.volume: float
        self.duration: int

    def __repr__(self) -> str:
        return self.preferred

    @classmethod
    def from_note_name(cls, note_name: str):
        ...

    @classmethod
    def from_frequency(cls,
                       frequency: float,
                       temperament_: Callable[..., tuple[float, ...]]
                       ) -> 'Note':
        if not frequency in temperament_():
            raise ValueError
        new_instance = cls()
        new_instance.frequency = frequency

        # If the note is natural, these will all be the same (e.g. C4)
        new_instance.sharp = nomenclature.convert_frequency_to_note(frequency, constants.SHARPS)
        new_instance.flat = nomenclature.convert_frequency_to_note(frequency, constants.FLATS)
        new_instance.binomial = nomenclature.convert_frequency_to_note(frequency, constants.BINOMIALS)

        enh = nomenclature.encode_scientific_enharmonic
        binomial = new_instance.binomial
        new_instance.enharmonics = tuple(
            [enh(binomial, name, keywords.ABOVE) for name in constants.NATURALS]
          + [enh(binomial, name, keywords.BELOW) for name in constants.NATURALS]
            )

        return new_instance
    


    
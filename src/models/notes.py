from src import (nomenclature)
from data import (constants)


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
    def from_frequency(cls, frequency: float):
        if not frequency in nomenclature.equal_temperament():
            raise ValueError
        new_instance = cls()
        new_instance.frequency = frequency
        new_instance.sharp = nomenclature.convert_frequecy_to_note(frequency, constants.SHARPS)
        new_instance.flat = nomenclature.convert_frequecy_to_note(frequency, constants.FLATS)
        new_instance.binomial = nomenclature.convert_frequecy_to_note(frequency, constants.BINOMIALS)

    
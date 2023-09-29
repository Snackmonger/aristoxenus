from src import nomenclature
from data import constants



def enharmonic_decoder():
    print(nomenclature.enharmonic_decoder())


def chromatic():
    print(nomenclature.chromatic(constants.BINOMIALS))


def encode_enharmonic(note_value: str, note_name: str):
    print(nomenclature.encode_enharmonic(note_value, note_name))
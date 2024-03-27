import rewrites
from tests.test_data import chord_tests
from data.intervallic_canon import *

for x, y in chord_tests.items():
    if set(y) != set( (z := rewrites.parse_chord_suffix(x)) ):
        print(f"Tested {x}")
        print(f"Expected {y}")
        print(f"Got {z}")

from src.nomenclature import encode_intervals_as_notes


print(encode_intervals_as_notes(["1", "b2", "bb3", "b5", "7"], "D#"))
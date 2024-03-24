from data import constants
from src import bitwise
from src import interface
from src.interface import render_plain
from src.models.heptatonic import HeptatonicStructure
from rich import print
from src.parsing import parse_polychord_symbol, remove_chord_prefix, parse_heptatonic_scale_structure


from data.intervallic_canon import *


my_scale = HeptatonicStructure("D", "diatonic", "lydian")

print(parse_heptatonic_scale_structure(DIATONIC_SCALE))

print(parse_heptatonic_scale_structure(bitwise.next_inversion(DIATONIC_SCALE, 12)))


# for i, inversion in enumerate(bitwise.inversions(DIATONIC_SCALE, 12)):
#     key = constants.NATURALS[i]
#     scale = interface.render_plain(inversion, key)
#     print(scale)
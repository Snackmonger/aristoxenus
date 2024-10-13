import random
from src.constants import HEPTATONIC_SCALES
from src.classes import HeptatonicScale

for scale, pattern in HEPTATONIC_SCALES.items():
    print(scale)
    print(pattern)
    chord_scale = HeptatonicScale(scale_name=scale)
    for degree in [6, 2, 5, 1]:
        inversion = random.randint(0, 3)
        print(chord_scale.tertial_tetrad(degree).invert(inversion).symbol)
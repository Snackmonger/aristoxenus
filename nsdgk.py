
from data import intervallic_canon
from src.models import heptatonic

x = heptatonic.HeptatonicStructure("Eb")
# y = heptatonic.Chord.from_parent_scale(x, 1)
y = heptatonic.Chord.from_interval_structure(intervallic_canon.DITONE | intervallic_canon.TRITONE | intervallic_canon.COMPOUND_DITONE, "Eb")

for _ in range(7):
    print(y)
    y = y.invert(1)

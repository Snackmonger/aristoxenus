
from src.models import interval_structures
from data import intervallic_canon


def test_double_octave():
    x = interval_structures.DoubleOctave()

    print(x, type(x))
    x += intervallic_canon.DITONE

    print(x, type(x))
    x += intervallic_canon.DIAPENTE

    print(x, type(x))

    x.next_inversion()

    print(x, type(x))

    x.previous_inversion()

    print(x, type(x))

    print(x.intervals)

    print(x.inversions)
    
    print(x.upper)

    print(x.lower)
from src.models.interval_structures import LimitedIntervalStructure, Octave
from src.intervallic_canon import DIATONIC_SCALE, HEMIOLION, NINTH, FLAT_NINTH

def test1():
    x = LimitedIntervalStructure(12)

    x += DIATONIC_SCALE

    print(x)
    x.previous_inversion()
    print(x)
    x.previous_inversion()
    print(x)
    x.previous_inversion()
    print(x)
    x.previous_inversion()
    print(x)
    x.previous_inversion()
    print(x)
    x.previous_inversion()
    print(x)
    x.previous_inversion()
    x += 33
    print(x, type(x))

def test2():
    x = LimitedIntervalStructure(12)

    x += DIATONIC_SCALE

    print(x, type(x))

    x += -HEMIOLION

    print(x, type(x))

    x -= HEMIOLION

    print(x, type(x))



def test3():

    x = Octave(DIATONIC_SCALE)

    print(x)

    print('adding NINTH')

    x += NINTH

    print(x)
    print('(transposed to 2, but already in scale)')

    print('adding FLAT NINTH')

    x += FLAT_NINTH

    print(x)
    print('transposed to b2 and added')

    
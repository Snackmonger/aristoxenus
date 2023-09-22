from src.models.interval_structures import LimitedIntervalStructure
from src.intervallic_canon import DIATONIC_SCALE
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
print(x)

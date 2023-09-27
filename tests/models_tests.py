from src.models import interval_structures
from src import intervallic_canon


x = interval_structures.LimitedIntervalStructure(12)

x += intervallic_canon.DITONE
x += intervallic_canon.DIAPENTE
x += intervallic_canon.COMPOUND_DITONE

print(x)

x.next_inversion()

print(x)

print(x.inversions)

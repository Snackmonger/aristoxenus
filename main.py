
from src.bitwise import inversions
from data.intervallic_canon import DIATONIC_SCALE
from src.nomenclature import name_heptatonic_intervals
from src.permutation import tetrad_variants
from src.rendering import render_plain


# for inv in inversions(DIATONIC_SCALE, 12):
#     print(name_heptatonic_intervals(render_plain(inv)))


# for x in tetrad_variants():
#     print(x['canonical_name'])

#     for name, expr in x['close'].items():
#         print(name, render_plain(expr))
#         print()

x = tetrad_variants()

r = x[3]['canonical_name']
print(r)
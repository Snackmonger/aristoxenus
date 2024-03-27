import rewrites
from tests.test_data import chord_tests
from data.intervallic_canon import *


print(rewrites.parse_slash_chord_symbol("Gmaj7#11/B"))

# 2024-03-27 05:17:54.448 | INFO     | rewrites:parse_chord_symbol:79 - G, maj7#11
# {'chord_symbol': 'Gmaj7#11/B', 'interval_names': ('3', '5', '7', '#11', '1'), 'note_names': ('B', 'B#', 'D', 'F#', 'G'), 'interval_structure': 395}
from overhaul.data.constants import DIATONIC, HEPTATONIC_SCALES
from overhaul.functions.permutation import get_heptatonic_chord_scale_tertial


print(get_heptatonic_chord_scale_tertial(HEPTATONIC_SCALES[DIATONIC], (3, 0), 6))
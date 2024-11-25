from aristoxenus.core.constants import AEOLIAN, ALTERED, DOUBLE_HARMONIC, IONIAN, LYDIAN, PALEOCHROMATIC
from aristoxenus.core.resolve import resolve_scale_pattern




resolve_scale_pattern((0, 2, 3, 4, 7, 9))

add = (
    ("dominant pentatonic", ["african pentatonic"], (0, 2, 4, 7, 10)),
    ("pelog pentatonic", ["phrygian pentatonic"], (0, 1, 3, 7, 8)),
    ("blues", ["minor blues"], (0, 3, 5, 6, 7, 10)),
    ("major blues", [], (0, 2, 3, 4, 7, 9)),
    )

names = [
    ("charukeshi", (ALTERED, AEOLIAN)),
    ("bhairav", (DOUBLE_HARMONIC, IONIAN)),
    ("double harmonic minor", (DOUBLE_HARMONIC, LYDIAN)),
    ("puriya daneshri", (PALEOCHROMATIC, LYDIAN)),
    ("indian pentatonic", ('pelog pentatonic', "5"))
]
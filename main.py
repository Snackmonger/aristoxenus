# from src.models.diagrams import (FingeringRepr,
#                                  FingeringType,
#                                  FingeringWidth,
#                                  GuitarFingeringDiagram,
#                                  simplify_guitar_fretboard,
#                                  guitar_fretboard,
#                                  convert_fretboard_to_relative)


# f = simplify_guitar_fretboard(guitar_fretboard())


# f = convert_fretboard_to_relative(f, "A")


# x = GuitarFingeringDiagram(5, f, FingeringWidth.OPEN, FingeringType.PINKY)


# x.apply_fingering()


# for y in x.grid:
#     for a in y:
#         a.flip()
#         a.rendering_mode = FingeringRepr.FINGER

#     print (y)

from data.intervallic_canon import DIATONIC_SCALE, DIMINISHED_SCALE, HEMIOLIC_SCALE
from src.bitwise import previous_inversion
from src.nomenclature import twelve_tone_scale_intervals


x = previous_inversion(DIATONIC_SCALE, 12)
wh = 0b111011011

print(twelve_tone_scale_intervals(wh))
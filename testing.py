# from src.permutation import tetrad_variants, triad_variants

# from src.rendering import render_plain


# for variant in tetrad_variants():
#     for k, v in variant.items():
#         if isinstance(v, dict):
#             for kk, vv in v.items():
#                 if isinstance(vv, int):
#                     print(k, kk, render_plain(vv))
#         elif isinstance(v, int):
#             print(k, render_plain(v))


from typing import Literal, NotRequired, TypedDict


ITEMA: str = "itema"
ITEMB: Literal["itemb"] = "itemb"
ITEMC: str = "itemc"
dictionary: dict[str, dict[str, int] | list[int]] = {"itema": {}, "itemb": []}
dictionary[ITEMA].update({"key1": 55})
dictionary[ITEMB].append(55)

class Dictionary(TypedDict):
    itema: dict[str, int]
    itemb: list[int]
    itemc: NotRequired[int]

dictionary2: Dictionary = Dictionary(itema={"key1": 33}, itemb=[77, 88, 99])
dictionary2[ITEMA].update({"key2": 101})
dictionary2[ITEMB].append(202)
dictionary2[ITEMC] = 909

print(dictionary2[ITEMC], dictionary2[ITEMA])


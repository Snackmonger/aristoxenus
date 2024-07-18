from src.data.keywords import MODAL_SERIES_KEYS
from src.data.intervallic_canon import HEPTATONIC_ORDER_VALUE_TO_KEY_MAP, HEPTATONIC_ORDER_VALUES
from src.functions.bitwise import get_rotation
from src.functions.nomenclature import force_heptatonic
from src.data.constants import LEGAL_ROOT_NAMES


for x in LEGAL_ROOT_NAMES:
    print(f"Now working out {x}")
    for y in HEPTATONIC_ORDER_VALUES:
        for z in range(0, 7):
            form = get_rotation(y, z)
            print(f"{HEPTATONIC_ORDER_VALUE_TO_KEY_MAP[y]} {MODAL_SERIES_KEYS[z]} = {force_heptatonic(x, form)}")
    print()

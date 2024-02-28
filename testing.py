
from data import (chord_symbols)

from src import (nomenclature)




print(nomenclature.basic_chord_scale("diatonic", "ionian", "C", "tetrad", "tertial"))




def chord_symbol_from_interval_names(interval_names: list[str]) -> list[str]:

    # when a chord's intervals have been derived from its position in a chord 
    # scale, we can distinguish between interval names that have the same 
    # enharmonic values. thus a chord 1 bb3 5 7 would be spelled maj7sus2
    # if we don't know the context in the parent chord scale, but when we
    # know how to interpret the intervals nomenclaturally, we can generate
    # something like maj7bb3

    symbol: str
    if chord_symbols.CHORD_3 in interval_names:
        symbol = chord_symbols.CHORD_MAJ
    
    if chord_symbols.CHORD_FLAT_3 in interval_names:
        if chord_symbols.CHORD_FLAT_5 in interval_names:
            ...

        symbol = chord_symbols.CHORD_DIM

    if chord_symbols.CHORD_FLAT_3:
        ...

    for x in [chord_symbols.CHORD_SHARP_5, chord_symbols.CHORD_FLAT_5]:
        if x in interval_names:
            ...
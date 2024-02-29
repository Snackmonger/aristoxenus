
from data import (chord_symbols, keywords)

from src import nomenclature



def chord_symbol_from_interval_names(interval_names: list[str]) -> list[str]:

    # when a chord's intervals have been derived from its position in a chord 
    # scale, we can distinguish between interval names that have the same 
    # enharmonic values. thus a chord 1 bb3 5 7 would be spelled maj7sus2
    # if we don't know the context in the parent chord scale, but when we
    # know how to interpret the intervals nomenclaturally, we can generate
    # something like maj7bb3

    symbols: list[str] = []
    fifth: str = ""
    i: int = 0
    interval_names.pop(0) # get rid of unison

    diminished_symbols = [chord_symbols.CHORD_FLAT_3, 
                          chord_symbols.CHORD_FLAT_5, 
                          chord_symbols.CHORD_DOUBLE_FLAT_7]
    
    main_suffixes = [chord_symbols.CHORD_FLAT_7, 
                     chord_symbols.CHORD_7, 
                     chord_symbols.CHORD_DOUBLE_FLAT_7]

    main_suffix: str = ""
    for symb in main_suffixes:
        if symb in interval_names:
            main_suffix = symb

    if chord_symbols.CHORD_7 in main_suffix:
        main_suffix.replace(chord_symbols.CHORD_7, chord_symbols.CHORD_MAJ_7)

    if chord_symbols.CHORD_FLAT_7 in main_suffix:
        main_suffix.replace(chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_7)

    if all([x in interval_names for x in diminished_symbols]):
        main_suffix = main_suffix.replace(chord_symbols.CHORD_DOUBLE_FLAT_7,
                                          chord_symbols.CHORD_DIM)
    largest_extension: str = ""
    for symb in [chord_symbols.CHORD_9,
                 chord_symbols.CHORD_11,
                 chord_symbols.CHORD_13]:
        if symb in interval_names:
            interval_names.pop(interval_names.index(symb))
            largest_extension = symb

    if largest_extension:
        main_suffix = main_suffix.replace(chord_symbols.CHORD_7, largest_extension)

    if chord_symbols.CHORD_3 in interval_names:
        if not chord_symbols.CHORD_FLAT_7 in interval_names:
            symbols.append(chord_symbols.CHORD_MAJ)

    if chord_symbols.CHORD_FLAT_3 in interval_names:
        if not any([chord_symbols.CHORD_DIM in main_suffix,
                    chord_symbols.CHORD_MAJ in main_suffix]):
            symbols.append(chord_symbols.CHORD_FLAT_3)

    if chord_symbols.CHORD_SHARP_5 in interval_names:
        i = interval_names.index(chord_symbols.CHORD_SHARP_5)
        fifth =  interval_names.pop(i)
    
    if chord_symbols.CHORD_FLAT_5 in interval_names:
        i = interval_names.index(chord_symbols.CHORD_FLAT_5)
        fifth = interval_names.pop(i)






    

    # main_suffix + fifth + altered_extensions
    


interval_chords: list[list[str]] = []
    

for scale in keywords.HEPTATONIC_ORDER:
    for mode in keywords.MODAL_NAME_SERIES:
        x = nomenclature.heptatonic_chord_scale(scale, mode, "C", 4)
        for y in x:
            if (z:=y['interval_names']) not in interval_chords:
                interval_chords.append(z)

for x in sorted(interval_chords):
    print (x, "\n")
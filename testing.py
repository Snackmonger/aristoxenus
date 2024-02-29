
import time
from data import (chord_symbols, keywords)
from src import nomenclature


def tetrad_intervals() -> list[list[str]]:
    """Use the canonical scales and modes to generate a list of all possible
    tetrad types, expressed as lists of their intervals in the contexts of 
    their parent scaleforms (and therefore may have enharmonic spellings).
    """
    interval_chords: list[list[str]] = []
    for scale in keywords.HEPTATONIC_ORDER:
        x = nomenclature.heptatonic_chord_scale(scale, keywords.IONIAN, "C", 4)
        for y in x:
            if (z := y['interval_names']) not in interval_chords:
                interval_chords.append(z)
    return interval_chords


def chord_symbol_from_interval_names(interval_names: list[str]
                                     ) -> str:

    # this function is obscenely slow & requires some kind of revision
    # probably all the pop(index()) is having to crawl the same lists 
    # over and over again
    normal3: str = ""
    main_suffix: str = ""
    alt3: str = ""
    alt5: str = ""
    no5: str = ""
    extensions: str = ""
    
    interval_names.pop(0)  # get rid of unison
    diminished_symbols: list[str] = [chord_symbols.CHORD_FLAT_3,
                                     chord_symbols.CHORD_FLAT_5,
                                     chord_symbols.CHORD_DOUBLE_FLAT_7]
    main_suffixes: list[str] = [chord_symbols.CHORD_FLAT_7,
                                chord_symbols.CHORD_7,
                                chord_symbols.CHORD_DOUBLE_FLAT_7]
    altered_fifths: list[str] = [chord_symbols.CHORD_FLAT_5,
                                 chord_symbols.CHORD_SHARP_5]
    altered_thirds: list[str] = list({x[1] for x in tetrad_intervals()
                                      if not x[1] in [chord_symbols.CHORD_FLAT_3,
                                                      chord_symbols.CHORD_3]})


    if chord_symbols.CHORD_3 in interval_names:
        interval_names.pop(interval_names.index(chord_symbols.CHORD_3))
        if not chord_symbols.CHORD_FLAT_7 in interval_names:
            normal3 = chord_symbols.CHORD_MAJ
            
    if chord_symbols.CHORD_FLAT_3 in interval_names:
        if all([x in interval_names for x in diminished_symbols]):
            for name in diminished_symbols:
                interval_names.pop(interval_names.index(name))
            main_suffix = chord_symbols.CHORD_DIM_7
        else:
            interval_names.pop(interval_names.index(chord_symbols.CHORD_FLAT_3))
        if not any([chord_symbols.CHORD_DIM in main_suffix,
                    chord_symbols.CHORD_MAJ in main_suffix]):
            normal3 = chord_symbols.CHORD_MIN

    for symb in main_suffixes:
        if symb in interval_names:
            main_suffix = interval_names.pop(interval_names.index(symb))

    # Change 7s from literal to symbolic value
    if chord_symbols.CHORD_DOUBLE_FLAT_7 in main_suffix:
        if all(x in interval_names for x in diminished_symbols):
            main_suffix = main_suffix.replace(
                chord_symbols.CHORD_DOUBLE_FLAT_7,
                chord_symbols.CHORD_DIM)
    elif chord_symbols.CHORD_FLAT_7 in main_suffix:
        main_suffix = main_suffix.replace(
            chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_7)
    elif chord_symbols.CHORD_7 in main_suffix:
        main_suffix = main_suffix.replace(
            chord_symbols.CHORD_7, chord_symbols.CHORD_MAJ_7)
        
    largest_extension: str = ""
    for symb in [chord_symbols.CHORD_9,
                 chord_symbols.CHORD_11,
                 chord_symbols.CHORD_13]:
        if symb in interval_names:
            largest_extension += interval_names.pop(interval_names.index(symb))
    
    if largest_extension:
        main_suffix = main_suffix.replace(
            chord_symbols.CHORD_7, largest_extension)
        
    for symb in altered_fifths:
        if symb in interval_names:
            alt5 = interval_names.pop(interval_names.index(symb))

    if chord_symbols.CHORD_FLAT_5 in interval_names:
        alt5 = interval_names.pop(
            interval_names.index(chord_symbols.CHORD_FLAT_5))

    if chord_symbols.CHORD_5 in interval_names:
        interval_names.pop(interval_names.index(chord_symbols.CHORD_5))
    elif not alt5:
        alt5 = chord_symbols.CHORD_NO + chord_symbols.CHORD_5

    for symb in altered_thirds:
        if symb in interval_names:
            alt3 = interval_names.pop(interval_names.index(symb))

    if chord_symbols.CHORD_MAJ in main_suffix and normal3 == chord_symbols.CHORD_MAJ:
        normal3 = ""

    symbols: list[str] = [normal3, main_suffix, alt5, alt3, no5, extensions]
    final_form = "".join(symbols)

    return final_form


for chord in tetrad_intervals():
    p1 = time.perf_counter()
    print(chord)
    print(chord_symbol_from_interval_names(chord))
    p2 = time.perf_counter()
    print(p2-p1)


def perf_test_chord_scale():
    p1 = time.perf_counter()
    nomenclature.heptatonic_chord_scale(keywords.DIATONIC, keywords.IONIAN, "C", 4)
    p2 = time.perf_counter()

    print(p2-p1)

def perf_test_tetrad_intervals():
    p1 = time.perf_counter()
    tetrad_intervals()
    p2 = time.perf_counter()

    print(p2-p1)


perf_test_chord_scale()

perf_test_tetrad_intervals()
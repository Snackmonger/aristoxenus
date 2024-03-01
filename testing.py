
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
    """Attempt to generate a chord symbol from the given interval names.
    
    This function anticipates that interval names might be unusual enharmonic
    variants used to accommodate a few unusual scale structures (e.g. bb3, 
    bb7) and attempts to generate a nomenclaturally-consistent name."""

    # The function does a pretty good job of naming the common chords
    # but it's not impregnable.
    

    parsed_symbols: list[str] = []
    normal3: str = ""
    primary_suffix: str = ""
    secondary_suffix: str = ""
    sus: str = ""
    alt3: str = ""
    alt5: str = ""
    add: str = ""
    no5: str = ""
    no3: str = ""
    extensions: str = ""
    
    interval_names.pop(0)  # get rid of unison
    diminished_symbols: list[str] = [chord_symbols.CHORD_FLAT_3,
                                     chord_symbols.CHORD_FLAT_5,
                                     chord_symbols.CHORD_DOUBLE_FLAT_7]
    primary_suffixes: list[str] = [chord_symbols.CHORD_FLAT_7,
                                chord_symbols.CHORD_7,
                                chord_symbols.CHORD_DOUBLE_FLAT_7]
    secondary_suffixes: list[str] = [chord_symbols.CHORD_6,
                                chord_symbols.CHORD_FLAT_6,
                                chord_symbols.CHORD_SHARP_6]
    altered_fifths: list[str] = [chord_symbols.CHORD_FLAT_5,
                                 chord_symbols.CHORD_SHARP_5]
    altered_thirds: list[str] = [chord_symbols.CHORD_DOUBLE_FLAT_3,
                                 chord_symbols.CHORD_SHARP_3]
    suspensions: list[str] = [chord_symbols.CHORD_2,
                              chord_symbols.CHORD_4]
    natural_extensions: list[str] = [chord_symbols.CHORD_9,
                 chord_symbols.CHORD_11,
                 chord_symbols.CHORD_13]

    # Does the chord have a primary/seconday suffix?
    for symb in primary_suffixes:
        if symb in interval_names:
            primary_suffix = symb
            interval_names.remove(symb)
            parsed_symbols.append(symb)

    for symb in secondary_suffixes:
        if symb in interval_names:
            secondary_suffix = symb
            interval_names.remove(symb)
            parsed_symbols.append(symb)

    # Change 7s from literal to symbolic value
    if chord_symbols.CHORD_DOUBLE_FLAT_7 in primary_suffix:
        if all(x in parsed_symbols for x in diminished_symbols):
            primary_suffix = primary_suffix.replace(
                chord_symbols.CHORD_DOUBLE_FLAT_7,
                chord_symbols.CHORD_DIM)
    elif chord_symbols.CHORD_FLAT_7 in primary_suffix:
        primary_suffix = primary_suffix.replace(
            chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_7)
    elif chord_symbols.CHORD_7 in primary_suffix:
        primary_suffix = primary_suffix.replace(
            chord_symbols.CHORD_7, chord_symbols.CHORD_MAJ_7)

    # How is the 3rd of the chord expressed?
    if chord_symbols.CHORD_3 in interval_names:
        interval_names.remove(chord_symbols.CHORD_3)
        parsed_symbols.append(chord_symbols.CHORD_3)
        if chord_symbols.CHORD_FLAT_7 not in parsed_symbols:
            normal3 = chord_symbols.CHORD_MAJ
    
    elif chord_symbols.CHORD_FLAT_3 in interval_names:
        interval_names.remove(chord_symbols.CHORD_FLAT_3)
        if all(x in parsed_symbols for x in diminished_symbols):
            primary_suffix = chord_symbols.CHORD_DIM_7
            interval_names.remove(chord_symbols.CHORD_FLAT_5)
        if not any([chord_symbols.CHORD_DIM in primary_suffix]):
            normal3 = chord_symbols.CHORD_MIN

    # Is there a colour tone or suspended tone?
    if not normal3:
        for symb in suspensions:
            if symb in interval_names:
                sus += chord_symbols.CHORD_SUS + symb
                interval_names.remove(symb)
                parsed_symbols.append(symb)
    else:
        for symb in suspensions:
            if symb in interval_names:
                add += chord_symbols.CHORD_ADD + symb
                interval_names.remove(symb)
                parsed_symbols.append(symb)

    # Does a series of extensions get condensed into a single symbol?
    # e.g. maj11 = maj7add9add11
    largest_extension: str = ""
    for symb in natural_extensions:
        if symb in interval_names:
            largest_extension = symb
            interval_names.remove(symb)
            parsed_symbols.append(symb)
    if largest_extension:
        if chord_symbols.CHORD_7 in primary_suffix:    
            primary_suffix = primary_suffix.replace(
                chord_symbols.CHORD_7, largest_extension)
        else:
            for symb in natural_extensions:
                if symb in parsed_symbols:
                    add += chord_symbols.CHORD_ADD + symb
        
    # Does the chord have a natural 5th, altered 5th, or no 5th at all?
    for symb in altered_fifths:
        if symb in interval_names:
            alt5 = symb
            interval_names.remove(symb)
            parsed_symbols.append(symb)
    if not chord_symbols.CHORD_5 in interval_names:
        if not alt5:
            alt5 = chord_symbols.CHORD_NO + chord_symbols.CHORD_5
    else:
        interval_names.remove(chord_symbols.CHORD_5)
    
    # Does the chord contain an altered 3rd?
    for symb in altered_thirds:
        if symb in interval_names:
            alt3 = symb
            interval_names.remove(symb)
    if not alt3 and not normal3:
        no3 = chord_symbols.CHORD_NO + chord_symbols.CHORD_3

    # Does the chord symbol contain a redundant sub-symbol?
    if chord_symbols.CHORD_MAJ in primary_suffix and normal3 == chord_symbols.CHORD_MAJ:
        normal3 = ""
    if chord_symbols.CHORD_DIM in primary_suffix:
        alt5 = ""

    # For most common chords, this process should be sufficient to reduce 
    # the remaining symbols to altered extensions. 
    extensions = "".join(interval_names)
    symbols: list[str] = [normal3,
                          primary_suffix,
                          secondary_suffix,
                          sus,
                          alt5, 
                          alt3, 
                          add,
                          no3,
                          no5, 
                          extensions]
    final_form = "".join(symbols)

    return final_form


# for chord in tetrad_intervals():
#     print(chord)
#     print(chord_symbol_from_interval_names(chord))



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


# perf_test_chord_scale()

# perf_test_tetrad_intervals()
    



def do_ch_tests(ch_dict: dict[str, list[str]]):

    def test_ch_symbol_generation(expected_symbol: str, interval_names: list[str]):
        err = f"Testing intervals {interval_names}"
        x = chord_symbol_from_interval_names(interval_names=interval_names)
        err += f"\nExpected symbol is {expected_symbol}"
        err += f"\nActual symbol is {x}"
        err += f"\nTest passed: {x == expected_symbol}\n"
        test_passed = x == expected_symbol
        if not test_passed:
            print (err)
        return test_passed

    test_total = 0
    for k,v in ch_dict.items():
        x = test_ch_symbol_generation(k, v)
        if x:
            test_total += 1
    print(f"Passed {test_total}/{len(ch_dict)} tests.")


chords = {"maj": ["1", "3", "5"],
          "min": ["1", "b3", "5"],
          "majb5": ["1", "3", "b5"],
          "minb5": ["1", "b3", "b5"],
          "maj#5": ["1", "3", "#5"],
          "min#5": ["1", "b3", "#5"],
          "maj7": ["1", "3", "5", "7"],
          "minmaj7": ["1", "b3", "5", "7"],
          "7": ["1", "3", "5", "b7"],
          "min7": ["1", "b3", "5", "b7"],
          "7b5": ["1", "3", "b5", "b7"],
          "7#5": ["1", "3", "#5", "b7"],
          "min7b5": ["1", "b3", "b5", "b7"],
          "maj6": ["1", "3", "5", "6"],
          "maj7#5": ["1", "3", "#5", "7"],
          "maj7b5": ["1", "3", "b5", "7"],
          "7#9": ["1", "3", "5", "b7", "#9"],
          "7b9": ["1", "3", "5", "b7", "b9"]}

do_ch_tests(chords)
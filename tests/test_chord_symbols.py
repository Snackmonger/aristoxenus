"""Tests that require a bit more detail than docstring testing can comfortably provide."""
from data import keywords
from data.annotations import HeptatonicChord
from src import parsing
from src.nomenclature import heptatonic_chord_scale
from src.parsing import parse_interval_names_as_chord_symbol
from tests.decorators import test_perf


@test_perf(True)
def test_chord_symbol_from_interval_names(ch_dict: dict[str, list[str]], verbose: bool = False):
    """Perform a series of tests on the chord symbol generation function to 
    see if the correct symbols are being created."""
    print("\n\nBeginning test of chord symbol generation.")
    @test_perf(verbose)
    def __test_ch_symbol_generation(expected_symbol: str, interval_names: list[str]):
        err = f"# Testing intervals\t{interval_names}"
        x = parse_interval_names_as_chord_symbol(interval_names)
        test_passed = x == expected_symbol
        err += f"\n# Expected symbol\t{expected_symbol}"
        err += f"\n# Actual symbol\t\t{x}"
        err += f"\n# Test passed\t\t{test_passed}"
        err += "\n#######################################################"
        
        if not test_passed or verbose:
            print(err)

        return test_passed

    test_total = 0
    for k, v in ch_dict.items():
        x = __test_ch_symbol_generation(k, v)
        if x:
            test_total += 1
    print(f"Passed {test_total}/{len(ch_dict)} tests.")


chord_tests = {"maj": ["1", "3", "5"],
          "min": ["1", "b3", "5"],
          "majb5": ["1", "3", "b5"],
          "minb5": ["1", "b3", "b5"],
          "maj#5": ["1", "3", "#5"],
          "min#5": ["1", "b3", "#5"],
          "maj7": ["1", "3", "5", "7"],
          "6sus2": ["1", "2", "5", "6"],
          "maj7addb6": ["1", "3", "5", "b6", "7"],
          "minmaj7": ["1", "b3", "5", "7"],
          "minmaj7b5": ["1", "b3", "b5", "7"],
          "7": ["1", "3", "5", "b7"],
          "7no3": ["1", "5", "b7"],
          "7add6": ["1", "3", "5", "6", "b7"],
          "7sus2#11": ["1", "2", "5", "b7", "#11"],
          "7sus2add11": ["1", "2", "5", "b7", "11"],
          "7sus2": ["1", "2", "5", "b7"],
          "7sus4": ["1", "4", "5", "b7"],
          "9sus2": ["1", "2", "5", "b7", "9"],
          "7sus4#9": ["1", "4", "5", "b7", "#9"],
          "9": ["1", "3", "5", "b7", "9"],
          "9#5": ["1", "3", "#5", "b7", "9"],
          "min7": ["1", "b3", "5", "b7"],
          "7b5": ["1", "3", "b5", "b7"],
          "7#5": ["1", "3", "#5", "b7"],
          "min7b5": ["1", "b3", "b5", "b7"],
          "maj6": ["1", "3", "5", "6"],
          "6sus4no5add9": ["1", "4", "6", "9"],
          "min6": ["1", "b3", "5", "6"],
          "majb6": ["1", "3", "5", "b6"],
          "maj7add6": ["1", "3", "5", "6", "7"],
          "maj7#5": ["1", "3", "#5", "7"],
          "maj7b5": ["1", "3", "b5", "7"],
          "7#9": ["1", "3", "5", "b7", "#9"],
          "7b9": ["1", "3", "5", "b7", "b9"],
          "maj7bb3": ["1", "bb3", "5", "7"],
          "maj7b5bb3": ["1", "bb3", "b5", "7"],
          "maj7sus2no5#4": ["1", "2", "#4", "7"],
          "dim7": ["1", "b3", "b5", "bb7"],
          "min6b5": ["1", "b3", "b5", "6"],
          "dim9": ["1", "b3", "b5", "bb7", "9"],
          "dim11": ["1", "b3", "b5", "bb7", "9", "11"],
          "dim9add13": ["1", "b3", "b5", "bb7", "9", "13"],
          "dim13": ["1", "b3", "b5", "bb7", "9", "11", "13"],
          "dim7add11": ["1", "b3", "b5", "bb7", "11"],
          "dim7b9": ["1", "b3", "b5", "bb7", "b9"]}


@test_perf(True)
def test_generate_chord_names_for_heptatonic():
    """Test that all scales in the heptatonic system generate symbols that 
    are at least readable (if not sensible).
    """
    print("\n\nBeginning test of heptatonic chord scale naming function.")
    for scale in keywords.HEPTATONIC_ORDER:
        triads = heptatonic_chord_scale(scale, keywords.IONIAN, "C")
        tetrads = heptatonic_chord_scale(scale, keywords.IONIAN, "C", 4)
        print("##################################################")
        print(f"# Now trying {scale} scale")
        for i in range(7):
            triad: HeptatonicChord = triads[i]
            tetrad: HeptatonicChord = tetrads[i]
            root = triad["root"]
            triad_stem = parsing.parse_interval_names_as_chord_symbol(triad["interval_names"])
            tetrad_stem = parsing.parse_interval_names_as_chord_symbol(tetrad["interval_names"])

            pad1 = 20 - len(root+triad_stem)
            pad2 = 20 -  len(root+tetrad_stem)
            print(f"# {triad['numeric_degree']}\t::{' '*pad1}{root + triad_stem}{' '*pad2}{root + tetrad_stem}")
        
            

def test_generate_interval_structure_from_chord_symbol():
    ...
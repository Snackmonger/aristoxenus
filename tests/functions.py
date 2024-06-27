"""Functions that test various parts of the program."""
import doctest
from typing import Mapping, Optional, Sequence
from src.functions import interface
from src.functions import (
    bitwise,
    nomenclature,
    permutation,
    parsing,
    sequences, 
    utils
)

from src.data import (
    keywords,
    annotations
)
from tests.decorators import test_perf
from tests import test_data


def do_doctests(verbose: bool = False) -> None:
    """Run the tests in the core modules' docstrings."""
    doctest.testmod(bitwise, verbose=verbose)
    doctest.testmod(nomenclature, verbose=verbose)
    doctest.testmod(permutation, verbose=verbose)
    doctest.testmod(parsing, verbose=verbose)
    doctest.testmod(sequences, verbose=verbose)
    doctest.testmod(utils, verbose=verbose)

@test_perf(True)
def test_chord_symbol_from_interval_names(
    chords: Optional[dict[str, list[str]]] = None,
    verbose: bool = False
) -> None:
    """Perform a series of tests on the chord symbol generation function to 
    see if the correct symbols are being created.
    """
    @test_perf(verbose)
    def __test_ch_symbol_generation(expected_symbol: str, interval_names: list[str]):
        report = f"# Testing intervals\t{interval_names}"
        x = parsing.parse_interval_names_as_chord_symbol(interval_names)
        test_passed = x == expected_symbol
        report += f"\n# Expected symbol\t{expected_symbol}"
        report += f"\n# Actual symbol\t\t{x}"
        report += f"\n# Test passed\t\t{test_passed}"
        report += "\n#######################################################"
        if not test_passed or verbose:
            print(report)
        return test_passed

    if not chords:
        chords = test_data.chord_tests
    print("\n\nBeginning test of interval names -> chord symbol.")
    test_total = 0
    for k, v in chords.items():
        result = __test_ch_symbol_generation(k, v)
        if result:
            test_total += 1
    print(f"Passed {test_total}/{len(chords)} tests.")


@test_perf(True)
def test_generate_intervals_from_chord_symbol(chords: Optional[Mapping[str, Sequence[str]]] = None, verbose: bool = False) -> None:
    """Perform a series of tests on the chord symbol recognition function to 
    see if the correct intervals are being returned.
    """

    @test_perf(verbose)
    def __test_ch_interval_generation(chord_symbol: str, expected_intervals: Sequence[str]) -> bool:
        report = f"# Testing chord symbol\t{chord_symbol}"
        x = list(parsing.parse_chord_suffix(chord_symbol=chord_symbol))
        test_passed = x == expected_intervals
        report += f"\n# Expected intervals\t{expected_intervals}"
        report += f"\n# Actual intervals\t\t{x}"
        report += f"\n# Test passed\t\t{test_passed}"
        report += "\n#######################################################"
        if not test_passed or verbose:
            print(report)
        return test_passed
    
    if not chords:
        chords = test_data.chord_tests
    print("\n\nBeginning test of chord symbol -> interval names.")
    test_total = 0
    for k, v in chords.items():
        result = __test_ch_interval_generation(k, v)
        if result:
            test_total += 1
    print(f"Passed {test_total}/{len(chords)} tests.")



@test_perf(True)
def test_generate_chord_names_for_heptatonic():
    """Test that all scales in the heptatonic system generate symbols that 
    are at least readable (if not sensible).
    """
    print("\n\nBeginning test of heptatonic chord scale naming function.")
    for scale in keywords.HEPTATONIC_ORDER_KEYS:
        triads = interface.heptatonic_chord_scale(scale, keywords.IONIAN, "C")
        tetrads = interface.heptatonic_chord_scale(
            scale, keywords.IONIAN, "C", 4)
        print("##################################################")
        print(f"# Now trying {scale} scale")
        for i in range(7):
            triad: annotations.HeptatonicChord = triads["chord_scale"][i]
            tetrad: annotations.HeptatonicChord = tetrads["chord_scale"][i]
            root = triad["root"]
            triad_stem = parsing.parse_interval_names_as_chord_symbol(
                triad["interval_names"])
            tetrad_stem = parsing.parse_interval_names_as_chord_symbol(
                tetrad["interval_names"])

            pad1 = 20 - len(root+triad_stem)
            pad2 = 20 - len(root+tetrad_stem)
            print(
                f"# {triad['numeric_degree']}\t::{' '*pad1}{root + triad_stem}{' '*pad2}{root + tetrad_stem}")



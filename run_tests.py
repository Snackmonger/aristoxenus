"""Other tests"""
from tests.test_chord_symbols import (test_chord_symbol_from_interval_names,
                                      chord_tests, 
                                      test_generate_chord_names_for_heptatonic)

test_chord_symbol_from_interval_names(chord_tests)
test_generate_chord_names_for_heptatonic()

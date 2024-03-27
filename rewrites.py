

from typing import Sequence, TypedDict

from data import chord_symbols, constants, errors
from src import nomenclature, utils


class ChordData(TypedDict):
    """Information implied in a chord symbol."""
    symbol: str
    note_names: tuple[str, ...]
    interval_names: tuple[str, ...]
    interval_structure: int


def split_chord_symbol(chord_symbol: str) -> tuple[str, str]:
    """Return the root and suffix of a chord symbol.

    This function only works on simple chords (i.e. not slash chords
    or polychords).
    """
    '''For a given chord symbol, return a tuple containing: (root, all other symbols).'''
    root: str
    # Case 1: Radical is a note name (e.g. Gb, A#, F)
    for note in sorted(constants.LEGAL_ROOT_NAMES, key=len, reverse=True):
        if note in chord_symbol:
            root = note
            chord_symbol = chord_symbol.removeprefix(note)
            return root, chord_symbol

    # Case 2: Radical is an interval name (e.g. bIII, V, vii)
    roman_intervals = list(utils.romanize_intervals(
        [str(x) for x in range(1, 8)]))
    roman_intervals += [x.lower() for x in roman_intervals]
    roman_intervals.sort(key=len, reverse=True)
    for interval in roman_intervals:
        if interval in chord_symbol:
            root = chord_symbol[:chord_symbol.index(interval)+len(interval)]
            chord_symbol = chord_symbol.removeprefix(root)
            return root, chord_symbol

    raise errors.ChordNameError(f'Unknown note name: {chord_symbol}.')


def parse_chord_symbol(chord_symbol: str) -> ChordData:
    """
    Return a set of data representing the information implied in a chord
    symbol.

    Args:
        chord_symbol: A chord symbol, expressed as a string.

    Returns:
        _description_
    """


def parse_chord_suffix(chord_symbol: str) -> tuple[str, ...]:
    """Return a list of interval names implied in a chord suffix.

    The names will respect the enharmonic-equivalences implied in the chord
    symbol, so that #2 is distinct from b3, etc.
    """
    def __remove(affix: str) -> None:
        nonlocal chord_symbol
        chord_symbol = chord_symbol.replace(affix, "")
    parsed_symbols: set[str] = set(["1", "5"])
    subtractive: set[str] = set()

    # Remove all 'add'/'no' modifiers to see what the base symbol is.
    for add in chord_symbols.additive:
        if add in chord_symbol:
            interval = add.replace(chord_symbols.CHORD_ADD, "")
            parsed_symbols.add(interval)
            __remove(add)
    for no in chord_symbols.subtractive:
        if no in chord_symbol:
            subtractive.add(no)
            __remove(no)

    # No suffix = major triad: C, D, E, etc.
    if len(chord_symbol) == 0:
        parsed_symbols.add(chord_symbols.CHORD_3)

    # Powerchord suffix: D5, E5, F5, etc.,
    # (implies a p5 and p8).
    if chord_symbol == chord_symbols.CHORD_5:
        chord_symbol = ""
        parsed_symbols.add(chord_symbols.CHORD_8)

    prefix_modifiers = {
        chord_symbols.CHORD_7: {'1'},  # dummy value; 7 is idiomatic
        chord_symbols.CHORD_9: {chord_symbols.CHORD_9},
        chord_symbols.CHORD_11: {chord_symbols.CHORD_9,
                                 chord_symbols.CHORD_11},
        chord_symbols.CHORD_13: {chord_symbols.CHORD_9,
                                 chord_symbols.CHORD_11,
                                 chord_symbols.CHORD_13}}

    # Parse the implicit meanings in prototypical prefixes.
    for extension, extended_structure in prefix_modifiers.items():
        for symbol in chord_symbols.CHORD_SYMBOL_LIST:
            if chord_symbol.startswith(symbol + extension):
                parsed_symbols |= extended_structure

                # maj7 (or variant) -> maj, maj7, plus extensions
                if symbol in chord_symbols.CHORD_MAJOR_SYMBOL_LIST:
                    __remove(symbol + extension)
                    parsed_symbols.add(chord_symbols.CHORD_7)
                    if chord_symbols.CHORD_SUS not in chord_symbol:
                        parsed_symbols.add(chord_symbols.CHORD_3)

                # dim7 (or variant) -> dim, bb7, plus extensions
                if symbol == chord_symbols.CHORD_DIM:
                    __remove(symbol + extension)
                    parsed_symbols |= {chord_symbols.CHORD_FLAT_3,
                                       chord_symbols.CHORD_FLAT_5,
                                       chord_symbols.CHORD_DOUBLE_FLAT_7}

                # min7 (or variant): ensure that b7 is present
                # if not explicit (e.g. Em11). If symbol has a '7',
                # remove it so it doesn't get interpreted as natural.
                if symbol in chord_symbols.CHORD_MINOR_SYMBOL_LIST:
                    parsed_symbols.add(chord_symbols.CHORD_FLAT_7)
                    __remove(chord_symbols.CHORD_7)

        # 7 (or variant) -> maj, b7, plus extensions
        if chord_symbol.startswith(extension):
            parsed_symbols |= extended_structure | {
                chord_symbols.CHORD_FLAT_7, chord_symbols.CHORD_3}
            __remove(extension)

    # First element is another number: C2, C4, C6, etc.
    # implies major triad plus colour tone (different from sus2,
    # sus4, which have no 3rd)
    for symbol in [chord_symbols.CHORD_6,
                   chord_symbols.CHORD_2,
                   chord_symbols.CHORD_4]:
        if chord_symbol.startswith(symbol):
            parsed_symbols.add(chord_symbols.CHORD_3)

    # All remaining sub-symbols in the chord symbol should
    # be plain interval names. Anything that can't be reconciled
    # with the known interval names and aliases will be left out.
    pairs = chord_symbols.symbol_elements.items()
    pairs = sorted(pairs, key=lambda key: len(key[0]), reverse=True)
    for symbol_element, interval in pairs:
        if symbol_element in chord_symbol:
            parsed_symbols.add(symbol_element)
            __remove(symbol_element)

    # The only things that we should expect to remain in the chord symbol
    # is malformed symbols or symbols from systems that haven't been
    # incorporated to the Aristoxenus lists.
    #
    # logger.info("Symbols parsed: {parsed_symbols}, remaining chord data: {chord_symbol}")

    # If the chord indicated sus, assume that this symbol overrides any
    # symbol indicating a 3rd and remove any thirds.
    suspensions = [chord_symbols.CHORD_SUS_2,
                   chord_symbols.CHORD_SUS_4,
                   chord_symbols.CHORD_SUS_DOUBLE_FLAT_3,
                   chord_symbols.CHORD_SUS_SHARP_3]
    for sus in suspensions:
        if sus in parsed_symbols:
            parsed_symbols -= {chord_symbols.CHORD_3,
                               chord_symbols.CHORD_FLAT_3}

    # Filter all the parsed symbols to ensure that they are interval names
    # and not special symbols (e.g. "maj")
    interval_names: set[str] = set("1")
    for symbol in parsed_symbols:
        if symbol in chord_symbols.CHORD_MAJOR_SYMBOL_LIST:
            interval_names |= {chord_symbols.CHORD_3, chord_symbols.CHORD_5}
        elif symbol == chord_symbols.CHORD_MAJ_7:
            interval_names.add(chord_symbols.CHORD_7)
        elif symbol in chord_symbols.CHORD_MINOR_SYMBOL_LIST:
            interval_names |= {
                chord_symbols.CHORD_FLAT_3, chord_symbols.CHORD_5}
        elif symbol in chord_symbols.CHORD_AUGMENTED_SYMBOL_LIST:
            interval_names |= {chord_symbols.CHORD_3,
                               chord_symbols.CHORD_SHARP_5}
        elif symbol in chord_symbols.CHORD_DIMINISHED_SYMBOL_LIST:
            interval_names |= {chord_symbols.CHORD_FLAT_5,
                               chord_symbols.CHORD_FLAT_3}
        elif symbol in suspensions:
            interval_names |= {symbol.replace(
                chord_symbols.CHORD_SUS, ""), chord_symbols.CHORD_5}
        else:
            interval_names.add(symbol)

    # If there's any altered fifth, assume that it
    # overrides the implied perfect fifth.
    for symbol in chord_symbols.CHORD_ALTERED_FIFTH_SYMBOL_LIST + [chord_symbols.CHORD_NO + chord_symbols.CHORD_5]:
        if symbol in interval_names and chord_symbols.CHORD_5 in interval_names:
            interval_names.remove(chord_symbols.CHORD_5)

    # Clean up final result by applying "no" modifiers to remove
    # any unwanted intervals.
    for no in subtractive:
        if (interval := no.replace(chord_symbols.CHORD_NO, "")) in parsed_symbols:
            interval_names -= {interval}

    return tuple(interval_names)






def convert_interval_names_to_integer(interval_names: Sequence[str]) -> int:
    """Return an integer representing a binary mapping of the given interval
    names.
    """
    structure = 1
    elements = chord_symbols.symbol_elements.items()
    elements = sorted(elements, key=lambda x: len(x[0]), reverse=True)
    for symbol_element, interval in elements:
        if symbol_element in interval_names:
            structure |= interval
    return structure


def parse_slash_chord(chord_symbol: str) -> ChordData:
    """
    Return information parsed from a given slash chord symbol. 

    The slash chord will be rotated to the inversion implied by its bass note,
    rather than simply superimposed over that bass in its root form. If the
    bass note is not a chord tone, then it will be added to the chord in the 
    lower octave, and the chord will be rotated to an 'inversion' beginning
    with that note.

    Args:
        chord_symbol: _description_

    Returns:
        _description_
    """

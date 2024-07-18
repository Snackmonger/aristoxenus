import re
from overhaul.data.constants import RE_SPLIT_CHORD_SYMBOL
from overhaul.data.errors import UnknownSymbolError


def split_chord_symbol(chord_symbol: str) -> tuple[str, str]:
    '''
    Take a complete chord symbol and return a tuple of the root name prefix
    and chord symbol suffixes.

    Parameters
    ----------
    chord_symbol : str
        A representation of a chord symbol, e.g. "Cmaj9", "Am7b5b9", "Gmaj6".

    Returns
    -------
    tuple[str, str]
        The note name that serves as the chord root, plus any suffixes.

    Raises
    ------
    UnknownSymbolError
        If the chord symbol does not conform to the expected format (e.g.
        begins with an unrecognizable root).
    '''
    chord = re.match(RE_SPLIT_CHORD_SYMBOL, chord_symbol)
    if chord:
        chord = chord.groupdict()
        return chord["root"], chord["suffix"]
    raise UnknownSymbolError(f"Unknown chord symbol: {chord_symbol}")


def parse_chord_suffix(chord_suffix: str) -> tuple[str, ...]:
    """Turn a chord suffix into interval names"""

    add = re.match("(add((#|b)*[\\D]+))")
    no = []
    primary = []
    secondary = []

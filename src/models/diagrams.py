'''
Functions pertaining to making musical diagrams (aside from staff notation).
'''

import dataclasses

from data import chord_symbols

def guitar_tuning(strings: int = 6, 
                  tuning: str | list[str] = 'E2A2D3G3B3E4', 
                  frets: int = 22
                  ) -> tuple[tuple[str, ...], ...]:
    '''
    Return a nested tuple representing a given number of strings and a given tuning.

    Parameters
    ----------
    strings : int   
        The number of strings the guitar will have.
    tuning : str or list of strings
        The notes that each open string will be tuned to. The number of notes
        must be the same as the number of strings.

    Returns
    -------
    tuple of tuple of str
        An array representing the notes of a guitar in the given formatting.

    Examples
    --------

    '''



@dataclasses.dataclass
class ChordSymbol:

    initial_symbol: str
    parsing_symbol: str = ''
    recognized_sub_symbols: list[str] = dataclasses.field(default_factory=list)
    unrecognized_sub_symbols: list[str] = dataclasses.field(default_factory=list)
    interval_structure: int = 1

    def __post_init__(self):
        self.parsing_symbol = self.initial_symbol

    def recognize(self, symbol):
        self.recognized_sub_symbols.append(symbol)
        self.parsing_symbol = self.parsing_symbol.replace(symbol, '')

    def ignore(self, symbol):
        self.unrecognized_sub_symbols.append(symbol)
        self.parsing_symbol = self.parsing_symbol.replace(symbol, '')

    def add(self, interval):
        self.interval_structure |= interval

    def subtract(self, interval):
        self.interval_structure ^= (interval -1)



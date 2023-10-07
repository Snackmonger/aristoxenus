'''
Functions pertaining to making musical diagrams (aside from staff notation).
'''

import dataclasses

from data import (chord_symbols, 
                  constants,
                  keywords)

from src import nomenclature


GUITAR_STANDARD_TUNING = ['E2', 'A3', 'D3', 'G3', 'B3', 'E4']

def guitar_tuning(strings: int = 6,
                  tuning: list[str] | tuple[str, ...] = GUITAR_STANDARD_TUNING,
                  frets: int = 15,
                  format_: str = keywords.SCIENTIFIC
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
        A table representing the notes on the strings of a guitar in the 
        given formatting.

    '''
    diagram = []
    frets += 1
    if format_ == keywords.SCIENTIFIC:
        all_notes = nomenclature.scientific_range()
        # Ensure that we use binomials in the output
        tuning =  list(map(nomenclature.decode_scientific_enharmonic, tuning))

    elif format_ == keywords.PLAIN:
        all_notes = nomenclature.chromatic() * (1 + (frets // 12))
        # Again binomials, but this function also
        # filters out scientific note names
        tuning = list(map(nomenclature.decode_enharmonic, tuning))

    else:
        raise ValueError(format_)

    for string in range(strings):

        starting_note = all_notes.index(tuning[string])
        ending_note = starting_note + frets
        string_notes = all_notes[starting_note : ending_note]
        diagram.append(tuple(string_notes))

    diagram.reverse()
    return tuple(diagram)
    



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



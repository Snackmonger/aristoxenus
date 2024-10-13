'''
This module supplies basic data structures that are used internally in the
program.
'''

from dataclasses import dataclass
from typing import Sequence


@dataclass
class ChordData:
    '''
    A representation of a chord per se, without any implied parent 
    structure.

    Parallel data attributes used elsewhere in the program:
        ``annotations.SimpleChord`` : typedDict used in API response data 
        ``classes.Chord`` : Object-oriented interface for chord manipulation.
    '''
    note_names: Sequence[str]
    interval_symbols: Sequence[str]
    interval_structure: Sequence[int]

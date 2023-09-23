'''
Functions pertaining to making musical diagrams (aside from staff notation).
'''
from src.nomenclature import scientific, decode_scientific_enharmonic

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



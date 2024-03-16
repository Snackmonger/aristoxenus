'''
Miscellaneous functions.
'''

from typing import Any, Sequence
from itertools import chain



def shift_array(array: Sequence[Any], new_first_member: Any) -> tuple[Any, ...]:
    '''
    Rotate the given array so that the given item is first.

    Returns
    -------
    list
        A list rotated so that the given member is first. Naturally, if the 
        array contains a duplicate value, the shift won't work right.
    '''
    array = list(array)
    return tuple(array[array.index(new_first_member): ] + array[ :array.index(new_first_member)])


def roman_numeral(indian_numeral: int) -> str:
    '''
    Convert an Indian numeral between 1 and 3,999 to a Roman numeral.

    Raises
    ------
    ValueError
        If the number exceeds 3,999 in the Indian form.
    '''

    if indian_numeral not in range(1, 4000):
        raise ValueError(indian_numeral)
    roman_numeral_: str = ''
    numerals: tuple[tuple[str, int], ...] = (('M', 1000),
                                             ('D', 500),
                                             ('C', 100),
                                             ('L', 50),
                                             ('X', 10),
                                             ('V', 5),
                                             ('I', 1))
    for numeral, value in numerals:
        while indian_numeral >= value:
            roman_numeral_ += numeral
            indian_numeral -= value
        for error, correction in {'IIII': 'IV',
                                  'VIV': 'IX',
                                  'XXXX': 'XL',
                                  'LXL': 'XC',
                                  'CCCC': 'CD',
                                  'DCD': 'CM'}.items():
            if error in roman_numeral_:
                roman_numeral_ = roman_numeral_.replace(error, correction)

    return roman_numeral_

def romanize_intervals(interval_names: Sequence[str] | str) -> tuple[str, ...]:
    """Convert Indian numeral interval names to use Roman numerals instead."""
    if isinstance(interval_names, str):
        interval_names = [interval_names]
    roman_intervals: list[str] = []
    for interval in interval_names:
        for number in range(1, 8):
            if (x := str(number)) in interval:
                roman_interval: str = interval.replace(x, roman_numeral(number))
                roman_intervals.append(roman_interval)
    return tuple(roman_intervals)



def flatten(iterable: Sequence[Sequence[Any]]) -> Sequence[Any]:
    """Flatten an array of arrays."""
    return list(chain.from_iterable(iterable))
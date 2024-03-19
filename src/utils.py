'''
Miscellaneous functions.
'''

from typing import Any, Optional, Sequence
from itertools import chain
import csv

from data import errors, keywords



def shift_array(array: Sequence[Any], new_first_member: Any) -> tuple[Any, ...]:
    '''
    Rotate the given array so that the given member is first.

    Returns
        tuple: The same members rotated to start at the given member.
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


def encode_numeration(number: int, category: str) -> str:
    """
    Encode a number as a keyword for the given category.

    Args:
        category: A category of numerical words, e.g. "ordinal", "cardinal"
        number: The number to encode.

    Returns:
        A string representing the number in the given category.
    """
    file = "data/numeration.csv"
    number = number if category == keywords.BASAL else number - 1
    keyword = ""
    with open(file, newline="") as numdata:
        reader = csv.DictReader(numdata)
        rows = list(reader)
        keyword = rows[number][category]
        numdata.close()
    return keyword
    

def decode_numeration(term: str) -> int:
    """
    Decode a numeric keyword into the number it represents.

    Args:
        term: A numeric keyword term, e.g. "tertial", "pentad"

    Raises:
        errors.UnknownKeywordError: If the term is not a known keyword.

    Returns:
        An integer between 1 and 15. If the keyword is in the "basal"
        category, then its number will be 1 lower than the name suggests.
        (This is so it can be used to slice lists starting at 0)
    """
    file = "data/numeration.csv"
    keyword: Optional[int] = None
    with open(file, newline="") as numdata:
        reader = csv.DictReader(numdata)
        for i, row in enumerate(reader):
            if term in row:
                keyword = i
                assert reader.fieldnames
                if reader.fieldnames[i] == "basal":
                    keyword += 1

    if not keyword:
        raise errors.UnknownKeywordError(term)
    return keyword
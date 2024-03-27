'''
Miscellaneous functions.
'''

from typing import Any, Optional, Sequence
from itertools import chain
import csv

from loguru import logger

from data import errors, keywords


def shift_array(array: Sequence[Any], new_first_member: Any) -> tuple[Any, ...]:
    '''
    Rotate the given array so that the given member is first.

    Returns
        tuple: The same members rotated to start at the given member.

    Examples
    --------
    >>> list_ = ["apple", "banana", "pear", "peach"]
    >>> shift_array(list_, "pear")
    ('pear', 'peach', 'apple', 'banana')
    '''
    array = list(array)
    return tuple(array[array.index(new_first_member):] + array[:array.index(new_first_member)])


def roman_numeral(indian_numeral: int) -> str:
    '''
    Convert an Indian numeral between 1 and 3,999 to a Roman numeral.

    Raises
    ------
    ValueError
        If the number exceeds 3,999 in the Indian form.

    Examples
    --------
    >>> roman_numeral(1449)
    'MCDXLIX'
    >>> roman_numeral(1318)
    'MCCCXVIII'
    >>> roman_numeral(959)
    'CMLIX'
    >>> roman_numeral(263)
    'CCLXIII'
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


def decode_roman_numeral(symbol: str) -> int:
    """Convert a Roman numeral to an Indian numeral.

    Examples
    --------
    >>> decode_roman_numeral('MCDXLIX')
    1449
    >>> decode_roman_numeral('MCCCXVIII')
    1318
    >>> decode_roman_numeral('CMLIX')
    959
    >>> decode_roman_numeral('CCLXIII')
    263
    """
    numerals: tuple[tuple[str, int], ...] = (('M', 1000),
                                             ('D', 500),
                                             ('C', 100),
                                             ('L', 50),
                                             ('X', 10),
                                             ('V', 5),
                                             ('I', 1))
    values: list[int] = []
    for partial, value in {'IV': 4,
                           'IX': 9,
                           'XL': 40,
                           'XC': 90,
                           'CD': 400,
                           'CM': 900}.items():
        if partial in symbol:
            values.append(value)
            symbol = symbol.replace(partial, "")
    for numeral, value in numerals:
        if numeral in symbol:
            values.append(value*symbol.count(numeral))
    return sum(values)


def romanize_intervals(interval_names: Sequence[str] | str) -> tuple[str, ...]:
    """Convert Indian numeral interval names to use Roman numerals instead."""
    if isinstance(interval_names, str):
        interval_names = [interval_names]
    roman_intervals: list[str] = []
    for interval in interval_names:
        for number in range(1, 8):
            if (x := str(number)) in interval:
                roman_interval: str = interval.replace(
                    x, roman_numeral(number))
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
        number: The number to encode. If the category is "basal", the number
                represents a list slice, and so should be 1 less than the name
                suggests (tertial=2).

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


def decode_numeration(keyword: str) -> int:
    """
    Decode a numeric keyword into the number it represents.

    Args:
        term: A numeric keyword term, e.g. "tertial", "pentad"

    Raises:
        errors.UnknownKeywordError: If the term is not a known keyword.

    Returns:
        An integer between 1 and 15. If the keyword is a basal word, then 
        its number will be 1 lower than the name suggests. (This is so it
        can be used to slice lists starting at 0)

    Examples:
        >>> decode_numeration("triad")
        3
        >>> decode_numeration("thirteenth")
        13
        >>> decode_numeration("sextuple")
        6

        Note: the words in the basal category are 1 less than their etymology:
        >>> decode_numeration("tertial")
        2

    """
    file = "data/numeration.csv"
    value: Optional[int] = None
    with open(file, newline="") as numdata:
        reader = csv.DictReader(numdata)
        for i, row in enumerate(reader):
            if keyword in row:
                value = i
                assert reader.fieldnames
                if reader.fieldnames[i] == "basal":
                    value += 1

    if not value:
        raise errors.UnknownKeywordError(keyword)
    return value


def order_interval_names(interval_names: Sequence[str]) -> tuple[str, ...]:
    """Take an array of interval names and ensure that they follow the order
    of their numerals, regardless of the accidentals.
    """
    interval_names = list(interval_names)
    interval_names.sort(key=extract_number)
    return tuple(interval_names)

def extract_number(number_symbol: str) -> int:
    """Take a string that contains numeric digits, and return an integer made 
    up of those digits.
    
    This function is meant to be used for interval names, so we only ever expect
    that digits will all come together in sequence (e.g. "#11" > 11). It can parse 
    other symbols like "12oclockand54minutes", but it would return 1254.
    """
    number = ""
    for char in number_symbol:
        if char.isdigit():
            number += char
    return int(number)
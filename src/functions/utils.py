'''
This module provides functions that are used by the other modules in 
performing their tasks but that don't easily fit into any other 
category. The user is not likely to need any of these functions.
'''

from typing import (
    Any,
    Sequence
)
import itertools
import csv
from src.data import errors


def shift_array(array: Sequence[Any], new_first_member: Any) -> tuple[Any, ...]:
    """
    Rotate the given array so that the given member is first. If there are 
    more than one matches for the given first member, the array will be 
    rotated to the leftmost match.

    :param array: An array of any members. These are intended to be immutable
    primitives.
    :param new_first_member: The same members rotated to start at the given member.
    :return: _description_

    :Example:
    >>> list_ = ["apple", "banana", "pear", "peach"]
    >>> shift_array(list_, "pear")
    ('pear', 'peach', 'apple', 'banana')
    """
    array = list(array)
    return tuple(array[array.index(new_first_member):] + array[:array.index(new_first_member)])


def roman_numeral(indian_numeral: int) -> str:
    """
    Convert an Indian numeral between 1 and 3,999 to a Roman numeral.

    :param indian_numeral: An integer between 1 and 3999.
    :raises ValueError: If the number exceeds 3,999 in the Indian form.
    :return: A string representing a Roman numeral.

    :Example:
    >>> roman_numeral(1449)
    'MCDXLIX'
    >>> roman_numeral(1318)
    'MCCCXVIII'
    >>> roman_numeral(959)
    'CMLIX'
    >>> roman_numeral(263)
    'CCLXIII'
    """
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
    """
    Convert a Roman numeral to an Indian numeral.

    :param symbol: A string representing a Roman numeral.
    :return: An integer.

    :Example:
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
    """
    Convert Indian numeral interval name(s) to use Roman numerals instead.

    :param interval_names: A string or array of strings representing interval
        symbols using Indian numerals (e.g "b3").
    :return: A tuple containing the same interval symbol(s) expressed using
        Roman numerals (e.g. "bIII").
    
    :Example:
    >>> romanize_intervals("b3")
    ('bIII',)
    >>> romanize_intervals(["#5", "b6"])
    ('#V', 'bVI')
    """
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
    """Flatten an array of arrays into a single array."""
    return list(itertools.chain.from_iterable(iterable))


def encode_numeration(number: int, category: str) -> str:
    """
    Encode a number as a keyword for the given category.

    :param number: The number to encode, between 1 and 15.
    .. note::
        This function automatically adjusts the number if the category is "basal".
        The basal numbers are used as a list slice, and so are understood as 1 
        less than the name suggests etymologically (i.e. "tertial" = 2, so that 
        list[::2] can get every third note).

    :param category: A category of numerical words, e.g. "ordinal", "cardinal"
    :return: A string representing the number in the given category.

    :Example:
    >>> encode_numeration(3, "polyad")
    'triad'
    >>> encode_numeration(2, "basal")
    'tertial'
    >>> encode_numeration(3, "cardinal")
    'three'
    >>> encode_numeration(3, "ordinal")
    'third'
    >>> encode_numeration(3, "uple")
    'triple'
    >>> encode_numeration(3, "tonal")
    'tritonic'
    >>> encode_numeration(5, "tonal")
    'pentatonic'
    >>> encode_numeration(7, "tonal")
    'heptatonic'
    """
    file = "src/data/numeration.csv"
    number = number if category == 'basal' else number - 1
    keyword = ""
    with open(file, newline="", encoding="utf8") as numdata:
        reader = csv.DictReader(numdata)
        rows = list(reader)
        keyword = rows[number][category]
        numdata.close()
    return keyword


def decode_numeration(keyword: str) -> int:
    """
    Decode a numeric keyword into the number it represents.

    :param keyword: A numeric keyword term, e.g. "tertial", "pentad".
    :raises errors.UnknownKeywordError: If the term is not a known keyword.
    :return: An integer between 1 and 15. If the keyword is a basal word, then
        its number will be 1 lower than the name suggests. (This is so it
        can be used to slice lists starting at 0)
    .. note::
        This function automatically adjusts the number if the category is "basal".
        The basal numbers are used as a list slice, and so are returned 1 
        less than the name suggests etymologically (i.e. "tertial" = 2, so that 
        list[::2] can get every third note).
    
    :Example:
    >>> decode_numeration("triad")
    3
    >>> decode_numeration("thirteenth")
    13
    >>> decode_numeration("sextuple")
    6
    >>> decode_numeration("tertial")
    2
    """
    file = "src/data/numeration.csv"
    with open(file, newline="", encoding="utf8") as numdata:
        reader = csv.DictReader(numdata)
        for i, row in enumerate(reader):
            if keyword in row.values():
                if row["basal"] != keyword:
                    return i + 1
                return i
    raise errors.UnknownKeywordError(keyword)


def order_interval_names(interval_names: Sequence[str]) -> tuple[str, ...]:
    """
    Take an array of interval names and ensure that they follow the order
    of their numerals, regardless of the accidentals.

    :param interval_names: An array of strings representing interval symbols
        using Indian numerals (e.g. "#4").
    :return: An array of the same, but ordered according to the numerals in
        the strings.
    """
    interval_names = list(interval_names)
    interval_names.sort(key=extract_number)
    return tuple(interval_names)

def extract_number(number_symbol: str) -> int:
    """
    Take a string that contains numeric digits, and return an integer made 
    up of those digits. Intended for interval names, but can work with
    any string.

    :param number_symbol: A string containing numeric digits.
    :return: An integer made up of all digits in sequence.

    :Example:
    >>> extract_number("#11")
    11
    >>> extract_number("12oclockand54minutes")
    1254
    """
    number = ""
    for char in number_symbol:
        if char.isdigit():
            number += char
    return int(number)


def encode_greek_notation(index: int, style: str) -> str:
    """
    Return the Greek musical symbol at the given index in the given style.

    :param index: The inventory number of the symbol.
    :param style: "vocal" or "instrumental"
    :raises IndexError: If the inventory number does not exist.
    :return: A unicode (utf-8) symbol representing a Greek musical symbol.
    """
    file = "src/data/greek_notation.csv"
    with open(file, newline="", encoding="utf8") as greek_data:
        reader = csv.DictReader(greek_data)
        for i, row in enumerate(reader):
            if index == i:
                return row[style]
    raise IndexError(index)


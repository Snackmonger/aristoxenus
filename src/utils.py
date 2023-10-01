'''
Miscellaneous functions.
'''
from typing import Any


def shift_list(list_: list[Any], new_first_member: Any) -> list[Any]:
    '''
    Rotate the list so that the given item is first.

    Parameters
    ----------
    list_ : list
        Python list with any values.
    
    new_first_member : Any
        The value that will start the new order.

    Returns
    -------
    list of Any
        A list rotated so that the given member is first.
    '''
    list_ = list_.copy()
    return list_[list_.index(new_first_member): ] + list_[ :list_.index(new_first_member)]


def roman_numeral(indian_numeral: int) -> str:
    '''
    Convert an Indian numeral between 1 and 3,999 to a Roman numeral.
    '''
    if indian_numeral not in range(1, 4000):
        raise ValueError(f'Numeral {indian_numeral} is out of range.')
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


def number_string():
    pass
numberstrings = {
    '1': {'cardinal': 'one',
          'ordinal': 'first',
          'ordinal_suffix': 'st',
          'uple': 'single'},

    '2': {'cardinal': 'two',
          'ordinal': 'second',
          'ordinal_suffix': 'nd',
          'uple': 'double'},

    '3': {'cardinal': 'three',
          'ordinal': 'third',
          'ordinal_suffix': 'rd',
          'uple': 'triple'},

    '4': {'cardinal': 'four',
          'ordinal': 'fourth',
          'ordinal_suffix': 'th',
          'uple': 'quadruple'},

    '5': {'cardinal': 'five',
          'ordinal': 'fifth',
          'ordinal_suffix': 'th',
          'uple': 'quintuple'},

    '6': {'cardinal': 'six',
          'ordinal': 'sixth',
          'ordinal_suffix': 'th',
          'uple': 'sextuple'},

    '7': {'cardinal': 'seven',
          'ordinal': 'seventh',
          'ordinal_suffix': 'th',
          'uple': 'septuple'},

    '8': {'cardinal': 'eight',
          'ordinal': 'eighth',
          'ordinal_suffix': 'th',
          'uple': 'octuple'},

    '9': {'cardinal': 'nine',
          'ordinal': 'ninth',
          'ordinal_suffix': 'th',
          'uple': 'nonuple'},

    '10': {'cardinal': 'ten',
           'ordinal': 'tenth',
           'ordinal_suffix': 'th'},

    '11': {'cardinal': 'eleven',
           'ordinal': 'eleventh',
           'ordinal_suffix': 'th'},

    '12': {'cardinal': 'twelve',
           'ordinal': 'twelfth',
           'ordinal_suffix': 'th'},

    '13': {'cardinal': 'thirteen',
           'ordinal': 'thirteenth',
           'ordinal_suffix': 'th'},

    '14': {'cardinal': 'fourteen',
           'ordinal': 'fourteenth',
           'ordinal_suffix': 'th'}
}

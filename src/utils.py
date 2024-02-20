'''
Miscellaneous functions.
'''

from typing import Any




def shift_list(list_: list[Any] | tuple[Any, ...],
               new_first_member: Any
               ) -> list[Any]:
    '''
    Rotate the given array so that the given item is first.

    Returns
    -------
    list
        A list rotated so that the given member is first. Naturally, if the 
        array contains a duplicate value, the shift won't work right.
    '''
    list_ = list(list_)
    return list_[list_.index(new_first_member): ] + list_[ :list_.index(new_first_member)]


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

def accidental_sorted(items: list[str]) -> list[str]:
    
    ...
'''
Miscellaneous functions.
'''


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

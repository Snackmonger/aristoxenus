'''
Functions for converting Roman numerals to Indian numerals and vice versa.
'''
__all__ = [
    'encode_roman_numeral', 
    'decode_roman_numeral'
]
__numerals: dict[str, int] = {
    'M': 1000,
    'D': 500,
    'C': 100,
    'L': 50,
    'X': 10,
    'V': 5,
    'I': 1
}

__partials: dict[str, int] = {
    'IV': 4,
    'IX': 9,
    'XL': 40,
    'XC': 90,
    'CD': 400,
    'CM': 900
}

__errors: dict[str, str] = {
    'IIII': 'IV',
    'VIV': 'IX',
    'XXXX': 'XL',
    'LXL': 'XC',
    'CCCC': 'CD',
    'DCD': 'CM'
}

def encode_roman_numeral(indian_numeral: int) -> str:
    '''
    Convert an Indian numeral between 1 and 3,999 to a Roman numeral.

    Parameters
    ----------
    indian_numeral : int
        An integer between 1 and 3999.

    Returns
    -------
    str
        A string representing a Roman numeral.

    Raises
    ------
    ValueError
        If the number exceeds 3,999 in the Indian form.

    Examples
    --------
    >>> encode_roman_numeral(1449)
    'MCDXLIX'
    >>> encode_roman_numeral(1318)
    'MCCCXVIII'
    >>> encode_roman_numeral(959)
    'CMLIX'
    >>> encode_roman_numeral(263)
    'CCLXIII'
    '''
    if indian_numeral not in range(1, 4000):
        raise ValueError(f"Can only convert numbers 1-399 ({indian_numeral=})")
    roman_numeral_: str = ''
    for numeral, value in __numerals.items():
        while indian_numeral >= value:
            roman_numeral_ += numeral
            indian_numeral -= value
        for error, correction in __errors.items():
            if error in roman_numeral_:
                assert isinstance(correction, str)
                roman_numeral_ = roman_numeral_.replace(error, correction)

    return roman_numeral_


def decode_roman_numeral(symbol: str) -> int:
    '''
    Convert a Roman numeral to an Indian numeral.

    Parameters
    ----------
    symbol : str
        A string representing a Roman numeral.

    Returns
    -------
    int
        An integer representing the given numeral.

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
    '''
    values: list[int] = []
    for partial, value in __partials.items():
        if partial in symbol:
            assert isinstance(value, int)
            values.append(value)
            symbol = symbol.replace(partial, "")
    for numeral, value in __numerals.items():
        if numeral in symbol:
            values.append(value*symbol.count(numeral))
    return sum(values)


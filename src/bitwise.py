'''
Miscellania pertaining to bitwise operations.

Notes
-----
We treat musical relationships as intervals, not as notes. All intervals are 
by definition distances between pitches. The least significant bit represents 
the lowest pitch of the strcuture. Since the lowest pitch of the structure is 
the pitch from which other intervals are calculated, every interval (and 
therefore every compound interval structure) must be an odd number. 
    
'''
import functools
from typing import Generator

from data import constants

def validate_interval(interval: int) -> bool:
    '''
    Checks whether an integer can be used as a valid interval.

    This entails that there are exactly 2 flipped bits, and that the integer 
    is an odd number.

    Parameters
    ----------
    interval : int
        An integer to be checked for valid interval status.

    Returns
    -------
    bool
        True, if the integer can be used as an interval.

    Notes
    -----
    All intervals consist of two extremities and a certain amount of distance 
    between them. This equates to a binary number beginning and ending with 1, 
    and with an indeterminate number of 0s between them (e.g. 1000001, 101,
    1000000000000001, etc.).

    Examples
    --------
    >>> validate_interval(0b10110)
    False
    >>> validate_interval(0b100001)
    True
    '''
    return interval.bit_count() == 2 and interval % 2 == 1


def validate_interval_structure(interval_structure: int,
                                 max_bits: int, 
                                 flipped_bits: int=0) -> bool:
    '''
    Return True if the interval structure is within the specified maximum 
    number of bits.

    Parameters
    ----------
    interval_structure : int
        An integer representing an interval structure.
    max_bits : int
        The maximum number of bits expected.
    flipped_bits : int, default=0
        The expected number of flipped bits. 0 means 'any number of flipped
        bits is valid'.

    Returns
    -------
    bool
        True, if the bit length of the given interval structure does
        not exceed the maximum number of bits, and contains the expected
        number of flipped bits.

    Examples
    --------
    >>> validate_interval_structure(0b100010000, 8, 2)
    False
    >>> validate_interval_structure(0b10010011, 8, 4)
    True
    >>> validate_interval_structure(0b10010011, 8)
    True
    >>> validate_interval_structure(0b1011, 8, 4)
    False
    >>> validate_interval_structure(0b1011, 8, 3)
    True
    >>> validate_interval_structure(0b1011, 8)
    True
    '''
    max_: bool = interval_structure.bit_length() <= max_bits
    flip_: bool = interval_structure.bit_count() == flipped_bits
    if flipped_bits == 0:
        flip_ = True
    return  max_ and flip_


def has_interval(interval_structure: int, interval: int) -> bool:
    '''
    Return true if the given interval appears in the interval structure.

    Parameters
    ----------
    interval_structure : int
        The interval structure that you want to test against.
    interval : int
        The interval that you want to test for.

    Returns
    -------
    bool
        True, if the interval's bit is flipped in the interval structure.

    Examples
    --------
    >>> has_interval(0b10110101, 0b10001)
    True
    >>> has_interval(0b10110101, 0b11)
    False
    '''
    return interval & interval_structure == interval


def transpose_interval(interval: int, octave: int = 1, echo: bool = False) -> int:
    '''
    Return the equivalent of the given interval sharpened by the given number
    of octaves.

    Parameters
    ----------
    interval : int
        The interval to be transposed.
    octave : int, default=1
        The number of octaves you want to transpose the interval by.
    echo : bool, default=False
        True: the whole interval is transposed n octaves
            0b101 -> 101000000000001 (ninth, octave, tonic)
        False: the interval is replaced with a compound of n octaves
            0b101 -> 100000000000001 (ninth, tonic)

    Returns
    -------
    int
        An integer representing the original interval shifted by 12 * n bits.

    Notes
    -----
    The `echo` parameter should be set to True when you want to ensure that 
    the transposed structure are exact copies of the interval or interval
    structure. Use this when making compounds for iterating over larger 
    chord/scale structures (e.g. 2-hand piano voicings).

    The `echo` parameter should be set to False when you don't want the 
    original root/tonic of an interval or interval structure to reappear 
    as an octave. Use this when adding specific extensions (and only those
    extensions) to the upper structure.

    See Also
    --------
    permutation.extend_structure : The main reason for the `echo` option.

    Examples
    --------
    >>> bin(transpose_interval(0b10001))
    '0b10000000000000001'
    >>> bin(transpose_interval(0b10001, echo=True))
    '0b10001000000000001'
    >>> bin(transpose_interval(0b10001, 2, echo=True))
    '0b10001000000000000000000000001'
    >>> bin(transpose_interval(0b10001, 2, echo=False))
    '0b10000000000000000000000000001'
    '''
    modifier: int = -1 if echo is False else 0
    return ((interval + modifier) << constants.TONES * octave) + 1



def rotate_left(collection: int, max_bits: int) -> int:
    '''Rotate the bit collection left 1 time.'''
    return (collection << 1 ) & (2 ** max_bits- 1) | (collection & (2 ** max_bits - 1)) >> (max_bits - 1)


def rotate_right(collection: int, max_bits: int) -> int:
    '''Rotate the bit collection right 1 time.'''
    return (collection & (2 ** max_bits - 1)) >> 1 | (collection << (max_bits - 1) & (2 ** max_bits - 1))


def previous_inversion(interval_structure: int, max_bits: int) -> int:
    '''
    Rotate the bit collection right to the next mode/inversion.

    Parameters
    ----------
    interval_structue : int
        The interval structure to be inverted.
    max_bits : int
        The expected maximum number of bits in the collection.

    Returns
    -------
    int
        An integer representing the inverted interval structure.

    Examples
    --------
    >>> bin(previous_inversion(0b101010110101, 12))
    '0b11010101101'
    >>> bin(previous_inversion(0b11010101101, 12))
    '0b10110101011'
    '''
    interval_structure = rotate_right(interval_structure, max_bits)
    while interval_structure % 2 == 0:
        interval_structure = rotate_right(interval_structure, max_bits)
    return interval_structure


def next_inversion(interval_structure: int, max_bits: int) -> int:
    '''
    Rotate the bit collection left to the next mode/inversion.

    Parameters
    ----------
    interval_structue : int
        The interval structure to be inverted.
    max_bits : int
        The expected maximum number of bits in the collection.

    Returns
    -------
    int
        An integer representing the inverted interval structure.

    Examples
    --------
    >>> bin(next_inversion(0b101010110101, 12))
    '0b10101101011'
    >>> bin(next_inversion(0b10101101011, 12))
    '0b10110101101'
    '''
    interval_structure = rotate_left(interval_structure, max_bits)
    while interval_structure % 2 == 0:
        interval_structure = rotate_left(interval_structure, max_bits)
    return interval_structure


def iterate_bits(integer: int) -> Generator[int, None, None]:
    '''
    Return the individual flipped bits for a given integer.

    Parameters
    ----------
    integer : int
        An integer with n flipped bits.

    Yields
    ------
    Generator[int, None, None]
        A series of n integers representing the flipped bits of the input.

    Examples
    --------
    >>> x = list(iterate_bits(0b101010110101))
    >>> bin(x[1])
    '0b100'
    >>> bin(x[2])
    '0b10000'
    '''
    # The logic of the operation:
    # x       = 01011000
    # ~x      = 10100111
    # ~x+1    = 10101000
    # x&(~x+1)= 00001000
    while integer != 0:
        current_bit = integer & ( ~ integer + 1)
        yield current_bit
        integer ^= current_bit
        

def iterate_intervals(interval_structure: int) -> Generator[int, None, None]:
    '''
    Iterate the intervals of a given interval structure.

    This function is identical to `iterate_bits`, except that it ensures that
    the yielded number must be odd.

    Parameters
    ----------
    interval_structure : int
        The interval structure to iterate over.

    Yields
    ------
    Generator[int, None, None]
        A series of intervals, expressed as integers.

     Examples
    --------
    >>> x = list(iterate_intervals(0b101010110101))
    >>> bin(x[1])
    '0b101'
    >>> bin(x[2])
    '0b10001'
    '''
    for result in iterate_bits(interval_structure):
        if result % 2 == 0:
            yield result + 1
        else:
            yield result


def reduce_(intervals: list[int] | tuple[int, ...]) -> int:
    '''
    Syntactic shortcut for reduction by bitwise OR.

    Parameters
    ----------
    intervals : list[int] | tuple[int, ...]
        A collection of integers, each representing one interval in a larger
        structure.

    Returns
    -------
    int
        A compound of all the intervals in the colection in a single integer.

    Examples
    --------
    >>> bin(reduce_([0b101, 0b10001, 0b10000001]))
    '0b10010101'
    '''
    return functools.reduce(lambda a, b: a | b, intervals)


def inversions(interval_structure: int, max_bits: int) -> tuple[int, ...]:
    '''
     
    Return a list containing the integer representations of all possible
    inversions of the current interval structure. 
    
    This is determined by looking at the expected length of the whole 
    structure, so multi-octave interval structures rotate all their octaves 
    as one long loop.

    Parameters
    ----------
    interval_structure : int
        An integer representing an interval structure.
    max_bits : int
        The maximum number of bits in the structure.

    Returns
    -------
    tuple[int, ...]
        A collection of integers, each representing one rotational 
        transformation of the given interval structure.

    Examples
    --------
    >>> inversions(0b101010110101, 12)
    (2741, 1709, 1451, 2773, 1717, 1453, 1387)
    '''
    rotations: list[int] = []
    for _ in range(interval_structure.bit_count()):
        rotations.append(interval_structure)
        interval_structure = previous_inversion(interval_structure, max_bits)
    return tuple(rotations)


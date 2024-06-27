'''
Aristoxenus internally represents musical structures as integers and uses
bitwise operations to manage harmonic transformation. This module provides 
functions pertaining to manipulating integers at the binary level. The user 
presumably will not need to use functions from this module.
'''
import functools
from typing import Generator, Sequence

from src.data import constants, errors

__all__ = [
    "validate_interval",
    "validate_interval_structure",
    "has_interval",
    "transpose_interval",
    "next_inversion",
    "previous_inversion",
    "iterate_bits",
    "iterate_intervals",
    "reduce_intervals",
    "get_rotation",
    "extend_structure"
]

def validate_interval(interval: int) -> bool:
    """
    Checks whether an integer can be used as a valid interval.

    This entails that there are exactly 2 flipped bits, and that the integer
    is an odd number (i.e. any binary number beginning and ending with 1 and
    having only zeroes or nothing in between).

    :param interval: An integer to be checked for valid interval status.
    :return: True, if the integer can be used as an interval.

    :Example:
    >>> validate_interval(0b100001)
    True
    >>> validate_interval(0b10110)
    False
    """
    return interval.bit_count() == 2 and interval % 2 == 1


def validate_interval_structure(interval_structure: int,
                                 max_bits: int, 
                                 flipped_bits: int = 0) -> bool:
    """
    Test whether the given interval structure is within the specified 
    bit-length and flipped bit-count.

    :param interval_structure: An integer representing an interval structure.
    :param max_bits: The maximum number of bits expected. Structures of fewer
        bits will be considered valid.
    :param flipped_bits: The expected number of flipped bits. 0 means 'any 
        number of flipped bits is valid', defaults to 0
    :return: True, if the bit length of the given interval structure does not 
        exceed the maximum number of bits, and contains the expected number of 
        flipped bits.

    :Example: Check whether the structure does not exceed the expected length:
    >>> validate_interval_structure(0b10010011, 8)
    True
    >>> validate_interval_structure(0b1011, 8)
    True
    >>> validate_interval_structure(0b100010100101, 8)
    False

    :Example: The exact number of expected flipped bits can be specified:
    >>> validate_interval_structure(0b1011, 8, 3)
    True
    >>> validate_interval_structure(0b10010011, 8, 4)
    True
    >>> validate_interval_structure(0b1011, 8, 4)
    False
    >>> validate_interval_structure(0b100010000, 8, 2)
    False
    """
    max_: bool = interval_structure.bit_length() <= max_bits
    flip_: bool = interval_structure.bit_count() == flipped_bits
    if flipped_bits == 0:
        flip_ = True
    return  max_ and flip_


def has_interval(interval_structure: int, interval: int) -> bool:
    """
    Return true if the given interval appears in the interval structure.

    :param interval_structure: An integer representing an interval structure.
    :param interval: An integer representing the interval that you want to 
        test for.
    :return: True, if the interval's bits are flipped in the interval 
        structure.

    :Example:
    >>> has_interval(0b10110101, 0b10001)
    True
    >>> has_interval(0b10110101, 0b11)
    False
    """
    return interval & interval_structure == interval


def transpose_interval(interval: int, octave: int = 1, echo: bool = False) -> int:
    """
    Return the equivalent of the given interval sharpened by the given number
    of octaves.

    :param interval: An integer representing the interval to be transposed.
    :param octave: The number of octaves by which to transpose the interval, 
        defaults to 1
    :param echo: Flag to repeat the lowest tone in the transposition(s), 
        defaults to False
    :return: An integer representing the original interval shifted by 
        12 * n bits.

    .. note::
        The ``echo`` parameter should be set to True when you want to ensure 
        that the transposed structure(s) are exact copies of the starting 
        structure, including its lowest tone. Use this when making compounds 
        for iterating over larger chord/scale structures (e.g. 2-hand piano 
        voicings).
        0b101 -> 101000000000001 (ninth, octave, tonic)

        The `echo` parameter should be set to False when you don't want the 
        original root/tonic of an interval or interval structure to reappear 
        as an octave. Use this when adding specific extensions (and only those
        extensions) to the upper structure.
        0b101 -> 100000000000001 (ninth, tonic)

    .. seealso:: 
        permutation.extend_structure : The main reason for the `echo` option.

    :Example:
    >>> bin(transpose_interval(0b10001))
    '0b10000000000000001'
    >>> bin(transpose_interval(0b10001, echo=True))
    '0b10001000000000001'
    >>> bin(transpose_interval(0b10001, 2, echo=True))
    '0b10001000000000000000000000001'
    >>> bin(transpose_interval(0b10001, 2, echo=False))
    '0b10000000000000000000000000001'
    """
    modifier: int = -1 if echo is False else 0
    return ((interval + modifier) << constants.TONES * octave) + 1


def __rotate_left(collection: int, max_bits: int) -> int:
    '''Auxiliary function. Rotate the bit collection left 1 time.'''
    return (collection << 1 ) & (2 ** max_bits- 1) | (collection & (2 ** max_bits - 1)) >> (max_bits - 1)


def __rotate_right(collection: int, max_bits: int) -> int:
    '''Auxiliary function. Rotate the bit collection right 1 time.'''
    return (collection & (2 ** max_bits - 1)) >> 1 | (collection << (max_bits - 1) & (2 ** max_bits - 1))


def next_inversion(interval_structure: int, max_bits: int) -> int:
    """
    Rotate an interval structure to its next mode/inversion.

    :param interval_structure: An integer representing an interval structure
        to be inverted.
    :param max_bits: The expected maximum number of bits in the structure.
    :return: An integer representing the inverted interval structure.

    :Example:
    >>> bin(next_inversion(0b101010110101, 12))
    '0b11010101101'
    >>> bin(next_inversion(0b10101101011, 12))
    '0b101010110101'
    """
    interval_structure = __rotate_right(interval_structure, max_bits)
    while interval_structure % 2 == 0:
        interval_structure = __rotate_right(interval_structure, max_bits)
    return interval_structure


def previous_inversion(interval_structure: int, max_bits: int) -> int:
    """
    Rotate an interval structure to its previous mode/inversion.

    :param interval_structure: An integer representing an interval structure
        to be inverted.
    :param max_bits: The expected maximum number of bits in the structure.
    :return: An integer representing the inverted interval structure.

    :Example:
    >>> bin(previous_inversion(0b101010110101, 12))
    '0b10101101011'
    >>> bin(previous_inversion(0b11010101101, 12))
    '0b101010110101'
    """
    interval_structure = __rotate_left(interval_structure, max_bits)
    while interval_structure % 2 == 0:
        interval_structure = __rotate_left(interval_structure, max_bits)
    return interval_structure


def iterate_bits(integer: int) -> Generator[int, None, None]:
    """
    Return the individual flipped bits for a given integer.

    :param integer: An integer with n flipped bits.
    :yield: A series of n integers representing the flipped bits of the input.

    :Example:
    >>> x = list(iterate_bits(0b101010110101))
    >>> bin(x[1])
    '0b100'
    >>> bin(x[2])
    '0b10000'
    """
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
    """
    Iterate the intervals of a given interval structure.

    This function is identical to ``iterate_bits``, except that it ensures 
    that the yielded number must be odd.

    :param interval_structure: An integer representing the interval structure 
        over which to iterate.
    :yield: A series of intervals, expressed as integers.

    :Example:
    >>> x = list(iterate_intervals(0b101010110101))
    >>> bin(x[1])
    '0b101'
    >>> bin(x[2])
    '0b10001'
    """
    for result in iterate_bits(interval_structure):
        if result % 2 == 0:
            yield result + 1
        else:
            yield result


def reduce_intervals(intervals: Sequence[int]) -> int:
    """
    Syntactic shortcut for reduction by bitwise OR.

    :param intervals: A collection of integers, each representing one interval
        in a larger structure.
    :return: A compound of all the intervals in the colection in a single 
        integer.
    
    :Example:
    >>> bin(reduce_intervals([0b101, 0b10001, 0b10000001]))
    '0b10010101'
    """
    return functools.reduce(lambda a, b: a | b, intervals)


def get_inversions(interval_structure: int, max_bits: int) -> tuple[int, ...]:
    """
    Return a tuple containing the integer representations of all possible
    rotations of the given interval structure. 

    :param interval_structure: An integer representing an interval structure.
    :param max_bits: The maximum number of bits in the structure.
    :return: A collection of integers, each representing one rotational 
        transformation of the given interval structure.

    :Example:
    >>> get_inversions(0b101010110101, 12)
    (2741, 1709, 1451, 2773, 1717, 1453, 1387)
    """
    rotations: list[int] = []
    for _ in range(interval_structure.bit_count()):
        rotations.append(interval_structure)
        interval_structure = next_inversion(interval_structure, max_bits)
    return tuple(rotations)


def get_rotation(interval_structure: int, rotations: int = 1) -> int:
    """
    For a given interval structure, return the nth rotation, assuming
    a bit-length of 12.

    :param interval_structure: An integer representing a scale form 
        not exceeding 12 bits.
    :param rotations: The number of forward rotations to perform, 
        defaults to 1
    :return: An integer representing a modal rotation of the initial 
        scale.
    
    :Example:
    >>> bin(get_rotation(0b101001))
    '0b1000000101'
    """
    for _ in range(rotations):
        interval_structure = next_inversion(interval_structure, 12)
    return interval_structure


def extend_structure(interval_structure: int,
                     extensions: int = constants.NUMBER_OF_OCTAVES
                     ) -> int:
    """
    Extend a 12-bit interval structure to the range of n identical octaves.

    :param interval_structure: An integer of no more than 12 bits representing 
        an interval structure.
    :param extensions: A number of octaves to extend the structure over, defaults 
        to 9.
    :raises errors.IntervalStructureError: Raised if the user passes a structure
        exceeding 12 bits.
    :return: An n*12-bit interval structure, with the original 12-bit structure 
        repeating every 12 bits.

    :Example:
    >>> bin(extend_structure(0b101010110101, 2))
    '0b101010110101101010110101'
    >>> bin(extend_structure(0b101010110101, 3))
    '0b101010110101101010110101101010110101'
    """
    if not validate_interval_structure(interval_structure, 12):
        raise errors.IntervalStructureError(interval_structure)

    compound_structure: int = interval_structure
    for transposed_octave in range(1, extensions):
        compound_structure |= transpose_interval(
            interval_structure, transposed_octave, echo=True)
    return compound_structure

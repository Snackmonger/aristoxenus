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
from typing import Generator



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
    '''
    return interval & interval_structure == interval


def transpose_interval(interval: int, octave: int = 1) -> int:
    '''
    Return the equivalent of the given interval sharpened by the given number
    of octaves.

    Parameters
    ----------
    interval : int
        The interval to be transposed.
    octave : int
        The number of octaves you want to transpose the interval by.

    Returns
    -------
    int
        An integer representing the original interval shifted by 12 * n bits.
    '''
    return ((interval - 1) << 12 * octave) + 1


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
    '''
    for result in iterate_bits(interval_structure):
        if result % 2 == 0:
            yield result + 1
        else:
            yield result
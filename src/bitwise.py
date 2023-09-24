'''
Miscellania pertaining to bitwise operations.

Notes
-----
All intervals are, by definition, distances between pitches. The least 
significant bit represents the lowest pitch of the strcuture. Since the 
lowest pitch of the structure is the pitch from which other intervals are 
calculated, every interval (and therefore every compound interval structure) 
must be an odd number. 
    
'''
import loguru
logger = loguru.logger


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

    Notes
    -----
    We use the maximum number of bits to keep track of whether a certain 
    number of 0s should implicitly be understood at the beginning of a
    structure, so that they can be added to the end of the structure
    as it rotates. If the rotation is an even number (i.e. ends in a binary
    0), we know that we have not completed rotating to the next inversion.
    '''
    logger.debug(f'{interval_structure} : {bin(interval_structure)}')
    while interval_structure % 2 == 0:
        interval_structure = rotate_right(interval_structure, max_bits)
    return interval_structure


def next_inversion(collection: int, max_bits: int) -> int:
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

    Notes
    -----
    We use the maximum number of bits to keep track of whether a certain 
    number of 0s should implicitly be understood at the beginning of a
    structure, so that they can be added to the end of the structure
    as it rotates. If the rotation is an even number (i.e. ends in a binary
    0), we know that we have not completed rotating to the next inversion.
    '''
    collection = rotate_left(collection, max_bits)
    while collection % 2 == 0:
        collection = rotate_left(collection, max_bits)
    return collection

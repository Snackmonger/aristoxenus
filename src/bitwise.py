'''
Miscellania pertaining to bitwise operations.
'''
import loguru

logger = loguru.logger

def has_interval(collection: int, interval: int) -> bool:
    '''
    Return true if the given interval appears in the interval collection.

    
    '''
    return interval & collection == interval


def transpose_interval(interval: int, octave: int = 1) -> int:
    '''
    Return the equivalent of the given interval shifted up by X number of octaves.
    '''
    return ((interval - 1) << 12 * octave) + 1


def rotate_bits_left(collection: int, max_bits: int) -> int:
    '''
    Rotate the bit collection left 1 time.
    '''
    return (collection << 1 ) & (2 ** max_bits- 1) | (collection & (2 ** max_bits - 1)) >> (max_bits - 1)


def rotate_bits_right(collection: int, max_bits: int) -> int:
    '''
    Rotate the bit collection right 1 time.
    '''
    return (collection & (2 ** max_bits - 1)) >> 1 | (collection << (max_bits - 1) & (2 ** max_bits - 1))


def next_mode(collection: int, max_bits: int) -> int:
    '''
    Rotate the bit collection right to the next mode/inversion.
    '''
    logger.debug(f'{collection} : {bin(collection)}')
    while collection % 2 == 0:
        collection = rotate_bits_right(collection, max_bits)
    return collection


def previous_mode(collection: int, max_bits: int) -> int:
    '''
    Rotate the bit collection left to the previous mode/inversion.
    '''
    collection = rotate_bits_left(collection, max_bits)
    while collection % 2 == 0:
        collection = rotate_bits_left(collection, max_bits)
    return collection

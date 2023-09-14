'''
Functions relating to processing integers as pitch maps.
'''
from typing import Any


def number_of_pitches(collection: int) -> int:
    '''
    Return the number of pitches in the collection.
    '''
    return collection.bit_count()


def __rotate_bits_left(collection: int, max_bits: int) -> int:
    '''
    Rotate the bit collection left 1 time.
    '''
    return (collection << 1 ) & (2 ** max_bits- 1) | (collection & (2 ** max_bits - 1)) >> (max_bits - 1)


def __rotate_bits_right(collection: int, max_bits: int) -> int:
    '''
    Rotate the bit collection right 1 time.
    '''
    return (collection & (2 ** max_bits - 1)) >> 1 | (collection << (max_bits - 1) & (2 ** max_bits - 1))


def next_mode(collection: int, max_bits: int) -> int:
    '''
    Rotate the bit collection left, but ensure that 
    the bit length is always at the given maximum.

    Ensures that we rotate to the next note of the 
    scale/chord (1), not the next chromatic (0).
    '''
    collection = __rotate_bits_right(collection, max_bits)
    while collection.bit_length() < max_bits:
        collection = __rotate_bits_right(collection, max_bits)
    return collection


def previous_mode(collection: int, max_bits:int) -> int:
    '''
    Rotate the bit collection right, but ensure that 
    the bit length is always at the given maximum.

    Ensures that we rotate to the previous note of the 
    scale/chord (1), not the previous chromatic (0).
    '''
    collection = __rotate_bits_left(collection, max_bits)
    while collection.bit_length() < max_bits:
        collection = __rotate_bits_left(collection, max_bits)
    return collection


def render(collection: int, chromatic_scale: list[str]) -> list[str]:
    '''
    Return a human-readable list of strings representing
    the pitch collection in the given accidental style.

    User is responsible for making sure that the length of the
    chromatic scale is the same as the number of bits in the 
    given collection integer.
    '''
    rendering: list[str] = []
    max_bits: int = len(chromatic_scale)
    if collection.bit_length() is not max_bits:
        raise ValueError('Pitch collection and chromatic scale must be the same length.')
    for interval in range(0, max_bits):
        binary_column: int = 1 << interval # tonic is least significant bit
        if (collection & binary_column) == binary_column:
            rendering.append(chromatic_scale[interval])
    return rendering


def shift_list(list_: list[Any], new_first_member: Any) -> list[Any]:
    '''
    Rotate the list so that the given item is first.
    (Just a shortcut for prettier syntax.)
    '''
    return list_[list_.index(new_first_member[0]): ] + list_[ :list_.index(new_first_member[0])]


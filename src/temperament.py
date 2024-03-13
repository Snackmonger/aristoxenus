'''The temperament module supplies the ranges of frequencies that 
correspond to the ranges of the 12-tone alphabetic scales.

For now, we really only deal with equal temperament, but eventually this will
allow us to change the temperament entirely, and to 'borrow' frequencies from differing
temperaments so as to create different sorts of interval feelings within a single scale.
'''


from data import (constants)
from src import (nomenclature)


def equal_temperament() -> tuple[float, ...]:
    '''
    Return a list of frequencies corresponding to the range of the scientific 
    chromatic scales (C0 - B8).

    Returns
    -------
    list of float
        A list of 108 frequencies, rounded to three decimal places.
    '''
    centre_name: str = constants.CENTRAL_REFERENCE_NOTE_NAME
    centre_freq: int = constants.CENTRAL_REFERENCE_NOTE_FREQUENCY
    limit: int = constants.FREQUENCY_DECIMAL_LIMIT
    equiv: int = constants.OCTAVE_EQUIVALENCE_FACTOR
    frequencies: list[float] = []
    frequency: float
    direction: int
    semitones: int
    
    full_range: tuple[str, ...] = nomenclature.scientific_range(constants.BINOMIALS)
    for note in full_range:
        if full_range.index(note) < full_range.index(centre_name):
            direction = constants.FLAT_VALUE
            semitones = full_range.index(centre_name) - full_range.index(note)
        else:
            direction = constants.SHARP_VALUE
            semitones = full_range.index(note) - full_range.index(centre_name)

        # 12 TET : next note = previous note * 2 ** (+ , -) 1/12
        frequency = centre_freq * equiv ** (direction * semitones / constants.TONES)
        if frequency not in frequencies:
            frequencies.append(round(frequency, limit))

    return tuple(frequencies)
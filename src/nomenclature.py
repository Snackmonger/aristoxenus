'''
Functions related to generating and processing musical nomenclatural material.
'''
from dataclasses import dataclass
from typing import Any
from .vocabulary import SHARP_SYMBOL, FLAT_SYMBOL, BINOMIAL_DIVIDER_SYMBOL

# Symbolic precursors.
__NATURALS: list[str] = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
__HALFSTEPS: dict[str, str] = {'E': 'F', 'B': 'C'}
__ACCIDENTAL_SYMBOLS: list[str] = [SHARP_SYMBOL, FLAT_SYMBOL]

# Numerical percursors.
__TONES: int = 12
__NOTES: int = 7
__CENTRAL_REFERENCE_NOTE_NAME: str = 'A4'
__CENTRAL_REFERENCE_NOTE_FREQUENCY: int = 440
__SHARP_VALUE: int = 1
__FLAT_VALUE: int = -1
__NUMBER_OF_OCTAVES: int = 9
__OCTAVE_EQUIVALENCE_FACTOR: int = 2
__FREQUENCY_DECIMAL_LIMIT: int = 3

# Accidental symbols.
__SHARPS: list[str] = [note + SHARP_SYMBOL for note in __NATURALS
                       if note not in __HALFSTEPS]

__FLATS: list[str] = [note + FLAT_SYMBOL for note in __NATURALS
                      if note not in __HALFSTEPS.values()]

__BINOMIALS: list[str] = [sharp + BINOMIAL_DIVIDER_SYMBOL + flat
                          for flat in __FLATS for sharp in __SHARPS
                          if __FLATS.index(flat) == __SHARPS.index(sharp)]

__ACCIDENTAL_NOTES: list[str] = __SHARPS + __FLATS


def shift_list(list_: list[Any], new_first_member: Any) -> list[Any]:
    '''
    Rotate the list so that the given item is first.

    Parameters
    ----------
    list_ : list
        Python list with any values.
    
    new_first_member : Any
        The value that will start the new order.

    Returns
    -------
    list of Any
        A list rotated so that the given member is first.
    '''
    return list_[list_.index(new_first_member[0]): ] + list_[ :list_.index(new_first_member[0])]



def __chromatic(accidental_notes: list[str]) -> list[str]:
    '''
    Return a chromatic octave using the given accidentals.

    Parameters
    ----------
    accidental_notes : list of str
        A list of 5 strings, one of __BINOMIALS, __SHARPS, __FLATS. This
        defines the type of accidentals that the octave will use.

    Returns
    -------
    list of str
        A list of 12 note names, in the given accidental style.
    '''
    new_scale: list[str] = []
    accidentals_in_scale: int = 0
    for note in __NATURALS:
        new_scale.append(note)
        if note not in __HALFSTEPS:
            new_scale.append(accidental_notes[accidentals_in_scale])
            accidentals_in_scale += 1
    return new_scale


def __enharmonic_decoder() -> dict[str, str]:
    '''
    Generate a table for decoding the binomial form of a note with any number 
    of sharps or flats.

    Returns
    -------
    dict
        E.g. {'C#': 'C#|Db', ..., 'Ebb': 'D', ..., 'F###': 'G#|Ab', ...}
    '''
    enharmonic_equivalence_decoder: dict[str, str] = {}
    chromatic_binomials: list[str] = chromatic()
    for accidental in __ACCIDENTAL_SYMBOLS:
        dummy_chromatic_binomials: list[str] = chromatic_binomials.copy()
        shift_degree = __SHARP_VALUE

        # Reverse sequence for flats.
        if accidental == FLAT_SYMBOL:
            shift_degree = __FLAT_VALUE + __TONES
            dummy_chromatic_binomials.reverse()
            dummy_chromatic_binomials = dummy_chromatic_binomials[shift_degree:] + \
                dummy_chromatic_binomials[:shift_degree]
            
        # Create accidentals from the 7 naturals only, but keep
        # track of their 12-tone equivalents in the binomial format.
        for binomial in chromatic_binomials:
            if binomial in __BINOMIALS:
                pass
            else:
                for added_accidental in range(__TONES):
                    enharmonic_equivalence_decoder.update(
                        {binomial + accidental * added_accidental: dummy_chromatic_binomials[added_accidental]})
            dummy_chromatic_binomials = dummy_chromatic_binomials[shift_degree:] + \
                dummy_chromatic_binomials[:shift_degree]
    return enharmonic_equivalence_decoder


def __get_enharmonic_equivalents(note_name: str) -> list[str]:
    '''
    Compile a list of all enharmonic equivalents of a note in sharps or flats.

    Examples
    --------
    >>> __get_enharmonic_equivalents('E') 
    ['E', 'Fb', 'Gbbb', ..., 'D##', 'C####', ...]
    '''
    list_of_equivalents: list[str] = []
    decoder: dict[str, str] = __enharmonic_decoder()
    for key, value in decoder.items():
        if value == note_name:
            list_of_equivalents.append(key)
    return list_of_equivalents


def legal_chord_names() -> list[str]:
    '''
    Return a list of note names that can function as legal chord root symbols. 

    Returns
    -------
    list of str
        A list of all notes with between 0 and 1 accidentals, excluding the
        binomials.
    '''
    # Any natural or any natural + 1 accidental
    enharmonic_: dict[str, str] = __enharmonic_decoder()
    legal_names_: list[str] = []
    for key in enharmonic_:
        if len(key) <= 2:
            legal_names_.append(key)
    return legal_names_


def __identity(note_name: str) -> str:
    '''
    Return the alphabetic name of an accidental note.

    Parameters
    ----------
    note_name : str
        An alphabetic note name with any number of accidentals.

    Returns
    -------
    str
        A natural note name.

    Examples
    --------
    >>> __identity('B###') 
    'B'
    '''
    if note_name in __BINOMIALS:
        raise ValueError('Cannot resolve a binomial note name.')
    return note_name[0]


def __is_homonymous(note_one: str, note_two: str) -> bool:
    '''
    Check whether two notes are variants of the same alphabetic name.

    Parameters
    ----------
    note_one : str
        An alphabetic note name with any number of accidentals.

    note_two : str
        An alphabetic note name with any number of accidentals.

    Returns
    -------
    bool
        True if the two notes have the same alphabetic letter name.

    Examples
    --------
    >>> __is_homonymous('B###', 'Bb') 
    True
    >>> __is_homonymous('B###', 'Eb') 
    False
    '''
    return __identity(note_one) == __identity(note_two)


def decode_enharmonic(note_name: str) -> str:
    '''
    Return the binomial form of a given note name with up to 12 accidentals.

    Parameters
    ----------
    note_name : str
        A note name with 0 to 12 accidentals.

    Returns
    -------
    str
        A binomial note name enharmonically equivalent to the given note name
        
    Examples
    --------
    >>> decode_scientific_enharmonic('B#')
    'C'
    >>> decode_scientific_enharmonic('A######')
    'D#|Eb'
    '''
    
    decoder: dict[str, str] = __enharmonic_decoder()
    if note_name in chromatic():
        return note_name
    if note_name not in decoder:
        raise ValueError(f'Note name {note_name} not recognized.')
    return decoder[note_name]


def encode_enharmonic(note_value: str, note_name: str) -> str:
    '''
    Return a note with the same enharmonic value as the given note,
    but under the given alphabetic name.

    Parameters
    ----------
    note_value : str
        A note name with 0 to 1 accidentals (binomials count as 1 accental).

    note_name : str    
        One of the 7 natural notes

    Notes
    -----
    This function prefers the enharmonic equivalent with the fewest 
    accidentals. When shifting by tritone, the number of accidentals will be 
    equal in both sharps and flats, so we arbitrarily default to sharps.

    Returns
    -------
    str
        A note with between 0 and 6 accidentals. No note name is more than six
        steps from any other name, depending on the direction.

    Examples
    --------
    >>> encode_enharmonic('Eb' , 'A') 
    'A######'
    >>> encode_enharmonic('Eb' , 'B')
    'B####'
    >>> encode_enharmonic('Eb' , 'C')
    'C###'
    >>> encode_enharmonic('Eb' , 'D')
    'D#' 
    >>> encode_enharmonic('Eb' , 'E')
    'Eb'
    >>> encode_enharmonic('Eb' , 'F') 
    'Fbb'
    >>> encode_enharmonic('Eb' , 'G') 
    'Gbbb'
    >>> encode_enharmonic('Eb' , 'A') 
    'A######'
    '''
    if note_name not in __NATURALS:
        raise ValueError('Target note name must be from the naturals.')
    
    note_value = decode_enharmonic(note_value)
    options: list[str] = __get_enharmonic_equivalents(note_value)
    homonymous_options: list[str] = []
    for option in options:
        if __is_homonymous(option, note_name):
            homonymous_options.append(option)
    return sorted(homonymous_options, key=len)[0]


def __scientific_octave(accidental_notes: list[str], octave: int) -> list[str]:
    '''
    Return a scientific chromatic scale in the given style and octave.

    Parameters
    ----------
    accidental_notes : list[str]
        A list of 5 strings, one of __BINOMIALS, __SHARPS, __FLATS. This
        defines the type of accidentals that the result will use.

    octave : int
        The range number appended to the note name.

    Returns
    -------
    str
        A binomial note name enharmonically equivalent to the given note name
        
    '''
    return [note + str(octave) for note in __chromatic(accidental_notes)]


def decode_scientific_enharmonic(note_name: str) -> str:
    '''
    Return the scientific binomial for a given scientific multi-accidental or halfstep.

    Parameters
    ----------
    note_name : str
        A note name with 1 or more accidentals and a numeral

    Returns
    -------
    str
        A binomial note name enharmonically equivalent to the given note name
        
    Examples
    --------
    >>> decode_scientific_enharmonic('B#4')
    'C5'

    >>> decode_scientific_enharmonic('A######7')
    'D#|Eb8'

    '''

    # A scientific binomial is already the requested note name.
    scientific_chromatic_binomials: list[str] = __scientific_range(__BINOMIALS)
    if note_name in scientific_chromatic_binomials:
        return note_name

    # Reject any note name without a terminal numeral.
    try:
        int(note_name[-1])
    except Exception as ex:
        raise ValueError('Must be a scientific note name in octave 0 to 8') from ex

    # Get some information about the note name.
    alphabetic_name: str = note_name[0] + note_name[-1]
    index: int = scientific_chromatic_binomials.index(alphabetic_name)
    sharps_: int = note_name.count(SHARP_SYMBOL)
    flats_: int = note_name.count(FLAT_SYMBOL)

    # Reject any note that mixes accidentals.
    if sharps_ != 0 and flats_ != 0:
        raise ValueError(note_name)
    
    # Find new index plus or minus the number of accidentals
    adjustment: int = __SHARP_VALUE * sharps_
    if sharps_ == 0:
        adjustment = __FLAT_VALUE * flats_
    index += adjustment

    # Check if index is out of bounds.
    if index < 0 or index > len(scientific_chromatic_binomials) - 1:
        raise IndexError(note_name)
    
    return scientific_chromatic_binomials[index]


def __scientific_range(accidental_notes: list[str]) -> list[str]:
    '''
    Return a full range (C0 - B8) of scientific notation for a given accidental.

    Parameters
    ----------
    accidental_notes : list of str
        A list of 5 strings, one of __BINOMIALS, __SHARPS, __FLATS. This
        defines the type of accidentals that the result will use.

    Returns
    -------
    list of str
        A list of 108 note names in the given accidental style.
    '''
    full_range: list[str] = []
    for octave in range(__NUMBER_OF_OCTAVES):
        new_octave = __scientific_octave(accidental_notes, octave)
        full_range += new_octave
    return full_range


def equal_temperament() -> list[float]:
    '''
    Return a list of frequencies corresponding to the range of the scientific 
    chromatic scales (C0 - B8).

    Returns
    -------
    list of float
        A list of 12 note names, using the given accidental and the naturals.
    '''
    centre_name: str = __CENTRAL_REFERENCE_NOTE_NAME
    centre_freq: int = __CENTRAL_REFERENCE_NOTE_FREQUENCY
    limit: int = __FREQUENCY_DECIMAL_LIMIT
    equiv: int = __OCTAVE_EQUIVALENCE_FACTOR
    frequencies: list[float] = []
    frequency: float
    direction: int
    semitones: int
    
    full_range: list[str] = __scientific_range(__BINOMIALS)
    for note in full_range:
        if full_range.index(note) < full_range.index(centre_name):
            direction = __FLAT_VALUE
            semitones = full_range.index(centre_name) - full_range.index(note)
        else:
            direction = __SHARP_VALUE
            semitones = full_range.index(note) - full_range.index(centre_name)

        # 12 TET : next note = previous note * 2 ** (+ , -) 1/12
        frequency = centre_freq * equiv ** (direction * semitones / __TONES)
        if frequency not in frequencies:
            frequencies.append(round(frequency, limit))

    return frequencies


def encode_frequency(frequency: float, accidental_notes: list[str]) -> str:
    '''
    Return a scientific note name for a given frequency and accidental style.

    Parameters
    ----------
    frequency : float 
        A frequency in 12-TET @ A4 = 440Hz

    accidental_notes : list of str
        A list of 5 strings, one of __BINOMIALS, __SHARPS, __FLATS. This
        defines the type of accidentals that the result will use.

    Returns
    -------
    str
        A note name with 0 to 1 accidentals plus a numeral representing
        the octave.

    Notes
    -----
    This is designed to be used internally, so the given frequency will not
    be recognized if it has been rounded to fewer than 3 decimal places.

    '''
    frequency = round(frequency, __FREQUENCY_DECIMAL_LIMIT)
    frequencies: list[float] = equal_temperament()
    if frequency in frequencies:
        return __scientific_range(accidental_notes)[frequencies.index(frequency)]
    raise ValueError(f'Invalid request {frequency} {accidental_notes}')


def decode_frequency(note_name: str) -> float:
    '''
    Return a frequency for a given scientific note name of any accidental style.

    Parameters
    ----------
    note_name : str
        A note name with 0 to 1 accidentals plus a numeral representing
        the octave.

    Returns
    -------
    float
        A frequency corresponding to the given note name.
    '''
    try:
        note_name = decode_scientific_enharmonic(note_name)
    except Exception as ex:
        raise ValueError(f'Could not contextualize note {note_name}') from ex
    
    return dict(zip(__scientific_range(__BINOMIALS), equal_temperament()))[note_name]
   

def render(interval_structure: int, 
           chromatic_scale: list[str] | None = None
           ) -> list[str]:
    '''
    Return a human-readable list of strings representing the pitch collection
    in the given accidental style.

    Params:
            
    '''
    # TODO: The rendering should involve a little bit more decision resolution:

    # 2) If the range of the interval map exceeds the chromatic scale, we should
    #    automatically switch to scientific rendering mode, so we can distinguish
    #    between the octaves of the multi-octave structure. No more of making the user
    #    check for exact lengths.

    # 3) We should add a function that raises or lowers the range of a whole scientific
    #    rendering, so that if the renderer is forced to use scientific notation starting
    #    from C0, we can easily shift it into the range of C3 (e.g.).

    # MOve rendering logic to separate module

    if chromatic_scale is None:
        chromatic_scale = chromatic()
    if interval_structure.bit_length() > len(chromatic_scale):
        chromatic_scale *= 8

    rendering: list[str] = []
    for interval in range(0, interval_structure.bit_length()):
        binary_column: int = 1 << interval # tonic is least significant bit
        if (interval_structure & binary_column) == binary_column:
            rendering.append(chromatic_scale[interval])
    return rendering


def force_heptatonic(note_name: str, scale_pattern: int) -> list[str]:
    '''
    Force a heptatonic scale pattern to conform to ABCDEFG nomenclature.

    For a given note name and scale pattern, return an alphabetic spelling in
    which each of ABCDEFG (or a variant) appears exactly once. The scale 
    pattern must have exactly 7 flipped bits in this type of nomenclature.

    Parameters
    ----------
    note_name : str 
        A real note name: a natural, sharp, or flat, but not a binomial.
    
    scale_pattern : int
        An integer of no more than 12 bits with exactly 7 flipped bits.

    Returns
    -------
    list of str
        A list of 7 str, representing 1 each of ABCDEFG, plus accidentals.

    Examples
    --------
    >>> force_heptatonic('B#', 0b101010110101)
    B#, C##, D##, E#, F##, G##, A##, B#

    '''
    if note_name in __BINOMIALS:
        raise ValueError(
            'Operation can only be performed on naturals, sharps, or flats.')
    if scale_pattern.bit_count() != __NOTES or scale_pattern.bit_length() > __TONES:
        raise ValueError(
            'Operation can only be performed on heptatonic scales in 12 tone style.')
    
    # Assemble basic alphabetic order to enforce.
    plain: list[str] = shift_list(naturals(), __identity(note_name))

    # Create binomial version of requested scale pattern.
    binomial: list[str] = render(scale_pattern, shift_list(chromatic(), decode_enharmonic(note_name)))

    # Force each binomial note value to adopt the next alphabetic note name.
    return [encode_enharmonic(binomial[i], plain[i]) for i in range(__NOTES)]


def best_heptatonic(note_name: str, scale_pattern: int) -> list[str]:
    '''
    Choose the best set of alphabetic note names for a given heptatonic scale.

    Given a note name and a scale pattern, return the better spelling of the 
    two accidental types (fewest total accidentals). Accepts naturals, sharps, 
    flats, and binomials.

    Parameters
    ----------
    note_name : str 
        Any note name.
    
    scale_pattern : int
        An integer of no more than 12 bits with exactly 7 flipped bits.

    Returns
    -------
    list of str
        A list of 7 str, representing 1 each of ABCDEFG, plus accidentals.

    
    Examples
    --------

    >>> best_heptatonic('A#|Bb', 0b101010110101)
    Bb, C, D, Eb, F, G, Ab
    
    '''
    # Convert sharps and flats to binomials.
    if note_name in __ACCIDENTAL_NOTES or __enharmonic_decoder():
        note_name = decode_enharmonic(note_name)
    elif note_name in __BINOMIALS or __NATURALS:
        pass
    else:
        raise ValueError(f'Unrecognized note name: {note_name}')

    # Naturals' default names will always be the best.
    if note_name in __NATURALS:
        return force_heptatonic(note_name, scale_pattern)

    @dataclass
    class ScaleSynopsis():
        '''A synopsis of the accidentals of a scale.'''
        sharps: int
        flats: int
        scale: list[str]
        mixed: bool

    # Create two versions of the scale
    note_index: int = __BINOMIALS.index(note_name)
    sharp_scale = ScaleSynopsis(0, 0, force_heptatonic(
        __SHARPS[note_index], scale_pattern), False)
    flat_scale = ScaleSynopsis(0, 0, force_heptatonic(
        __FLATS[note_index], scale_pattern), False)
    synopseis = [sharp_scale, flat_scale]

    # Count the accidentals in each version.
    for synopsis in synopseis:
        for note in synopsis.scale:
            synopsis.sharps = note.count('#') + synopsis.sharps
            synopsis.flats = note.count('b') + synopsis.flats
        if synopsis.sharps > 0 and synopsis.flats > 0:
            synopsis.mixed = True
    s_total: int = sharp_scale.sharps + sharp_scale.flats
    f_total: int = flat_scale.sharps + flat_scale.flats

    # Return the scale with the fewest accidentals.
    if s_total > f_total:
        return flat_scale.scale
    if s_total < f_total:
        return sharp_scale.scale

    # With both scales having equal accidentals, return the pure one.
    if s_total == f_total:
        if sharp_scale.mixed is True and flat_scale.mixed is False:
            return flat_scale.scale
        if sharp_scale.mixed is False and flat_scale.mixed is True:
            return sharp_scale.scale

    # Scales are equivalent, arbitrarily default to sharps
    return sharp_scale.scale


def is_abcdefg(note_names: list[str]) -> bool:
    '''
    Check if a given collection of note names adheres to the heptatonic 
    ABCDEFG nomenclature, in which each alphebetic name appears once and
    only once.
    '''
    naturals_: list[str] = naturals()
    approved_names: list[str] = []
    for note in note_names:
        if note in __BINOMIALS:
            raise ValueError(f'Notes must use mononomial form: {note}')
        if __identity(note) in naturals_:
            naturals_.pop(naturals_.index(__identity(note)))
            approved_names.append(note)

    # Check that an enharmonic equivalent is not masking the number of notes
    # in the collection (e.g. A# and Bb should count as 1, not 2).
    enharmonic: set[str] = set(decode_enharmonic(note) for note in approved_names)
    return len(naturals_) == 0 and len(approved_names) == __NOTES and len(enharmonic) == __NOTES


def name_heptatonic_intervals(note_names: list[str]) -> list[str]:
    '''
    For a given heptatonic scale, return the Indian numerals describing
    the pattern's relation to the major scale. 

    Thus:       C D Eb Fb Gbb Ab Bb 
             >> 1 2 b3 b4 bb5 b6 b7

                C D#  E  F  G#  A# B 
             >> 1 #2  3  4  #5  #6 7
    '''
    tonic: str = note_names[0]
    binomial_names = [decode_enharmonic(note_name) for note_name in note_names]
    if len(binomial_names) != __NOTES:
        raise ValueError('Only works on heptatonic scales.')
    chromatic_names: list[str] = shift_list(chromatic(), tonic)
    major_names: list[str] = render(2741, chromatic_names)
    intervals: list[str] = []
    for index in range(__NOTES):
        expected_note: str = major_names[index]
        given_note: str = binomial_names[index]
        difference: int = chromatic_names.index(given_note) - chromatic_names.index(expected_note)
        accidental: str = SHARP_SYMBOL
        if difference < 0:
            accidental = FLAT_SYMBOL
            difference *= __FLAT_VALUE
        intervals.append((accidental * difference) + str(index + 1))
    return intervals


def generate_interval_map(note_names: list[str]) -> int:
    '''
    Return an integer representing a given collection of note names.

    Notes will be parsed into their simplest binomial form. The first 
    note of the given list will serve as the tonic or root of the pitch 
    map, and other notes will be considered sharper intervals from that 
    note name. Unrecognizable note names will be ignored.

    E.g.:   ['C', 'D###4', 'Db', 'Fbbb5', 'Mb', 'G###6', 'F#####9', 'F#|Gb', 'F#|Gb5']
        >> 0b101010101011
    '''
    simplified_notes: list[str] = []
    for note_name in note_names:
        if note_name in __BINOMIALS:
            simplified_notes.append(note_name)
        elif not note_name.isalpha():
            note_name = note_name.removesuffix(note_name[-1])
        else:
            try:
                simplified_notes.append(decode_enharmonic(note_name))
            except ValueError:
                pass
    tonic: str = simplified_notes[0]
    chromatic_: list[str] = chromatic()
    chromatic_ = shift_list(chromatic_, tonic)
    interval_map: int = 0
    for note_name in simplified_notes:
        interval_map |= (1 << chromatic_.index(note_name))
    return interval_map


def naturals() -> list[str]:
    '''Return the 7 natural notes, beginning at C.'''
    return __NATURALS.copy()


def sharps() -> list[str]:
    '''Return the 5 accidental notes as sharps, beginning at C#.'''
    return __SHARPS.copy()


def flats() -> list[str]:
    '''Return the 5 accidental notes as flats, beginning at Db.'''
    return __FLATS.copy()


def binomials() -> list[str]:
    '''Return the 5 accidentals in binomial form, beginning at C#|Db.'''
    return __BINOMIALS.copy()


def chromatic() -> list[str]:
    '''Return a chromatic scale using binomials as accidentals.'''
    return __chromatic(__BINOMIALS).copy()


def ch_flats() -> list[str]:
    '''Return a chromatic scale using flats as accidentals.'''
    return __chromatic(__FLATS).copy()


def ch_sharps() -> list[str]:
    '''Return a chromatic scale using sharps as accidentals.'''
    return __chromatic(__SHARPS).copy()


def scientific() -> dict[str, float]:
    '''Return a scientific chromatic range of notes and frequencies using 
    binomials as accidentals.'''
    return dict(zip(__scientific_range(__BINOMIALS), equal_temperament())).copy()


def sci_flats() -> dict[str, float]:
    '''Return a scientific chromatic range of notes and frequencies using 
    flats as accidentals.'''
    return dict(zip(__scientific_range(__FLATS), equal_temperament())).copy()


def sci_sharps() -> dict[str, float]:
    '''Return a scientific chromatic range of notes and frequencies using 
    sharps as accidentals.'''
    return dict(zip(__scientific_range(__SHARPS), equal_temperament())).copy()


'''
Functions related to generating and processing musical nomenclatural material.

In general, the Aristoxenus library prefers to treat musical phenomena in 
mathematical terms using integers and bitwise operations. We defer assigning
alphabetic nomenclature to the mathematics for as long as possible, since none
of the mechanics of musical structure, transformation, permutation, harmony, 
consonance, dissonance, etc. ever depend on the notes having names.

The names are used as the basis from which to render staff notation, since the
format demands that we refer to notes as sharp or flat in contradistinction to
natural. Although the computer doesn't care about the names of the notes, most
people tend to think of note names rather than mathematic intervallic 
relationships, so the user interface (not yet implemented) will accept and 
display note names for most functions.
'''
import sys
import loguru
from dataclasses import dataclass

from data import (constants,
                  keywords,
                  errors)

from src import (utils,
                 rendering)


# ----------------------------------------------------------
logger = loguru.logger
logger.add(sys.stderr, format="{time} {level} {message}",
           filter="my_module", level="INFO")
logger.add("file_1.log", rotation="10 MB")
#-----------------------------------------------------------


def chromatic(accidental_notes: list[str] | tuple[str, ...]=constants.BINOMIALS) -> list[str]:
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

    Examples
    --------
    >>> chromatic(constants.BINOMIALS)
    ['C', 'C#|Db', 'D', 'D#|Eb', 'E', 'F', 'F#|Gb', 'G', 'G#|Ab', 'A', 'A#|Bb', 'B']
    '''
    new_scale: list[str] = []
    accidentals_in_scale: int = 0
    for note in constants.NATURALS:
        new_scale.append(note)
        if note not in constants.HALFSTEPS:
            new_scale.append(accidental_notes[accidentals_in_scale])
            accidentals_in_scale += 1
    return new_scale


def enharmonic_decoder() -> dict[str, str]:
    '''
    Return a table for decoding the binomial form of a note with any number 
    of sharps or flats.

    Returns
    -------
    dict
        E.g. {'C#': 'C#|Db', ..., 'Ebb': 'D', ..., 'F###': 'G#|Ab', ...}
    '''
    enharmonic_equivalence_decoder: dict[str, str] = {}
    chromatic_binomials: list[str] = chromatic(constants.BINOMIALS)
    for accidental in constants.ACCIDENTAL_SYMBOLS:
        dummy_chromatic_binomials: list[str] = chromatic_binomials.copy()
        shift_degree = constants.SHARP_VALUE

        # Reverse sequence for flats.
        if accidental == constants.FLAT_SYMBOL:
            shift_degree = constants.FLAT_VALUE + constants.TONES
            dummy_chromatic_binomials.reverse()
            dummy_chromatic_binomials = dummy_chromatic_binomials[shift_degree:] + \
                dummy_chromatic_binomials[:shift_degree]
            
        # Create accidentals from the 7 naturals only, but keep
        # track of their 12-tone equivalents in the binomial format.
        for binomial in chromatic_binomials:
            if binomial in constants.BINOMIALS:
                pass
            else:
                for added_accidental in range(constants.TONES):
                    enharmonic_equivalence_decoder.update(
                        {binomial + accidental * added_accidental: dummy_chromatic_binomials[added_accidental]})
            dummy_chromatic_binomials = dummy_chromatic_binomials[shift_degree:] + \
                dummy_chromatic_binomials[:shift_degree]
    return enharmonic_equivalence_decoder


def get_enharmonic_equivalents(note_name: str) -> list[str]:
    '''
    Compile a list of all enharmonic equivalents of a note in sharps or flats.

    Examples
    --------
    >>> get_enharmonic_equivalents('E') 
    ['C####', 'D##', 'E', 'F###########', 'G#########', 'A#######', 'B#####', 'Cbbbbbbbb', 'Dbbbbbbbbbb', 'Fb', 'Gbbb', 'Abbbbb', 'Bbbbbbbb']
    '''
    return [key for key, value in enharmonic_decoder().items() if value == note_name]


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
    return [key for key in enharmonic_decoder() if len(key) <= 2]


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
    if note_name in constants.BINOMIALS:
        raise ValueError('Cannot resolve a binomial note name.')
    return note_name[0]


def __is_homonymous(note_one: str, note_two: str) -> bool:
    '''
    Check whether two notes are variants of the same alphabetic name.

    Parameters
    ----------
    note_one, note_two : str
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
    >>> decode_enharmonic('B#')
    'C'
    >>> decode_enharmonic('A######')
    'D#|Eb'
    '''
    if note_name[-1].isnumeric():
        note_name = note_name[:-1]
    decoder: dict[str, str] = enharmonic_decoder()
    if note_name in chromatic(constants.BINOMIALS):
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
        One of the 7 natural notes.

    Returns
    -------
    str
        A note with between 0 and 6 accidentals. No note name is more than six
        steps from any other name, depending on the direction.

    Notes
    -----
    This function prefers the enharmonic equivalent with the fewest 
    accidentals. When shifting by tritone, the number of accidentals will be 
    equal in both sharps and flats, so we arbitrarily default to sharps.

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
    'Gbbbb'
    >>> encode_enharmonic('Eb' , 'A') 
    'A######'
    '''
    if note_name not in constants.NATURALS:
        raise ValueError('Target note name must be from the naturals.')
    
    note_value = decode_enharmonic(note_value)
    options: list[str] = get_enharmonic_equivalents(note_value)
    homonymous_options: list[str] = [option for option in options if __is_homonymous(option, note_name)]
    return sorted(homonymous_options, key=len)[0]


def scientific_octave(accidental_notes: list[str] | tuple[str, ...]=constants.BINOMIALS, octave: int=0) -> list[str]:
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
    return [note + str(octave) for note in chromatic(accidental_notes)]


def encode_scientific_enharmonic(note_value:str, note_name: str, position: str) -> str:
    '''
    Return a note name that represents the given note name from the perspective of a
    higher or lower note name.

    This function allows you to rephrase a scientific note name as an accidental with
    up to 11 sharps or flats, with the correct scientific numeral.

    Parameters
    ----------
    note_value : str
        The scientific note you want to mask; a sharp, flat, natural, or binomial.
    note_name : str
        A note name from the naturals that will serve as the mask.
    position : str
        A description of whether the target name is to be treated as 
        being the note above the given source name or below.

    Returns
    -------
    str
        A new note name with the same enharmonic value as the given note name, 
        but with the new alphabetic name, a certain number of sharps or flats,
        and the proper numeral for its alphabetic perspective.

    Raises
    ------
    ValueError
        If any of the parameters is incompatible with the function.

    Examples
    --------
    >>> encode_scientific_enharmonic('A4', 'G', 'below')
    'G##4'
    >>> encode_scientific_enharmonic('A4', 'G', 'above')
    'Gbbbbbbbbbb5'
    '''
    i = equal_temperament().index(convert_note_to_frequency(note_value))
    octave: list[str] = []
    symbol: str = ''

    match position:
        case keywords.BELOW:
            octave = scientific_range()[i-11 : i+1]
            octave.reverse()
            symbol = constants.SHARP_SYMBOL

        case keywords.ABOVE:
            octave = scientific_range()[i : i+12]
            symbol = constants.FLAT_SYMBOL

        case _:
            raise ValueError(position)
            
    for i, note in enumerate(octave):
        if note[:-1] == note_name:
            return note[:-1] + (symbol * i) + note[-1]
    
    raise ValueError(note_name)


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
    scientific_chromatic_binomials: list[str] = scientific_range(constants.BINOMIALS)
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
    sharps_: int = note_name.count(constants.SHARP_SYMBOL)
    flats_: int = note_name.count(constants.FLAT_SYMBOL)

    # Reject any note that mixes accidentals.
    if sharps_ != 0 and flats_ != 0:
        raise ValueError(note_name)
    
    # Find new index plus or minus the number of accidentals
    adjustment: int = constants.SHARP_VALUE * sharps_
    if sharps_ == 0:
        adjustment = constants.FLAT_VALUE * flats_
    index += adjustment

    # Check if index is out of bounds.
    if index < 0 or index > len(scientific_chromatic_binomials) - 1:
        raise IndexError(note_name)
    
    return scientific_chromatic_binomials[index]


def scientific_range(accidental_notes: list[str] | tuple[str, ...]=constants.BINOMIALS) -> list[str]:
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
    for octave in range(constants.NUMBER_OF_OCTAVES):
        new_octave = scientific_octave(accidental_notes, octave)
        full_range += new_octave
    return full_range


def equal_temperament() -> list[float]:
    '''
    Return a list of frequencies corresponding to the range of the scientific 
    chromatic scales (C0 - B8).

    Returns
    -------
    list of float
        A list of 108 frequencies, rounded to three decimal places.
    '''

    # NOTE: equal_temperament should be part of a module called
    # temperament, then change the frequency conversions to
    # take a temperament function as an argument, which then
    # generates the necessary range.
    centre_name: str = constants.CENTRAL_REFERENCE_NOTE_NAME
    centre_freq: int = constants.CENTRAL_REFERENCE_NOTE_FREQUENCY
    limit: int = constants.FREQUENCY_DECIMAL_LIMIT
    equiv: int = constants.OCTAVE_EQUIVALENCE_FACTOR
    frequencies: list[float] = []
    frequency: float
    direction: int
    semitones: int
    
    full_range: list[str] = scientific_range(constants.BINOMIALS)
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

    return frequencies


def convert_frequency_to_note(frequency: float, 
                             accidental_notes: list[str] | tuple[str, ...]=constants.BINOMIALS
                             ) -> str:
    '''
    Return a scientific note name for a given frequency and accidental style.

    Parameters
    ----------
    frequency : float 
        A frequency in 12-TET @ A4 = 440Hz

    accidental_notes : list of str
        A list of 5 strings, one of __BINOMIALS, __SHARPS, __FLATS. This
        defines the type of accidentals that the result will use, if it 
        is not a natural note.

    Returns
    -------
    str
        A note name with 0 to 1 accidentals plus a numeral representing
        the octave. 

    Notes
    -----
    If the frequency is not among the ones generated by the program,
    the function attempts to round the frequency to different decimal
    places to see if the given frequency might be close.

    Examples 
    --------
    >>> convert_frequency_to_note(440.0, constants.BINOMIALS)
    'A4'
    >>> convert_frequency_to_note(138.591, constants.SHARPS)
    'C#3'
    >>> convert_frequency_to_note(138.59, constants.SHARPS)
    'C#3'
    >>> convert_frequency_to_note(138.6, constants.SHARPS)
    'C#3'
    '''
    frequency = round(frequency, constants.FREQUENCY_DECIMAL_LIMIT)
    frequencies: list[float] = list(equal_temperament())
    for num in [2, 1, 0]:
        if frequency in frequencies:
            return scientific_range(accidental_notes)[frequencies.index(frequency)]
        frequencies = [round(x, num) for x in frequencies]

    raise ValueError(frequency)


def convert_note_to_frequency(note_name: str) -> float:
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

    Examples
    --------
    >>> convert_note_to_frequency('A4')
    440.0
    >>> convert_note_to_frequency('Db3')
    138.591
    '''
    try:
        note_name = decode_scientific_enharmonic(note_name)
    except Exception as ex:
        raise ValueError(note_name) from ex
    
    return dict(zip(scientific_range(constants.BINOMIALS), equal_temperament()))[note_name]
   

def force_heptatonic(note_name: str, interval_structure: int) -> list[str]:
    '''
    Force a heptatonic scale pattern to conform to ABCDEFG nomenclature.

    For a given note name and scale pattern, return an alphabetic spelling in
    which each of ABCDEFG (or a variant) appears exactly once. The scale 
    pattern must have exactly 7 flipped bits in this type of nomenclature.

    Parameters
    ----------
    note_name : str 
        A real note name: a natural, sharp, or flat, but not a binomial.
    
    interval_structure : int
        An integer of no more than 12 bits with exactly 7 flipped bits.

    Returns
    -------
    list of str
        A list of 7 str, representing 1 each of ABCDEFG, plus accidentals.

    Examples
    --------
    >>> force_heptatonic('B#', 0b101010110101)
    ['B#', 'C##', 'D##', 'E#', 'F##', 'G##', 'A##']

    '''
    if note_name in constants.BINOMIALS:
        raise ValueError(
            'Operation can only be performed on naturals, sharps, or flats.')
    if interval_structure.bit_count() != constants.NOTES or interval_structure.bit_length() > constants.TONES:
        raise ValueError(
            'Operation can only be performed on heptatonic scales in 12 tone style.')
    # Assemble basic alphabetic order to enforce.
    plain: list[str] = utils.shift_list(constants.NATURALS, __identity(note_name))
    # Create binomial version of requested scale pattern.
    binomial: list[str] = rendering.render_plain(interval_structure, utils.shift_list(chromatic(constants.BINOMIALS), decode_enharmonic(note_name)))
    # Force each binomial note value to adopt the next alphabetic note name.
    return [encode_enharmonic(binomial[i], plain[i]) for i in range(constants.NOTES)]


def best_heptatonic(note_name: str, interval_structure: int) -> list[str]:
    '''
    Choose the best set of alphabetic note names for a given heptatonic scale.

    Given a note name and a scale pattern, return the better spelling of the 
    two accidental types (fewest total accidentals). Accepts naturals, sharps, 
    flats, and binomials.

    Parameters
    ----------
    note_name : str 
        Any note name.
    
    interval_structure : int
        An integer of no more than 12 bits with exactly 7 flipped bits.

    Returns
    -------
    list of str
        A list of 7 str, representing 1 each of ABCDEFG, plus accidentals.

    
    Examples
    --------

    >>> best_heptatonic('A#|Bb', 0b101010110101)
    ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
    >>> best_heptatonic('E#', 0b101010110101)
    ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']
    '''
    # Convert sharps and flats to binomials.
    note_name = decode_enharmonic(note_name)

    # Naturals' default names will always be the best.
    if note_name in constants.NATURALS:
        return force_heptatonic(note_name, interval_structure)

    @dataclass
    class ScaleSynopsis():
        '''A synopsis of the accidentals of a scale.'''
        sharps: int
        flats: int
        scale: list[str]
        mixed: bool

    note_index: int = constants.BINOMIALS.index(note_name)
    sharp_scale = ScaleSynopsis(0, 0, force_heptatonic(constants.SHARPS[note_index], interval_structure), False)
    flat_scale = ScaleSynopsis(0, 0, force_heptatonic(constants.FLATS[note_index], interval_structure), False)

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

    Parameters
    ----------
    note_names : list[str]
        A list of alphabetic note names from the naturals, sharps, or flats.

    Returns
    -------
    bool
        True, if each of ABCDEFG appears exactly once.

    Raises
    ------
    NoteNameError
        Raised if a binomial is passed.

    Examples
    --------
    >>> is_abcdefg(['C', 'Db', 'E#', 'F#', 'G', 'A', 'B'])
    True
    >>> is_abcdefg(['C', 'Db', 'E#', 'F', 'G', 'A', 'B'])
    False
    '''
    naturals_: list[str] = list(constants.NATURALS)
    approved_names: set[str] = set()
    for note in note_names:
        if note in constants.BINOMIALS:
            raise errors.NoteNameError(note)
        
        if __identity(note) in naturals_:
            naturals_.pop(naturals_.index(__identity(note)))
            approved_names.add(decode_enharmonic(note))

    return len(naturals_) == 0 and len(approved_names) == constants.NOTES


def decode_numeric_keyword(term: str) -> int:
    '''
    Auxiliary function that converts certain terms into the numbers they 
    represent.

    Parameters
    ----------
    term : str
        One of a limited number of structural terms

    Returns
    -------
    int
        The corresponding numerical meaning of the term.

    Examples
    --------
    >>> decode_numeric_keyword('tertial')
    3
    >>> decode_numeric_keyword('pentad')
    5
    '''
    # 0 = polyad, 1 = tonal, 2 = basal
    # but we will expand this later... so let's not 
    for number, tuple_ in enumerate(keywords.NUMERATION):
        if term in tuple_:
            return number + 1
    raise errors.UnknownKeywordError(term)


def encode_numeric_keyword(number: int, keyword_type: str) -> str|None:
    '''
    Return a keyword for a given numeral and keyword type.

    Parameters
    ----------
    number : int
        The number that will be encoded into a keyword.
    keyword_type : str {'polyad', 'tonal', 'basal'}
        The type of number word being requested

    Returns
    -------
    str
        A numeric keyword representing the given number and keyword type.

    Examples
    --------
    >>> encode_numeric_keyword(3, 'polyad')
    'triad'
    >>> encode_numeric_keyword(3, 'basal')
    'tertial'
    >>> encode_numeric_keyword(5, 'tonal')
    'pentatonic'
    '''
    number = number - 1
    for type_index, label in enumerate(keywords.NUMERATION_INDICES):
        if label == keyword_type:
            return keywords.NUMERATION[number][type_index]


def is_scientific(note_name: str) -> bool:
    '''
    Return true if the given note name uses scientific notation.

    Parameters
    ----------
    note_name : str
        A note name you want to test.

    Returns
    -------
    bool
        True, if the note name ends with a scientific numeral.

    Examples
    --------
    >>> is_scientific('C##')
    False
    >>> is_scientific('D##4')
    True
    '''
    return note_name[-1].isnumeric()


def get_accidentals(note_name: str
                    ) -> tuple[str, ...]:
    '''
    Tries to identify which accidental group the given note name belongs to.

    Parameters
    ----------
    note_name : str
        A note name you want to test

    Returns
    -------
    tuple[str, ...]
        The accidentals for this type, or binomials, if it is a natural note.
    '''

    if constants.BINOMIAL_DIVIDER_SYMBOL in note_name:
        return constants.BINOMIALS
    elif constants.SHARP_SYMBOL in note_name:
        return constants.SHARPS
    elif constants.FLAT_SYMBOL in note_name:
        return constants.FLATS
    else:
        return constants.BINOMIALS

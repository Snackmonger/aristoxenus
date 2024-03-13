# pylint:disable=trailing-whitespace, trailing-newlines
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

from typing import Callable, Optional, Sequence

from data import (constants,
                  keywords,
                  errors,
                  chord_symbols,
                  intervallic_canon)

from src import (bitwise,
                 utils,
                 rendering,
                 temperament)

__all__ = ["chromatic",
           "enharmonic_decoder",
           "get_enharmonic_equivalents",
           "decode_enharmonic",
           "encode_enharmonic",
           "scientific_octave",
           "encode_scientific_enharmonic",
           "decode_scientific_enharmonic",
           "scientific_range",
           "convert_frequency_to_note",
           "convert_note_to_frequency",
           "force_heptatonic",
           "best_heptatonic",
           "is_abcdefg",
           "decode_numeric_keyword",
           "encode_numeric_keyword",
           "is_scientific",
           "get_accidentals",
           "name_heptatonic_intervals",
           "twelve_tone_scale_intervals",
           "twelve_tone_scale_names",
           "interval_identity",
           "get_interval_map"]


def chromatic(accidental_notes: list[str] | tuple[str, ...] = constants.BINOMIALS) -> list[str]:
    '''
    Return a chromatic octave using the given accidentals.

    Examples
    --------
    >>> chromatic(constants.BINOMIALS)
    ['C', 'C#|Db', 'D', 'D#|Eb', 'E', 'F', 'F#|Gb', 'G', 'G#|Ab', 'A', 'A#|Bb', 'B']
    >>> chromatic(constants.SHARPS)
    ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    >>> chromatic(constants.FLATS)
    ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
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


def __identity(note_name: str) -> str:
    '''
    Return the alphabetic name of an accidental note.

    Examples
    --------
    >>> __identity('B###') 
    'B'
    '''
    if note_name in constants.BINOMIALS:
        raise errors.NoteNameError('Cannot resolve a binomial note name.')
    return note_name[0]


def __is_homonymous(note_one: str, note_two: str) -> bool:
    '''
    Check whether two notes are variants of the same alphabetic name.

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
        raise errors.NoteNameError(f'Note name {note_name} not recognized.')
    return decoder[note_name]


def encode_enharmonic(note_value: str, note_name: str) -> str:
    '''
    Return a note with the same enharmonic value as the given note,
    but under the given alphabetic name.

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
        raise errors.NoteNameError(
            'Target note name must be from the naturals.')

    note_value = decode_enharmonic(note_value)
    options: list[str] = get_enharmonic_equivalents(note_value)
    homonymous_options: list[str] = [
        option for option in options if __is_homonymous(option, note_name)]
    return sorted(homonymous_options, key=len)[0]


def scientific_octave(accidental_notes: list[str] | tuple[str, ...] = constants.BINOMIALS,
                      octave: int = 0
                      ) -> list[str]:
    '''
    Return a scientific chromatic scale in the given style and octave.        
    '''
    return [note + str(octave) for note in chromatic(accidental_notes)]


def encode_scientific_enharmonic(note_value: str,
                                 note_name: str,
                                 position: str
                                 ) -> str:
    '''
    Return a note name that represents the given note name from the perspective of a
    higher or lower note name.

    This function allows you to rephrase a scientific note name as an accidental with
    up to 11 sharps or flats, with the correct scientific numeral.

    Examples
    --------
    >>> encode_scientific_enharmonic('A4', 'G', 'below')
    'G##4'
    >>> encode_scientific_enharmonic('A4', 'G', 'above')
    'Gbbbbbbbbbb5'
    '''
    if note_value in scientific_range(constants.SHARPS):
        a = constants.SHARPS
    elif note_value in scientific_range(constants.FLATS):
        a = constants.FLATS
    else:
        raise errors.NoteNameError(note_value)

    i = scientific_range(a).index(note_value)
    octave: list[str] = []
    symbol: str = ''

    match position:
        case keywords.BELOW:
            octave = scientific_range()[i-11: i+1]
            octave.reverse()
            symbol = constants.SHARP_SYMBOL

        case keywords.ABOVE:
            octave = scientific_range()[i: i+12]
            symbol = constants.FLAT_SYMBOL

        case _:
            raise errors.UnknownKeywordError(position)

    for i, note in enumerate(octave):
        if note[:-1] == note_name:
            return note[:-1] + (symbol * i) + note[-1]

    raise errors.NoteNameError(note_name)


def decode_scientific_enharmonic(note_name: str) -> str:
    '''
    Return the scientific binomial for a given scientific multi-accidental or halfstep.

    Examples
    --------
    >>> decode_scientific_enharmonic('B#4')
    'C5'
    >>> decode_scientific_enharmonic('A######7')
    'D#|Eb8'
    '''
    # A scientific binomial is already the requested note name.
    scientific_chromatic_binomials: list[str] = scientific_range(
        constants.BINOMIALS)
    if note_name in scientific_chromatic_binomials:
        return note_name

    # Reject any note name without a terminal numeral.
    try:
        int(note_name[-1])
    except Exception as ex:
        raise errors.NoteNameError(
            'Must be a scientific note name in octave 0 to 8') from ex

    # Get some information about the note name.
    alphabetic_name: str = note_name[0] + note_name[-1]
    index: int = scientific_chromatic_binomials.index(alphabetic_name)
    sharps_: int = note_name.count(constants.SHARP_SYMBOL)
    flats_: int = note_name.count(constants.FLAT_SYMBOL)

    # Reject any note that mixes accidentals.
    if sharps_ != 0 and flats_ != 0:
        raise errors.NoteNameError(note_name)

    # Find new index plus or minus the number of accidentals
    adjustment: int = constants.SHARP_VALUE * sharps_
    if sharps_ == 0:
        adjustment = constants.FLAT_VALUE * flats_
    index += adjustment

    # Check if index is out of bounds.
    if index < 0 or index > len(scientific_chromatic_binomials) - 1:
        raise errors.AristoxenusIndexError(note_name)

    return scientific_chromatic_binomials[index]


def scientific_range(accidental_notes: list[str] | tuple[str, ...] = constants.BINOMIALS) -> list[str]:
    '''
    Return a full range (C0 - B8) of scientific notation for a given accidental.
    '''
    full_range: list[str] = []
    for octave in range(constants.NUMBER_OF_OCTAVES):
        new_octave = scientific_octave(accidental_notes, octave)
        full_range += new_octave
    return full_range


def convert_frequency_to_note(frequency: float,
                              accidental_notes: list[str] | tuple[str, ...] = constants.BINOMIALS,
                              temperament_: Callable[..., tuple[float, ...]
                                                     ] = temperament.equal_temperament
                              ) -> str:
    '''
    Return a scientific note name for a given frequency and accidental style.

    Notes
    -----
    If the frequency is not among the ones generated by the program,
    the function attempts to round the frequency to different decimal
    places to see if the given frequency might be close. Python's rounding
    sometimes means values are missed.

    Examples 
    --------
    >>> convert_frequency_to_note(440.0)
    'A4'
    >>> convert_frequency_to_note(138.591, constants.SHARPS)
    'C#3'
    >>> convert_frequency_to_note(138.59, constants.SHARPS)
    'C#3'
    >>> convert_frequency_to_note(138.6, constants.SHARPS)
    'C#3'
    '''
    frequency = round(frequency, constants.FREQUENCY_DECIMAL_LIMIT)
    frequencies: list[float] = list(temperament_())
    for num in [2, 1, 0]:
        if frequency in frequencies:
            return scientific_range(accidental_notes)[frequencies.index(frequency)]
        frequencies = [round(x, num) for x in frequencies]

    raise errors.AristoxenusValueError(frequency)


def convert_note_to_frequency(note_name: str,
                              temperament_: Callable[..., tuple[float, ...]
                                                     ] = temperament.equal_temperament
                              ) -> float:
    '''
    Return a frequency for a given scientific note name of any accidental style.

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
        raise errors.NoteNameError(note_name) from ex

    return dict(zip(scientific_range(constants.BINOMIALS), temperament_()))[note_name]


def force_heptatonic(note_name: str, interval_structure: int) -> list[str]:
    '''
    Force a heptatonic scale pattern to conform to ABCDEFG nomenclature.

    Parameters
    ----------
    note_name           Any note name
    interval_structure  An integer of no more than 12 bits, of which 
                        exactly 7 are flipped.

    Examples
    --------
    >>> force_heptatonic('B#', 0b101010110101)
    ['B#', 'C##', 'D##', 'E#', 'F##', 'G##', 'A##']

    '''
    if note_name in constants.BINOMIALS:
        raise errors.NoteNameError(
            'Operation can only be performed on naturals, sharps, or flats.')
    if interval_structure.bit_count() != constants.NOTES or interval_structure.bit_length() > constants.TONES:
        raise errors.IntervalStructureError(
            'Operation can only be performed on heptatonic scales in 12 tone style.')
    # Assemble basic alphabetic order to enforce.
    plain: list[str] = utils.shift_list(
        constants.NATURALS, __identity(note_name))
    # Create binomial version of requested scale pattern.
    binomial: list[str] = rendering.render_plain(interval_structure, utils.shift_list(
        chromatic(constants.BINOMIALS), decode_enharmonic(note_name)))
    # Force each binomial note value to adopt the next alphabetic note name.
    return [encode_enharmonic(binomial[i], plain[i]) for i in range(constants.NOTES)]


def best_heptatonic(note_name: str, interval_structure: Optional[int] = intervallic_canon.DIATONIC_SCALE) -> list[str]:
    '''
    Choose the best set of alphabetic note names for a given heptatonic scale.

    Parameters
    ----------
    note_name           Any note name
    interval_structure  An integer of no more than 12 bits, of which 
                        exactly 7 are flipped.

    Examples
    --------
    >>> best_heptatonic('A#|Bb', 0b101010110101)
    ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
    >>> best_heptatonic('D#|Eb', 0b101010110101)
    ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D']
    >>> best_heptatonic('E#', 0b101010110101)
    ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']
    '''
    # Convert sharps and flats to binomials.
    note_name = decode_enharmonic(note_name)

    # Naturals' default names will always be the best.
    if note_name in constants.NATURALS:
        return force_heptatonic(note_name, interval_structure)

    note_index: int = constants.BINOMIALS.index(note_name)
    sharps_scale = force_heptatonic(
        constants.SHARPS[note_index], interval_structure)
    flats_scale = force_heptatonic(
        constants.FLATS[note_index], interval_structure)

    # The best name can be decided by fewest total accidentals
    f_count = count_accidentals(flats_scale)
    s_count = count_accidentals(sharps_scale)
    s_total = s_count["#"] + s_count["b"]
    f_total = f_count["#"] + f_count["b"]
    if s_total > f_total:
        return flats_scale
    if f_total > s_total:
        return sharps_scale

    # If accidentals are equal, the best name is the one that does not mix
    smix = s_count["#"] > 0 and s_count["b"] > 0
    fmix = f_count["#"] > 0 and f_count["b"] > 0
    if f_total == s_total:
        if smix and not fmix:
            return flats_scale
        if fmix and not smix:
            return sharps_scale

    # By this point, we know that the scales have equal number accidentals,
    # and both/neither are mixed. Resolve by arbitrarily defaulting to sharps.
    return sharps_scale


def is_abcdefg(note_names: list[str]) -> bool:
    '''
    Check if a given collection of note names adheres to the heptatonic 
    ABCDEFG nomenclature, in which each alphebetic name appears once and
    only once.

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

    Examples
    --------
    >>> decode_numeric_keyword('triad')
    3
    >>> decode_numeric_keyword('tertial')
    2

    The basal numbers are used to encode steps 
    in list slices, so tertial => 2.

    >>> decode_numeric_keyword('pentad')
    5
    '''
    # 0 = polyad, 1 = tonal, 2 = basal
    # but we will expand this later... so let's not
    j: int = keywords.NUMERATION_INDICES.index(keywords.BASAL)
    basal_words: list[str] = [
        x for k in keywords.NUMERATION for x in k if x and k.index(x) == j]
    for i, terms in enumerate(keywords.NUMERATION):
        if term in terms:
            if term in basal_words:
                return i
            return i + 1
    raise errors.UnknownKeywordError(term)


def encode_numeric_keyword(number: int, keyword_type: str) -> str:
    '''
    Return a keyword for a given numeral and keyword type.

    Examples
    --------
    >>> encode_numeric_keyword(3, 'polyad')
    'triad'
    >>> encode_numeric_keyword(2, 'basal')
    'tertial'
    >>> encode_numeric_keyword(5, 'tonal')
    'pentatonic'
    '''
    number = number - 1 if not keyword_type == "basal" else number
    for type_index, label in enumerate(keywords.NUMERATION_INDICES):
        if label == keyword_type:
            return str(keywords.NUMERATION[number][type_index])
    raise errors.UnknownKeywordError(keyword_type)


def is_scientific(note_name: str) -> bool:
    '''
    Return true if the given note name uses scientific notation.

    Examples
    --------
    >>> is_scientific('C##')
    False
    >>> is_scientific('D##4')
    True
    '''
    return note_name[-1].isnumeric()


def get_accidentals(note_name: str) -> tuple[str, ...]:
    '''Return the accidental group to which the given note name belongs.

    Examples
    --------
    >>> get_accidentals("C#")
    ('C#', 'D#', 'F#', 'G#', 'A#')
    '''
    if constants.BINOMIAL_DIVIDER_SYMBOL in note_name:
        return constants.BINOMIALS
    if constants.SHARP_SYMBOL in note_name:
        return constants.SHARPS
    if constants.FLAT_SYMBOL in note_name:
        return constants.FLATS
    return constants.BINOMIALS


def get_accidental_keyword(note_name: str) -> str:
    """Return the keyword representing the accidental group to which the given
    note name belongs.

    Examples
    --------
    >>> get_accidental_keyword("C#")
    'sharp'
    """
    if constants.BINOMIAL_DIVIDER_SYMBOL in note_name:
        return keywords.BINOMIAL
    if constants.SHARP_SYMBOL in note_name:
        return keywords.SHARP
    if constants.FLAT_SYMBOL in note_name:
        return keywords.FLAT
    return keywords.BINOMIAL


def name_heptatonic_intervals(scale_data: Sequence[str] | int) -> list[str]:
    '''For a given collection of note names, return the Indian numerals describing
    the pattern's relation to the diatonic scale.

    Parameters
    ----------
    scale_data : list[str] | int
        A list of exactly 7 note names, from the naturals, sharps, flats, or
        binomials; OR an integer representing an interval structure not 
        exceeding 12 bits, of which 7 are flipped.

    Returns
    -------
    list[str]
        A list of numbers modified by the sharp or flat symbol according to
        their relationship to the given scale. 

    Examples
    --------
    >>> name_heptatonic_intervals(['C', 'D', 'Eb', 'Fb', 'Gbb', 'Ab', 'Bb']) 
    ['1', '2', 'b3', 'b4', 'bb5', 'b6', 'b7']
    >>> name_heptatonic_intervals(['C', 'D#', 'E', 'F', 'G#', 'A#', 'B']) 
    ['1', '#2', '3', '4', '#5', '#6', '7']
    '''
    if isinstance(scale_data, int):
        scale_data = rendering.render_plain(scale_data)

    tonic: str = decode_enharmonic(scale_data[0])
    binomial_names: list[str] = [decode_enharmonic(x) for x in scale_data]
    if len(binomial_names) != constants.NOTES:
        raise errors.HeptatonicScaleError('Only works on heptatonic scales.')

    chromatic_names: list[str] = utils.shift_list(
        chromatic(constants.BINOMIALS), tonic)
    major_names: list[str] = rendering.render_plain(
        intervallic_canon.DIATONIC_SCALE, chromatic_names)
    intervals_: list[str] = []

    # Add one accidental for every step of difference between
    # the actual binomial name and the major binomial name.
    for index in range(constants.NOTES):
        expected_note: int = chromatic_names.index(major_names[index])
        given_note: int = chromatic_names.index(binomial_names[index])
        difference: int = given_note - expected_note
        accidental: str = constants.SHARP_SYMBOL
        if difference < 0:
            accidental = constants.FLAT_SYMBOL
            difference *= constants.FLAT_VALUE

        intervals_.append((accidental * difference) + str(index + 1))

    return intervals_


def twelve_tone_scale_intervals(scale: int) -> list[str]:
    """Return a list that consists of the 7 correctly-spelled intervals of any
    heptatonic scale, plus 5 more intervals that fill in the chromatic notes.

    Examples
    --------
    >>> from data.intervallic_canon import HEMIOLIC_SCALE, DIATONIC_SCALE
    >>> print(twelve_tone_scale_intervals(DIATONIC_SCALE))
    ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', '#5', '6', 'b7', '7']
    >>> print(twelve_tone_scale_intervals(HEMIOLIC_SCALE))
    ['1', 'b2', '2', '#2', '3', '4', 'b5', '5', '#5', '6', 'b7', '7']
    """
    if not bitwise.validate_interval_structure(scale, 12, 7):
        raise errors.HeptatonicScaleError(
            "Function requires a heptatonic scale.")

    ch: list[str] = utils.shift_list(chromatic(), "C")
    note_names: list[str] = rendering.render_plain(scale, ch)
    rendering_: list[str] = name_heptatonic_intervals(scale)
    intervals: list[str] = []
    for i, n in enumerate(ch):
        if n in note_names:
            j = note_names.index(n)
            intervals.append(rendering_[j])
        else:
            intervals.append(
                list(chord_symbols.interval_symbol_prescription.values())[i])

    return intervals


def twelve_tone_scale_names(note_names: Sequence[str]) -> list[str]:
    """Return a list that contains the given 7 note names, plus
    5 more note names that supply the missing chromatic notes.

    This function is designed to ensure that heptatonic scales that mix sharps
    and flats, or which begin with an enharmonic halfstep (e.g. Cb), are still
    able to be contextualized within chromatic scales.
    """
    if not len({decode_enharmonic(x) for x in note_names}) == 7:
        raise errors.HeptatonicScaleError(
            "Function requires a heptatonic scale.")

    if any([x in constants.BINOMIALS for x in note_names]):
        raise errors.NoteNameError(
            "Function cannot process binomial note names.")

    scale: list[str] = list(note_names)
    chromatic_: list[str] = ["" for _ in range(12)]
    enharmonic_keynote: str = decode_enharmonic(scale[0])
    binomial_scale_names: list[str] = [decode_enharmonic(x) for x in scale]
    accidental_signature: dict[str, int] = count_accidentals(scale)
    binomial_chromatic: list[str] = utils.shift_list(
        chromatic(), enharmonic_keynote)
    accidentals: tuple[str, ...] = constants.SHARPS
    if accidental_signature[constants.SHARP_SYMBOL] < accidental_signature[constants.FLAT_SYMBOL]:
        accidentals = constants.FLATS

    for i, note in enumerate(binomial_chromatic):
        if note in binomial_scale_names:
            chromatic_[i] = scale[binomial_scale_names.index(note)]
        elif note in constants.BINOMIALS:
            chromatic_[i] = accidentals[constants.BINOMIALS.index(note)]
        elif note in constants.NATURALS:
            chromatic_[i] = note

    return chromatic_


def count_accidentals(note_names: Sequence[str]) -> dict[str, int]:
    """Return the total number of accidentals of each type in a given list of
    note names.
    """
    if any(x in constants.BINOMIALS for x in note_names):
        raise errors.NoteNameError(
            "Function cannot process binomial note names.")
    sharps: int = 0
    flats: int = 0
    for note in note_names:
        sharps += note.count(constants.SHARP_SYMBOL)
        flats += note.count(constants.FLAT_SYMBOL)
    return {constants.SHARP_SYMBOL: sharps, constants.FLAT_SYMBOL: flats}


def interval_identity(item: str) -> int:
    """Return the numeric part of a numerical interval symbol.

    Examples
    --------
    >>> interval_identity("bbb7")
    7
    >>> interval_identity("#4")
    4
    """
    return int(item[-1])


def get_interval_map(tonal_centre: str,
                     scale: int = intervallic_canon.DIATONIC_SCALE,
                     binomial: bool = False
                     ) -> dict[str, str]:
    """A dictionary containing a mapping of 12 unique note names to 12 unique
    interval names, following the logic of ``twelve_tone_scale_intervals``.

    The names will be based on the premise that the tonal centre will be
    used to force a heptatonic scale, and the missing 5 notes will be drawn
    from the chromatic notes of that centre's accidental type. If the tonal 
    centre is a binomial, it will resolve into the best names. If the binomial
    flag is set to True, then the note names will simply be the binomials.
    """
    if tonal_centre not in constants.LEGAL_ROOT_NAMES:
        tonal_centre = decode_enharmonic(tonal_centre)

    accidentals = get_accidentals(tonal_centre)
    if tonal_centre in constants.BINOMIALS:
        real_names = best_heptatonic(tonal_centre, scale)
    else:
        real_names = force_heptatonic(tonal_centre, scale)

    interval_symbols: Sequence[str] = list(twelve_tone_scale_intervals(scale))
    mapping = dict(zip(utils.shift_list(
        chromatic(), decode_enharmonic(tonal_centre)), interval_symbols))

    if not binomial:
        if accidentals == constants.BINOMIALS:
            accidentals = constants.SHARPS
        for note_name in real_names:
            if (n := decode_enharmonic(note_name)) in mapping:
                v = mapping.pop(n)
                mapping[note_name] = v

        for note_name in constants.BINOMIALS:
            if note_name in mapping:
                i = constants.BINOMIALS.index(note_name)
                note_name_ = accidentals[i]
                v = mapping.pop(note_name)
                mapping[note_name_] = v

    return mapping

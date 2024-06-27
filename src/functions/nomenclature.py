# pylint:disable=trailing-whitespace, trailing-newlines, line-too-long, too-many-return-statements
'''
Functions related to generating and processing musical nomenclatural material.

Aristoxenus generates all nomenclatural material used in the program except for
a small number of constants. This module was created out of a desire to avoid 
having to type out tables of note name conversions manually, and it also helps 
to ensure that the program is able to characterize note and interval names for 
unusual scales in the most efficient way. Mostly, the user should not need to 
use any of the functions in this module directly.
'''
import re
from typing import Optional, Sequence
from src.data import (
    constants,
    keywords,
    errors,
    chord_symbols,
    intervallic_canon
)
from src.functions import (
    bitwise,
    utils,
    rendering,
    temperament
)
__all__ = [
    "generate_chromatic_octave",
    "get_enharmonic_decoder",
    "get_enharmonic_equivalents",
    "get_note_identity",
    "notes_are_homonymous",
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
    "is_scientific",
    "get_accidentals",
    "name_heptatonic_intervals",
    "twelve_tone_scale_intervals",
    "twelve_tone_scale_names",
    "interval_identity",
    "get_interval_map"
]


def generate_chromatic_octave(accidental_notes: Sequence[str] = constants.BINOMIALS) -> tuple[str, ...]:
    """
    Generate and return a chromatic octave using the given accidentals.

    :param accidental_notes: A set of five note names to use as the accidental
        notes (i.e. black keys), defaults to constants.BINOMIALS.
    :return: A tuple of twelve note names, consisting of the seven natural notes
        defined in constants.NATURALS and the five given accidentals.
    
    :Example:
    >>> from src.data import constants
    >>> generate_chromatic_octave(constants.BINOMIALS)
    ('C', 'C#|Db', 'D', 'D#|Eb', 'E', 'F', 'F#|Gb', 'G', 'G#|Ab', 'A', 'A#|Bb', 'B')
    >>> generate_chromatic_octave(constants.SHARPS)
    ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
    >>> generate_chromatic_octave(constants.FLATS)
    ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')
    """
    new_scale: list[str] = []
    accidentals_in_scale: int = 0
    for note in constants.NATURALS:
        new_scale.append(note)
        if note not in constants.HALFSTEPS:
            new_scale.append(accidental_notes[accidentals_in_scale])
            accidentals_in_scale += 1
    return tuple(new_scale)


def get_enharmonic_decoder() -> dict[str, str]:
    """
    Return a table for decoding the binomial form of a note with any number 
    of sharps or flats.

    :return: A dictionary mapping all unique note names (with any number of
        accidentals) to their binomial equivalents.
        E.g. {'C#': 'C#|Db', ..., 'Ebb': 'D', ..., 'F###': 'G#|Ab', ...}
    """
    enharmonic_equivalence_decoder: dict[str, str] = {}
    chromatic_binomials: tuple[str, ...] = generate_chromatic_octave(
        constants.BINOMIALS)
    for accidental in constants.ACCIDENTAL_SYMBOLS:
        dummy_chromatic_binomials: list[str] = list(chromatic_binomials)
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


def get_enharmonic_equivalents(note_name: str) -> tuple[str, ...]:
    """
    Return a list of all enharmonic equivalents of a given note name.

    :param note_name: A note name with any number of accidentals.
    :return: A tuple of note names with the same enharmonic value as the given
        note name.

    :Example:
    >>> get_enharmonic_equivalents('E') 
    ('C####', 'D##', 'E', 'F###########', 'G#########', 'A#######', 'B#####', 'Cbbbbbbbb', 'Dbbbbbbbbbb', 'Fb', 'Gbbb', 'Abbbbb', 'Bbbbbbbb')
    """
    return tuple(key for key, value in get_enharmonic_decoder().items() if value == note_name)


def get_note_identity(note_name: str) -> str:
    """
    Return the alphabetic name of an accidental note.

    :param note_name: A note name with any number of accidentals.
    :raises errors.NoteNameError: If the note name is a binomial.
    :return: The alphabetic name of the note without accidentals.

    :Example:
    >>> get_note_identity('B###') 
    'B'
    """
    if note_name in constants.BINOMIALS:
        raise errors.NoteNameError('Cannot resolve a binomial note name.')
    return note_name[0]


def notes_are_homonymous(note_one: str, note_two: str) -> bool:
    """
    Check whether two notes are variants 
    of the same alphabetic name.

    :param note_one: A note name with any number of accidentals.
    :param note_two: A note name with any number of accidentals.
    :return: True, if the alphabetic name is the same, regardless
        of accidentals.
    
    :Example:
    >>> notes_are_homonymous('B###', 'Bb') 
    True
    >>> notes_are_homonymous('B###', 'Eb') 
    False
    """
    return get_note_identity(note_one) == get_note_identity(note_two)


def decode_enharmonic(note_name: str) -> str:
    """
    Return the binomial form of a given note name with up to 12 accidentals.

    Any scientific note names (e.g. "C#4") will be stripped of their numerals.

    :param note_name: A valid note name.
    :raises errors.NoteNameError: If the note name is invalid.
    :return: A string representing the plain binomial version of the given 
        note name.

    :Example:
    >>> decode_enharmonic('B#')
    'C'
    >>> decode_enharmonic('A######')
    'D#|Eb'
    >>> decode_enharmonic("C#4")
    'C#|Db'
    """
    if note_name[-1].isnumeric():
        note_name = note_name[:-1]
    decoder: dict[str, str] = get_enharmonic_decoder()
    if note_name in generate_chromatic_octave(constants.BINOMIALS):
        return note_name
    if note_name not in decoder:
        raise errors.NoteNameError(f'Note name {note_name} not recognized.')
    return decoder[note_name]


def encode_enharmonic(note_value: str, note_name: str) -> str:
    """
    Return a note with the same enharmonic value as the given note,
    but under the given alphabetic name.

    This function prefers the enharmonic equivalent with the fewest 
    accidentals. When shifting by tritone, the number of accidentals will be 
    equal in both sharps and flats, so we arbitrarily default to sharps.

    :param note_value: The intended enharmonic value of the note.
    :param note_name: The intended alphabetic name of the note.
    :raises errors.NoteNameError: If the alphabetic name is not one of ABCEDEFG
    :return: A string with the given alphabetic name as the given note name, 
        but with the value of the given note value.

    :Example:
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
    """
    if note_name not in constants.NATURALS:
        raise errors.NoteNameError(
            'Target note name must be from the naturals.')

    note_value = decode_enharmonic(note_value)
    options: tuple[str, ...] = get_enharmonic_equivalents(note_value)
    homonymous_options: list[str] = [
        option for option in options if notes_are_homonymous(option, note_name)]
    return sorted(homonymous_options, key=len)[0]


def scientific_octave(accidental_notes: Sequence[str] = constants.BINOMIALS, octave: int = 0) -> tuple[str, ...]:
    """
    Return a scientific chromatic scale in the given style and octave. 

    :param accidental_notes: The five accidental notes to use in crearing the
        chromatic scale, defaults to constants.BINOMIALS
    :param octave: The numeral to attach to the notes of the octave, defaults 
        to 0.
    :return: The chromatic scale with scientific note names in the given 
        octave.
    """
    return tuple(note + str(octave) for note in generate_chromatic_octave(accidental_notes))


def encode_scientific_enharmonic(note_value: str, note_name: str, position: str) -> str:
    """
    Return a note name that represents the given note name from the perspective of a
    higher or lower note name.

    This function allows you to rephrase a scientific note name as an accidental with
    up to 11 sharps or flats, with the correct scientific numeral.

    :param note_value: The intended enharmonic value of the note, expressed 
        as a scientific note name.
    :param note_name: The intended alphabetic name of the note.
    :param position: The relative position of the note name, either "below" 
        or "above".
    :raises errors.NoteNameError: If the note value is not a recognized 
        scientific note name.
    :raises errors.UnknownKeywordError: If something other than "above" or
        "below" is passed as a position.
    :raises errors.NoteNameError: If the note name is not recognized.
    :return: A string representing a note name, rephrased so as to reflect
        the given perspective.
    
    :Example:
    >>> encode_scientific_enharmonic('A4', 'G', 'below')
    'G##4'
    >>> encode_scientific_enharmonic('A4', 'G', 'above')
    'Gbbbbbbbbbb5'
    """
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
            octave = list(scientific_range()[i-11: i+1])
            octave.reverse()
            symbol = constants.SHARP_SYMBOL

        case keywords.ABOVE:
            octave = list(scientific_range()[i: i+12])
            symbol = constants.FLAT_SYMBOL

        case _:
            raise errors.UnknownKeywordError(position)

    for i, note in enumerate(octave):
        if note[:-1] == note_name:
            return note[:-1] + (symbol * i) + note[-1]

    raise errors.NoteNameError(note_name)


def decode_scientific_enharmonic(note_name: str) -> str:
    """
    Return the scientific binomial for a given scientific multi-accidental or halfstep.

    :param note_name: A scientific note name with any number of accidentals.
    :raises errors.NoteNameError: If the scientific note does not end with a
        valid numeral.
    :raises errors.NoteNameError: If the note name mixes accidental types.
    :raises errors.AristoxenusIndexError: If the requested note would exceed 
        the limits of the system note range (C0 - B8).
    :return: A scientific binomial with the same value as the given note name.

    :Example:
    >>> decode_scientific_enharmonic('B#4')
    'C5'
    >>> decode_scientific_enharmonic('A######7')
    'D#|Eb8'
    """
    # A scientific binomial is already the requested note name.
    scientific_chromatic_binomials: tuple[str, ...] = scientific_range(
        constants.BINOMIALS)
    if note_name in scientific_chromatic_binomials:
        return note_name

    # Reject any note name without a terminal numeral.
    try:
        int(note_name[-1])
    except Exception as ex:
        raise errors.NoteNameError(
            'Must be a scientific note name in octave 0 to 8') from ex
    
    alphabetic_name: str = note_name[0] + note_name[-1]
    index: int = scientific_chromatic_binomials.index(alphabetic_name)
    sharps_: int = note_name.count(constants.SHARP_SYMBOL)
    flats_: int = note_name.count(constants.FLAT_SYMBOL)

    # Reject any note that mixes accidentals.
    if sharps_ != 0 and flats_ != 0:
        raise errors.NoteNameError(note_name)

    adjustment: int = constants.SHARP_VALUE * sharps_
    if sharps_ == 0:
        adjustment = constants.FLAT_VALUE * flats_
    index += adjustment
    if index < 0 or index > len(scientific_chromatic_binomials) - 1:
        raise errors.AristoxenusIndexError(note_name)

    return scientific_chromatic_binomials[index]


def scientific_range(accidental_notes: Sequence[str] = constants.BINOMIALS) -> tuple[str, ...]:
    """
    Return a full range (C0 - B8) of scientific notation for a given accidental.

    :param accidental_notes: A set of five accidental notes, defaults to 
        constants.BINOMIALS
    :return: A full range of scientific notation using the given accidentals.
    """
    full_range: list[str] = []
    for octave in range(constants.NUMBER_OF_OCTAVES):
        new_octave = list(scientific_octave(accidental_notes, octave))
        full_range += new_octave
    return tuple(full_range)


def convert_frequency_to_note(frequency: float, accidental_notes: Sequence[str] = constants.BINOMIALS, temperament_: Optional[Sequence[float]] = None) -> str:
    """
    Return a scientific note name for a given frequency and accidental style.

    :param frequency: A decimal number representing a frequency.
    :param accidental_notes: A group of five accidental notes to use in
        the chromatic scale, defaults to constants.BINOMIALS
    :param temperament_: An array of scientific note names, corresponding to
        the system range, defaults to None, representing 12-TET @ A440
    :raises errors.AristoxenusValueError: If the frequency is not in the 
        temperament's list of frequencies (or close, see below).
    :return: A note name representing the given frequency.

    If the frequency is not among the frequencies generated by the program,
    the function attempts to round the frequency to different decimal
    places to see if the given frequency might be close. 

    :Example:
    >>> convert_frequency_to_note(440.0)
    'A4'
    >>> convert_frequency_to_note(138.591, constants.SHARPS)
    'C#3'
    >>> convert_frequency_to_note(138.59, constants.SHARPS)
    'C#3'
    >>> convert_frequency_to_note(138.6, constants.SHARPS)
    'C#3'
    """
    frequency = round(frequency, constants.FREQUENCY_DECIMAL_LIMIT)
    frequencies: list[float] = list(temperament_) if temperament_ else list(temperament.equal_temperament())
    for num in [2, 1, 0]:
        if frequency in frequencies:
            return scientific_range(accidental_notes)[frequencies.index(frequency)]
        frequencies = [round(x, num) for x in frequencies]

    raise errors.AristoxenusValueError(frequency)


def convert_note_to_frequency(note_name: str, temperament_: Optional[Sequence[float]] = None) -> float:
    """
    Return a frequency for a given scientific note name of any accidental style.

    :param note_name: A scientific note name in any accidental style.
    :param temperament_: An array of scientific note names, corresponding to
        the system range, defaults to None, representing 12-TET @ A440
    :raises errors.NoteNameError: _description_
    :return: A decimal number representing the frequency of the given note 
        name.

    :Example:
    >>> convert_note_to_frequency('A4')
    440.0
    >>> convert_note_to_frequency('Db3')
    138.591
    """
    try:
        note_name = decode_scientific_enharmonic(note_name)
    except Exception as ex:
        raise errors.NoteNameError(note_name) from ex
    if not temperament_:
        temperament_ = temperament.equal_temperament()
    return dict(zip(scientific_range(constants.BINOMIALS), temperament_))[note_name]


def force_heptatonic(note_name: str, interval_structure: int = intervallic_canon.DIATONIC_SCALE) -> tuple[str, ...]:
    """
    Force a heptatonic scale pattern to conform to ABCDEFG nomenclature.

    :param note_name: Any real plain keynote name (i.e. not a scientific name, 
        and not a binomial name).
    :param interval_structure: An integer of no more than 12 bits, of which
        exactly 7 are flipped, defaults to intervallic_canon.DIATONIC_SCALE.
    :raises errors.NoteNameError: If the note name is a binomial.
    :raises errors.HeptatonicScaleError: If the interval structure is not a
        12-tone heptatonic scale.
    :return: A tuple of seven note names representing the given scaleform, but
        from the perspective of the given keynote.
    
    :Example:
    >>> force_heptatonic('B#', 0b101010110101)
    ('B#', 'C##', 'D##', 'E#', 'F##', 'G##', 'A##')
    """
    if note_name in constants.BINOMIALS:
        raise errors.NoteNameError(
            'Function requires naturals, sharps, or flats.')
    if not bitwise.validate_interval_structure(interval_structure, 12, 7):
        raise errors.HeptatonicScaleError(
            "Function requires a heptatonic scale.")
    basic_order: tuple[str, ...] = utils.shift_array(
        constants.NATURALS, get_note_identity(note_name))
    binomial_version: tuple[str, ...] = rendering.render_plain(interval_structure, utils.shift_array(
        generate_chromatic_octave(constants.BINOMIALS), decode_enharmonic(note_name)))
    return tuple(encode_enharmonic(binomial_version[i], basic_order[i]) for i in range(constants.NOTES))


def best_heptatonic(note_name: str, interval_structure: int = intervallic_canon.DIATONIC_SCALE) -> tuple[str, ...]:
    """
    Choose the best set of alphabetic note names for a given heptatonic scale.

    :param note_name: Any plain note name, including real names and binomial 
        names, but not a scientific name.
    :param interval_structure: An integer of no more than 12 bits, of which 
        exactly 7 are flipped., defaults to intervallic_canon.DIATONIC_SCALE
    :return: A tuple of seven note names, representing the best spelling of 
        the scaleform.

    :Example:
    >>> best_heptatonic('A#|Bb', 0b101010110101)
    ('Bb', 'C', 'D', 'Eb', 'F', 'G', 'A')
    >>> best_heptatonic('D#|Eb', 0b101010110101)
    ('Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D')
    >>> best_heptatonic('E#', 0b101010110101)
    ('F', 'G', 'A', 'Bb', 'C', 'D', 'E')
    """
    note_name = decode_enharmonic(note_name)
    # Naturals' default names will always be the best.
    if note_name in constants.NATURALS:
        return force_heptatonic(note_name, interval_structure)

    note_index: int = constants.BINOMIALS.index(note_name)
    sharps_scale = force_heptatonic(
        constants.SHARPS[note_index], interval_structure)
    flats_scale = force_heptatonic(
        constants.FLATS[note_index], interval_structure)

    # The best name can usually be decided by fewest total accidentals
    f_count = count_accidentals(flats_scale)
    s_count = count_accidentals(sharps_scale)
    s_total = s_count["#"] + s_count["b"]
    f_total = f_count["#"] + f_count["b"]
    if s_total > f_total:
        return flats_scale
    if f_total > s_total:
        return sharps_scale

    # If accidentals are equal, the best name is the # one that does not
    # mix different accidental types.
    smix = s_count["#"] > 0 and s_count["b"] > 0
    fmix = f_count["#"] > 0 and f_count["b"] > 0
    if f_total == s_total:
        if smix and not fmix:
            return flats_scale
        if fmix and not smix:
            return sharps_scale

    # By this point, we know that the scales have an equal number accidentals,
    # and both/neither are mixed. Resolve by arbitrarily defaulting to sharps.
    return sharps_scale


def is_abcdefg(note_names: Sequence[str]) -> bool:
    """
    Check if a given collection of note names adheres to the heptatonic 
    ABCDEFG nomenclature, in which each alphebetic name appears once and
    only once.

    :param note_names: A sequence of note names.
    :raises errors.NoteNameError: If a binomial is passed as a note name.
    :return: True, if the collection has exactly one each of ABCDEFG.

    :Example:
    >>> is_abcdefg(['C', 'Db', 'E#', 'F#', 'G', 'A', 'B'])
    True
    >>> is_abcdefg(['C', 'Db', 'E#', 'F', 'G', 'A', 'B'])
    False
    """
    naturals_: list[str] = list(constants.NATURALS)
    approved_names: set[str] = set()
    for note in note_names:
        if note in constants.BINOMIALS:
            raise errors.NoteNameError(note)

        if get_note_identity(note) in naturals_:
            naturals_.pop(naturals_.index(get_note_identity(note)))
            approved_names.add(decode_enharmonic(note))

    return len(naturals_) == 0 and len(approved_names) == constants.NOTES


def is_scientific(note_name: str) -> bool:
    """
    Return true if the given note name uses scientific notation.

    :param note_name: Any note name.
    :return: True, if the name is a scientific note name.

    :Example:
    >>> is_scientific('C##')
    False
    >>> is_scientific('D##4')
    True
    """
    return note_name[-1].isnumeric()


def get_accidentals(symbol: Optional[str] = None) -> tuple[str, ...]:
    """
    Return the accidental group to which the given note name or 
    keyword belongs. If the given symbol cannot be resolved, default
    to binomials.

    :param symbol: Any note name or accidental keyword, optional, default is 
        None, representing the binomials.
    :return: A tuple of five note names representing the accidental notes in 
        the requested style.

    :Example:
    >>> get_accidentals("C#")
    ('C#', 'D#', 'F#', 'G#', 'A#')
    >>> get_accidentals("E#")
    ('C#', 'D#', 'F#', 'G#', 'A#')
    >>> get_accidentals("sharp")
    ('C#', 'D#', 'F#', 'G#', 'A#')
    >>> get_accidentals()
    ('C#|Db', 'D#|Eb', 'F#|Gb', 'G#|Ab', 'A#|Bb')
    >>> get_accidentals("C")
    ('C#|Db', 'D#|Eb', 'F#|Gb', 'G#|Ab', 'A#|Bb')
    >>> get_accidentals("any_invalid_symbol")
    ('C#|Db', 'D#|Eb', 'F#|Gb', 'G#|Ab', 'A#|Bb')
    """
    if not symbol:
        return constants.BINOMIALS
    
    if symbol == keywords.SHARP:
        return constants.SHARPS
    if symbol == keywords.FLAT:
        return constants.FLATS
    if symbol == keywords.BINOMIAL:
        return constants.BINOMIALS
    if symbol.endswith("#"):
        return constants.SHARPS
    if symbol.endswith("b"):
        return constants.FLATS

    return constants.BINOMIALS


def get_accidental_keyword(note_name: Optional[str] = None) -> str:
    """
    Return the keyword representing the accidental group to which the given
    note name belongs.

    :param note_name: Any note name, default is None, representing "binomial". 
        Unrecognized names will return "binomial".
    :return: A keyword representing the type of accidental in the note name,
        "sharp", "flat", "binomial".

    :Example:
    >>> get_accidental_keyword("C#")
    'sharp'
    >>> get_accidental_keyword("Cb")
    'flat'
    >>> get_accidental_keyword("C#|Db")
    'binomial'
    >>> get_accidental_keyword("C")
    'binomial'
    >>> get_accidental_keyword()
    'binomial'
    >>> get_accidental_keyword("any_invalid_symbol")
    'flat'
    """
    if not note_name:
        return keywords.BINOMIAL
    if constants.BINOMIAL_DIVIDER_SYMBOL in note_name:
        return keywords.BINOMIAL
    if constants.SHARP_SYMBOL in note_name:
        return keywords.SHARP
    if constants.FLAT_SYMBOL in note_name:
        return keywords.FLAT
    return keywords.BINOMIAL


def name_heptatonic_intervals(scale_data: Sequence[str] | int) -> tuple[str, ...]:
    """
    For a given collection of note names or an interval structure, return 
    the Indian numerals describing the pattern's relation to the diatonic 
    scale.

    :param scale_data: A list of exactly 7 note names, from the naturals, 
        sharps, flats, or binomials; OR an integer representing an interval 
        structure not exceeding 12 bits, of which 7 are flipped.
    :raises errors.HeptatonicScaleError: If the given scale is not a 
        heptatonic scale in 12 tone form.
    :return: A list of numbers modified by the sharp or flat symbol according 
        to their relationship to the given scale.

    :Example:
    >>> name_heptatonic_intervals(['C', 'D', 'Eb', 'Fb', 'Gbb', 'Ab', 'Bb']) 
    ('1', '2', 'b3', 'b4', 'bb5', 'b6', 'b7')
    >>> name_heptatonic_intervals(['C', 'D#', 'E', 'F', 'G#', 'A#', 'B']) 
    ('1', '#2', '3', '4', '#5', '#6', '7')
    >>> name_heptatonic_intervals(['D#', 'E#', 'F##', 'G#', 'A#', 'B#', 'C##'])
    ('1', '2', '3', '4', '5', '6', '7')
    >>> name_heptatonic_intervals(2741)
    ('1', '2', '3', '4', '5', '6', '7')
    """
    if isinstance(scale_data, int):
        scale_data = rendering.render_plain(scale_data)

    tonic: str = decode_enharmonic(scale_data[0])
    binomial_names: list[str] = [decode_enharmonic(x) for x in scale_data]
    if len(binomial_names) != constants.NOTES:
        raise errors.HeptatonicScaleError(
            "Function requires a heptatonic scale.")

    chromatic_names: tuple[str, ...] = utils.shift_array(
        generate_chromatic_octave(constants.BINOMIALS), tonic)
    major_names: tuple[str, ...] = rendering.render_plain(
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

    return tuple(intervals_)


def twelve_tone_scale_intervals(scale: int = intervallic_canon.DIATONIC_SCALE) -> tuple[str, ...]:
    """
    Return a list that consists of the 7 correctly-spelled intervals of any
    heptatonic scale, plus 5 more intervals that fill in the chromatic notes.

    The purpose of this function is to ensure that the more unusual scale
    structures are able to keep their unusual intervals with their correct
    relative names when embedded in chromatic contexts.

    :param scale: An integer representing a heptatonic scale, defaults to 
        intervallic_canon.DIATONIC_SCALE
    :raises errors.HeptatonicScaleError: If the given integer is not a 
        heptatonic scale structure.
    :return: A tuple of twelve names; the seven correctly-spelled intervals
        of the given scaleform, plus five more logical accidental names.
    
    :Example:
    >>> from src.data.intervallic_canon import HEMIOLIC_SCALE, DIATONIC_SCALE, BISEPTIMAL_SCALE, HARMONIC_SCALE
    >>> print(twelve_tone_scale_intervals(DIATONIC_SCALE))
    ('1', 'b2', '2', 'b3', '3', '4', 'b5', '5', '#5', '6', 'b7', '7')
    >>> print(twelve_tone_scale_intervals(HEMIOLIC_SCALE))
    ('1', 'b2', '2', '#2', '3', '4', 'b5', '5', '#5', '6', 'b7', '7')
    >>> print(twelve_tone_scale_intervals(BISEPTIMAL_SCALE))
    ('1', 'b2', '2', 'b3', '3', '4', 'b5', '5', '#5', '6', '#6', '7')
    >>> print(twelve_tone_scale_intervals(HARMONIC_SCALE))
    ('1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7')
    """
    if not bitwise.validate_interval_structure(scale, 12, 7):
        raise errors.HeptatonicScaleError(
            "Function requires a heptatonic scale.")

    chromatic_scale: tuple[str, ...] = generate_chromatic_octave()
    note_names: tuple[str, ...] = rendering.render_plain(scale, chromatic_scale)
    rendering_: tuple[str, ...] = name_heptatonic_intervals(scale)
    intervals: list[str] = []
    for i, n in enumerate(chromatic_scale):
        if n in note_names:
            j = note_names.index(n)
            intervals.append(rendering_[j])
        else:
            intervals.append(
                list(chord_symbols.DEFAULT_SCALE_INTERVAL_TO_SYMBOL_MAP.values())[i])

    return tuple(intervals)


def twelve_tone_scale_names(note_names: Sequence[str]) -> tuple[str, ...]:
    """
    Return a list that contains the given 7 note names, plus 5 more note names
    that supply the missing accidental notes.

    The purpose of this function is to ensure that heptatonic scales that mix 
    sharps and flats, or which begin with an enharmonic halfstep (e.g. Cb), are 
    still able to be contextualized within chromatic scales.

    :param note_names: An array of 7 note names representing a heptatonic 
        scale.
    :raises errors.HeptatonicScaleError: If the given array is not a 
        heptatonic scale.
    :raises errors.NoteNameError: If any of the note names in the scale
        is a binomial.
    :return: A tuple containing a chromatic scale in which the given scale's
        note names are respected.

    :Example:
    >>> twelve_tone_scale_names(['G', 'A', 'Bb', 'C', 'D', 'E', 'F#'])
    ('G', 'G#', 'A', 'Bb', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#')
    """
    if not len({decode_enharmonic(x) for x in note_names}) == 7:
        raise errors.HeptatonicScaleError(
            "Function requires a heptatonic scale.")

    if any(x in constants.BINOMIALS for x in note_names):
        raise errors.NoteNameError(
            "Function cannot process binomial note names.")

    scale: list[str] = list(note_names)
    chromatic_: list[str] = ["" for _ in range(12)]
    enharmonic_keynote: str = decode_enharmonic(scale[0])
    binomial_scale_names: list[str] = [decode_enharmonic(x) for x in scale]
    accidental_signature: dict[str, int] = count_accidentals(scale)
    binomial_chromatic: tuple[str, ...] = utils.shift_array(
        generate_chromatic_octave(), enharmonic_keynote)
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

    return tuple(chromatic_)


def count_accidentals(note_names: Sequence[str]) -> dict[str, int]:
    """
    Return the total number of accidentals of each type in a given list of
    note names.

    :param note_names: An array of real (i.e. not binomial) note names.
    :raises errors.NoteNameError: If a note name is a binomial.
    :return: A dictionary with the following keys
        "#" : int - the number of sharps
        "b" : int - the number of flats
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


def interval_identity(interval_name: str) -> int:
    """
    Return the numeric part of a numerical interval symbol. 

    :param interval_name: An interval, in Indian numeral notation
        (e.g. "#4")
    :raises errors.NoteNameError: If the interval name does not end in a 
        digit.
    :return: An integer, representing the numeric portion of the symbol.

    :Example:
    >>> interval_identity("bbb7")
    7
    >>> interval_identity("#4")
    4
    """
    x =  re.search("(\\d+)$", interval_name)
    if x:
        return int(x[1])
    raise errors.NoteNameError(f"Interval name must end in a digit (interval_name={interval_name})")


def get_interval_map(tonal_centre: str, scale: int = intervallic_canon.DIATONIC_SCALE, binomial: bool = False) -> dict[str, str]:
    """
    Return a mapping of the correct note names and interval names for the 
    given heptatonic scale form, along with 5 additional names representing 
    the missing chromatic steps.

    This function is designed to ensure that scales that use mixed or multiple
    accidentals will be able to reference chromatic notes with logical names.

    If the binomial flag is set to True, then the note names will simply be the 
    binomials. Otherwise, a binomial keynote will be resolved into its optimal 
    keynote name.

    :param tonal_centre: The keynote of the interval structure.
    :param scale: An integer representing a heptatonic scale, defaults to 
        intervallic_canon.DIATONIC_SCALE
    :param binomial: Flag that overrides the nomenclature and returns a mapping
        of the interval names to binomial note names, defaults to False
    :return: A mapping of note_name : interval_name
    TODO: Example
    """
    if tonal_centre not in constants.LEGAL_ROOT_NAMES:
        tonal_centre = decode_enharmonic(tonal_centre)

    accidentals = get_accidentals(tonal_centre)
    if tonal_centre in constants.BINOMIALS:
        real_names = best_heptatonic(tonal_centre, scale)
    else:
        real_names = force_heptatonic(tonal_centre, scale)

    interval_symbols: list[str] = list(twelve_tone_scale_intervals(scale))
    mapping = dict(zip(utils.shift_array(
        generate_chromatic_octave(), decode_enharmonic(tonal_centre)), interval_symbols))

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


def heptatonic_range(heptatonic_names: Sequence[str]) -> dict[str, str]:
    '''
    Create a mapping of the full scientific range to the proper twelve tone
    interval names for a given heptatonic scale.

    :param heptatonic_names: An array of seven real (i.e. not binomial) note
        names to use as the base.
    :return: An array of constants.NUMBER_OF_OCTAVES octaves of chromatic 
        scales with scientific numerals, respecting the original note names.
    TODO: Example
    '''
    twelve_tones = twelve_tone_scale_names(heptatonic_names)
    binomial_version = [decode_enharmonic(x) for x in twelve_tones]
    mapping: dict[str, str] = {}
    for scientific_chromatic in scientific_range():
        name = scientific_chromatic[:-1]
        if name in binomial_version:
            mapping[scientific_chromatic] = dict(
                zip(binomial_version, twelve_tones))[name]
    return mapping


def encode_intervals_as_note_names(interval_names: Sequence[str], keynote: str) -> tuple[str, ...]:
    """
    Return a list of note names that correspond to the given interval names,
    as considered from the given keynote.

    The names will respect the enharmonic-equivalences implied in the interval
    names, so that in C #2 is D# and b3 is Eb.

    :param interval_names: An array of interval names in Indian numeral 
        notation (e.g. "#4").
    :param keynote: A real (i.e. not binomial) note name that will serve as 
        the note from which intervals are reckoned.
    :return: A tuple of note names respecting the given interval pattern 
        and keynote.

    :Example:
    >>> encode_intervals_as_note_names(('1', '3', '5', '7'), "C")
    ('C', 'E', 'G', 'B')
    >>> encode_intervals_as_note_names(('1', 'b3', '5', 'bb7'), "C")
    ('C', 'Eb', 'G', 'Bbb')
    >>> encode_intervals_as_note_names(('1', '3', '#5', '7'), "C")
    ('C', 'E', 'G#', 'B')
    >>> encode_intervals_as_note_names(('1', '3', 'b6', '7'), "C")
    ('C', 'E', 'Ab', 'B')
    >>> encode_intervals_as_note_names(('1', '3', '5', '7', '#9', '#11'), "C")
    ('C', 'E', 'G', 'B', 'D#', 'F#')
    """    
    diatonic_names = force_heptatonic(keynote)
    interval_names = utils.order_interval_names(interval_names)
    natural_intervals = [str(x) for x in range(1, 8)]
    final_names: list[str] = []

    for interval_name in interval_names:
        if interval_name in natural_intervals:
            i = natural_intervals.index(interval_name)
            final_names.append(diatonic_names[i])
        else:
            numeral: int = utils.extract_number(interval_name)
            accidentals = interval_name.replace(str(numeral), "")

            # Find the 'normal' index of extensions (e.g. #11 -> #4) to get 
            # the simple note name.
            while numeral > constants.NOTES:
                numeral -= constants.NOTES

            i = natural_intervals.index(str(numeral))
            diatonic_name = diatonic_names[i]
            name = diatonic_name + accidentals
            final_names.append(name)
    for i, name in enumerate(final_names):
        accidentals = 0
        accidentals += constants.FLAT_VALUE * name.count(constants.FLAT_SYMBOL)
        accidentals += constants.SHARP_VALUE * \
            name.count(constants.SHARP_SYMBOL)
        if accidentals > 0:
            symbol = constants.SHARP_SYMBOL
        elif accidentals < 0:
            symbol = constants.FLAT_SYMBOL
        else:
            symbol = str()
        final_names[i] = get_note_identity(name) + (symbol * abs(accidentals))
    return tuple(final_names)

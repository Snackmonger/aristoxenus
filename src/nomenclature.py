'''
Functions related to generating and processing musical nomenclatural material.
'''
from dataclasses import dataclass
from src.pitch_mapping import render, shift_list

# ---------------------------- PRECURSOR MATERIAL -------------------------- #

# Basic nomenclatural material.
__NATURALS: list[str] = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
__HALFSTEPS: dict[str, str] = {'E': 'F', 'B': 'C'}

# Basic tonal material.
__TONES: int = 12
__SHARP_VALUE: int = 1
__FLAT_VALUE: int = -1

# Symbolic material.
__SHARP_SYMBOL: str = '#'
__FLAT_SYMBOL: str = 'b'
__BINOMIAL_DIVIDER_SYMBOL: str = '/'

# Range and frequency material.
__CENTRAL_REFERENCE_NOTE_NAME: str = 'A4'
__CENTRAL_REFERENCE_NOTE_FREQUENCY: int = 440
__NUMBER_OF_OCTAVES: int = 9
__OCTAVE_EQUIVALENCE_FACTOR: int = 2
__FREQUENCY_DECIMAL_LIMIT: int = 3

# --------------------------------- GENERATED MATERIAL --------------------- #

__ACCIDENTAL_SYMBOLS: list[str] = [__SHARP_SYMBOL, __FLAT_SYMBOL]
__SHARPS: list[str] = [note + __SHARP_SYMBOL for note in __NATURALS
                       if note not in __HALFSTEPS]
__FLATS: list[str] = [note + __FLAT_SYMBOL for note in __NATURALS
                      if note not in __HALFSTEPS.values()]
__BINOMIALS: list[str] = [sharp + __BINOMIAL_DIVIDER_SYMBOL + flat
                          for flat in __FLATS for sharp in __SHARPS
                          if __FLATS.index(flat) == __SHARPS.index(sharp)]
__ACCIDENTAL_NOTES: list[str] = __SHARPS + __FLATS
#__BASIC_NOTE_NAMES = __ACCIDENTAL_NOTES + __NATURALS + __BINOMIALS


def __chromatic(accidental_notes: list[str]) -> list[str]:
    '''
    Return a chromatic scale using the given accidentals.
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
    Generate a table for decoding the binomial form 
    of a note with any number of sharps or flats.
    '''
    enharmonic_equivalence_decoder: dict[str, str] = {}
    chromatic_binomials: list[str] = chromatic()
    for accidental in __ACCIDENTAL_SYMBOLS:
        dummy_chromatic_binomials: list[str] = chromatic_binomials.copy()
        shift_degree = __SHARP_VALUE

        # Reverse sequence for flats.
        if accidental == __FLAT_SYMBOL:
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

        E.g.:   'E' >>  ['E', 'Fb', 'Gbbb', ..., 'D##', 'C####', ...]
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
    '''
    # Any natural or binomial, or any natural + 1 accidental
    enharmonic_: dict[str, str] = __enharmonic_decoder()
    legal_names_: list[str] = __BINOMIALS.copy()
    for key in enharmonic_:
        if len(key) <= 2:
            legal_names_.append(key)
    return legal_names_


def __identity(note_name: str) -> str:
    '''
    Return the alphabetic name of an accidental note.

    E.g.:   'B###' >> 'B'
    '''
    if note_name in __BINOMIALS:
        raise ValueError('Cannot resolve a binomial note name.')
    return note_name[0]


def __is_homonymous(note_one: str, note_two: str) -> bool:
    '''
    Check whether two notes are variants of the same alphabetic name.
    '''
    return __identity(note_one) == __identity(note_two)


def decode_enharmonic(note_name: str) -> str:
    '''
    Return the binomial form of a given note name with up to 12 accidentals.
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

    Params:
        note_value:     a scientific note with 0 to 1 accidentals 
                        (binomials count as 1 accental)
        note_name:      one of the 7 natural notes

    This function prefers the enharmonic equivalent with the 
    fewest accidentals. When shifting by tritone, the number 
    of accidentals will be equal in both sharps and flats, 
    so we arbitrarily default to sharps.

    Returns
    =======
        E.g.    'Eb' , 'A' >> 'A######'
                'Eb' , 'B' >> 'B####'
                'Eb' , 'C' >> 'C###'
                'Eb' , 'D' >> 'D#' 
                'Eb' , 'E' >> 'Eb'
                'Eb' , 'F' >> 'Fbb'
                'Eb' , 'G' >> 'Gbbb'
                'Eb' , 'A' >> 'A######'
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
    '''
    return [note + str(octave) for note in __chromatic(accidental_notes)]


def decode_scientific_enharmonic(note_name: str) -> str:
    '''
    Return the scientific binomial for a given scientific multi-accidental or halfstep.

    E.g.:   B#4        >>  C5
            A######7   >>  D#/Eb8
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
    sharps_: int = note_name.count(__SHARP_SYMBOL)
    flats_: int = note_name.count(__FLAT_SYMBOL)

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
    Return a full range (C0 - B8) of scientific notation for a given
    accidental.
    '''
    full_range: list[str] = []
    for octave in range(__NUMBER_OF_OCTAVES):
        new_octave = __scientific_octave(accidental_notes, octave)
        full_range += new_octave
    return full_range


# def __scientific_names() -> list[str]:
#     '''Get all basic scientific names with 0 or 1 accidentals.'''
#     return list(set(__scientific_range(__BINOMIALS) 
#                     + __scientific_range(__SHARPS) 
#                     + __scientific_range(__FLATS)))
    

def equal_temperament() -> list[float]:
    '''
    Return a list of frequencies corresponding to the range of the 
    scientific chromatic scales (C0 - B8).
    '''
    calculated_pitch: float
    full_range: list[str] = __scientific_range(__BINOMIALS)
    centre: str = __CENTRAL_REFERENCE_NOTE_NAME
    freq: int = __CENTRAL_REFERENCE_NOTE_FREQUENCY
    frequencies: list[float] = []
    direction: int

    for note in full_range:
        if full_range.index(note) < full_range.index(centre):
            direction = __FLAT_VALUE
            semitones_from_centre = full_range.index(
                centre) - full_range.index(note)
        else:
            direction = __SHARP_VALUE
            semitones_from_centre = full_range.index(
                note) - full_range.index(centre)

        # 12 TET : next note = previous note * 2 ** (+ , -) 1/12
        calculated_pitch = freq * \
            __OCTAVE_EQUIVALENCE_FACTOR ** (direction *
                                            semitones_from_centre / __TONES)
        if calculated_pitch not in frequencies:
            frequencies.append(
                round(calculated_pitch, __FREQUENCY_DECIMAL_LIMIT))

    return frequencies


def encode_frequency(frequency: float, accidentals: list[str]) -> str:
    '''
    Return a scientific note name for a 
    given frequency and accidental style.
    '''
    frequencies: list[float] = equal_temperament()
    if frequency in frequencies:
        return __scientific_range(accidentals)[frequencies.index(frequency)]
    raise ValueError(f'Invalid request {frequency} {accidentals}')


def decode_frequency(note_name: str) -> float:
    '''
    Return a frequency for a given scientific 
    note name of any accidental style.
    '''
    try:
        note_name = decode_scientific_enharmonic(note_name)
    except Exception as ex:
        raise ValueError(f'Could not contextualize note {note_name}') from ex
    
    return dict(zip(__scientific_range(__BINOMIALS), equal_temperament()))[note_name]
   

def force_heptatonic(note_name: str, scale_pattern: int) -> list[str]:
    '''
    Take a starting note from the naturals, sharps, or flats, 
    and a scale pattern, and return an alphabetic spelling 
    in which each of ABCDEFG (or a variant) appears exactly
    once. 

    The scale pattern is supplied in the form of an integer 
    representing a binary map, and must have exactly 7 
    flipped bits.

    E.g.: 'B#', 0b101011010101 >> B#, C##, D##, E#, F##, G##, A##, B#
    '''
    if note_name in __BINOMIALS:
        raise ValueError(
            'Operation can only be performed on naturals, sharps, or flats.')
    if scale_pattern.bit_count() != 7:
        raise ValueError(
            'Operation can only be performed on heptatonic scales.')
    
    # Assemble basic alphabetic order to enforce.
    plain_scale: list[str] = naturals()
    plain_name: str = __identity(note_name)
    plain_scale = plain_scale[plain_scale.index(
        plain_name):] + plain_scale[:plain_scale.index(plain_name)]

    # Create binomial version of requested scale pattern.
    tonic: str = decode_enharmonic(note_name)
    chrom = __chromatic(__BINOMIALS)
    chrom = chrom[chrom.index(tonic):] + chrom[:chrom.index(tonic)]
    binomial_scale: list[str] = render(scale_pattern, chrom)
    # binomial_scale = binomial_scale[binomial_scale.index(tonic):] + binomial_scale[:binomial_scale.index(tonic)]

    # Force each binomial note name to become the right alphabetic note name.
    heptatonic_names: list[str] = []
    for scale_index in range(7):
        binomial_name = binomial_scale[scale_index]
        note_value = plain_scale[scale_index]
        heptatonic_names.append(encode_enharmonic(binomial_name, note_value))

    return heptatonic_names


def best_heptatonic(note_name: str, scale_pattern: int) -> list[str]:
    '''
    Given a note name and a scale pattern, return the better 
    spelling of the two accidental types (fewest total accidentals).

    Accepts naturals, sharps, flats, and binomials.

        E.g.:   'A#/Bb', 0b101011010101   >>  Bb, C, D, Eb, F, G, Ab
                'A#/Bb', 0b101101011010   >>  A#, B#, C, D#, E#, F#, G#
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
    return len(naturals_) == 0 and len(approved_names) == 7 and len(enharmonic) == 7


def name_heptatonic_intervals(note_names: list[str]) -> list[str]:
    '''
    For a given heptatonic scale, return the Indian numerals describing
    the pattern's relation to the major scale.

    Thus:       C D Eb Fb Gbb Ab Bb 
             >> 1 2 b3 b4 bb5 b6 b7

    And also:   C D#  E  F  G#  A# B 
             >> 1 #2  3  4  #5  #6 7
    
    '''
    tonic: str = note_names[0]
    binomial_names = [decode_enharmonic(note_name) for note_name in note_names]
    if len(binomial_names) != 7:
        raise ValueError('Only works on heptatonic scales.')
    chromatic_names: list[str] = shift_list(chromatic(), tonic)
    major_names: list[str] = render(2741, chromatic_names)
    intervals: list[str] = []
    for index in range(7):
        expected_note: str = major_names[index]
        given_note: str = binomial_names[index]
        difference: int = chromatic_names.index(given_note) - chromatic_names.index(expected_note)
        accidental: str = '#'
        if difference < 0:
            accidental = 'b'
            difference *= -1
        intervals.append((accidental * difference) + str(index + 1))
    return intervals


def generate_interval_map(note_names: list[str]) -> int:
    '''
    Return an integer representing a given collection of note names.

    Notes will be parsed into their simplest binomial form. The first 
    note of the given list will serve as the tonic or root of the pitch 
    map, and other notes will be considered sharper intervals from that 
    note name. Unrecognizable note names will be ignored.

    E.g.:   ['C', 'D###4', 'Db', 'Fbbb5', 'Mb', 'G###6', 'F#####9', 'F#/Gb', 'F#/Gb5']
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
    pitch_map: int = 0
    for note_name in simplified_notes:
        pitch_map |= (1 << chromatic_.index(note_name))
    return pitch_map


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
    '''Return the 5 accidentals in binomial form, beginning at C#/Db.'''
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


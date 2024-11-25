
import re
from typing import Iterable, Optional

from aristoxenus.core.heptatonic_spelling import get_heptatonic_interval_names
from aristoxenus.core.interval import sort_interval_names
from aristoxenus.core.roman_numeral import encode_roman_numeral

from aristoxenus.core.annotations import (
    ChordData, 
    ScalePatternData
)
from aristoxenus.core.chord_symbol import decode_chord_symbol
from aristoxenus.core.convert_names import (
    convert_interval_names_to_integers,
    convert_interval_names_to_note_names,
    convert_interval_names_to_roman_names,
    convert_note_names_to_integers
)
from aristoxenus.core.constants import (
    CHORD_SYMBOL,
    DIATONIC,
    EMPTY_STRING,
    HEPTATONIC_SCALES,
    HEXATONIC_SCALES,
    IONIAN,
    MODAL_SERIES_KEYS,
    MODE_NAME,
    NATURAL_NAMES, NOTE_NAME,
    NOTES,
    PENTATONIC_SCALES,
    RE_ADDED_INTERVAL,
    RE_ALTERED_INTERVAL,
    RE_CANON_NAMES,
    RE_COMPLETE_CANON_EXPR,
    RE_KEYNOTE_EXPR,
    RE_MODENAMES,
    RE_NATURAL_INTERVAL,
    RE_PARSE_CHORD_SYMBOL,
    RE_SUBTRACTED_INTERVAL,
    SCALE_NAME,
    SCALE_ALIASES,
    SLASH_SYMBOL,
    TONES,
)
from aristoxenus.core.errors import (
    ArgumentError, 
    AristoxenusError, 
    StringValidationError)
from aristoxenus.core.note_name import decode_note_name
from aristoxenus.core.rotate import rotate_interval_structure
from aristoxenus.core.validation import validate_roman_name


def resolve_heptatonic_scale(scale_name: str, mode_name: Optional[str | int] = None) -> tuple[int, ...]:
    '''
    Attempt to resolve the given scale and mode name into a sequence of 
    integers representing a scale's interval structure.

    Parameters
    ----------
    scale_name : str
        The scale name to search for.
    mode_name : str or int
        The mode to rotate the scale to, such that the base form is 'ionian',
        first rotation is 'dorian', second rotation is 'phrygian', etc.

    Returns
    -------
    tuple[int, ...]
        A collection of integers representing an interval structure.

    Raises
    ------
    StringValidationError
        If the name of the scale or mode cannot be resolved.
    '''
    if scale_name not in HEPTATONIC_SCALES:
        try:
            config = resolve_scale_alias(scale_name)
            return resolve_heptatonic_scale(*config)
        except StringValidationError:
            pass

    # We expect that mode_name==None when scale_name is an alias,
    # so None at this point presumably means 'ionian'.
    if mode_name is None:
        rotations = 0
    elif isinstance(mode_name, int):
        rotations = mode_name
    elif mode_name.isdigit():
        rotations = int(mode_name)
    elif mode_name in MODAL_SERIES_KEYS:
        rotations = MODAL_SERIES_KEYS.index(mode_name)
    else:
        raise StringValidationError(mode_name, MODE_NAME)

    if scale_name in MODAL_SERIES_KEYS:
        rotations = MODAL_SERIES_KEYS.index(scale_name)
        scale = HEPTATONIC_SCALES[DIATONIC]
        return rotate_interval_structure(scale, rotations % NOTES)

    if scale_name in HEPTATONIC_SCALES:
        scale = HEPTATONIC_SCALES[scale_name]
        return rotate_interval_structure(scale, rotations % NOTES)

    raise StringValidationError(scale_name, SCALE_NAME)


def resolve_chord_symbol(chord_symbol: str) -> ChordData:
    '''
    Extrapolate a chord symbol into a complete set of chord data.

    Parameters
    ----------
    chord_symbol : str
        A string representing a chord symbol, e.g. "Cmaj7/E", "iim7",

    Returns
    -------
    ChordData
        A collection of data about a chord's intervals and note names.

    Raises
    ------
    StringValidationError
        If the chord symbol cannot be parsed.
    '''
    chord = re.match(RE_PARSE_CHORD_SYMBOL, chord_symbol)
    if chord is None:
        for numeral in range(1, 8):
            if encode_roman_numeral(numeral).lower() in chord_symbol.lower() and SLASH_SYMBOL in chord_symbol:
                raise StringValidationError(
                    chord_symbol, CHORD_SYMBOL, "Slash notation is not supported for chords expressed using Roman numeral.")
        raise StringValidationError(chord_symbol, CHORD_SYMBOL)
    name = chord.group(NOTE_NAME)
    interval_names = decode_chord_symbol(chord_symbol)
    if validate_roman_name(name):
        note_names = convert_interval_names_to_roman_names(interval_names)
        structure = convert_interval_names_to_integers(interval_names)
    else:
        note_names = convert_interval_names_to_note_names(
            decode_note_name(name), interval_names)
        structure = convert_note_names_to_integers(note_names)
    return ChordData(
        chord_symbol=chord_symbol,
        note_names=note_names,
        interval_names=interval_names,
        interval_structure=structure)


def resolve_scale_pattern(interval_structure: Iterable[int] | int) -> ScalePatternData:
    '''
    Search our library of scale names for a given scale pattern.

    NOTE: We provide the most common scales and many unusual ones, but the list 
    is not exhaustive, and not all theoretically-possible scales are actually 
    accounted for and named in our scale library.

    Parameters
    ----------
    interval_structure : Iterable[int] | int
        A scale pattern, either a collection of integers representing
        intervals in 12-tone temperament, or a single 12-bit integer 
        representing an interval structure in binary (LSB == unison).

    Returns
    -------
    ScalePatternResponse
        The input pattern, the scale and modal names of the given form, and any
        known aliases.

    Raises
    ------
    ArgumentError
        - If the input pattern is not valid.
        - If the input pattern cannot be found.

    Examples
    --------
    TODO: Examples
    '''
    # When a scale pattern is an int, LSB is the unison, so all valid scales
    # must be odd numbers, e.g. 2741 = 101010110101 -> [0, 2, 4, 5, 7, 9, 11]
    if isinstance(interval_structure, int):
        if interval_structure % 2 == 0:
            raise ArgumentError(
                f"Scale pattern integers must be odd numbers ({interval_structure=}).")
        interval_structure = [
            i for i in range(TONES)
            if (n := 1 << i) & interval_structure == n
        ]

    def __resolve_scale_pattern_in_group(
        interval_structure: Iterable[int], 
        scale_group: dict[str, tuple[int, ...]]
        ) -> Optional[ScalePatternData]:
        for scale, base in scale_group.items():
            for i in range(len(base)):
                pattern = rotate_interval_structure(base, i)
                if set(pattern) == set(interval_structure):
                    aliases = [
                    name for name, _, (s, m) in SCALE_ALIASES
                    if s == scale and m == str(i + 1)
                    ]
                    return ScalePatternData(
                        interval_structure=tuple(interval_structure),
                        scale_name=scale,
                        mode_name=str(i + 1),
                        aliases=tuple(aliases)
                    )

    if (s := __resolve_scale_pattern_in_group(interval_structure, HEPTATONIC_SCALES)):
        s.update(mode_name=MODAL_SERIES_KEYS[int(s["mode_name"]) - 1])
        return s
    
    for scale_group in (HEXATONIC_SCALES, PENTATONIC_SCALES):
        if (s := __resolve_scale_pattern_in_group(interval_structure, scale_group)):
            return s

    # TODO: sort out octatonics with regard to handling barry scales
    raise ArgumentError(f"Failed to find a match for {interval_structure=}. ")




def resolve_modal_name(mode_name: str) -> tuple[str, ...]:
    '''
    Take a string representing a modified modal name, and return the set of
    intervals implied in the name.

    The function accepts a string consisting of a mode name (e.g. "dorian") 
    with optional structural modifiers (e.g. '#4', 'no5', 'add7'), then 
    applies the given modifications to the modal form. The function accepts
    a variety of variant formatting types, e.g. "dor.Nat7", 'mixo_#4', 
    'lydianb3', 'loc_natural_5', 'IonianAddb6', "d_no_b7", "b3_no5_ion", etc.

    Parameters
    ----------
    mode_name : str
        A string representing a modal name with zero or more modifiers.

    Returns
    -------
    tuple[str, ...]
        A collection of interval names representing the given modal pattern,
        modified according to the given modifications.

    Raises
    ------
    ArgumentError
        If there is more than one recognizeable mode name.
    '''
    base_symbol: list[str] = []
    for i, regex in enumerate(RE_MODENAMES):
        if re.findall(regex, mode_name, flags=re.I):
            base_symbol.append(MODAL_SERIES_KEYS[i])

    if len(base_symbol) > 1:
        raise ArgumentError(f"Too many modal names in {base_symbol=}.")
    if not base_symbol:
        base_symbol = [IONIAN]

    i = MODAL_SERIES_KEYS.index(base_symbol.pop())
    d = HEPTATONIC_SCALES[DIATONIC]
    mode_pattern = rotate_interval_structure(d, i)
    naturals = re.findall(RE_NATURAL_INTERVAL, mode_name, flags=re.I)
    altereds = re.findall(RE_ALTERED_INTERVAL, mode_name, flags=re.I)
    additions = re.findall(RE_ADDED_INTERVAL, mode_name, flags=re.I)
    subtractions = re.findall(RE_SUBTRACTED_INTERVAL, mode_name, flags=re.I)
    substitutions = naturals + altereds
    normal_intervals = get_heptatonic_interval_names(mode_pattern)
    collation: list[str] = []
    for interval in normal_intervals:
        found = False
        for substitution in substitutions:
            d1 = list(x for x in interval if x.isdigit())
            d2 = list(x for x in substitution if x.isdigit())
            if d1 == d2:
                found = True
                collation.append(substitution)
        if not found:
            collation.append(interval)

    for addition in additions:
        collation.append(addition)
    for subtraction in subtractions:
        if subtraction in collation:
            collation.remove(subtraction)
    return sort_interval_names(collation)


def resolve_scale_alias(scale_name: str) -> tuple[str, str]:
    '''
    Attempt to turn a scale alias symbol into a canonical scaleform pair.

    If the scale name is not a variant of a known alias, then this function
    tries to fall back to ``resolve_modal_name`` before raising an error.

    Parameters
    ----------
    scale_name : str
        A symbol that represents a different name for a scale in the library.

    Returns
    -------
    tuple[str, str]
        A pair consisting of the canonical scale and mode names for the given
        alias.

    Raises
    ------
    ArgumentError
        If the scale alias cannot be parsed within the confines of the system.
    '''
    # TODO tests
    for _, regex, _id in SCALE_ALIASES:
        if re.match(regex, scale_name, flags=re.I):
            return _id
    try:
        intervals = resolve_modal_name(scale_name)
        structure = convert_interval_names_to_integers(intervals)
        pattern = resolve_scale_pattern(structure)
        return (pattern[SCALE_NAME], pattern[MODE_NAME])
    except AristoxenusError as e:
        raise ArgumentError(f"Unable to parse scale name {scale_name=}.") from e
    


def resolve_generic_scale_request(scale_name: str) -> tuple[str, str, str]:
    '''
    Resolve a generic key-and-scale symbol and return a tuple containing 
    the key, the parent scale, and the modal rotation implied in the symbol.

    A generic key-and-scale symbol consists of a valid scale-name symbol, 
    which may be a canonical scale name + mode name, or a mode name, or a 
    mode name + interval modifications, or an alias, or a variant of any of 
    the above. The key-and-scale symbol may also contain a keynote, but if
    one is not provided, 'C' will be used.

    E.g.:

    "E augmented lydian"    (canonical scale name + mode name)
    "aug lyd"               (implied 'C' keynote, variant on canonical name)
    "E ukranian dorian"     (alias of canonical scale form)
    "E_UkrDor"              (variant of previous)
    "lydian"                (implied 'C' keynote, implied diatonic scale)
    "lydian #5 b7"          (implied 'C' keynote, implied diatonic, with modifications)
    "lyd_#5_b7"             (implied variant of previous)
    
    Parameters
    ----------
    scale_name : str
        A string representing a scale form. This may contain a keynote for the
        tonic of the scale, but if the keynote is absent, then 'C' will be used.

    Returns
    -------
    tuple[str, str, str]
        The tonic note name, plus the names in our canon for the scale and mode
        represented by the scale symbol.
    '''
    if (match := re.match(RE_COMPLETE_CANON_EXPR, scale_name, flags=re.I)) is not None:
        note = match.group(NOTE_NAME) or NATURAL_NAMES[0]
        scale_abbr = match.group(SCALE_NAME)
        mode_abbr = match.group(MODE_NAME)
        scale, mode = "", ""
        for i, name in enumerate(RE_CANON_NAMES):
            if re.match(name, scale_abbr, flags=re.I):
                scale = list(HEPTATONIC_SCALES.keys())[i]
        for i, mode_name in enumerate(RE_MODENAMES):
            if re.match(mode_name, mode_abbr, flags=re.I):
                mode = MODAL_SERIES_KEYS[i]
                
        return note, scale, mode
    
    keynote = re.match(RE_KEYNOTE_EXPR, scale_name)
    if not keynote:
        kn = NATURAL_NAMES[0]
    else:
        kn = keynote.group(NOTE_NAME)
    scale_name =  scale_name.replace(kn, EMPTY_STRING)
    if scale_name == EMPTY_STRING:
        scale_name = IONIAN
    return (kn, *resolve_scale_alias(scale_name))
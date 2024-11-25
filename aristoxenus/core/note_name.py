
import re
from aristoxenus.core.annotations import NoteNameData
from aristoxenus.core.constants import (
    ACCIDENTALS,
    DIATONIC,
    FLAT_SYMBOL,
    HEPTATONIC_SCALES,
    NATURAL_NAMES,
    NOTE_NAME,
    NOTE_NAME_INDEX,
    RE_PARSE_NOTE_NAME,
    SHARP_SYMBOL,
    TONES
)
from aristoxenus.core.errors import (
    StringValidationError,
    ArgumentError
)


def is_enharmonically_natural(note_data: NoteNameData) -> bool:
    '''
    Test whether a note is equivalent to a natural note name, considering 
    the enharmonic equivalence of any accidentals.

    Parameters
    ----------
    note_data : NoteData
        Data about a note name.

    Returns
    -------
    bool
        True, if the note is enharmonically equivalent to a natural.
    '''
    note_data = simplify_note_name(note_data)
    return note_data[ACCIDENTALS] == 0


def encode_note_name(note_data: NoteNameData) -> str:
    '''
    Get a note symbol with the given name and number of accidentals.

    Parameters
    ----------
    note_data : NoteData
        Data about the note name.

    Returns
    -------
    str
        A note symbol with the given name and number of accidentals.
    '''
    note_name = NATURAL_NAMES[note_data[NOTE_NAME_INDEX]]
    accidentals = note_data[ACCIDENTALS]
    if accidentals > 0:
        return note_name + SHARP_SYMBOL * (accidentals)
    return note_name + FLAT_SYMBOL * (-accidentals)


def decode_note_name(note_name: str) -> NoteNameData:
    '''
    For the given note name, return a tuple containing two integers:
    the index of the alphabetic name and the number (+/-) of accidentals.

    Parameters
    ----------
    note_name : str
        A note name with any number of accidentals.

    Returns
    -------
    NoteData
        The index of the alphabetic name, plus the number of accidentals 
        in the note name (a negative number represents flats).

    Raises
    ------
    StringValidationError
        If the note name does not conform to the expected format (e.g. begins
        with an unrecognizable root).
    '''
    name = re.match(RE_PARSE_NOTE_NAME, note_name)
    if name:
        name = name.groupdict()
        accidentals: int = name[ACCIDENTALS].count(
            SHARP_SYMBOL) - name[ACCIDENTALS].count(FLAT_SYMBOL)
        return NoteNameData(
            note_name_index=NATURAL_NAMES.index(name[NOTE_NAME]),
            accidentals=accidentals
        )
    raise StringValidationError(note_name, NOTE_NAME)


def simplify_note_name(note_data: NoteNameData) -> NoteNameData:
    '''
    Take a note name that has accidentals and return the simplest 
    enharmonically-equivalent name. 

    Parameters
    ----------
    note_data: NoteData
        Data about the note name.

    Returns
    -------
    tuple[int, int]
        A tuple with the index of the new name and new accidentals (0 or 1).
    '''
    if note_data[ACCIDENTALS] == 0:
        return note_data
    value = (HEPTATONIC_SCALES[DIATONIC]
             [note_data[NOTE_NAME_INDEX]] + note_data[ACCIDENTALS]) % TONES
    if value in HEPTATONIC_SCALES[DIATONIC]:
        return NoteNameData(
            note_name_index=HEPTATONIC_SCALES[DIATONIC].index(value),
            accidentals=0)
    if note_data[ACCIDENTALS] > 1:
        value -= 1
        return NoteNameData(
            note_name_index=HEPTATONIC_SCALES[DIATONIC].index(value),
            accidentals=1)
    value += 1
    return NoteNameData(
        note_name_index=HEPTATONIC_SCALES[DIATONIC].index(value),
        accidentals=-1)


def split_binomial_note(keynote: NoteNameData) -> tuple[NoteNameData, NoteNameData]:
    '''
    Take a any non-natural note and return the two names that represent
    it enharmonically (e.g. G# -> G#, Ab).

    Parameters
    ----------
    keynote : NoteData
        A note name for which another enharmonic name exists

    Returns
    -------
    tuple[NoteData, NoteData]
        The two enharmonic names that represent the same given name.

    Raises
    ------
    ArgumentError
        If the note name is a natural.
    '''
    if is_enharmonically_natural(keynote):
        raise ArgumentError(
            f"This function is only intended for accidental note names ({keynote=})")
    accidentals = keynote[ACCIDENTALS]
    alpha = keynote[NOTE_NAME_INDEX]
    if accidentals == 1:
        alpha += 1
        accidentals = -1
    elif accidentals == -1:
        alpha -= 1
        accidentals = 1
    return keynote, NoteNameData(note_name_index=alpha, accidentals=accidentals)

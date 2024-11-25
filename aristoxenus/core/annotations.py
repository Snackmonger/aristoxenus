from typing import Optional, TypedDict


class IntervalData(TypedDict):
    ''' 
    Data about a musical interval.
    '''
    absolute: int
    relative: str


class ChordData(TypedDict):
    '''
    Data about a chord's configuration.
    '''
    chord_symbol: str
    note_names: tuple[str, ...]
    interval_names: tuple[str, ...]
    interval_structure: tuple[int, ...]


class NoteNameData(TypedDict):
    ''' 
    Data about a note name.

    Key
    ---
    note_name_index
        The index of the base name in 'CDEFGAB'
    accidentals
        The number of accidentals (+ for sharps, - for flats).
    '''
    note_name_index: int
    accidentals: int


class ChordStyle(TypedDict, total=False):
    '''
    A dictionary of settings for how a chord symbol will appear.

    Keys
    ----
    slash : bool
        A flag that indicates whether the chord will express its inversion
        using slash notation (e.g. 'Emin7/G')
    maj_symbol : str
        A symbol that will be used to indicate 'major' elements in a chord
        (e.g. 'maj' in 'Cmaj7', 'M' in 'CmM7', etc.)
    min_symbol : str
        A symbol that will be used to indicate 'minor' elements in a chord
        (e.g. 'min' in 'Cmin7', 'm' in 'CmM7', etc.)
    dim_symbol : str
        A symbol that will be used to indicate 'diminished' elements in a chord
        (e.g. 'dim' in 'Cdim7', 'o' in 'Co9', etc.)

    '''
    slash: bool
    maj_symbol: str
    min_symbol: str
    dim_symbol: str

class HeptatonicScaleData(TypedDict):
    '''
    A dictionary of information about a heptatonic scale form.

    Keys
    ----
    keynote: str
        The alphabetic note name that orients the scaleform.
    scale_name: str
        The name of the main scale from which this form was derived.
    mode_name: str
        The name of the mode to which the main scale was rotated to derive
        this form, assuming that 'ionian' means 0 rotations, 'dorian' means 1
        rotation, etc.
    interval_structure: tuple[int, ...]
        A collection of integers representing the intervals of the scale form,
        assuming that 0 is the unison.
    interval_names: tuple[str, ...]
        The intervals of the scale form, expressed as Indian interval names 
        (e.g. '#4')
    roman_names: tuple[str, ...]
        The intervals of the scale form, expressed as Roman interval names
        (e.g. '#IV')
    requested_rendering: tuple[str, ...]
        The note names for the scale form, based on the keynote above.
    recommended_keynote: str
        The optimal keynote, which produces note names with the fewest
        accidentals.
    recommended_rendering: tuple[str, ...]
        The optimal note names for the scale form, based on the optimal
        keynote above.
    '''
    keynote: str
    scale_name: str
    mode_name: Optional[str]
    interval_structure: tuple[int, ...]
    interval_names: tuple[str, ...]
    roman_names: tuple[str, ...]
    requested_rendering: tuple[str, ...]
    recommended_keynote: str
    recommended_rendering: tuple[str, ...]
    step_formula: tuple[str, ...]


class ChordSymbolData(TypedDict):
    '''
    A dictionary of information about a chord symbol.

    Keys
    ----
    configuration: dict[str, str]
        A dictionary of sub-symbols that the chord symbol will use,
        where the keys are 'maj_symbol', 'min_symbol', and 'dim_symbol'.
        The default values of each of these is 'maj', 'min', and 'dim',
        respectively.
    interval_names: tuple[str, ...]
        The intervals of the chord, expressed as Indian interval 
        names (e.g. '#4')
    chord_symbol: str
        The string by which the chord is symbolized.
    '''
    configuration: ChordStyle
    interval_names: tuple[str, ...]
    chord_symbol: str


class ScalePatternData(TypedDict):
    '''
    A dictionary of information about a scale pattern identity.

    Keys
    ----
    interval_structure: tuple[int, ...]
        A collection of integers representing the intervals of the scale,
        assuming that 0 is the unison.
    scale_name: str
        The name of the main scale from which this pattern was derived.
    modal_name: str
        The name of the mode to which the main scale was rotated to derive
        this pattern, assuming that 'ionian' means 0 rotations, 'dorian' 
        means 1 rotation, etc. For non-heptatonic patterns, this will be a 
        digit representing the number of rotations.
    aliases: tuple[str, ...]
        A list of any registered aliases for this scale.
    '''
    interval_structure: tuple[int, ...]
    scale_name: str
    mode_name: str
    aliases: tuple[str, ...]


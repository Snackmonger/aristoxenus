"""
Aristoxenus is a back-end for simple music programs. It generates musical 
data of various kinds, which can then be used in your front-end application.
"""

from aristoxenus import api
from aristoxenus.api import (
    endpoints,
    classes
)
from aristoxenus.core import constants
from aristoxenus.core.constants import (
    CLOSE,
    OPEN,
    D2,
    D23,
    D24,
    D3,

    MAJ_SYMBOL,
    MIN_SYMBOL,
    DIM_SYMBOL,

    SUS2,
    SUS4,
    TERTIAL,

    DIATONIC,
    ALTERED,
    HEMITONIC,
    HEMIOLIC,
    DIMINISHED,
    AUGMENTED,
    HARMONIC,
    BISEPTIMAL,
    PALEOCHROMATIC,
    ENIGMATIC,
    NEAPOLITAN,
    HUNGARIAN_MINOR,
    HUNGARIAN,
    HARMONIC_MINOR,
    DOUBLE_HARMONIC,
    PERSIAN,

    IONIAN,
    DORIAN,
    PHRYGIAN,
    LYDIAN,
    MIXOLYDIAN,
    AEOLIAN,
    LOCRIAN,
)
from aristoxenus.api.endpoints import (
    get_chord_from_symbol, 
    get_chord_symbol, 
    get_heptatonic_scale, 
    get_heptatonic_chord
)
from aristoxenus.api.classes import (
    Chord, 
    HeptatonicScale
)
__all__ = [
    "api",
    "classes",
    'endpoints',
    'constants',

    "Chord",
    'HeptatonicScale',

    'get_chord_from_symbol',
    'get_chord_symbol',
    'get_heptatonic_scale',
    'get_heptatonic_chord',

    "CLOSE",
    "OPEN",
    "D2",
    "D23",
    "D24",
    "D3",
    "MAJ_SYMBOL",
    "MIN_SYMBOL",
    "DIM_SYMBOL",
    "SUS2",
    "SUS4",
    "TERTIAL",
    "DIATONIC",
    "ALTERED",
    "HEMITONIC",
    "HEMIOLIC",
    "DIMINISHED",
    "AUGMENTED",
    "HARMONIC",
    "BISEPTIMAL",
    "PALEOCHROMATIC",
    "ENIGMATIC",
    "NEAPOLITAN",
    "HUNGARIAN_MINOR",
    "HUNGARIAN",
    "HARMONIC_MINOR",
    "DOUBLE_HARMONIC",
    "PERSIAN",
    "IONIAN",
    "DORIAN",
    "PHRYGIAN",
    "LYDIAN",
    "MIXOLYDIAN",
    "AEOLIAN",
    "LOCRIAN",
]

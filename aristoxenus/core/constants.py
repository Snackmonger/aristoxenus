'''Constants used in the program.'''

##############
# Raw Values #
##############
NOTES = 7
TONES = 12
NATURAL_NAMES = "CDEFGAB"
OCTAVE_EQUIVALENCE_FACTOR = 2
FREQUENCY_DECIMAL_LIMIT = 3
CENTRAL_REFERENCE_NOTE_NAME = 'A4'
CENTRAL_REFERENCE_NOTE_FREQUENCY = 440
FLAT_SYMBOL = "b"
SHARP_SYMBOL = '#'
SLASH_SYMBOL = "/"
EMPTY_STRING = ''
WHITESPACE = ' '
UNDERSCORE = '_'

############
# Keywords #
############

# Scale names
DIATONIC = 'diatonic'
ALTERED = 'altered'
HEMITONIC = 'hemitonic'
HEMIOLIC = 'hemiolic'
DIMINISHED = 'diminished'
AUGMENTED = 'augmented'
HARMONIC = 'harmonic'
BISEPTIMAL = 'biseptimal'
PALEOCHROMATIC = 'paleochromatic'
ENIGMATIC = 'enigmatic'
NEAPOLITAN = 'neapolitan'
HUNGARIAN = 'hungarian'
HARMONIC_MINOR = 'harmonic_minor'
DOUBLE_HARMONIC = 'double_harmonic'
HUNGARIAN_MINOR = 'hungarian_minor'
PERSIAN = 'persian'
ROMANIAN = 'romanian'

# Heptatonic modal names
IONIAN = 'ionian'
DORIAN = 'dorian'
PHRYGIAN = 'phrygian'
LYDIAN = 'lydian'
MIXOLYDIAN = 'mixolydian'
AEOLIAN = 'aeolian'
LOCRIAN = 'locrian'

# Octatonic scale names
HALF_WHOLE_DIMINISHED = 'half_whole_diminished'
# Barry Harris Scales
MAJ_6_DIMINISHED = 'maj_6_diminished'
MIN_6_DIMINISHED = 'min_6_diminished'
DOM_7_DIMINISHED = 'dom_7_diminished'
DOM_7_FLAT_5_DIMINISHED = 'dom_7_flat_5_diminished'

# Pentatonic scale names
MINOR_PENTATONIC = 'minor_pentatonic'
IN = 'in'
INSEN = 'insen'
IWATO = 'iwato'
PELOG_PENTATONIC = 'pelog_pentatonic'
DOMINANT_PENTATONIC = 'donimant_pentatonic'

# Hexatonic scale names
ISTRIAN = 'istrian'
WHOLE_TONE = 'whole_tone'
BLUES = 'blues'
MAJOR_BLUES = 'major_blues'

# Internal search order for modal names
MODAL_SERIES_KEYS = (
    IONIAN,
    DORIAN,
    PHRYGIAN,
    LYDIAN,
    MIXOLYDIAN,
    AEOLIAN,
    LOCRIAN
)

# Chord terms
ROOT = 'root'
POSITION = 'position'
ROOT_POSITION = 'root_position'
MAIN = 'main'
INVERSION = 'inversion'
EXTENSION = 'extension'
MODIFICATION = 'modification'
SLASH = 'slash'
CLOSE = 'close'
OPEN = 'open'
D2 = 'd2'
D24 = 'd24'
D23 = 'd23'
D3 = 'd3'
TERTIAL = 'tertial'
SUS2 = 'sus2'
SUS4 = 'sus4'

# General musical terms
INTERVAL_STRUCTURE = 'interval_structure'
INTERVAL_NAME = 'interval_name'
INTERVAL_NAMES = 'interval_names'
SCALE_NAME = 'scale_name'
ALIAS_NAME = 'alias_name'
MODE_NAME = 'mode_name'
CHORD_SYMBOL = 'chord_symbol'
CONFIGURATION = 'configuration'
NOTE_NAME = 'note_name'
NOTE_NAMES = 'note_names'
ROMAN_NAME = 'roman_name'
ROMAN_NAMES = 'roman_names'
ACCIDENTALS = 'accidentals'
NOTE_NAME_INDEX = 'note_name_index'
RELATIVE = 'relative'
ABSOLUTE = 'absolute'
MAJ_SYMBOL = 'maj_symbol'
MIN_SYMBOL = 'min_symbol'
DIM_SYMBOL = 'dim_symbol'

##############
# Scaleforms #
##############
HEPTATONIC_SCALES = {
    DIATONIC: (0, 2, 4, 5, 7, 9, 11),
    ALTERED: (0, 1, 3, 4, 6, 8, 10),
    HEMITONIC: (0, 1, 4, 5, 7, 9, 11),
    HEMIOLIC: (0, 3, 4, 5, 7, 9, 11),
    DIMINISHED: (0, 2, 4, 5, 6, 9, 11),
    AUGMENTED: (0, 2, 4, 5, 8, 9, 11),
    HARMONIC: (0, 2, 4, 5, 7, 8, 11),
    BISEPTIMAL: (0, 2, 4, 5, 7, 10, 11),
    PALEOCHROMATIC: (0, 1, 4, 5, 6, 9, 11),
    ENIGMATIC: (0, 1, 4, 6, 8, 10, 11),
    DOUBLE_HARMONIC: (0, 1, 4, 5, 7, 8, 11),
    NEAPOLITAN: (0, 1, 3, 5, 7, 9, 11),
    HUNGARIAN: (0, 3, 4, 6, 7, 9, 10),
    PERSIAN: (0, 1, 4, 5, 6, 8, 11),
    ROMANIAN: (0, 1, 4, 6, 7, 9, 10)
}
BARRY_HARRIS_SCALES = {
    MAJ_6_DIMINISHED: (0, 2, 4, 5, 7, 8, 9, 11),
    MIN_6_DIMINISHED: (0, 2, 3, 5, 7, 8, 9, 11),
    DOM_7_DIMINISHED: (0, 2, 4, 5, 7, 8, 10, 11),
    DOM_7_FLAT_5_DIMINISHED: (0, 2, 4, 5, 6, 8, 10, 11)
}
HEXATONIC_SCALES = {
    ISTRIAN: (0, 1, 3, 4, 6, 7),
    WHOLE_TONE: (0, 2, 4, 6, 8, 10),
    BLUES: (0, 3, 5, 6, 7, 10),
    MAJOR_BLUES: (0, 2, 3, 4, 7, 9)
}
PENTATONIC_SCALES = {
    MINOR_PENTATONIC: (0, 3, 5, 7, 10),
    PELOG_PENTATONIC: (0, 1, 3, 7, 8),
    IN: (0, 1, 5, 7, 8),
    INSEN: (0, 1, 5, 7, 10),
    IWATO: (0, 1, 5, 6, 10),
    DOMINANT_PENTATONIC:  (0, 2, 4, 7, 10)
}

#######################
# Chord Voicing Forms #
#######################
DROP_2_VOICING: tuple[int, ...] = (1,)           # 1573 c e g b -> c g b e
DROP_2_AND_4_VOICING: tuple[int, ...] = (1, 3)   # 1537 c e g b -> c g e b
DROP_2_AND_3_VOICING: tuple[int, ...] = (2,)     # 1375 c e g b -> c e b g
DROP_3_VOICING: tuple[int, ...] = (1, 2)         # 1735 c e g b -> c b e g
SPREAD_TRIAD = DROP_2_VOICING                    # 153  c e g   -> c g e

VOICINGS: dict[str, tuple[int, ...]] = {
        OPEN: DROP_2_VOICING,
        D2: DROP_2_VOICING,
        D3: DROP_3_VOICING,
        D23: DROP_2_AND_3_VOICING,
        D24: DROP_2_AND_4_VOICING
    }

#################
# Chord Symbols #
#################
CHORD_DIM = 'dim'
CHORD_O = 'o'
CHORD_AUG = 'aug'
CHORD_MAJ = 'maj'
CHORD_MAJ_DELTA = 'Δ'
CHORD_HALFDIM_OE = 'ø'
CHORD_MIN = 'min'
CHORD_M_UPPER = 'M'
CHORD_M_LOWER = 'm'
CHORD_PLUS = '+'
CHORD_MINUS = '-'
CHORD_SUS = 'sus'
CHORD_ADD = 'add'
CHORD_NO = 'no'
CHORD_2 = "2"
CHORD_3 = "3"
CHORD_4 = "4"
CHORD_5 = "5"
CHORD_6 = "6"
CHORD_7 = "7"
CHORD_9 = "9"
CHORD_11 = "11"
CHORD_13 = "13"
CHORD_FLAT_2 =  FLAT_SYMBOL + CHORD_2
CHORD_SHARP_2 = SHARP_SYMBOL + CHORD_2
CHORD_FLAT_4 = FLAT_SYMBOL + CHORD_4
CHORD_SHARP_4 = SHARP_SYMBOL + CHORD_4
CHORD_DOUBLE_FLAT_3 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_3
CHORD_FLAT_3 = FLAT_SYMBOL + CHORD_3
CHORD_SHARP_3 = SHARP_SYMBOL + CHORD_3
CHORD_FLAT_5 = FLAT_SYMBOL + CHORD_5
CHORD_DOUBLE_FLAT_5 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_5
CHORD_SHARP_5 = SHARP_SYMBOL + CHORD_5
CHORD_DOUBLE_SHARP_5 = SHARP_SYMBOL + SHARP_SYMBOL + CHORD_5
CHORD_DOUBLE_FLAT_7 = FLAT_SYMBOL + FLAT_SYMBOL + CHORD_7
CHORD_FLAT_7 = FLAT_SYMBOL + CHORD_7
CHORD_MAJOR_SYMBOLS = [CHORD_MAJ, CHORD_M_UPPER, CHORD_MAJ_DELTA]
CHORD_MINOR_SYMBOLS = [CHORD_MIN, CHORD_M_LOWER, CHORD_MINUS]
CHORD_DIM_SYMBOLS = [CHORD_DIM, CHORD_O]
CHORD_AUGMENTED_SYMBOLS = [CHORD_AUG, CHORD_PLUS]
CHORD_HALFDIM_SYMBOLS = [CHORD_HALFDIM_OE]
CHORD_LEGAL_THIRD = [CHORD_3, CHORD_FLAT_3]
CHORD_LEGAL_SUS = [
    CHORD_SHARP_3,
    CHORD_SHARP_2,
    CHORD_2,
    CHORD_FLAT_2,
    CHORD_DOUBLE_FLAT_3,
    CHORD_SHARP_4,
    CHORD_FLAT_4,
    CHORD_4
]
CHORD_LEGAL_ALT5 = [CHORD_FLAT_5, CHORD_SHARP_5,
                    CHORD_DOUBLE_FLAT_5, CHORD_DOUBLE_SHARP_5]

#######################
# Regular Expressions #
#######################
# Chord symbol parsing
_MAJ = "|".join(CHORD_MAJOR_SYMBOLS)
_MIN = "|".join(CHORD_MINOR_SYMBOLS)
_ROM = 'VII|vii|VI|vi|V|v|IV|iv|III|iii|II|ii|I|i'
_DIM = "|".join(CHORD_DIM_SYMBOLS)
_HD = "|".join(CHORD_HALFDIM_SYMBOLS)
_NAME = f"(?P<{NOTE_NAME}>([A-G](#|b)*|(#|b)*({_ROM})))"
_MAIN = f"(?P<{MAIN}>(?:{_MAJ}|{_MIN}|{_DIM}|aug|\\+|{_HD}))?"
_EXT = f"(?P<{EXTENSION}>((?:{_MAJ})?(13|11|9|7)))?"
_MOD = f'(?P<{MODIFICATION}>(?:[\\w\\d+#]+))?'
_SL = f'(?:\\/(?P<{SLASH}>([A-G](?:#|b)*)))?'
RE_PARSE_NOTE_NAME = f"^(?P<{NOTE_NAME}>[A-G])(?P<{ACCIDENTALS}>(#|b)*)$"
RE_PARSE_INTERVAL_NAME = f'^(?P<{INTERVAL_NAME}>(?:#|b)*(?:[1-7]|1[13]|9))$'
RE_PARSE_ROMAN_NAME = f"^(?P<{ACCIDENTALS}>(#|b)*)(?P<{ROMAN_NAME}>({_ROM}))$"
RE_PARSE_CHORD_SYMBOL = f"^{_NAME}{_MAIN}{_EXT}{_MOD}{_SL}$"

# Scale alias parsing
RE_ION = '(ionian|ion)'
RE_DOR = '(dorian|dor)'
RE_PHR = '(phrygian|phryg|phry|phr)'
RE_LYD = '((?<!mixo)(?:lydian|lyd))'
RE_MIX = '(mixolydian|mixolyd|mixo|mix)'
RE_AEO = '(aeolian|aeol|aeo)'
RE_LOC = '(locrian|locr|loc)'
RE_MODENAMES = (RE_ION, RE_DOR, RE_PHR, RE_LYD, RE_MIX, RE_AEO, RE_LOC)
RE_NATURAL_INTERVAL = f"(?:(?:natural|nat|n)(?: |_)?(?P<{INTERVAL_NAME}>(?:7|6|5|4|3|2|1)))"
RE_ALTERED_INTERVAL = f'(?P<{INTERVAL_NAME}>(?:#|b)+(?:7|6|5|4|3|2|1))'
RE_ADDED_INTERVAL = f"(?:add)(?: |_)?(?P<{INTERVAL_NAME}>(?:b|#)*(?:7|6|5|4|3|2|1))"
RE_SUBTRACTED_INTERVAL = f"(?:no)(?: |_)?(?P<{INTERVAL_NAME}>(?:b|#)*(?:7|6|5|4|3|2|1))"

RE_MAJ = '(major|maj)'
RE_DOM = '(dominant|dom)'
RE_MIN = '(minor|min)'
RE_PENT = '(pentatonic|pent)'
RE_SUP = '(super|sup)'
RE_NAT = '(natural|nat|n)'
RE_MEL = '(melodic|melod|mel)'
RE_HARM = '(harmonic|harmon|harm)'
RE_AUG = '(augmented|aug)'
RE_DIM = '(diminished|dimin|dim)'
RE_ALT = '(altered|alt)'
RE_ULT = '(ultra|ult)'
RE_NEAP = '(neapolitan|neapolit|neapol|neap|nea)'
RE_UKR = '(ukranian|ukran|ukr)'
RE_HNG = '(hungarian|hungar|hung|hun)'
RE_GYP = '(gypsy|gyp|romani|rom)'
J_ = '( |_)*'

RE_DIATONIC = '(diatonic|diaton|dia)'
RE_HEMITONIC = '(hemitonic|hemiton)'
RE_HEMIOLIC = '(hemiolic|hemiol)'
RE_BISEPTIMAL = '(biseptimal|bisept|bs)'
RE_PALEOCHROMATIC = '(paleochromatic|paleo|paleoch|pal)'
RE_ENIGMATIC = '(enigmatic|enigmat|enigma|enig)'
RE_NEAPOLITAN = '(neapolitan|neapolit|neapol|neap)'
RE_DOUBLE_HARMONIC = f'((double|doubl|doub|dub){J_}(harmonic|harmon|harm))'
RE_PERSIAN = '(persian)'
RE_ROMANIAN = '(romanian)'

RE_CANON_NAMES = [
    RE_DIATONIC,
    RE_ALT,
    RE_HEMITONIC,
    RE_HEMIOLIC,
    RE_DIM,
    RE_AUG,
    RE_HARM,
    RE_BISEPTIMAL,
    RE_PALEOCHROMATIC,
    RE_ENIGMATIC,
    RE_DOUBLE_HARMONIC,
    RE_NEAP,
    RE_HNG,
    RE_PERSIAN,
    RE_ROMANIAN
]

RE_KEYNOTE_EXPR = f"(?P<{NOTE_NAME}>[A-G](#|b)*)"
RE_CANON_SCALE_EXPR = f"(?P<{SCALE_NAME}>{'|'.join(RE_CANON_NAMES)})"
RE_MODE_EXPR = f"(?P<{MODE_NAME}>{'|'.join(RE_MODENAMES)})"
RE_COMPLETE_CANON_EXPR = f"({J_}{RE_KEYNOTE_EXPR})?{J_}({RE_CANON_SCALE_EXPR}{J_}{RE_MODE_EXPR}{J_})"

SCALE_ALIASES = (
    ('major', f'^{J_}{RE_MAJ}{J_}$', (DIATONIC, IONIAN)),
    ('dominant', f'^{J_}{RE_DOM}{J_}$', (DIATONIC, MIXOLYDIAN)),
    ('minor', f'^{J_}{RE_MIN}{J_}$', (DIATONIC, AEOLIAN)),

    ('major pentatonic', f'^{J_}{RE_MAJ}{J_}{RE_PENT}{J_}$', (MINOR_PENTATONIC, '1')),
    ('minor blues', f"{J_}{RE_MIN}{J_}(blues|blu){J_}", (BLUES, '0')),
    ('african pentatonic', f'{J_}(african|afric|afr){J_}{RE_PENT}{J_}', (DOMINANT_PENTATONIC, '0')),
    ('pelog pentatonic', f"{J_}{RE_PHR}{J_}{RE_PENT}{J_}", (PELOG_PENTATONIC, '0')),

    ('super locrian', f'^{J_}{RE_SUP}{J_}{RE_LOC}{J_}$', (ALTERED, IONIAN)),
    ('altered dominant', f'^{J_}{RE_ALT}{J_}{RE_DOM}{J_}$', (ALTERED, IONIAN)),
    ('melodic minor', f'^{J_}{RE_MEL}{J_}{RE_MIN}{J_}$', (ALTERED, DORIAN)),
    ('lydian augmented', f'^{J_}{RE_LYD}{J_}{RE_AUG}{J_}$', (ALTERED, LYDIAN)),
    ('lydian dominant', f'^{J_}{RE_LYD}{J_}{RE_DOM}{J_}$', (ALTERED, MIXOLYDIAN)),
    ('acoustic', f'^{J_}(acoustic|acoust|acou)({J_}scale)?{J_}$', (ALTERED, MIXOLYDIAN)),
    ('aeolian dominant', f'^{J_}{RE_AEO}{J_}{RE_DOM}{J_}$', (ALTERED, AEOLIAN)),
    ('half diminished', f'^{J_}(half){J_}{RE_DIM}{J_}$', (ALTERED, LOCRIAN)),

    ('augmented major', f"^{J_}{RE_AUG}{J_}{RE_MAJ}{J_}$", (AUGMENTED, IONIAN)),
    ('ukrainian dorian', f'^{J_}{RE_UKR}{J_}{RE_DOR}{J_}$', (AUGMENTED, DORIAN)),
    ('romanian minor', f'^{J_}{RE_ROMANIAN}{J_}{RE_MIN}{J_}$', (AUGMENTED, DORIAN)),
    ('phrygian dominant', f'^{J_}{RE_PHR}{J_}{RE_DOM}{J_}$', (AUGMENTED, PHRYGIAN)),
    ('freygish', f'^{J_}freygish{J_}$', (AUGMENTED, PHRYGIAN)),
    ('super locrian bb7', f'^{J_}{RE_SUP}{J_}{RE_LOC}{J_}bb7{J_}$', (AUGMENTED, LOCRIAN)),
    ('altered diminished', f'^{J_}{RE_ALT}{J_}{RE_DIM}{J_}bb7{J_}$', (AUGMENTED, LOCRIAN)),

    ('ultra locrian', f'^{J_}{RE_ULT}{J_}{RE_LOC}{J_}$', (HEMIOLIC, DORIAN)),
    ('altered diminished', f'^{J_}{RE_ALT}{J_}{RE_DIM}{J_}$', (HEMIOLIC, DORIAN)),
    ('neapolitan minor', f'^{J_}{RE_NEAP}{J_}{RE_MIN}{J_}$', (HEMIOLIC, PHRYGIAN)),
    ('mixolydian augmented', f'^{J_}{RE_MIX}{J_}{RE_AUG}{J_}$', (HEMIOLIC, MIXOLYDIAN)),
    ('gypsy minor', f'^{J_}{RE_GYP}{J_}{RE_MIN}{J_}$', (HEMIOLIC, AEOLIAN)),
    ('locrian dominant', f'^{J_}{RE_LOC}{J_}{RE_DOM}{J_}$', (HEMIOLIC, LOCRIAN)),
    ('harmonic major', f'^{J_}{RE_HARM}{J_}{RE_MAJ}{J_}$', (HARMONIC, IONIAN)),

    ('neapolitan major', f'^{J_}{RE_NEAP}{J_}{RE_MAJ}{J_}$', (NEAPOLITAN, IONIAN)),
    ('leading whole tone', f'^{J_}(leading|lead){J_}(whole|wh){J_}tone{J_}$', (NEAPOLITAN, DORIAN)),
    ('lydian augmented #6', f'^{J_}{RE_LYD}{J_}{RE_AUG}{J_}#6{J_}$', (NEAPOLITAN, DORIAN)),
    ('lydian augmented dominant', f'^{J_}{RE_MIX}{J_}{RE_AUG}{J_}{RE_DOM}{J_}$', (NEAPOLITAN, PHRYGIAN)),
    ('lydian dominant b6', f'^{J_}{RE_LYD}{J_}{RE_DOM}{J_}b6{J_}$', (NEAPOLITAN, LYDIAN)),
    ('major locrian', f'^{J_}{RE_MAJ}{J_}{RE_LOC}{J_}#6{J_}$', (NEAPOLITAN, MIXOLYDIAN)),
    ('half diminished b4', f'^{J_}(half){J_}{RE_DIM}{J_}b4{J_}$', (NEAPOLITAN, AEOLIAN)),
    ('altered dominant #2', f'^{J_}{RE_ALT}{J_}{RE_DOM}{J_}#2{J_}$', (NEAPOLITAN, AEOLIAN)),
    ('altered dominant bb3', f'^{J_}{RE_ALT}{J_}{RE_DOM}{J_}bb3{J_}$', (NEAPOLITAN, LOCRIAN)),

    ('byzantine', f'^{J_}(byzantine|byzant|byzan|byz){J_}$', (DOUBLE_HARMONIC, IONIAN)),
    ('gypsy major', f'^{J_}{RE_GYP}{J_}{RE_MAJ}{J_}$', (DOUBLE_HARMONIC, IONIAN)),
    ('hungarian minor', f'^{J_}{RE_HNG}{J_}{RE_MIN}{J_}$', (DOUBLE_HARMONIC, LYDIAN)),
    ('ultra phrygian', f'^{J_}{RE_ULT}{J_}{RE_PHR}{J_}$', (DOUBLE_HARMONIC, PHRYGIAN)),

    ('hungarian major', f"{J_}{RE_HNG}{J_}{RE_MAJ}{J_}$", (HUNGARIAN, IONIAN)),
    ('altered diminished bb6', f"{J_}{RE_ALT}{J_}{RE_DIM}{J_}bb6{J_}$", (HUNGARIAN, DORIAN)),
    ('harmonic minor b5', f"{J_}{RE_HARM}{J_}{RE_MIN}{J_}b5{J_}$", (HUNGARIAN, PHRYGIAN)),
    ('altered dominant natural 6', f"{J_}{RE_ALT}{J_}{RE_DOM}{J_}{RE_NAT}{J_}6{J_}$", (HUNGARIAN, LYDIAN)),
    ('melodic minor #5', f"{J_}{RE_MEL}{J_}{RE_MIN}{J_}$", (HUNGARIAN, MIXOLYDIAN)),
    ('ukranian dorian b2', f"{J_}{RE_UKR}{J_}{RE_DOR}{J_}b2{J_}$", (HUNGARIAN, AEOLIAN)),
    ('lydian augmented #3', f"{J_}{RE_LYD}{J_}{RE_AUG}{J_}#3{J_}$", (HUNGARIAN, LOCRIAN)),

    ('lydian dominant b9', f"^{J_}{RE_LYD}{J_}{RE_DOM}{J_}b9{J_}$", (ROMANIAN, IONIAN) ),
    ('super lydian augmented natural 6', f"^{J_}{RE_SUP}{J_}{RE_LYD}{J_}{RE_AUG}{J_}{RE_NAT}{J_}6{J_}$", (ROMANIAN, DORIAN)),
    ('super locrian bb6', f"^{J_}{RE_SUP}{J_}{RE_LOC}{J_}bb6{J_}$", (ROMANIAN, LYDIAN)),
    ('jeths', f"^{J_}jeth('s|s|s'|s's)?{J_}(mode){J_}$", (ROMANIAN, MIXOLYDIAN)),
    ('melodic minor b5', f"^{J_}{RE_MEL}{J_}{RE_MIN}{J_}b5{J_}$", (ROMANIAN, MIXOLYDIAN)),
    ('jazz minor b5', f"^{J_}jazz{J_}{RE_MIN}{J_}b5{J_}$", (ROMANIAN, MIXOLYDIAN)),
    ('javanese b4', f"^{J_}(javanese|java){J_}b4{J_}$", (ROMANIAN, AEOLIAN)),
    ('superphrygian natural 6', f"^{J_}{RE_SUP}{J_}{RE_PHR}{J_}{RE_NAT}{J_}6{J_}$", (ROMANIAN, AEOLIAN)),
    ('lydian augmented b3', f"^{J_}{RE_LYD}{J_}{RE_AUG}{J_}b3{J_}$", (ROMANIAN, LOCRIAN))
)

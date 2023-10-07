'''Strings used as dictionary keywords in the program.'''

# Basic interface terms
NOTE_NAME: str = 'note_name'
FREQUENCY: str = 'frequency'
ACCIDENTAL_NOTES: str = 'accidental_notes'
OCTAVE: str = 'octave'
CHROMATIC: str = 'chromatic'
SCIENTIFIC: str = 'scientific'
PLAIN: str = 'plain'
INTERVAL_STRUCTURE: str = 'interval_structure'
INTERVAL: str = 'interval'
PREFERRED_NAME: str = 'preferred_name'
MODAL_NAME: str = 'modal_name'
RECOGNIZED_NAMES: str = 'recognized_names'
CHORD_SYMBOL: str = 'chord_symbol'

# Modal names
IONIAN: str = 'ionian'
DORIAN: str = 'dorian'
PHRYGIAN: str = 'phrygian'
LYDIAN: str = 'lydian'
MIXOLYDIAN: str = 'mixolydian'
AEOLIAN: str = 'aeolian'
LOCRIAN: str = 'locrian'

MODAL_NAME_SERIES: tuple[str, ...] = (IONIAN,
                                DORIAN,
                                PHRYGIAN,
                                LYDIAN,
                                MIXOLYDIAN,
                                AEOLIAN,
                                LOCRIAN)

# Polyads
MONAD: str = 'monad'
DYAD: str = 'dyad'
TRIAD: str = 'triad'
TETRAD: str = 'tetrad'
PENTAD: str = 'pentad'
HEXAD: str = 'hexad'
HEPTAD: str = 'heptad'
OCTAD: str = 'octad'
ENNEAD: str = 'nonad'
DECAD: str = 'decad'
HENDECAD: str = 'undecad'
DUODECAD: str = 'duodecad'

# Scale structures
MONOTONIC: str = 'monotonic'
DITONIC: str = 'ditonic'
TRITONIC: str = 'tritonic'
TETRATONIC: str = 'tetratonic'
PENTATONIC: str = 'pentatonic'
HEXATONIC: str = 'hexatonic'
HEPTATONIC: str = 'heptatonic'
OCTATONIC: str = 'octatonic'
ENNEATONIC: str = 'enneatonic'
DECATONIC: str = 'decatonic'
HENDECATONIC: str = 'hendecatonic'
DUODECATONIC: str = 'duodecatonic'

# Chord structures
PRIMAL: str = 'primal'
SECUNDAL: str = 'secundal'
TERTIAL: str = 'tertial'
QUARTAL: str = 'quartal'
QUINTAL: str = 'quintal'
SEXTAL: str = 'sextal'
SEPTIMAL: str = 'septimal'
OCTONAL: str = 'octonal'
NONAL: str = 'nonal'
DECIMAL: str = 'decimal'
UNDECIMAL: str = 'undecimal'
DUODECIMAL: str = 'duodecimal'

# Scale identifiers
DIATONIC_LABEL: str = 'diatonic'
ALTERED_LABEL: str = 'altered'
HEMITONIC_LABEL: str = 'hemitonic'
HEMIOLIC_LABEL: str = 'hemiolic'
DIMINISHED_LABEL: str = 'diminished'
AUGMENTED_LABEL: str = 'augmented'
HARMONIC_LABEL: str = 'harmonic'
BISEPTIMAL_LABEL: str = 'biseptimal'
PALEOCHROMATIC_LABEL: str = 'paleochromatic'

# Groups of above
HEPTATONIC_ORDER: tuple[str, ...] = (DIATONIC_LABEL,
                                      ALTERED_LABEL,
                                      HEMITONIC_LABEL,
                                      HEMIOLIC_LABEL,
                                      DIMINISHED_LABEL,
                                      AUGMENTED_LABEL,
                                      HARMONIC_LABEL,
                                      BISEPTIMAL_LABEL,
                                      PALEOCHROMATIC_LABEL)

NUMERATION: tuple[tuple[str, str, str], ...] = (
    (MONAD, MONOTONIC, PRIMAL),
    (DYAD, DITONIC, SECUNDAL),
    (TRIAD, TRITONIC, TERTIAL),
    (TETRAD, TETRATONIC, QUARTAL),
    (PENTAD, PENTATONIC, QUINTAL),
    (HEXAD, HEXATONIC, SEXTAL),
    (HEPTAD, HEPTATONIC, SEPTIMAL),
    (OCTAD, OCTATONIC, OCTONAL),
    (ENNEAD, ENNEATONIC, NONAL),
    (DECAD, DECATONIC, DECIMAL),
    (HENDECAD, HENDECATONIC, UNDECIMAL),
    (DUODECAD, DUODECATONIC, DUODECIMAL)
)

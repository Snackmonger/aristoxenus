'''Strings used as dictionary keywords in the program.'''

NOTE_NAME: str = 'note_name'
FREQUENCY: str = 'frequency'
ACCIDENTAL_NOTES: str = 'accidental_notes'
OCTAVE: str = 'octave'
CHROMATIC: str = 'chromatic'
INTERVAL_STRUCTURE: str = 'interval_structure'
INTERVAL: str = 'interval'
PREFERRED_NAME: str = 'preferred_name'
MODAL_NAME: str = 'modal_name'
RECOGNIZED_NAMES: str = 'recognized_names'
CHORD_SYMBOL: str = 'chord_symbol'

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
QUARTAL: str = 'quaral'
QUINTAL: str = 'quintal'
SEXTAL: str = 'sextal'
SEPTIMAL: str = 'septimal'
OCTONAL: str = 'octonal'
NONAL: str = 'nonal'
DECIMAL: str = 'decimal'
UNDECIMAL: str = 'undecimal'
DUODECIMAL: str = 'duodecimal'

# Scale identifiers
DIATONIC_LABEL = 'diatonic'
ALTERED_LABEL = 'altered'
HEMITONIC_LABEL = 'hemitonic'
HEMIOLIC_LABEL = 'hemiolic'
DIMINISHED_LABEL = 'diminished'
AUGMENTED_LABEL = 'augmented'
HARMONIC_LABEL = 'harmonic'
BISEPTIMAL_LABEL = 'biseptimal'
PALEOCHROMATIC_LABEL = 'paleochromatic'

numeration: tuple[tuple[str, str, str], ...] = (
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
import aristoxenus as arx

def test_chord_consistency_1():
    # Chords derived from scales use the explicit data of the scale to
    # populate their own data. Chords derived from symbols must populate
    # their data by extrapoliation, and have no knowledge of their parent
    # scale form. This test makes sure that different methods of deriving
    # chord forms always produce identical data.
    chord_from_symbol = arx.get_chord_from_symbol('Emin7/G')
    chord_from_chord_scale = arx.get_heptatonic_chord("E", mode_name='dorian',
                                    chord_inversion=1,
                                    chord_size=4,
                                    chord_style={'slash': True}
                                    )
    obj_chord = (
        arx.HeptatonicScale('E', mode_name='dorian')
            .get_tertial_tetrad(1)
            .invert(1)
            .use_slash(True)
    )
    obj_chord_from_symbol = arx.Chord.from_symbol("Emin7/G").to_ChordData()
    chord_from_obj = obj_chord.to_ChordData()
    assert chord_from_symbol == chord_from_chord_scale 
    assert chord_from_symbol == obj_chord_from_symbol
    assert chord_from_symbol == chord_from_obj

def test_chord_consistency_2():
    # Ensure that the chord is consistent across different scale sources.
    # e.g. that when E is the root of a ii, iii, vi chord, it is not being
    # derived incorrectly from different scale rotations.
    chord_from_symbol = arx.get_chord_from_symbol('Emin7/G')
    chord_from_chord_scale = arx.get_heptatonic_chord(
        mode_name='ionian', 
        chord_degree=3,
        chord_inversion=1,
        chord_size=4,
        chord_style={'slash': True}
        )
    obj_chord = (
        arx.HeptatonicScale(mode_name='ionian')
            .get_tertial_tetrad(3)
            .invert(1)
            .use_slash(True)
    )
    chord_from_obj = obj_chord.to_ChordData()
    assert chord_from_symbol == chord_from_chord_scale
    assert chord_from_symbol == chord_from_obj
''' 
Type hint annotations used in the program.
'''
from typing import TypedDict

class HeptatonicScaleForm(TypedDict):
    '''
    Dictionary mapping the response from ``api.heptatonic_scale_form``
    API endpoint.
    '''
    keynote: str
    scale_name: str
    modal_name: str
    interval_structure: tuple[int, ...]
    interval_scale: tuple[str, ...]
    requested_rendering: tuple[str, ...]
    recommended_keynote: str
    recommended_rendering: tuple[str, ...]

class SimpleChord(TypedDict):
    '''
    Dictionary of chord structure information.
    
    (Segment of the ``api.heptatonic_chord_scale`` response)
    '''
    note_names: tuple[str, ...]
    interval_structure: tuple[int, ...]
    interval_names: tuple[str, ...]
    
class TriadProfile(TypedDict):
    ''' 
    Dictionary of triad variants.
    
    (Segment of the ``api.heptatonic_chord_scale`` response)
    '''
    close_voicing: SimpleChord
    open_voicing: SimpleChord

class TetradProfile(TypedDict):
    ''' 
    Dictionary of tetrad variants.
    
    (Segment of the ``api.heptatonic_chord_scale`` response)
    '''
    close_voicing: SimpleChord
    drop_2_voicing: SimpleChord
    drop_3_voicing: SimpleChord
    drop_2_and_3_voicing: SimpleChord
    drop_2_and_4_voicing: SimpleChord

class TetradInversions(TypedDict):
    ''' 
    Dictionary of tetrad inversions and their variants.
    
    (Segment of the ``api.heptatonic_chord_scale`` response)
    '''
    chord_symbol: str
    root_note: str
    scale_degree: str
    roman_degree: str
    root_position: TetradProfile
    first_inversion: TetradProfile
    second_inversion: TetradProfile
    third_inversion: TetradProfile

class TriadInversions(TypedDict):
    ''' 
    Dictionary of triad inversions and their variants.

    (Segment of the ``api.heptatonic_chord_scale`` response)
    '''
    chord_symbol:str
    root_note: str
    scale_degree: str
    roman_degree: str
    root_position: TriadProfile
    first_inversion: TriadProfile
    second_inversion: TriadProfile

class HeptatonicChordScale(TypedDict):
    '''
    Dictionary mapping the response from ``api.heptatonic_chord_scale``
    API endpoint.
    '''
    keynote: str
    scale_name: str
    modal_name: str
    tertial_triads: tuple[TriadInversions, ...]
    tertial_tetrads: tuple[TetradInversions, ...]
''' 
Type hint annotations used in the program.
'''
from typing import TypedDict

class HeptatonicScaleFormAPIResponse(TypedDict):
    '''
    Dictionary mapping the response from ``heptatonic_scale_form``
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

class Chord(TypedDict):
    '''
    Dictionary of chord structure information.
    '''
    note_names: tuple[str, ...]
    interval_structure: tuple[int, ...]
    interval_names: tuple[str, ...]
    
class TriadProfile(TypedDict):
    ''' 
    Dictionary of triad variants.
    '''
    close_voicing: Chord
    open_voicing: Chord

class TetradProfile(TypedDict):
    ''' 
    Dictionary of tetrad variants.
    '''
    close_voicing: Chord
    drop_2_voicing: Chord
    drop_3_voicing: Chord
    drop_2_and_3_voicing: Chord
    drop_2_and_4_voicing: Chord

class TetradInversions(TypedDict):
    ''' 
    Dictionary of tetrad inversions and their variants.
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
    '''
    chord_symbol:str
    root_note: str
    scale_degree: str
    roman_degree: str
    root_position: TriadProfile
    first_inversion: TriadProfile
    second_inversion: TriadProfile

class HeptatonicChordScaleAPIResponse(TypedDict):
    '''
    Dictionary mapping the response from ``heptatonic_chord_scale``
    API endpoint.
    '''
    keynote: str
    scale_name: str
    modal_name: str
    triads: tuple[TriadInversions, ...]
    tetrads: tuple[TetradInversions, ...]
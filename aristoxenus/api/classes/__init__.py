'''
Aristoxenus Behaviour-Oriented API
----------------------------------

This module provides a set of object-oriented interfaces for manipulating
musical data using the functions in the ``core`` module.

For a more data-oriented interface for accessing the ``core`` functions,
see the endpoint functions available in the ``api`` module.
'''
from aristoxenus.api.classes.chord import Chord
from aristoxenus.api.classes.heptatonic_scale import HeptatonicScale

__all__ = [
    'Chord', 
    'HeptatonicScale'
]
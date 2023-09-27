===========
ARISTOXENUS
===========

Musical Manipulation Tool Changelog

Version 0.11: 27/09/2023
------------------------

    Added models for pitch structures with methods for rotation and easy collation of variants. 

    Refined some of the bitwise operations a bit.

    Begin replacing docstrings with something more consistent.

    Reorganize the code a bit. Still not totally happy, but it's a bit easier to manage.

    Spend a lot of time fighting with the linter about the subclass returned from the decorated
    dunder method `__iadd__` .... the decorator needs to declare a return type, but the linter
    doesn't recognize which subclass of pitch structure has been returned. Still needs work._


Version 0.1: 14/09/2023
-----------------------

    A few functions involved in the operation of the program so far:

    best_heptatonic_scale
        Choose the best name for a given interval structure and tonic note name.
    force_heptatonic_scale
        Force a given heptatonic interval structure to follow ABCDEFG nomenclature regardless of any accidentals.
    parse_chord_symbol
        Attempt to generate an interval map from the sub-symbols in a given chord symbol (e.g. Em7b5 >> 0b10001001001)
    encode_frequency / decode_frequency
        Translate scientific notes (e.g. A4) of any accidental type (#, b, #/b) to frequencies (e.g. 440 hz) and vice versa.
    parse_chord_symbol
        Generate



====================================
ARISTOXENUS MUSIC MANIPULATION SUITE
====================================
Generate and manipulate musical structures in various representations.

Version 0.0.1
-------------
Aristoxenus is a hobby project that I use as a long-term way of motivating
my programming learning. "Aristoxenus" was an Ancient Greek musical theorist 
whose work shaped the understanding of generations of musicians, and this project 
is named in his honour. 

Version 0.0.1 aims to bring this hobby project into an --if not professional-- 
at least useable and well-documented state. 

Checklist:

- All functions in the src.functions subpackage have complete docstrings in NumPy format.
- All errors raised in the src.functions subpackage have been documented in context, and are subclasses of a common library parent exception.
- All docstrings in the src.functions subpackage have thorough code examples that pass doctests.
- Sphinx documentation is working properly and looks nice.
- All constants, symbols, keywords, etc. have unique identifiers across all src.data modules to prevent name collisions.

    
    - Keywords have their name
    - Integers representing intervals are suffixed _INTV
    - Integers representing chords are suffixed _CH
    - Integers representing scales are suffixed _SCALE

MASSIVE TODO: The behaviour of LEGAL_ROOT_NAMES is all wrong. We want to be able to
make chords with Ebb as a root, because we allow for scales like C Db Ebb, etc. 

Features
++++++++



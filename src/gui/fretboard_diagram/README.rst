Fretboard Diagram App
---------------------

This app demonstrates how Aristoxenus can be used as a back-end for a musical
tool with a GUI. I wrote it to help me learn tkinter better, and I think I was
successful in that. Tkinter is an ugly framework and I am always unsure whether
ugliness in my code is because of my poor coding, or because tkinter is simply
ugly. So, I don't think that this program is as clean as it could be, but it's
definitely an improvement on my older tkinter apps.

This program needs to be extracted and re-organized as its own python project.
------------------------------------------------------------------------------

- Track the dependencies of the project: 
    Which parts of aristoxenus does the program rely on? Would those parts be easily accessible if Aristoxenus were pip installed as a pypackage?
    What kind of external dependencies does the GUI project rely on?
    What kind of external dependencies does Aristoxenus rely on?

It's time to make the Aristoxenus back-end into a standalone package. 
---------------------------------------------------------------------
Aristoxenus is still very incomplete, but it's clear from the GUI and FILEOUT modules
that we're already thinking about leveraging what we have in making useful applications.

- Remove GUI constants from the aristoxenus/data/ files (constants, keywords, style information, annotations)
- Make sure that any Aristoxenus constants used by the GUI are available in the library's base __init__.py so we can do things like ``import aristoxenus as arx; x = arx.BINOMIALS;``
- Make sure that any functions used by the GUI are available in one way or another through the interface module

Look at the tkinter package: 
- all const are import * in the main __init__.py
- there are a few modules
- almost all classes are defined in the __init__.py

So, basically, we want to take the aristoxenus __init__.py and
- from data import \* (in data/__init__.py we have from constants import \*, from chord_symbols import \*, etc)
- from interface import *

Then in our GUI we can just
- import aristoxenus
- chromatic = aristoxenus.get_cromatic("G#", aristoxenus.DIATONIC_SCALE)

This means that we need to make sure that keyword constants and value contstants are kept separate. 
Maybe it is time to implement keyword enums... 

Interface
---------
I'd like anything useful in the back end to be routed through a friendly interface. Someday, we can turn this into a fastAPI application 
and fetch relevant content through the web.

This means that we should try/catch our calls to the main functions, and always
return a response that embeds either the requested data or an error code.

We should research a little bit about standard ways to format an API response,
if we're thinking of making a web API at some point.


The CLI
-------

The CLI is useful for testing things, so I'd like to keep it a part of the main library. Maybe there's a GUI we could write that's appropriate to 
library-internal things... I'm not sure whether it's necessary or useful.


DEPENDENCIES
------------

Going through the GUI app:

config.py takes from data.keywords, but only terms that should be in the GUI constants anyway
app.py takes from interface, src.models, data.data_models, data.annotations, data.keywords
    - Interface and data_models should stay part of the central library. (data_models are endpoint dataclasses, so they are useful to 
    provide to the user regardless of what the front end does with them)
    - annotations and keywords specific to the GUI should move there 
    - the models are just fretboard diagrams, so they should be part of the fretboard GUI
widgets.py takes from keywords, annotations, errors, interface, models, diagrams
    - see above, with the note that GUI specific errors get moved to the GUI, and ax errors stay with the library.
functions.py has no aristoxenus dependencies



FILE STRUCTURE
--------------

- data/data_models can become src/models, since we will let the front end worry about models for diagrams, sheet music, etc.
- data/instrument_config can be part of the GUI, get rid of it from the library
- src/gui and src/models are part of the frontend, so get rid of them from the library
- src/fileout should be a separate frontend application with its own dependencies

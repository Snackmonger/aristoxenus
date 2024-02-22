

from data.keywords import DIATONIC, IONIAN
from src import interface

from src.models import data_structures

x = data_structures.HeptatonicRendering(**interface.render_heptatonic_form(DIATONIC, IONIAN, "C"))


print(vars(x))
from src.interface import HeptatonicStructure
from rich import print

my_scale = HeptatonicStructure("hemiolic", "lydian", "D")


for degree in range(1, 8):
    print(my_scale.chord_scale(degree, notes=4))


from src.parsing import remove_chord_prefix


print(remove_chord_prefix("bbVIImaj7b13"))
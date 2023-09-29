
from src import permutation
from src import rendering
from src import nomenclature
from data import constants







def generate_intmap():
    x = permutation.extend_structure(0b101010110101)
    y = nomenclature.scientific_range(constants.BINOMIALS)
    z = rendering.render(x, y)
    print(z)
        

def chordify():
    print(permutation.chordify(0b101010110101))
    print(permutation.chordify(0b101010110101, 4))
    print(permutation.chordify(0b101010110101, 5))
    print(permutation.chordify(0b101010110101, 6))
    print(permutation.chordify(0b101010110101, 7))



def spread_triad():
    x = permutation.spread_triad(0b10010001)
    print(bin(x))
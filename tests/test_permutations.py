
from src import permutation
from src import rendering
from src import nomenclature
from data import constants
from data import intervallic_canon







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
    print([bin(item) for item in permutation.chordify(0b101010110101, 14, 16)])



def spread_triad():
    x = permutation.spread_triad(0b10010001)
    print(bin(x))


from src import rendering



def drop_voicing():
    print(bin(0b100010010001))
    print(rendering.render(0b100010010001))

    x =  permutation.drop_voicing(0b100010010001, constants.DROP_2) 
    print(bin(x))
    print(rendering.render(x))

    x =  permutation.drop_voicing(0b100010010001, constants.DROP_3) 
    print(bin(x))
    print(rendering.render(x))

    x =  permutation.drop_voicing(0b100010010001, constants.DROP_2_AND_4) 
    print(bin(x))
    print(rendering.render(x))

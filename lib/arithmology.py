'''
Arithmology
-----------
Tool for translating numerical terms into the numbers they represent and 
vice versa.

There are six categories of terms:

Polyad: Greek nouns for describing n-sized groups
Tonal: Greek adjectives describing structures with n-tones
Basal: Latin adjectives describing structures of every n-th member of a group
Cardinal: English numerals for counting n-number of items
Ordinal: English numerals describing n-th position in a sequence
Uple: Latin adjectives describing n-sized groups

Examples
--------
Get a keyword by encoding a number in a particular category:
>>> Arithmology.encode(1, "ordinal")
'one'
>>> Arithmology.encode(2, "tonal")
'ditonic'
>>> Arithmology.encode(3, "polyad")
'triad'
>>> Arithmology.encode(7, "basal")
'septimal'
>>> Arithmology.encode(5, "uple")
'quntuple'

Get a number by decoding a keyword:
>>> Arithmology.decode("triskaidecad")
13
>>> Arithmology.decode("four")
4
>>> Arithmology.decode("seventh")
7
>>> Arithmology.decode("pentatonic")
5
>>> Arithmology.decode("tertial")
3
>>> Arithmology.decode("triple")
3

Get a keyword by encoding a number using a shortcut method:
>>> Arithmology.polyad(3)
'triad'
>>> Arithmology.tonal(7)
'heptatonic'
>>> Arithmology.ordinal(13)
'thirteenth'
>>> Arithmology.uple(8)
'octuple'
>>> Arithmology.cardinal(6)
'six'
'''

class Arithmology:
    '''
    This class is a thin wrapper around a two dimensional array of terms for
    numbers in various categories. 
    '''
    __table = [
        ['polyad', 'tonal', 'basal', 'cardinal', 'ordinal', 'uple'],
        ['monad', 'monotonic', 'primal', 'one', 'first', 'single'],
        ['dyad', 'ditonic', 'secundal', 'two', 'second', 'double'],
        ['triad', 'tritonic', 'tertial', 'three', 'third', 'triple'],
        ['tetrad', 'tetratonic', 'quartal', 'four', 'fourth', 'quadruple'],
        ['pentad', 'pentatonic', 'quintal', 'five', 'fifth', 'quintuple'],
        ['hexad', 'hexatonic', 'sextal', 'six', 'sixth', 'sextuple'],
        ['heptad', 'heptatonic', 'septimal', 'seven', 'seventh', 'septuple'],
        ['octad', 'octatonic', 'octonal', 'eight', 'eighth', 'octuple'],
        ['ennead', 'enneatonic', 'nonal', 'nine', 'ninth', 'nonuple'],
        ['decad', 'decatonic', 'decimal', 'ten', 'tenth', 'decuple'],
        ['hendecad', 'hendecatonic', 'undecimal',
            'eleven', 'eleventh', 'hendecuple'],
        ['duodecad', 'duodecatonic', 'duodecimal',
            'twelve', 'twelfth', 'duodecuple'],
        ['triskaidecad', 'triskaidecatonic', 'tredecimal',
            'thirteen', 'thirteenth', 'tredecuple'],
        ['tettarakaidecad', 'tettarakaidecatonic', 'quattuordecimal',
            'fourteen', 'fourteenth', 'quattuordecuple'],
        ['pentekaidecad', 'pentekaidecatonic', 'quindecimal',
            'fifteen', 'fifteenth', 'quindecuple']
    ]

    @staticmethod
    def columns() -> list[str]:
        '''Return the headings of the table.'''
        return Arithmology.__table[0]

    @staticmethod
    def rows() -> list[list[str]]:
        '''Return the values of the table'''
        return [Arithmology.__table[x] for x in range(1, len(Arithmology.__table))]

    @staticmethod
    def decode(keyword: str) -> int:
        for i, row in enumerate(Arithmology.__table):
            for word in row:
                if keyword == word:
                    return i
        raise ValueError(f"Unknown keyword: {keyword}")

    @staticmethod
    def encode(category: str, number: int) -> str:
        if not category in Arithmology.columns():
            raise ValueError(f"Unknown category: {category}")
        if not number in range(1, len(Arithmology.__table)):
            raise ValueError(f"Cannot encode number: {number}")
        i = Arithmology.columns().index(category)
        return Arithmology.__table[number][i]

    @staticmethod
    def polyad(number: int) -> str:
        return Arithmology.encode("polyad", number)

    @staticmethod
    def tonal(number: int) -> str:
        return Arithmology.encode("tonal", number)

    @staticmethod
    def basal(number: int) -> str:
        return Arithmology.encode("basal", number)

    @staticmethod
    def cardinal(number: int) -> str:
        return Arithmology.encode("cardinal", number)

    @staticmethod
    def uple(number: int) -> str:
        return Arithmology.encode("uple", number)

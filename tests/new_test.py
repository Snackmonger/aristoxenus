from src.nomenclature import chromatic, ch_flats, ch_sharps, scientific, sci_sharps, sci_flats
from src.nomenclature import force_heptatonic, best_heptatonic, name_heptatonic_intervals
from src.rendering import render
from src.parsing import parse_chord_symbol
from src.utils import roman_numeral


def test_chromatics():
    '''Test the chromatics'''
    print(chromatic())
    print(ch_flats())
    print(ch_sharps())


def test_scientifics():
    '''Test the scientific'''
    print(scientific())
    print(sci_flats())
    print(sci_sharps())


def test_heptatonic(note_name: str):
    '''Print a major then a minor scale for the given note name.'''
    print(f'Now testing note {note_name}')
    major = 0b101010110101
    minor = 0b10110101101
    print('Force heptatonic')
    print(force_heptatonic(note_name, major))
    print(force_heptatonic(note_name, minor))
    print('Best heptatonic')
    print(best_heptatonic(note_name, major))
    print(best_heptatonic(note_name, minor))


def test_rendering():
    '''Run through the chromatic binomials 
    and render a major scale for each.'''
    ch = chromatic()
    for _ in range(12):
        print(render(2773, ch))
        ch = ch[1:] + ch[:1]

def test_interval_recognition(heptatonic_scale: list[str]):
    '''Return the intervals for the given collection of 
    note names, using the first name as the tonic.'''
    print(name_heptatonic_intervals(heptatonic_scale))


def test_chord_symbol_parser(chord_symbol: str):
    '''Test the chord symbol parser (and the renderer!)'''

    print(bin(parse_chord_symbol(chord_symbol)))
    #print(render(parse_chord_symbol(chord_symbol), chromatic()))




def test_roman_numerals():
    # A number containing two or more decimal digits is built by appending the Roman numeral equivalent for each, from highest to lowest, as in the following examples:

    print(roman_numeral(39)) # XXX + IX = XXXIX.
    print(roman_numeral(246)) # CC + XL + VI = CCXLVI.
    print(roman_numeral(789)) # = DCC + LXXX + IX = DCCLXXXIX.
    print(roman_numeral(2421)) # MM + CD + XX + I = MMCDXXI.

    # Any missing place (represented by a zero in the place-value equivalent) is omitted, as in Latin (and English) speech:

    print(roman_numeral(160)) # = C + LX = CLX
    print(roman_numeral(207)) #= CC + VII = CCVII
    print(roman_numeral(1009)) #= M + IX = MIX
    print(roman_numeral(1066)) # = M + LX + VI = MLXVI[7][8]

    # The largest number that can be represented in this manner is 3,999 (MMMCMXCIX), but this is sufficient for the values for which Roman numerals are commonly used today, such as year numbers:

    print(roman_numeral(1776)) #= M + DCC + LXX + VI = MDCCLXXVI (the date written on the book held by the Statue of Liberty).
    print(roman_numeral(1918)) # = M + CM + X + VIII = MCMXVIII (the first year of the Spanish flu pandemic)
    print(roman_numeral(1944)) # = M + CM + XL + IV = MCMXLIV (erroneous copyright notice of the 1954 movie The Last Time I Saw Paris)[3]
    print(roman_numeral(2023)) # = MMXXIII (this year)[b]
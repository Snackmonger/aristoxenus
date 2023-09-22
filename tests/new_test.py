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

    def verify(indian: int, roman: str):
        '''Verify that the correct roman numeral was generated.'''
        res: str = 'PASS' if roman == roman_numeral(indian) else 'FAIL'
        print(f'Expected: {roman}, Actual: {roman_numeral(indian)}, Result: {res}')

    verify(39, 'XXXIX')
    verify(246, 'CCXLVI')
    verify(789, 'DCCLXXXIX')
    verify(2421, 'MMCDXXI')
    verify(160, 'CLX')
    verify(207, 'CCVII')
    verify(1009, 'MIX')
    verify(1066, 'MLXVI')
    verify(1776, 'MDCCLXXVI')
    verify(1918, 'MCMXVIII')
    verify(1944, 'MCMXLIV')
    verify(2023, 'MMXXIII')
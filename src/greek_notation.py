'''
Functions relating to Ancient Greek musical notation. 
'''

# This will probably get moved to a different folder for all the greek related stuff



ANCIENT_GREEK_MUSICAL_SYMBOLS: list[dict[str, int | str]] = [{'index': 1,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-1}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-1}',
                                  'heimholz group': 'E'},
                                 {'index': 2,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-2}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-2}',
                                  'heimholz group': 'E'},
                                 {'index': 3,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-3}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-3}',
                                  'heimholz group': 'E'},

                                 {'index': 4,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-4}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-4}',
                                  'heimholz group': 'F'},
                                 {'index': 5,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-5}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-5}',
                                  'heimholz group': 'F'},
                                 {'index': 6,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-6}',
                                  'instrumental': '\N{GREEK CAPITAL LETTER TAU}',
                                  'heimholz group': 'F'},

                                 {'index': 7,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-7}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-7}',
                                  'heimholz group': 'G'},
                                 {'index': 8,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-8}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-8}',
                                  'heimholz group': 'G'},
                                 {'index': 9,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-9}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-7}',
                                  'heimholz group': 'G'},

                                 {'index': 10,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-10}',
                                  'instrumental': '\N{GREEK CAPITAL LETTER ETA}',
                                  'heimholz group': 'A'},
                                 {'index': 11,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-11}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-11}',
                                  'heimholz group': 'A'},
                                 {'index': 12,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-12}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-12}',
                                  'heimholz group': 'A'},

                                 {'index': 13,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-13}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-13}',
                                  'heimholz group': 'B'},
                                 {'index': 14,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-14}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-14}',
                                  'heimholz group': 'B'},
                                 {'index': 15,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-15}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-15}',
                                  'heimholz group': 'B'},

                                 {'index': 16,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-16}',
                                  'instrumental': '\N{GREEK CAPITAL LETTER EPSILON}',
                                  'heimholz group': 'c'},
                                 {'index': 17,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-17}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-17}',
                                  'heimholz group': 'c'},
                                 {'index': 18,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-18}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-18}',
                                  'heimholz group': 'c'},

                                 {'index': 19,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-19}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-19}',
                                  'heimholz group': 'd'},
                                 {'index': 20,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-20}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-54}',
                                  'heimholz group': 'd'},
                                 {'index': 21,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-21}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-6}',
                                  'heimholz group': 'd'},

                                 {'index': 22,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-22}',
                                  'instrumental': '\N{GREEK CAPITAL LETTER GAMMA}',
                                  'heimholz group': 'e'},
                                 {'index': 23,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-23}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-23}',
                                  'heimholz group': 'e'},
                                 {'index': 24,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-24}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-24}',
                                  'heimholz group': 'e'},

                                 {'index': 25,
                                  'vocal': '\N{GREEK CAPITAL LETTER OMEGA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-25}',
                                  'heimholz group': 'f'},
                                 {'index': 26,
                                  'vocal': '\N{GREEK CAPITAL LETTER PSI}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-26}',
                                  'heimholz group': 'f'},
                                 {'index': 27,
                                  'vocal': '\N{GREEK CAPITAL LETTER CHI}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-27}',
                                  'heimholz group': 'f'},

                                 {'index': 28,
                                  'vocal': '\N{GREEK CAPITAL LETTER PHI}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-20}',
                                  'heimholz group': 'g'},
                                 {'index': 29,
                                  'vocal': '\N{GREEK CAPITAL LETTER UPSILON}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-29}',
                                  'heimholz group': 'g'},
                                 {'index': 30,
                                  'vocal': '\N{GREEK CAPITAL LETTER TAU}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-30}',
                                  'heimholz group': 'g'},

                                 {'index': 31,
                                  'vocal': '\N{GREEK CAPITAL LUNATE SIGMA SYMBOL}',
                                  'instrumental': '\N{GREEK CAPITAL LUNATE SIGMA SYMBOL}',
                                  'heimholz group': 'a'},
                                 {'index': 32,
                                  'vocal': '\N{GREEK CAPITAL LETTER RHO}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-32}',
                                  'heimholz group': 'a'},
                                 {'index': 33,
                                  'vocal': '\N{GREEK CAPITAL LETTER PI}',
                                  'instrumental': '\N{GREEK CAPITAL REVERSED LUNATE SIGMA SYMBOL}',
                                  'heimholz group': 'a'},

                                 {'index': 34,
                                  'vocal': '\N{GREEK CAPITAL LETTER OMICRON}',
                                  'instrumental': '\N{GREEK CAPITAL LETTER KAPPA}',
                                  'heimholz group': 'b'},
                                 {'index': 35,
                                  'vocal': '\N{GREEK CAPITAL LETTER XI}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-15}',
                                  'heimholz group': 'b'},
                                 {'index': 36,
                                  'vocal': '\N{GREEK CAPITAL LETTER NU}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-36}',
                                  'heimholz group': 'b'},

                                 {'index': 37,
                                  'vocal': '\N{GREEK CAPITAL LETTER MU}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-37}',
                                  'heimholz group': "c'"},
                                 {'index': 38,
                                  'vocal': '\N{GREEK CAPITAL LETTER LAMDA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-38}',
                                  'heimholz group': "c'"},
                                 {'index': 39,
                                  'vocal': '\N{GREEK CAPITAL LETTER KAPPA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-39}',
                                  'heimholz group': "c'"},

                                 {'index': 40,
                                  'vocal': '\N{GREEK CAPITAL LETTER IOTA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-40}',
                                  'heimholz group': "d'"},
                                 {'index': 41,
                                  'vocal': '\N{GREEK CAPITAL LETTER THETA}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-14}',
                                  'heimholz group': "d'"},
                                 {'index': 42,
                                  'vocal': '\N{GREEK CAPITAL LETTER ETA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-42}',
                                  'heimholz group': "d'"},

                                 {'index': 43,
                                  'vocal': '\N{GREEK CAPITAL LETTER ZETA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-43}',
                                  'heimholz group': "e'"},
                                 {'index': 44,
                                  'vocal': '\N{GREEK CAPITAL LETTER EPSILON}',
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-9}',
                                  'heimholz group': "e'"},
                                 {'index': 45,
                                  'vocal': '\N{GREEK CAPITAL LETTER DELTA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-45}',
                                  'heimholz group': "e'"},

                                 {'index': 46,
                                  'vocal': '\N{GREEK CAPITAL LETTER GAMMA}',
                                  'instrumental': '\N{GREEK CAPITAL LETTER NU}',
                                  'heimholz group': "f'"},
                                 {'index': 47,
                                  'vocal': '\N{GREEK CAPITAL LETTER BETA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-47}',
                                  'heimholz group': "f'"},
                                 {'index': 48,
                                  'vocal': '\N{GREEK CAPITAL LETTER ALPHA}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-48}',
                                  'heimholz group': "f'"},

                                 {'index': 49,
                                  'vocal': '\N{LATIN CAPITAL LETTER UPSILON}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-49}',
                                  'heimholz group': "g'"},
                                 {'index': 50,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-50}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-50}',
                                  'heimholz group': "g'"},
                                 {'index': 51,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-51}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-51}',
                                  'heimholz group': "g'"},

                                 {'index': 52,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-52}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-52}',
                                  'heimholz group': "a'"},
                                 {'index': 53,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-53}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-53}',
                                  'heimholz group': "a'"},
                                 {'index': 54,
                                  'vocal': '\N{GREEK VOCAL NOTATION SYMBOL-54}',
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-54}',
                                  'heimholz group': "a'"},

                                 {'index': 55,
                                  'vocal': '\N{GREEK CAPITAL LETTER OMICRON}'+"'",
                                  'instrumental': '\N{GREEK CAPITAL LETTER KAPPA}'+"'",
                                  'heimholz group': "b'"},
                                 {'index': 56,
                                  'vocal': '\N{GREEK CAPITAL LETTER XI}'+"'",
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-15}'+"'",
                                  'heimholz group': "b'"},
                                 {'index': 57,
                                  'vocal': '\N{GREEK CAPITAL LETTER NU}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-36}'+"'",
                                  'heimholz group': "b'"},

                                 {'index': 58,
                                  'vocal': '\N{GREEK CAPITAL LETTER MU}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-37}'+"'",
                                  'heimholz group': 'c"'},
                                 {'index': 59,
                                  'vocal': '\N{GREEK CAPITAL LETTER LAMDA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-38}'+"'",
                                  'heimholz group': 'c"'},
                                 {'index': 60,
                                  'vocal': '\N{GREEK CAPITAL LETTER KAPPA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-39}'+"'",
                                  'heimholz group': 'c"'},

                                 {'index': 61,
                                  'vocal': '\N{GREEK CAPITAL LETTER IOTA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-40}'+"'",
                                  'heimholz group': 'd"'},
                                 {'index': 62,
                                  'vocal': '\N{GREEK CAPITAL LETTER THETA}'+"'",
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-14}'+"'",
                                  'heimholz group': 'd"'},
                                 {'index': 63,
                                  'vocal': '\N{GREEK CAPITAL LETTER ETA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-42}'+"'",
                                  'heimholz group': 'd"'},

                                 {'index': 64,
                                  'vocal': '\N{GREEK CAPITAL LETTER ZETA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-43}'+"'",
                                  'heimholz group': 'e"'},
                                 {'index': 65,
                                  'vocal': '\N{GREEK CAPITAL LETTER EPSILON}'+"'",
                                  'instrumental': '\N{GREEK VOCAL NOTATION SYMBOL-9}'+"'",
                                  'heimholz group': 'e"'},
                                 {'index': 66,
                                  'vocal': '\N{GREEK CAPITAL LETTER DELTA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-45}'+"'",
                                  'heimholz group': 'e"'},

                                 {'index': 67,
                                  'vocal': '\N{GREEK CAPITAL LETTER GAMMA}'+"'",
                                  'instrumental': '\N{GREEK CAPITAL LETTER NU}'+"'",
                                  'heimholz group': 'f"'},
                                 {'index': 68,
                                  'vocal': '\N{GREEK CAPITAL LETTER BETA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-47}'+"'",
                                  'heimholz group': 'f"'},
                                 {'index': 69,
                                  'vocal': '\N{GREEK CAPITAL LETTER ALPHA}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-48}'+"'",
                                  'heimholz group': "f'"},

                                 {'index': 70,
                                  'vocal': '\N{LATIN CAPITAL LETTER UPSILON}'+"'",
                                  'instrumental': '\N{GREEK INSTRUMENTAL NOTATION SYMBOL-49}'+"'",
                                  'heimholz group': 'g"'},

                                 ]



def greek_notation(index: int, style: str) -> str:
    '''
    Fetch the Greek musical symbol according to its index number
    '''
    index -= 1
    if index > 70 or index < 0:
        raise ValueError
    if style not in ['instrumental', 'vocal']:
        raise ValueError
    return str(ANCIENT_GREEK_MUSICAL_SYMBOLS[index][style])



def recognize(note_data: str | list[str] | tuple[str, ...]) -> list[tuple[int, str, str]]:
    '''
    Recognize a Greek musical symbol, or a group of symbols, and return the corresponding symbol number.
    '''
    symbols: list[str] = []
    if isinstance(note_data, str):
        for char in note_data:
            symbols.append(char)
    elif type(note_data) in [list, tuple]:
        for symbol in note_data:
            symbols.append(symbol)

    identified_symbols: list[tuple[int, str, str]] = []
    for symbol in symbols:
        for item in ANCIENT_GREEK_MUSICAL_SYMBOLS:
            if symbol == item['instrumental']:
                identified_symbols.append((int(item['index']), symbol, 'instrumental'))
            elif symbol == item['vocal']:
                identified_symbols.append((int(item['index']), symbol, 'vocal'))
        
    return identified_symbols


def parse_formatting(text: str) -> str:
    '''
    Dirty function for easy insertion of Greek musical symbols into plaintext
    to be formatted more precisely later. 

    Write your plain text, and wherever you want to use a Greek musical notation
    symbol, use the following notation:

        &34i&   ::  sign 34, instrumental (i)
        &7v&    ::  sign 7, vocal (v)
    '''
    for item in ANCIENT_GREEK_MUSICAL_SYMBOLS:
        text = text.replace('&'+str(item['index'])+'v&', str(item['vocal']))
        text = text.replace('&'+str(item['index'])+'i&', str(item['instrumental']))

    return text




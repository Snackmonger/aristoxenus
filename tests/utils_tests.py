from src.utils import recognize, greek_notation


def test_greek_notation():
    limenius_hypolydian: tuple[int, ...] = (22, 23, 31, 34, 35, 40, 43, 44, 52)
    limenius_lydian: tuple[int, ...] = (28, 31, 32, 33, 40, 43, 44, 49, 52, 53)
    limenius_hyperlydian: tuple[int, ...] = (28, 31, 32, 33, 40, 41, 49, 52)

    combination: str = ''
    for note in limenius_hypolydian:
        combination += greek_notation(note, 'instrumental')
    

    print(combination)

    combination: str = ''
    for note in limenius_lydian:
        combination += greek_notation(note, 'instrumental')
    

    print(combination)

    combination: str = ''
    for note in limenius_hyperlydian:
        combination += greek_notation(note, 'instrumental')
    

    print(combination)


    print(recognize('Γ𝈪ϹΚ𝈎𝈶𝈸𝈈𝈿'))

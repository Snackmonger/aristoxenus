from src import parsing

def parse_note_sequence():

    x = parsing.parse_simple_literal_sequence(['C', 'G', 'B', 'E'])
    print(bin(x))
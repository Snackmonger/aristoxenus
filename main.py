from tests import new_test
from src.nomenclature import sharps, flats, naturals, chromatic, generate_interval_map
from src.pitch_mapping import render
from src.structures import DITONE, DIAPASON, TONE, DIATESSARON, COMPOUND_DITONE, COMPOUND_TONE, DIAPENTE
from src.structures import parse_chord_symbol

# new_test.test_rendering()


# for note in sharps():
#     new_test.test_heptatonic(note)

# for note in flats():
#     new_test.test_heptatonic(note)

# for note in naturals():
#     new_test.test_heptatonic(note)

# new_test.test_interval_recognition(['E', 'F#/Gb', 'G#/Ab', 'A', 'B', 'C#/Db', 'D#/Eb'])
# new_test.test_interval_recognition(['E', 'F#/Gb', 'Abb', 'A#', 'B#', 'C#/Db', 'D#/Eb'])
# print(bin(generate_interval_map(['E', 'F#/Gb', 'G#/Ab', 'A', 'B', 'C#/Db', 'D#/Eb'])))

# Create a scale by overlapping intervals.
# maj = TONE | DITONE | DIATESSARON | DIAPENTE | COMPOUND_TONE | COMPOUND_DITONE
# print(bin(maj))
# # 0b101010110101
# # The largest interval is represented by the most significant bit.
# # The tonic or root is represented by the least significant bit.
# # Intervallic structures of any size can be thus created.
# # All intervallic structures must therefore begin and end with a flipped bit

# upper = DITONE -1 << 24
# print(bin(maj|upper))
# # Shift a ditone by 2 octaves higher and add to the major scale above.
# # We subtract 1 because 1 represents the tonic, and we don't necessarily
# # want the note 2 octaves above the tonic to be part of the structure too.

# print(0b101010110101)

new_test.test_chord_symbol_parser('Cmaj11b13')
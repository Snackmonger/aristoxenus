from tests.utils_tests import test_greek_notation
from src.greek_notation import parse_formatting


sample = 'This is sample text to test whether the symbol replacement is working. &7i&.'
print(parse_formatting(sample))
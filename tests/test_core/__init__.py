'''
Testing Notes
-------------


Q: Why do the tests use ``typing.cast``?
A: Casting is irrelevant at runtime, but mistyped parameters make linters
mad. Specifically, passing ``TypedDict``s as parameters in the pytest
``parametrize`` function makes them appear as partial ``Unknown`` type.
'''

import sys
sys.path.append('.')
sys.path.append('./aristoxenus')


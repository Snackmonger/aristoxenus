
# Not all parts of the template are necessary, but this is the
# general order of information. autodocstring will fill in the
# basic parameters and return, but sometimes you want to add
# other helpful information too.

numpy_template: str = '''
Short, 1-sentence description of WHAT the function does (not HOW it does it),
without using parameter names or function names. (There is some discrepancy
about whether the verb should be imperative or indicative. PEP257 says to use
imperative, Google style says indicative. Whatever you do, be consistent.)

.. deprecated:: 1.6.0
          `ndobj_old` will be removed in NumPy 2.0.0, it is replaced by
          `ndobj_new` because the latter works also with array subclasses.

Longer description of what the function does, if necessary. This should 
explain functionality, not implementation or background theory. We can 
refer to parameters and functions by name in this section, but descriptions
of the parameters themselves belong in the Parameters section.

Parameters
----------
param_name : param_type
    Description of parameter `x`
param_with_default : param_type, default=value | default value | default : value
    The description can also explain the default instead of the definition.
optional_param : param_type, optional
    Used for parameters that are not required.
    Also used when a function has a default value that won't actually be used.
fixed_values : {'fixed', 'values', 'only'}
    Description of parameter in which only fixed values can be passed.
x1, x2 : param_type
    Multiple objects with the same type, shape, and description can be 
    combined.
*args : tuple
    Additional positional arguments get one unpacking asterisk.
**kwargs : dict, optional
    Keyword arguments get two unpacking asterisks

Returns
-------
int
    Description of anonymous integer return value.
err_code : int
    Description of a named return value
err_msg : str or None
    These descriptions follow the same principals as the parameters

Yields
------
int
    Description of the anonymous integer return value.

Other Parameters
----------------
(Only used if we have lots of parameters and don't want to clutter the upper
section with parameters that are mostly going to have default values anyway)

Raises
------
NameOfException
    Description of conditions under which the exception is raised.

See Also
--------
function_name : Description of the related function
(This section should be used sparingly for functions that are not obvious.)

Notes
-----
This section provides additional information about the code, possibly 
including a discussion of the algorithm or method.

References
----------
References cited in the Notes section may be listed here, e.g. if you cited 
the article below using the text [1]_, include it as in the list as follows:

.. [1] This will show up as a footnote link in RST rendering.

Examples
--------
Give some examples of the code in doctest format. This isn't required in
every situation, but it can be useful.
'''
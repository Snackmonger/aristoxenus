class ParentError(Exception):
    ...


class UnknownSymbolError(ParentError):
    ...


class HeptatonicScaleError(ParentError):
    ...


class UnknownKeywordError(ParentError):
    ...


class BadValueError(ParentError):
    ...
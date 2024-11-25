from aristoxenus.core.constants import WHITESPACE


class Scale:
    '''Middleman placeholder for now.'''

    def __init__(self):
        ...

    @property
    def note_names(self) -> tuple[str, ...]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({WHITESPACE.join(self.note_names)})"
    
    def __len__(self) -> int:
        return len(self.note_names)


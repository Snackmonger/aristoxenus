import re
from typing import Any
from overhaul.data.constants import NATURAL_MAP, RE_VALIDATE_NOTE_NAME

class SemitoneMap:
    """
    Simple representation of an interval structure.
    """

    def __init__(self, mapping: tuple[tuple[int, str], ...]):
        self.__members = mapping

    def members(self) -> tuple[tuple[int, str], ...]:
        '''
        Get all the members of the semitone map.

        Returns
        -------
        tuple[tuple[int, str], ...]
            The basic elements of the map, as a tuple of tuples.
        '''
        return self.__members

    def __getitem__(self, item: int | slice) -> tuple[int, str] | tuple[tuple[int, str], ...]:
        if isinstance(item, slice):
            nums: tuple[int, ...] = self.all_semitones[item.start: item.stop: item.step]
            names: tuple[str, ...] = self.all_names[item.start: item.stop: item.step]
            return tuple((nums[i], names[i]) for i in range(len(nums)))
        return self.__members[item]

    def __setitem__(self, index: Any, value: Any) -> None:
        pass

    def __len__(self) -> int:
        return len(self.__members)

    def __int__(self) -> int:
        '''
        Get the integer expression of this structure, assuming that the least
        significant bit is the tonic/root.

        Returns
        -------
        int
            An integer representing this interval structure.
        '''

        num = 1
        for semitones in self.all_semitones:
            val = 1 << semitones
            num |= val
        return num

    def contains(self, item: str | int) -> bool:
        """Indicate whether the given name or interval exists in the structure."""
        if isinstance(item, str):
            return item in self.all_names
        return item in self.all_semitones

    def index(self, item: str | int) -> int:
        """Get the index of the given item."""
        if isinstance(item, str):
            if re.match(RE_VALIDATE_NOTE_NAME, item):
                return self.all_names.index(item)
        return self.all_semitones.index(item)

    def semitones(self, index: int) -> int:
        """Get the number of semitones at the given index."""
        return self.__members[index][0]

    def name(self, index: int) -> str:
        """Get the name at the given index."""
        return self.__members[index][1]

    @property
    def all_names(self) -> tuple[str, ...]:
        """Get a tuple of all member names in the map."""
        return tuple(self.name(i) for i in range(len(self)))

    @property
    def all_semitones(self) -> tuple[int, ...]:
        """Get a tuple of all semitone values in the map."""
        return tuple(self.semitones(i) for i in range(len(self)))
    

Naturals = SemitoneMap(NATURAL_MAP)
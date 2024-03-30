from typing import Sequence
from data import (
    constants,
    errors,
    keywords
)
from data.annotations import ChordData
from src import (
    interface,
    nomenclature,
    parsing,
    utils
)


class Nomenclator:
    """Class that provides static methods for generating raw musical material
    from precursor constants. Can be used on its own or as a mixin.
    """
    @staticmethod
    def legal_root_names() -> tuple[str, ...]:
        return constants.LEGAL_ROOT_NAMES

    @staticmethod
    def chromatic(keynote: str, binomial: bool = False) -> tuple[str, ...]:
        return interface.chromatic(keynote=keynote, binomial=binomial)
    

class Parser:
    """Class that provides static methods for symbol parsing offered by the 
    program. Can be used on its own or as a mixin."""

    @staticmethod
    def parse_chord_symbol(chord_symbol: str) -> ChordData:
        """
         Return an integer representing an interval map of a given chord symbol.

        Parameters:
            chord_symbol : A chord symbol with note name, extensions, and modifiers.
        Returns:
            dict {
                chord_symbol: str
                note_names: tuple[str, ...]
                interval_names: tuple[str, ...]
                interval_structure: int
            }
        Examples:
            
        """
        return parsing.parse_chord_symbol(chord_symbol=chord_symbol)

    @staticmethod
    def parse_interval_names_as_chord_symbol(interval_names: Sequence[str]) -> str:
        """Attempt to generate a chord symbol from the given interval names.

        Parameters:
            interval_names: An array of strings consisting of numbers from 1 to 15,
            possibly modified by the '#' or 'b' symbol.
        Returns:
            str : A chord symbol representing the intervals.
        Examples:
            >>> parse_interval_names_as_chord_symbol(["1","3","5"])
            'maj'
            >>> parse_interval_names_as_chord_symbol(["1","b3","5"])
            'min'
            >>> parse_interval_names_as_chord_symbol(["1","b3","b5", "b7"])
            'min7b5'
            >>> parse_interval_names_as_chord_symbol(["1","b3","b5", "bb7"])
            'dim7'
            >>> parse_interval_names_as_chord_symbol(["1","3","5","7","9"])
            'maj9'
            >>> parse_interval_names_as_chord_symbol(["1","b3","b5", "bb7", "9", "11"])
            'dim11'
            >>> parse_interval_names_as_chord_symbol(["1","3","7","9"])
            'maj9no5'
            >>> parse_interval_names_as_chord_symbol(["1","bb3","5"])
            'susbb3'
            >>> parse_interval_names_as_chord_symbol(["1","bb3","#5","7"])
            'maj7susbb3#5'
        """
        return parsing.parse_interval_names_as_chord_symbol(interval_names=interval_names)

    @staticmethod
    def parse_interval_structure_as_chord_symbol(interval_structure: int) -> str:
        """Attempt to generate a chord symbol from the given interval 
        structure, expressed as an integer.
        """

        return parsing.parse_interval_structure_as_chord_symbol(interval_structure=interval_structure)


class Converter:
    """Class that provides static methods for conversions offered by the 
    program. Can be used on its own or as a mixin.
    """

    @staticmethod
    def decode_enharmonic(note_name: str) -> str:
        """Decode a real note name, possibly with many accidentals, back into
        a neutral binomial form.

        Parameters:
            note_name: The name of a note, with up to 11 accidentals.
        Raises:
            NoteNameError: If the input is invalid.
        Returns:
            An enharmonically-equivalent note with a neutral binomial name.
        Examples:
        >>> decode_enharmonic('B#')
        'C'
        >>> decode_enharmonic('Cb')
        'B'
        >>> decode_enharmonic('A######')
        'D#|Eb'
        >>> decode_enharmonic('Bbbb')
        'G#|Ab'
        """
        return nomenclature.decode_enharmonic(note_name=note_name)

    @staticmethod
    def encode_enharmonic(note_value: str, note_name: str) -> str:
        """Encode a note name so that it has the enharmonic value of one note
        and the alphabetic name of another.

        Parameters:
            note_value: The enharmonic value, either binomial or real.
            note_name: The target name, one of the natural note names.
        Raises:
            NoteNameError: If any of the inputs is invalid.
        Return:
            A note name that has the given value and alphabetic identity.
        Notes:
            This function prefers the enharmonic equivalent with the fewest 
            accidentals. When shifting by tritone, the number of accidentals 
            will be equal in both sharps and flats, so we arbitrarily default 
            to sharps.
        Examples:
        >>> encode_enharmonic('Eb' , 'A') 
        'A######'
        >>> encode_enharmonic('Eb' , 'B')
        'B####'
        >>> encode_enharmonic('Eb' , 'C')
        'C###'
        >>> encode_enharmonic('Eb' , 'D')
        'D#'
        >>> encode_enharmonic('Eb' , 'E')
        'Eb'
        >>> encode_enharmonic('Eb' , 'F') 
        'Fbb'
        >>> encode_enharmonic('Eb' , 'G') 
        'Gbbbb'
        >>> encode_enharmonic('Eb' , 'A') 
        'A######'
        """
        return nomenclature.encode_enharmonic(note_value=note_value, note_name=note_name)

    @staticmethod
    def decode_numeration(keyword: str) -> int:
        """
        Decode a numeric keyword into the number it represents.

        Parameters:
            term: A numeric keyword term, e.g. "tertial", "pentad"
        Raises:
            UnknownKeywordError: If the term is not a known keyword.
        Returns:
            An integer between 1 and 15. If the keyword is "basal", then 
            its number will be 1 lower than the name suggests. (This is so it
            can be used to slice lists starting at 0)
        """
        return utils.decode_numeration(keyword=keyword)

    @staticmethod
    def encode_numeration(number: int, category: str) -> str:
        """
        Encode a number as a keyword for the given category.

        Parameters:
            category: A category of numerical words, e.g. "ordinal", "cardinal"
            number: The number to encode. If the category is "basal", the number
                    represents a list slice, and so should be 1 less than the name
                    suggests (tertial=2).
        Returns:
            A string representing the number in the given category.
        """
        return utils.encode_numeration(number=number, category=category)

    @staticmethod
    def convert_frequency_to_note_name(frequency: float, accidental_type: str) -> str:
        """Return a note name in scientific notation corresponding to the given 
        frequency.

        Parameters:
            frequency:          The Hertz value of the frequency.
            accidental_type:    "sharp", "flat", or "binomial"
        Raises
            UnknownKeywordError:    If the accidental type is not a legal option.
            AristoxenusValueError:  If the frequency is not in 12-TET @ A4 = 440hz.
        """
        match accidental_type:
            case keywords.SHARP:
                accidentals = constants.SHARPS
            case keywords.FLAT:
                accidentals = constants.FLATS
            case keywords.BINOMIAL:
                accidentals = constants.BINOMIALS
            case _:
                raise errors.UnknownKeywordError(accidental_type)
        return nomenclature.convert_frequency_to_note(frequency, accidentals)

    @staticmethod
    def convert_note_name_to_frequency(note_name: str) -> float:
        """
        Convert a note name to a frequency in 12-TET A4 = 440 hz.

        Parameters
            note_name : A note name of any accidental type, in scientific notation.
        Returns
            float : A frequency expressed in Hertz, rounded to three places.
        Raises
            NoteNameError : If the note name does not exist or is not in scientific
                            notation.
        """
        return nomenclature.convert_note_to_frequency(note_name)

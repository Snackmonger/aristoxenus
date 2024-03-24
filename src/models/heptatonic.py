from typing import Sequence

from data import (
    annotations,
    constants,
    keywords
)
from src import (
    bitwise,
    interface,
    nomenclature,
    utils
)
from src.models.bases import ScaleStructure
from src.models.mixins import (
    ConverterMixin, 
    ParserMixin
)

class HeptatonicStructure(ScaleStructure, ConverterMixin, ParserMixin):
    def __init__(self, 
                 keynote: str,
                 scale_name: annotations.HeptatonicScales = keywords.DIATONIC,
                 modal_name: annotations.ModalNames = keywords.IONIAN,
                 ) -> None:
        
        # Basic identification.
        self.scale_name: annotations.HeptatonicScales = scale_name
        self.modal_name: annotations.ModalNames = modal_name
        self.keynote: str = keynote

        # Populate details.
        data = interface.render_heptatonic_form(keynote, scale_name, modal_name)
        self.interval_structure: int = data[keywords.INTERVAL_STRUCTURE]
        self.interval_scale: tuple[str, ...] = data[keywords.INTERVAL_SCALE]
        self.interval_map: dict[str, str] = data[keywords.INTERVAL_MAP]
        self.binomial_rendering: tuple[str, ...] = data[keywords.BINOMIAL_RENDERING]
        self.forced_rendering: tuple[str, ...] = data[keywords.FORCED_RENDERING]
        self.best_keynote: str = data[keywords.BEST_KEYNOTE]
        self.best_rendering: tuple[str, ...] = data[keywords.BEST_RENDERING]
        self.scientific_map: dict[str, str] = nomenclature.heptatonic_range(
            self.forced_rendering)

    def scale_segment(self, start: int, end: int, descending: bool = False, octaves: int = 1) -> tuple[str, ...]:
        """Return a segment of the scale running from a starting degree to 
        an ending degree, and containing all the notes in between.
        
        Args:
            start:  The relative degree (1 to 7) that will begin the sequence.
            end:    The relative degree (1 to 7) that will end the sequence.
            descending: Flag to decide whether to reverse the array.
            octaves: The number of octaves that the segment will span.
            
        """
        # Adjust for 0 index
        start -= 1
        end -= 1
        for x in [start, end]:
            if x not in range(7):
                raise ValueError("Must be a number between 1 and 7, inclusive.")
        if not 0 < octaves < constants.NUMBER_OF_OCTAVES:
            raise ValueError(f"Octaves must be between 1 and {constants.NUMBER_OF_OCTAVES}")
        if start == end and octaves == 1:
            octaves = 2

        segment = list(self.forced_rendering)
        if descending:
            segment.reverse()
        segment = list(utils.shift_array(segment, self.forced_rendering[start]))
        end = segment.index(self.forced_rendering[end]) + 1
        if octaves > 1:
            segment *= octaves
            end += (7 * (octaves - 1))
        return tuple(segment[: end])
        

    def contains(self, material: Sequence[int] | Sequence[str] | int | str) -> bool:
        """
        Test whether the given material is contained in the structure.

        Args:
            material:   An integer representing an interval or interval 
                        structure, or a string representing a note name,
                        or an array of either of these types.
        Returns:
            True, if the material appears anywhere in the structure. 

        Notes:
            Intervals and interval structures will be considered from the
            tonic and will only match if the whole structure matches.
        """
        def __contains(material: int | str) -> bool:
            if isinstance(material, int):
                return bitwise.has_interval(self.interval_structure, material)
            return nomenclature.decode_enharmonic(material) in self.binomial_rendering
        
        if isinstance(material, (int, str)):
            return __contains(material)
        return all(__contains(x) for x in material)


    def chord_scale(self,
                    relative_degree: int,
                    notes: int = 3
                    ) -> annotations.HeptatonicChord:
        """Return a chord from the chord scale of the instance's scaleform.

        Args:
            relative_degree: The scale degree from which to build the chord
            notes: The number of notes in the chord (default=3)
            formatting: A keyword indicating how to display the chord.

        Returns:
        """
        if not 0 < relative_degree < 8:
            raise ValueError(
                f"Requested degree must be between 1 and 7. Got value: {relative_degree}")
        if not 2 < notes < 8:
            raise ValueError(
                f"Number of notes must be between 2 and 7, inclusive. Got value: {notes}")
        chord_scale = interface.heptatonic_chord_scale(
            self.scale_name, self.modal_name, self.keynote, number_of_notes=notes)
        return chord_scale["chord_scale"][relative_degree-1]
    


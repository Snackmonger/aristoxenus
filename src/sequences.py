'''
Sequences module pertains to the ordering of notes from a given structure
in diachronic context.
'''

from src import nomenclature, parsing, rendering
from data import constants


class NoteSequence():
    '''
    -- a basic way of ordering notes --
    '''

    def __init__(self,
                 structure: int,
                 keynote: str = 'C',
                 order: tuple[int, ...] | None = None
                 ) -> None:
        
        self.structure = structure
        self.note_set: list[str]
        
        if order is None: 
            self.order_ = tuple(range(structure.bit_count()))
        else:
            self.order_ = order

        if not nomenclature.is_scientific(keynote):
            keynote += '0'

        accidentals = nomenclature.get_accidentals(keynote)
        self.note_set = rendering.render_scientific(structure, accidentals, keynote)
        

    @property
    def order(self) -> tuple[int, ...]:
        return self.order_
        

    @order.setter
    def order(self, order: tuple[int, ...]) -> None:
        note_set: list[str] = []
        for number in order:
            note_set.append(self.note_set[number])
        self.note_set = note_set


    @property
    def keynote(self) -> str:
        return self.keynote_
    

    @keynote.setter
    def keynote(self, keynote: str) -> None:
        if keynote in nomenclature.enharmonic_decoder():
            self.keynote_ = keynote

        

    







class Order():


    def __init__(self):
        ...



    
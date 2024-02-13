



# from data.annotations import GuitarFretboard
# from data.intervallic_canon import HEPTATONIC_SYSTEM_BY_NAME

# from src.nomenclature import chromatic
# from src.rendering import render_plain
# from src.utils import shift_list




# class DiagramController():

#     def __init__(self) -> None:

#         self.fretboard: GuitarFretboard
#         self.key: str
#         self.position: int
#         self.scale: str
#         self.width: int
#         self.rendering_style: str
#         self.type: str


#     @property
#     def scale_notes(self) -> list[str]:
#         scale: int = HEPTATONIC_SYSTEM_BY_NAME[self.scale]
#         return render_plain(scale, shift_list(chromatic(), self.key))

#     @property
#     def available_positions(self) -> list[int]:
#         return [i for i, note in enumerate(self.fretboard[0]) if note in self.scale_notes]
    


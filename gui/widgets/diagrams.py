


from tkinter import Canvas, Tk
from tkinter.ttk import Button, Frame, OptionMenu
from typing import Any, Callable

from data.annotations import GuitarFretboard
from data.intervallic_canon import HEPTATONIC_SYSTEM_BY_NAME
from src.nomenclature import chromatic
from src.rendering import render_plain
from src.utils import shift_list



class DiagramView(Frame):

    def __init__(self, master: Frame | Tk):
        self.master = master
        self.callbacks: dict[str, Callable[..., Any]]

        # Frame 1: Fingering Diagram (LEFT, PERMANENT)
        self.canvas: Canvas

        # Frame 2: String-Fingering Controls (RIGHT, PERMANENT)
        self.fingering_panel: Frame
        # for string in diagram, a button toggle i or e
        
        # Frame 3: Scale selector (RIGHT, PERMANENT)
        self.scale_selection: OptionMenu
        self.key_selection: OptionMenu
        self.position_selection: OptionMenu

        # Frame 4: Main Option Panel (RIGHT, STATE-BASED)
        self.mode_toggle: Button # change state
        self.current_main_panel: Frame

        # Frame 4a: Scale Mode Panel (RIGHT, STATE)
        self.scale_panel: Frame
        # for interval in scale, a subpanel of frame 5

        # Frame 4b: Arpeggio Mode Panel (RIGHT, STATE)
        self.arpeggio_panel: Frame

        # Frame 5: Node Options Subpanel
        # (This must be a separate class for a repeating widget.)
        self.node_options: Frame
        self.node_colour: str
        self.node_shape: str
        self.node_textcolour: str
        self.node_textdisplay: str


    def add_callback(self, key: str, func: Callable[..., Any]) -> None:
        if not key in self.callbacks:
            self.callbacks.update({key: func})

    def bind_callbacks(self) -> None:
        """Bind the callbacks to their appropriate tkinter events."""
        ...


    


class DiagramController():

    def __init__(self) -> None:

        self.fretboard: GuitarFretboard
        self.key: str
        self.position: int
        self.scale: str
        self.width: int
        self.rendering_style: str
        self.type: str


    @property
    def scale_notes(self) -> list[str]:
        scale: int = HEPTATONIC_SYSTEM_BY_NAME[self.scale]
        return render_plain(scale, shift_list(chromatic(), self.key))

    @property
    def available_positions(self) -> list[int]:
        return [i for i, note in enumerate(self.fretboard[0]) if note in self.scale_notes]
    


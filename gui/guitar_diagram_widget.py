"""Widget to display segments of guitar fretboards as diagrams."""

from typing import Literal

from tkinter import *
from tkinter.ttk import *


from src.models.diagrams import GuitarFingering, convert_fretboard_to_relative, get_interval_map, standard_fretboard
from data.keywords import (OPEN, CLOSE, INDEX, PINKY, NOTE_NAME, SCALE_DEGREE, FINGER, FRET)

class DiagramWidget(Tk):


    def __init__(self) -> None:
        super().__init__()
        self.node_repr_style: str = NOTE_NAME
        self.diagram: GuitarFingering = GuitarFingering(5, standard_fretboard(), 5, INDEX)

        self.rows: int = len(self.diagram.grid)
        self.columns: int = len(self.diagram.grid[0])

        self.diagram.flash_diagram()
        self.diagram.mask_note_names(["C", "D#|Eb", "G", "B", "A", "D", "F"])
        self.diagram.define_intervals(get_interval_map("C"))
        self.change_repr_style("scale_degree")


        # Left: Chord diagram
        self.display_frame: Frame = Frame(self)
        self.canvas: Canvas = Canvas(self, height=500, width=500, bg="white")
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.update()
        self.draw_grid()
        self.display_active_nodes()

        # Right: Controls
        self.control_frame: Frame = Frame(self)


    def change_repr_style(self, style: str) -> None:
        for string in self.diagram.grid:
            for note in string:
                note.repr_style = style


    def show_notes(self, scale: list[str]) -> None:
        """Display only the given note names in the diagram."""
        self.diagram.clear_diagram()
        self.diagram.flash_diagram()
        self.diagram.mask_note_names(scale)


    def draw_grid(self) -> None:
        """Draw the grid based on the dimensions of the diagram object."""
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        self.canvas.delete("grid_line")

        for i in range(0, width, width//self.columns):
            self.canvas.create_line([(i, 0), (i, height)], tags="grid_line")
        for i in range(0, height, height//self.rows):
            self.canvas.create_line([(0, i), (width, i)], tags="grid_line")

        self.canvas.pack()


    def display_active_nodes(self) -> None:
        """Reload the display to show only the diagram's active nodes."""
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        square_size: tuple[int, int] = width//self.columns, height//self.rows

        for i, string in enumerate(self.diagram.grid):
            for j, note in enumerate(string):
                if note.is_active:
                    centre = (square_size[0] // 2) + square_size[0] * j, (square_size[1] // 2) + square_size[1] * i
                    self.canvas.create_text(centre[0], centre[1], text=repr(note))

        self.canvas.pack()
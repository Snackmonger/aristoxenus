"""Widget to display segments of guitar fretboards as diagrams."""

from typing import Literal

from tkinter import *
from tkinter.ttk import *


from src.models.diagrams import (GuitarFingering, 
                                 convert_fretboard_to_relative, 
                                 get_interval_map, 
                                 standard_fretboard)
from data.keywords import (OPEN, 
                           CLOSE, 
                           INDEX, 
                           PINKY, 
                           NOTE_NAME, 
                           SCALE_DEGREE, 
                           FINGER, 
                           FRET)



class FretboardDiagramWidget(Tk):
    """Widget to display interactive fretboard diagrams."""


    def __init__(self) -> None:
        super().__init__()
        self.node_repr_style: str = NOTE_NAME
        self.diagram: GuitarFingering = GuitarFingering(5, standard_fretboard(), 4, INDEX)

        self.rows: int = len(self.diagram.grid)
        self.columns: int = len(self.diagram.grid[0])

        self.diagram.flash_diagram()
        self.diagram.mask_note_names(["C", "D#|Eb", "G", "A#|Bb", "A", "D", "F"])
        self.diagram.define_intervals(get_interval_map("C"))
        self.diagram.apply_fingering()
        self.change_rendering_style("finger")


        # Left: Chord diagram
        self.display_frame: Frame = Frame(self)
        self.canvas: Canvas = Canvas(self.display_frame, height=500, width=500, bg="white")
        self.canvas.grid()
        self.canvas.update()
        self.draw_grid()
        self.display_active_nodes()
        self.display_frame.grid(column=0, row=0)

        # Right: Controls
        self.control_frame: Frame = Frame(self)
        self.control_frame.grid(column=1, row=0)


    def change_rendering_style(self, style: str) -> None:
        """Indicate a new rendering style.."""
        for string in self.diagram.grid:
            for note in string:
                note.rendering_mode = style


    def mask_note_names(self, scale: list[str]) -> None:
        """Display only the given note names in the diagram."""
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

        self.canvas.grid()


    def display_active_nodes(self) -> None:
        """Reload the display to show only the diagram's active nodes."""
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        square_size: tuple[int, int] = width//self.columns, height//self.rows

        for i, string in enumerate(self.diagram.grid):
            for j, note in enumerate(string):
                if note.is_active:
                    centre = (square_size[0] // 2) + square_size[0] * j, (square_size[1] // 2) + square_size[1] * i
                    
                    match note.shape:

                        case "circle":
                            self.canvas.create_oval(centre[0]-15, centre[1]-15, centre[0]+15, centre[1]+15, fill=note.shape_colour)

                        case "inverted_triangle":
                            p1, p2 = centre[0]-20, centre[1]-10
                            p3, p4 = centre[0]+20, centre[1]-10
                            p5, p6 = centre[0], centre[1]+20
                            self.canvas.create_polygon(p1, p2, p3, p4, p5, p6, fill=note.shape_colour)

                        case "triangle":
                            p1, p2 = centre[0]+20, centre[1]+15
                            p3, p4 = centre[0]-20, centre[1]+15
                            p5, p6 = centre[0], centre[1]-20
                            self.canvas.create_polygon(p1, p2, p3, p4, p5, p6, fill=note.shape_colour)


                    self.canvas.create_text(centre[0], centre[1], text=repr(note), fill=note.text_colour, font=("Times", "16", "bold"))

        self.canvas.grid()
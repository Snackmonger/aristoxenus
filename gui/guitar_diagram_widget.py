"""Widget to display segments of guitar fretboards as diagrams.

This code is really just a mockup to help work out the kinks.

Abstract: The left side of the screen displays a diagram generated 
based on the inputs in the right side of the screen. The diagram is
meant to teach positional fingerings of scales and arpeggios using
the diatonic scale and its modes.

The input options are: 
    SCALE       The base scale for the fingering diagram
    KEYNOTE     The tonal centre that will define interval relations
    ARPEGGIO    The degree of the chord-scale that will be highligted within the scale
    POSITION    A position generated from possible positions for this scale/keynote
                (i.e. frets on the lowest string that have notes in the scale)

Options that affect all nodes in the diagram:
    TEXT        Defines which type of diaplay will be used (note names,
                interval names, finger names)
    
For each interval in an arpeggio, the user can adjust: 
    SHAPE       Define which intervals are represented by which shapes.
    COLOUR      Define which intervals are represented by which colour.
    TEXTCOLOUR  Define which colour is used in the text.

This way, the user can use the shapes and colours to indicate the intervals,
so the node text can display the note name or finger name.

Idea: what if we display a transparency of a hand over the fretboard instead of
displaying finger names in the nodes?
"""

from random import random
from tkinter import *
from tkinter.ttk import *

from data.intervallic_canon import DIATONIC_SCALE, HEPTATONIC_SYSTEM_BY_NAME, HEPTATONIC_SYSTEM_BY_NUMBER

from src.nomenclature import chromatic
from src.rendering import render_plain
from src.utils import shift_list
from src.models.diagrams import (GuitarFingering, check_fingering,
                                 get_interval_map, get_positional_fingering,
                                 standard_fretboard)
from data.keywords import (OPEN, 
                           CLOSE, 
                           INDEX, 
                           PINKY, 
                           NOTE_NAME, 
                           SCALE_DEGREE, 
                           FINGER, 
                           FRET,
                           HEPTATONIC_ORDER)






class FretboardDiagramWidget(Tk):
    """Widget to display interactive fretboard diagrams."""


    def __init__(self) -> None:
        super().__init__()

        # Pre-set values for testing. This initializer will have to change
        # for the real version of the widget.
        self.node_repr_style: str = NOTE_NAME
        self.diagram: GuitarFingering = GuitarFingering(5, standard_fretboard(), 5, INDEX)

        self.stretch: str = INDEX
        self.rows: int = len(self.diagram.grid)
        self.columns: int = len(self.diagram.grid[0])
        self.diagram.flash_diagram()

        self.current_scale: str = "diatonic"
        self.current_key: str = "C"
        self.current_position: int = 5
        
        self.diagram.define_intervals(get_interval_map("C"))
        self.diagram.apply_fingering()
        self.change_rendering_style("note_name")


        # Set up tkinter frames.

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
        self.scale_selection = StringVar(self)

        # Control 1: Scales dropdown menu
        scales =  HEPTATONIC_ORDER
        self.scale_selection.set(scales[0])
        scales_ = OptionMenu(self.control_frame, self.scale_selection, scales[0], *scales, command=self.change_scale)
        scales_.grid(column=0, row=0)
        scales_.config(width=15)


        self.control_frame.grid(column=1, row=0)
        self.mask_note_names(self.__get_scale(self.current_scale))

    def __get_scale(self, scale_name: str) -> list[str]:        
        scale: int = HEPTATONIC_SYSTEM_BY_NAME[scale_name]
        return render_plain(scale, shift_list(chromatic(), self.current_key))
    

    def refresh_diagram(self, position: int, width: int, stretch: str) -> None:
        self.diagram = GuitarFingering(position, standard_fretboard(), width, stretch)


    def change_position(self, position: int) -> None:
        """Adjust the diagram to display a different position of the 
        fretboard."""
        width = 4 if check_fingering(
            self.__get_scale(self.current_scale), 
            get_positional_fingering(
                self.diagram.fretboard, position, 4)) else 5
        
        self.diagram = GuitarFingering(position, 
                                       standard_fretboard(),
                                       width, 
                                       self.stretch)


    def change_scale(self, *args) -> None:
        """Change the scale that underlies the diagram."""
        self.current_scale = self.scale_selection.get()
        self.mask_note_names(self.__get_scale(self.current_scale))
        if not self.diagram.lowest_note:
            adjustment = random.choice(1, -1)
            self.change_position(self.current_position + adjustment)
            return self.change_scale()
        
        


    def change_stretch(self, *args) -> None:
        """Change which finger stretches in the diagram."""
        # self.stretch = self.stretch_selection.get()

    def change_key(self, *args) -> None:
        # self.current_key = self.key_selection.get()
        ...


    def change_rendering_style(self, style: str) -> None:
        """Indicate a new rendering style.."""
        for string in self.diagram.grid:
            for note in string:
                note.rendering_mode = style


    def mask_note_names(self, scale: list[str]) -> None:
        """Set the diagram to display only note names in the given list."""
        self.diagram.mask_note_names(scale)
        self.display_active_nodes()


    # Mask the scale so that only scale tones are allowed to show.
    # But we also want to distinguish so that chord tones are not
    # the same as scale tones.
    # Scale tones in grey, but chord tones in black (e.g.)
    # But also, rephrase the intervals for each tonal centre,
    # so that each chord's root becomes the tonic of its own mode
    # OR, use the absolute relation to the parent scale.


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

        self.canvas.delete("node_shape")
        self.canvas.delete("node_text")
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        square_size: tuple[int, int] = width//self.columns, height//self.rows

        for i, string in enumerate(self.diagram.grid):
            for j, note in enumerate(string):
                if note.is_active:
                    centre: tuple[int, int] = (
                        (square_size[0] // 2) + square_size[0] * j, 
                        (square_size[1] // 2) + square_size[1] * i
                        )
                    
                    match note.shape:
                        case "circle":
                            self.canvas.create_oval(centre[0] - 15,
                                                    centre[1] - 15,
                                                    centre[0] + 15,
                                                    centre[1] + 15,
                                                    fill=note.shape_colour,
                                                    tags="node_shape"
                                                    )

                        case "inverted_triangle":
                            p1, p2 = centre[0] - 20, centre[1] - 10
                            p3, p4 = centre[0] + 20, centre[1] - 10
                            p5, p6 = centre[0], centre[1] + 20
                            self.canvas.create_polygon(p1, p2, p3, p4, p5, p6,
                                                       fill=note.shape_colour,
                                                       tags="node_shape"
                                                       )

                        case "triangle":
                            p1, p2 = centre[0] + 20, centre[1] + 15
                            p3, p4 = centre[0] - 20, centre[1] + 15
                            p5, p6 = centre[0], centre[1] - 20
                            self.canvas.create_polygon(p1, p2, p3, p4, p5, p6,
                                                       fill=note.shape_colour,
                                                       tags="node_shape"
                                                       )

                    self.canvas.create_text(centre[0],
                                            centre[1],
                                            text=repr(note),
                                            fill=note.text_colour,
                                            font=("Times", "16", "bold"),
                                            tags="node_text"
                                            )

        self.canvas.grid()
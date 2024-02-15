"""Widgets that make up the GUI"""


from tkinter import E, EW, NS, NSEW, S, W, Canvas, Tk, StringVar, IntVar
from tkinter.ttk import Button, Frame, OptionMenu, LabelFrame, Label
from typing import Any, Callable, cast

from data.annotations import NodeDisplayReport, FingeringReport, ScaleformReport
from data.intervallic_canon import DIATONIC_SCALE, HEPTATONIC_SYSTEM_BY_NAME
from data.keywords import (DIATONIC, FINGER, FINGERING, FRET,
                           INVERSE_TRIANGLE,
                           IONIAN, KEYNOTE, MODAL_NAME_SERIES, MODE, NOTE_NAME, SCALE,
                           SHAPE,
                           COLOUR,
                           HEPTATONIC_ORDER,
                           SIZE,
                           SQUARE,
                           STRING,
                           TEXT_SIZE,
                           TEXT_COLOUR,
                           INTERVAL,
                           BLACK,
                           TRIANGLE,
                           WHITE,
                           CIRCLE)
from gui.config import (DIAGRAM_NODE_SIZES,
                        DIAGRAM_SHAPES,
                        DIAGRAM_TEXT_SIZES,
                        COLOURS,
                        FINGERING_TYPES)
from src import bitwise
from src.models.diagrams import GuitarFingeringDiagram, get_interval_map, standard_fretboard
from src.nomenclature import chromatic, twelve_tone_scale_intervals
from src.rendering import render_plain
from src.utils import shift_list


class ScaleSelectorWidget(LabelFrame):
    """A widget that allows the user to change which scale, mode, key, and 
    position the diagram is currently set to.

    Scale defines the basic pattern of intervals that will be used.
    Key defines which note will serve as the tonic of the scale.
    Mode defines which degree of the scale the intervals will be related to.
    Position defines where on the fretboard to show the scale form."""

    def __init__(self,
                 master: Tk | Frame | LabelFrame,
                 callback: Callable[..., Any]
                 ) -> None:

        LabelFrame.__init__(self, master, text="Select Scale Pattern")
        self.scale = StringVar(self, value=DIATONIC)
        self.mode = StringVar(self, value=IONIAN)
        self.key = StringVar(self, "C")
        self.callback = callback

        self.select_scale = OptionMenu(
            self, self.scale, self.scale.get(), *HEPTATONIC_ORDER, command=self.change_state)
        self.select_mode = OptionMenu(
            self, self.mode, self.mode.get(), *MODAL_NAME_SERIES, command=self.change_state)
        self.select_key = OptionMenu(
            self, self.key, self.key.get(), *chromatic(), command=self.change_state)

        self.select_scale.grid(column=0, row=0)
        self.select_scale.config(width=15)
        self.select_mode.grid(column=1, row=0)
        self.select_mode.config(width=15)
        self.select_key.grid(column=2, row=0)
        self.select_key.config(width=10)

    def change_state(self, *args) -> None:
        """Alert the controller about any change in state."""
        self.callback(self.report())

    def report(self) -> dict[str, str]:
        """Return a report about the current state of the widget."""
        return {SCALE: self.scale.get(),
                MODE: self.mode.get(),
                KEYNOTE: self.key.get()}


class StringFingeringWidget(Frame):
    """A small widget that controls how a string will be fingered.

    A button is displayed and will cycle through a series of states
    when it is clicked. It reports any change of state to a callback
    function.
    """

    def __init__(self,
                 master: Frame | Tk | LabelFrame,
                 callback: Callable[..., Any],
                 string: int
                 ) -> None:

        Frame.__init__(self, master)
        self.callback: Callable[..., Any] = callback

        self.string = string
        self.fingering_options: list[str] = FINGERING_TYPES
        self.current_fingering: str = FINGERING_TYPES[0]

        self.string_toggle: Button = Button(self,
                                            text=self.current_fingering,
                                            command=self.change_state)
        self.string_toggle.grid()

    def report(self) -> FingeringReport:
        """Return a report about the current state of the widget."""
        return cast(FingeringReport, {
            STRING: self.string,
            FINGERING: self.current_fingering}
        )

    def change_state(self, *args) -> None:
        """Toggle the string's fingering into the next state, and inform the
        callback function of the current state of the widget."""
        state: int = self.fingering_options.index(self.current_fingering)
        if state == len(self.fingering_options) - 1:
            self.current_fingering = self.fingering_options[0]
        else:
            self.current_fingering = self.fingering_options[state + 1]
        self.string_toggle.configure(text=self.current_fingering)
        self.callback(self.report())


class IntervalDisplayWidget(Frame):
    """A small widget that controls how an interval will be displayed in the 
    fingering diagram.

    The widget shows options for the shape, size, colour, text colour, and 
    text size for the individual interval nodes in the fretboard diagram.
    The user is able to select from pre-defined options in each category
    and any change of state is reported to a callback function."""

    def __init__(self,
                 master: Frame | Tk | LabelFrame,
                 callback: Callable[..., Any],
                 interval: str,
                 shape: str = CIRCLE,
                 size: int = 2,
                 colour: str = BLACK,
                 text_colour: str = WHITE,
                 text_size: int = 14) -> None:

        Frame.__init__(self, master)
        self.callback: Callable[..., Any] = callback

        self.interval = interval

        self.shape_options: list[str] = DIAGRAM_SHAPES
        self.size_options: list[int] = DIAGRAM_NODE_SIZES
        self.text_size_options: list[int] = DIAGRAM_TEXT_SIZES
        self.colour_options: list[str] = COLOURS

        self.shape = StringVar(self, value=shape)
        self.size = IntVar(self, value=size)
        self.colour = StringVar(self, value=colour)
        self.text_colour = StringVar(self, value=text_colour)
        self.text_size = IntVar(self, value=text_size)

        self.select_shape = OptionMenu(
            self,
            self.shape,
            self.shape.get(),
            *self.shape_options,
            command=self.change_state)

        self.select_size = OptionMenu(
            self,
            self.size,
            str(self.size.get()),
            *[str(x) for x in self.size_options],
            command=self.change_state)

        self.select_colour = OptionMenu(
            self,
            self.colour,
            self.colour.get(),
            *self.colour_options,
            command=self.change_state)

        self.select_text_colour = OptionMenu(
            self,
            self.text_colour,
            self.text_colour.get(),
            *self.colour_options,
            command=self.change_state)

        self.select_text_size = OptionMenu(
            self,
            self.text_size,
            str(self.text_size.get()),
            *[str(x) for x in self.text_size_options],
            command=self.change_state)

        for i, (label, widget) in enumerate(
            [(SHAPE, self.select_shape),
             (SIZE, self.select_size),
             (COLOUR, self.select_colour),
             (TEXT_COLOUR, self.select_text_colour),
             (TEXT_SIZE, self.select_text_size)]):

            label_ = Label(self, text=str.replace(
                label, "_", " ").capitalize())
            label_.grid(column=0, row=i, sticky="w")
            widget.grid(column=1, row=i, sticky="e")
            widget.config(width=15)

    def change_state(self, *args) -> None:
        """Respond to any change of state by sending a report about the 
        current state to the controller's callback."""
        self.callback(self.report())

    def report(self) -> dict[str, str | int]:
        """Return a report about the current state of the widget."""
        return {INTERVAL: self.interval,
                SHAPE: self.shape.get(),
                SIZE: self.size.get(),
                COLOUR: self.colour.get(),
                TEXT_COLOUR: self.text_colour.get(),
                TEXT_SIZE: self.text_size.get()}


class IntervalDisplaySelector(LabelFrame):
    """Widget that contains many IntervalDisplayWidgets allows the user to
    select which one is currently displayed.

    The widget shows a dropdown menu which, when an interval is selected, 
    causes an interval node control panel for that interval to appear below.
    It passes a callback function to all the control panels generated by
    the list of intervals provided."""

    def __init__(self,
                 master: Frame | Tk,
                 callback: Callable[..., Any],
                 intervals: list[str]
                 ) -> None:

        LabelFrame.__init__(self, master)
        self.callback = callback
        self.intervals = intervals

        self.current_interval = StringVar(self, value=self.intervals[0])
        self.select_interval = OptionMenu(
            self,
            self.current_interval,
            self.current_interval.get(),
            *self.intervals,
            command=self.display_subwidget)

        self.subwidgets: list[IntervalDisplayWidget] = []
        for x in self.intervals:
            self.subwidgets.append(IntervalDisplayWidget(self, callback, x))

        self.current_subwidget: IntervalDisplayWidget = self.subwidgets[0]
        label = Label(self, text="Select interval: ")
        label.grid(column=0, row=0, sticky="w")
        self.select_interval.grid(column=1, row=0, sticky="e")
        self.current_subwidget.grid(column=0, row=1, columnspan=2)

        self.config(text="Interval Controls",
                    borderwidth=5,
                    labelanchor="nw",
                    relief="sunken",)

    def rename_intervals(self, intervals: list[str]) -> None:
        """Rename the series of intervals that label the subwidgets."""
        for i, interval in enumerate(intervals):
            self.subwidgets[i].interval = interval

    def display_subwidget(self, *args) -> None:
        """Change which subwidget is currently being displayed, based on the 
        selected option in the dropdown menu."""
        self.current_subwidget.grid_forget()
        for x in self.subwidgets:
            if x.interval == self.current_interval.get():
                self.current_subwidget = x
        self.current_subwidget.grid(column=0, row=1, columnspan=2)

    def summarize(self) -> list[dict[str, int | str]]:
        """Return a summary of the current state of all subwidgets
        controlled by this widget."""
        return [x.report() for x in self.subwidgets]


class StringFingeringSelector(LabelFrame):
    """Widget that contains a number of buttons to cycle strings' 
    fingerings through various states."""

    def __init__(self,
                 master: Tk | Frame | LabelFrame,
                 callback: Callable[..., Any],
                 number_of_strings: int) -> None:

        LabelFrame.__init__(self, master)
        self.config(text="String Fingering Controls",
                    borderwidth=5,
                    labelanchor="nw",
                    relief="sunken")
        self.subwidgets: list[StringFingeringWidget] = []

        padding: int = 175 // number_of_strings
        for x in range(number_of_strings):
            w = StringFingeringWidget(self, callback, x)
            self.subwidgets.append(w)
            l = Label(self, text=f"String {x}: ")
            l.grid(column=0, row=x, sticky=W, pady=padding)
            w.grid(column=1, row=x, sticky=E, pady=padding)

    def summarize(self) -> list[FingeringReport]:
        """Return a summary of the current state of all subwidgets
        controlled by this widget."""
        return [x.report() for x in self.subwidgets]


class FingerboardGridWidget(LabelFrame):
    """A large widget that represents a grid, in the cells of which are shapes
    representing notes, fingers, or intervals.

    This widget only ever displays information, it doesn't pass anything back to
    the controller."""

    def __init__(self, master: Tk | Frame | LabelFrame, diagram: GuitarFingeringDiagram) -> None:

        LabelFrame.__init__(self, master)
        self.config(text="Fretboard Diagram")
        self.canvas: Canvas = Canvas(self, height=500, width=500, bg="white")

        self.canvas.grid()
        self.canvas.update()

        self.draw_diagram(diagram)

    def draw_diagram(self, diagram: GuitarFingeringDiagram) -> None:
        """Create a rendering of the given diagram."""
        self.__draw_grid(len(diagram.grid), len(diagram.grid[0]))
        self.__draw_active_nodes(diagram)

    def __draw_grid(self, rows: int, columns: int) -> None:
        """Draw the grid based on the dimensions of the diagram object."""
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        self.canvas.delete("all")

        for i in range(0, width, width // columns):
            self.canvas.create_line([(i, 0), (i, height)], tags="grid_line")
        for i in range(0, height, height // rows):
            self.canvas.create_line([(0, i), (width, i)], tags="grid_line")
        self.canvas.grid()

    def __draw_active_nodes(self, diagram: GuitarFingeringDiagram) -> None:
        """Reload the display to show only the diagram's active nodes."""

        self.canvas.delete("node_shape")
        self.canvas.delete("node_text")
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        square_size: tuple[int,
                           int] = width//len(diagram.grid[0]), height//len(diagram.grid)

        for i, string in enumerate(diagram.grid):
            for j, node in enumerate(string):
                if not node.is_active:
                    continue

                centre: tuple[int, int] = (
                    (square_size[0] // 2) + square_size[0] * j,
                    (square_size[1] // 2) + square_size[1] * i
                )

                if node.shape == CIRCLE:
                    x0, y0 = centre[0] - 15, centre[1] - 15
                    x1, y1 = centre[0] + 15, centre[1] + 15
                    self.canvas.create_oval(x0, y0, x1, y1,
                                            fill=node.shape_colour,
                                            tags="node_shape"
                                            )

                elif node.shape == SQUARE:
                    x0, y0 = centre[0] - 15, centre[1] - 15
                    x1, y1 = centre[0] + 15, centre[1] + 15
                    self.canvas.create_rectangle(x0, y0, x1, y1,
                                                 fill=node.shape_colour,
                                                 tags="node_shape"
                                                 )

                elif node.shape == INVERSE_TRIANGLE:
                    x0, y0 = centre[0] - 20, centre[1] - 10
                    x1, y1 = centre[0] + 20, centre[1] - 10
                    x2, y2 = centre[0], centre[1] + 20
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2,
                                               fill=node.shape_colour,
                                               tags="node_shape"
                                               )

                elif node.shape == TRIANGLE:
                    x0, y0 = centre[0] + 20, centre[1] + 15
                    x1, y1 = centre[0] - 20, centre[1] + 15
                    x2, y2 = centre[0], centre[1] - 20
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2,
                                               fill=node.shape_colour,
                                               tags="node_shape"
                                               )

                else:
                    raise ValueError(
                        f"Unknown node setting: shape={node.shape}")

                self.canvas.create_text(centre[0],
                                        centre[1],
                                        text=repr(node),
                                        fill=node.text_colour,
                                        font=("Times", "12", "bold"),
                                        tags="node_text"
                                        )
        self.canvas.grid()


class DisplaySelector(LabelFrame):
    """A small widget that controls the display type."""

    def __init__(self, master: Tk | Frame | LabelFrame, callback: Callable[..., Any]) -> None:
        LabelFrame.__init__(self, master)
        self.callback = callback
        self.config(text="Select Display Mode")
        self.display_type = StringVar(self)
        self.display_options = [INTERVAL, FINGER, NOTE_NAME, FRET]
        self.select_display = OptionMenu(
            self,
            self.display_type,
            self.display_options[0],
            *self.display_options,
            command=self.change_state)

        self.select_display.grid()

    def change_state(self, *args) -> None:
        """Report any change of state to the controller."""
        self.callback(self.display_type.get())


class PositionSelector(LabelFrame):
    """A small widget that controls the current position."""

    def __init__(self, master: Tk | Frame | LabelFrame, positions: list[int], callback: Callable[..., Any]) -> None:
        LabelFrame.__init__(self, master)
        self.callback = callback
        self.config(text="Select Position")
        self.position = IntVar(self)
        self.position_options = positions
        self.select_position = OptionMenu(self,
                                          self.position,
                                          *[str(x) for x in positions],
                                          command=self.change_state)
        self.select_position.grid()

    def change_state(self, *args) -> None:
        """Report any change of state to the controller."""
        self.callback(self.report())

    def set_position(self, position: int) -> None:
        """Set the current position. (Used when the scale has changed in such
        a way that the previous position is no longer legal)."""
        self.position.set(position)

    def report(self) -> int:
        """Report on the current state of the widget."""
        return self.position.get()


class FretboardDiagram(Frame):
    """Main widget for the fretboard diagram."""

    def __init__(self, master: Frame | Tk):
        Frame.__init__(self, master)

        self.diagram: GuitarFingeringDiagram = GuitarFingeringDiagram(
            5, standard_fretboard(), 5)
        self.diagram.define_scale(render_plain(DIATONIC_SCALE))
        self.diagram.define_intervals(get_interval_map("C"))
        self.diagram.turn_on_names(render_plain(DIATONIC_SCALE))

        # Top bar
        self.scale_selector = ScaleSelectorWidget(
            self,
            self.on_scale_change)
        self.scale_selector.grid(column=0, row=0, sticky=W)

        self.position_selector = PositionSelector(
            self,
            self.diagram.positions(render_plain(DIATONIC_SCALE)),
            self.on_position_change)
        self.position_selector.grid(column=1, row=0, sticky=W)

        self.display_type_selector = DisplaySelector(
            self,
            self.on_display_mode_change)
        self.display_type_selector.grid(column=2, row=0, sticky=W)

        # Left large window (main diagram display)
        self.fingerboard_grid = FingerboardGridWidget(
            self,
            self.diagram)
        self.fingerboard_grid.grid(column=0, row=1, columnspan=2)

        # Centre narrow window
        self.fingering_panel = StringFingeringSelector(
            self,
            self.on_fingering_change,
            self.diagram.number_of_strings)
        self.fingering_panel.grid(column=2, row=1, sticky=EW)


        # self.interval_panel = IntervalDisplaySelector(self, self.on_node_option_change, )

        # Frame 4: Main Option Panel (RIGHT, STATE-BASED)
        self.mode_toggle: Button  # change state
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

        self.grid()

        # Display initial values
        self.scale_selector.change_state()
        for report in self.fingering_panel.summarize():
            self.diagram.apply_fingering(**report)


    def on_fingering_change(self, report: FingeringReport) -> None:
        """Receive a report about the change in fingering and modify the 
        diagram to reflect it"""
        self.diagram.apply_fingering(**report)
        self.fingerboard_grid.draw_diagram(self.diagram)

    def on_node_option_change(self, report: NodeDisplayReport) -> None:
        """Receive a report about the change to an interval node's
        display options and modify the diagram to reflect it."""
        print(f"main class got report {report}")

    def on_scale_change(self, report: ScaleformReport) -> None:
        """Receive a report about the change to the main scale paradigm
        and modify the diagram to reflect it."""
        note_names_ = list(set(self.diagram.active_names))
        pos = self.diagram.positions(note_names_)
        i = pos.index(self.diagram.position)

        scaleform: int = HEPTATONIC_SYSTEM_BY_NAME[report[SCALE]]
        j: int = MODAL_NAME_SERIES.index(report[MODE])
        modalform = bitwise.inversions(scaleform, 12)[j]
        keynote = report[KEYNOTE]
        note_names = render_plain(
            modalform, shift_list(chromatic(), keynote))
        intervals = get_interval_map(keynote, modalform)

        self.diagram.define_scale(note_names)
        self.diagram.define_intervals(intervals)
        self.diagram.turn_on_names(note_names)

        pos = self.diagram.positions(note_names)
        if self.diagram.position not in pos:
            self.on_position_change(pos[i])

        self.fingerboard_grid.draw_diagram(self.diagram)

    def on_display_mode_change(self, report: str) -> None:
        """Receive a report about the change to the display mode
        and modify the diagram to reflect it."""
        self.diagram.apply_rendering_mode(report)
        self.fingerboard_grid.draw_diagram(self.diagram)

    def on_position_change(self, report: int) -> None:
        """Receive a report about the change to the position
        and modify the diagram to reflect it."""
        self.diagram.position = report
        scale = self.diagram.active_names
        # Keep working here. We need to write a function
        # in the diagram class that can extract the notes 
        # and intervals and transfer them to the new grid.
        # also extract node options settings.

        self.diagram.grid = self.diagram.new_grid()
        self.fingerboard_grid.draw_diagram(self.diagram)
        


        # get node options
        # rename intervals in widget
        # rename intervals in node options
        # for report in node options self.node_option_change(report)

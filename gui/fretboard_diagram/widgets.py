
"""Widgets that make up the GUI of the Fingering Diagram app."""
import typing
import tkinter as tk
from tkinter import (
    ttk,
    font as tkfont
)

from data import (
    keywords as K,
    annotations as T,
    errors as E
)

from src import interface
from src.models import diagrams
from gui.fretboard_diagram import (
    config,
    functions
)

if typing.TYPE_CHECKING:
    from .app import FretboardDiagramApp

__all__ = [
    "ScaleSelector",
    "PositionSelector",
    "RenderingModeSelector",
    "InterfaceModeToggle",
    "FingerboardGrid",
    "StringFingeringSelector",
    "IntervalDisplaySelector",
    "ArpeggioModeControlPanel"
]


class ScaleSelector(ttk.LabelFrame):
    """A widget that allows the user to change which scale, mode, key, and 
    position the diagram is currently set to.

    Scale defines the basic pattern of intervals that will be used.
    Key defines which note will serve as the tonic of the scale.
    Mode defines which degree of the scale the intervals will be related to.
    Position defines where on the fretboard to show the scale form."""

    def __init__(self,
                 master: "FretboardDiagramApp",
                 callback: typing.Callable[..., typing.Any]
                 ) -> None:

        ttk.LabelFrame.__init__(self, master, text="Select Scale Pattern")
        self.scale = tk.StringVar(self, value=K.DIATONIC)
        self.mode = tk.StringVar(self, value=K.IONIAN)
        self.key = tk.StringVar(self, "C")
        self.callback = callback

        self.select_scale = ttk.OptionMenu(
            self, self.scale, self.scale.get(), *K.HEPTATONIC_ORDER, command=self.change_state)
        self.select_mode = ttk.OptionMenu(
            self, self.mode, self.mode.get(), *K.MODAL_NAME_SERIES, command=self.change_state)
        self.select_key = ttk.OptionMenu(
            self, self.key, self.key.get(), *interface.chromatic(), command=self.change_state)

        self.select_scale.grid(column=0, row=0)
        self.select_scale.config(width=15)
        self.select_mode.grid(column=1, row=0)
        self.select_mode.config(width=15)
        self.select_key.grid(column=2, row=0)
        self.select_key.config(width=10)

    def change_state(self, *_: typing.Any) -> None:
        """Alert the controller about any change in state."""
        self.callback(self.report())

    def report(self) -> dict[str, str]:
        """Return a report about the current state of the widget."""
        return {K.SCALE_NAME: self.scale.get(),
                K.MODAL_NAME: self.mode.get(),
                K.KEYNOTE: self.key.get()}


class StringFingeringSubWidget(ttk.Frame):
    """A small widget that controls how a string will be fingered.

    A button is displayed and will cycle through a series of states
    when it is clicked. It reports any change of state to a callback
    function.
    """

    def __init__(self,
                 master: ttk.Frame | tk.Tk | ttk.LabelFrame,
                 callback: typing.Callable[..., typing.Any],
                 string: int
                 ) -> None:

        ttk.Frame.__init__(self, master)
        self.callback: typing.Callable[..., typing.Any] = callback

        self.string = string
        self.fingering_options: list[str] = config.FINGERING_TYPES
        self.current_fingering: str = config.FINGERING_TYPES[0]

        self.string_toggle: ttk.Button = ttk.Button(self,
                                                    text=self.current_fingering,
                                                    command=self.change_state)
        self.string_toggle.grid()

    def report(self) -> T.FingeringReport:
        """Return a report about the current state of the widget."""
        # return cast(T.FingeringReport, {
        #     K.STRING: self.string,
        #     K.FINGERING: self.current_fingering}
        # )
        return T.FingeringReport(
            string=self.string,
            fingering=self.current_fingering
        )

    def change_state(self) -> None:
        """Toggle the string's fingering into the next state, and inform the
        callback function of the current state of the widget."""
        i: int = functions.cycle_indices(
            self.fingering_options, self.current_fingering)
        self.current_fingering = self.fingering_options[i]
        self.string_toggle.configure(text=self.current_fingering)
        self.callback(self.report())


class IntervalDisplaySubWidget(ttk.Frame):
    """A small widget that controls how an interval will be displayed in the 
    fingering diagram.

    The widget shows options for the shape, size, colour, text colour, and 
    text size for the individual interval nodes in the fretboard diagram.
    The user is able to select from pre-defined options in each category
    and any change of state is reported to a callback function."""

    def __init__(self,
                 master: ttk.Frame | tk.Tk | ttk.LabelFrame,
                 callback: typing.Callable[..., typing.Any],
                 interval: str,
                 shape: str = K.CIRCLE,
                 size: int = 2,
                 colour: str = K.BLACK,
                 text_colour: str = K.WHITE,
                 text_size: int = 14) -> None:

        ttk.Frame.__init__(self, master)
        self.callback: typing.Callable[..., typing.Any] = callback

        self.interval = interval

        self.shape_options: list[str] = config.DIAGRAM_SHAPES
        self.size_options: list[int] = config.DIAGRAM_NODE_SIZES
        self.text_size_options: list[int] = config.DIAGRAM_TEXT_SIZES
        self.colour_options: list[str] = config.COLOURS

        self.shape = tk.StringVar(self, value=shape)
        self.size = tk.IntVar(self, value=size)
        self.colour = tk.StringVar(self, value=colour)
        self.text_colour = tk.StringVar(self, value=text_colour)
        self.text_size = tk.IntVar(self, value=text_size)

        self.select_shape = ttk.OptionMenu(
            self,
            self.shape,
            self.shape.get(),
            *self.shape_options,
            command=self.change_state)

        self.select_size = ttk.OptionMenu(
            self,
            self.size,  # type:ignore
            str(self.size.get()),
            *[str(x) for x in self.size_options],
            command=self.change_state)

        self.select_colour = ttk.OptionMenu(
            self,
            self.colour,
            self.colour.get(),
            *self.colour_options,
            command=self.change_state)

        self.select_text_colour = ttk.OptionMenu(
            self,
            self.text_colour,
            self.text_colour.get(),
            *self.colour_options,
            command=self.change_state)

        self.select_text_size = ttk.OptionMenu(
            self,
            self.text_size,  # type:ignore
            str(self.text_size.get()),
            *[str(x) for x in self.text_size_options],
            command=self.change_state)

        for i, (label, widget) in enumerate(
            [(K.SHAPE, self.select_shape),
             (K.SHAPE_SIZE, self.select_size),
             (K.SHAPE_COLOUR, self.select_colour),
             (K.TEXT_COLOUR, self.select_text_colour),
             (K.TEXT_SIZE, self.select_text_size)]):

            label_ = ttk.Label(self, text=str.replace(
                label, "_", " ").capitalize())
            label_.grid(column=0, row=i, sticky="w")
            widget.grid(column=1, row=i, sticky="e")
            widget.config(width=15)

    def change_state(self, *_: typing.Any) -> None:
        """Respond to any change of state by sending a report about the 
        current state to the controller's callback."""
        self.callback(self.report())

    def report(self) -> T.NodeDisplayReport:
        """Return a report about the current state of the widget."""
        return T.NodeDisplayReport(interval=self.interval,
                                   shape=self.shape.get(),
                                   size=self.size.get(),
                                   shape_colour=self.colour.get(),
                                   text_colour=self.text_colour.get(),
                                   text_size=self.text_size.get())


class IntervalDisplaySelector(ttk.LabelFrame):
    """Widget that contains many IntervalDisplaySubWidgets allows the user to
    select which one is currently displayed.

    The widget shows a dropdown menu which, when an interval is selected, 
    causes an interval node control panel for that interval to appear below.
    It passes a callback function to all the control panels generated by
    the list of intervals provided.
    """

    def __init__(self,
                 master: "FretboardDiagramApp",
                 callback: typing.Callable[..., typing.Any],
                 intervals: list[str]
                 ) -> None:

        ttk.LabelFrame.__init__(self, master)
        self.callback = callback
        self.intervals = intervals

        self.current_interval = tk.StringVar(self, value=self.intervals[0])
        self.select_interval = ttk.OptionMenu(
            self,
            self.current_interval,
            self.current_interval.get(),
            *self.intervals,
            command=self.display_subwidget)

        self.subwidgets: list[IntervalDisplaySubWidget] = []
        for x in self.intervals:
            self.subwidgets.append(IntervalDisplaySubWidget(self, callback, x))

        self.current_subwidget: IntervalDisplaySubWidget = self.subwidgets[0]
        label = ttk.Label(self, text="Select interval: ")
        label.grid(column=0, row=0, sticky=tk.W)
        self.select_interval.grid(column=1, row=0, sticky=tk.E)
        self.current_subwidget.grid(column=0, row=2, columnspan=2)

        self.config(text="Interval Controls",
                    borderwidth=5,
                    labelanchor=tk.NW,
                    relief=tk.SUNKEN,)

    def set_subwidget(self, interval: str) -> None:
        """Set the currently visible subwidget to the given interval."""
        self.current_interval.set(interval)
        self.display_subwidget()

    def rename_intervals(self, intervals: list[str]) -> None:
        """Rename the series of intervals that label the subwidgets."""
        self.intervals = intervals
        for i, interval in enumerate(intervals):
            self.subwidgets[i].interval = interval
        self.select_interval.set_menu(
            self.intervals[0], *self.intervals)  # type:ignore

    def display_subwidget(self, *_: typing.Any) -> None:
        """Change which subwidget is currently being displayed, based on the 
        selected option in the dropdown menu."""
        self.current_subwidget.grid_forget()
        for x in self.subwidgets:
            if x.interval == self.current_interval.get():
                self.current_subwidget = x
        self.current_subwidget.grid(column=0, row=1, columnspan=2)

    def summarize(self) -> list[T.NodeDisplayReport]:
        """Return a summary of the current state of all subwidgets
        controlled by this widget."""
        return [x.report() for x in self.subwidgets]


class StringFingeringSelector(ttk.LabelFrame):
    """Widget that contains a number of buttons to cycle strings' 
    fingerings through various states.
    """

    def __init__(self,
                 master: "FretboardDiagramApp",
                 callback: typing.Callable[..., typing.Any],
                 number_of_strings: int) -> None:

        ttk.LabelFrame.__init__(self, master)
        self.config(text="String Fingering Controls",
                    borderwidth=5,
                    labelanchor="nw",
                    relief="sunken")
        self.subwidgets: list[StringFingeringSubWidget] = []

        padding: int = 175 // number_of_strings
        for x in range(number_of_strings):
            w = StringFingeringSubWidget(self, callback, x)
            self.subwidgets.append(w)
            l = ttk.Label(self, text=f"String {x}: ")
            l.grid(column=0, row=x, sticky=tk.W, pady=padding)
            w.grid(column=1, row=x, sticky=tk.E, pady=padding)

    def summarize(self) -> list[T.FingeringReport]:
        """Return a summary of the current state of all subwidgets
        controlled by this widget."""
        return [x.report() for x in self.subwidgets]


class FingerboardGrid(ttk.LabelFrame):
    """A large widget that represents a grid, in the cells of which are shapes
    representing notes, fingers, or intervals.

    This widget only ever displays information, it doesn't pass anything back to
    the controller."""

    def __init__(self,
                 master: "FretboardDiagramApp",
                 diagram: diagrams.GuitarFingeringDiagram) -> None:

        ttk.LabelFrame.__init__(self, master)
        self.config(text="Fretboard Diagram")
        self.canvas: tk.Canvas = tk.Canvas(
            self, height=config.CANVAS_SIZE, width=config.CANVAS_SIZE, bg="white")

        self.canvas.grid()
        self.canvas.update()

        self.draw_diagram(diagram)

    def draw_diagram(self, diagram: diagrams.GuitarFingeringDiagram) -> None:
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

    def __draw_active_nodes(self, diagram: diagrams.GuitarFingeringDiagram) -> None:
        """Reload the display to show only the diagram's active nodes."""

        self.canvas.delete("node_shape")
        self.canvas.delete("node_text")
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        square_size: tuple[int, int] = (width//len(diagram.grid[0]), 
                                        height//len(diagram.grid))

        for i, string in enumerate(diagram.grid):
            for j, node in enumerate(string):
                if not node.is_active:
                    continue

                centre: tuple[int, int] = (
                    (square_size[0] // 2) + square_size[0] * j,
                    (square_size[1] // 2) + square_size[1] * i
                )

                if node.shape == K.CIRCLE:
                    x0, y0 = centre[0] - 15, centre[1] - 15
                    x1, y1 = centre[0] + 15, centre[1] + 15
                    self.canvas.create_oval(x0, y0, x1, y1,
                                            fill=node.shape_colour,
                                            tags="node_shape"
                                            )

                elif node.shape == K.SQUARE:
                    x0, y0 = centre[0] - 15, centre[1] - 15
                    x1, y1 = centre[0] + 15, centre[1] + 15
                    self.canvas.create_rectangle(x0, y0, x1, y1,
                                                 fill=node.shape_colour,
                                                 tags="node_shape"
                                                 )

                elif node.shape == K.INVERSE_TRIANGLE:
                    x0, y0 = centre[0] - 20, centre[1] - 10
                    x1, y1 = centre[0] + 20, centre[1] - 10
                    x2, y2 = centre[0], centre[1] + 20
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2,
                                               fill=node.shape_colour,
                                               tags="node_shape"
                                               )

                elif node.shape == K.TRIANGLE:
                    x0, y0 = centre[0] + 20, centre[1] + 15
                    x1, y1 = centre[0] - 20, centre[1] + 15
                    x2, y2 = centre[0], centre[1] - 20
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2,
                                               fill=node.shape_colour,
                                               tags="node_shape"
                                               )

                elif node.shape == K.DIAMOND:
                    x0, y0 = centre[0], centre[1] - 15
                    x1, y1 = centre[0] - 15, centre[1]
                    x2, y2 = centre[0], centre[1] + 15
                    x3, y3 = centre[0] + 15, centre[1]
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                                               fill=node.shape_colour,
                                               tags="node_shape")

                else:
                    raise E.UnknownKeywordError(
                        f"Unknown node setting: shape={node.shape}")

                font = tkfont.Font(self,
                                   family="Times",
                                   size=node.text_size,
                                   weight="bold"
                                   )
                self.canvas.create_text(centre[0],
                                        centre[1],
                                        text=repr(node),
                                        fill=node.text_colour,
                                        font=font,
                                        tags="node_text"
                                        )
        self.canvas.grid()


class RenderingModeSelector(ttk.LabelFrame):
    """A small widget that controls the display type."""

    def __init__(self, master: "FretboardDiagramApp",
                 callback: typing.Callable[..., typing.Any]
                 ) -> None:
        ttk.LabelFrame.__init__(self, master)
        self.callback = callback
        self.config(text="Select Display Mode")
        self.current_mode = tk.StringVar(self)
        self.rendering_modes = [K.INTERVAL,
                                K.FINGER,
                                K.NOTE_NAME,
                                K.FRET]
        self.select_rendering_mode = ttk.OptionMenu(
            self,
            self.current_mode,
            self.rendering_modes[0],
            *self.rendering_modes,
            command=self.change_state)

        self.select_rendering_mode.grid()

    def report(self) -> str:
        """Return a report about the current state of the widget."""
        return self.current_mode.get()

    def change_state(self, *_: typing.Any) -> None:
        """Report any change of state to the controller."""
        self.callback(self.current_mode.get())


class PositionSelector(ttk.LabelFrame):
    """A small widget that controls the current position."""

    def __init__(self,
                 master: "FretboardDiagramApp",
                 positions: list[int],
                 callback: typing.Callable[..., typing.Any]
                 ) -> None:
        ttk.LabelFrame.__init__(self, master)
        self.callback = callback
        self.config(text="Select Position")
        self.position = tk.IntVar(self, value=5)
        self.position_options = positions
        self.select_position = ttk.OptionMenu(self,
                                              self.position,  # type:ignore
                                              str(self.position.get()),
                                              *[str(x)
                                                for x in positions if 0 < x < 13],
                                              command=self.change_state)
        self.select_position.grid()

    def change_state(self, *_: typing.Any) -> None:
        """Report any change of state to the controller."""
        self.callback(self.report())

    def set_position(self, position: int, positions: typing.Sequence[int]) -> None:
        """Set the current position. (Used when the scale has changed in such
        a way that the previous position is no longer legal)."""
        self.position.set(position)
        self.position_options = positions
        self.select_position.set_menu(
            str(position), *positions)  # type: ignore

    def report(self) -> int:
        """Report on the current state of the widget."""
        return self.position.get()


class InterfaceModeToggle(ttk.LabelFrame):
    """Simple button widget to change the state of the main app."""

    def __init__(self, master: "FretboardDiagramApp", callback: typing.Callable[..., typing.Any]) -> None:
        ttk.LabelFrame.__init__(self, master)
        self.callback = callback
        self.config(text="Select Control Mode")
        self.interface_mode_options: list[str] = [
            K.SCALE, K.ARPEGGIO]
        self.current_interface_mode: str = self.interface_mode_options[0]
        self.interface_mode_toggle: ttk.Button = ttk.Button(
            self, text=self.current_interface_mode, command=self.change_state)
        self.interface_mode_toggle.grid()

    def change_state(self) -> None:
        """Cycle to the next state, and use the callback to update the 
        controller.
        """
        i: int = functions.cycle_indices(
            self.interface_mode_options, self.current_interface_mode)
        self.current_interface_mode = self.interface_mode_options[i]
        self.interface_mode_toggle.configure(text=self.current_interface_mode)

        self.callback()


class ArpeggioModeControlPanel(ttk.LabelFrame):
    """A more sophisticated version of the IntervalDisplaySelector that allows
    the user to define which chord will be the focal point of the diagram.
    """

    def __init__(self, master: "FretboardDiagramApp", callback: typing.Callable[..., typing.Any]) -> None:
        ttk.LabelFrame.__init__(self, master)
        self.config(text="Arpeggio Display Controls")
        self.callback = callback

        window = ttk.LabelFrame(self, text="Select chord type")
        self.polyad_options = ["triad", "tetrad"]
        self.current_polyad: str = self.polyad_options[0]
        self.polyad_toggle = ttk.Button(window,
                                        text=self.current_polyad,
                                        command=self.toggle_polyad)

        # for the select chord dropdown, we want to be able to parse
        # a chord scale and generate the correct chord symbol:
        # 1. Imaj7, 2. iimin7, 3. iiimin7, 4. IVmaj7

        # but also: we should be able to name the chord too
        # 1. Dbmaj7, 2. Ebmin7, 3. Fmin7, 4. Gbmaj7

        # so maybe the dropdown is just for 1, 2, b3, 4, 5, etc.,
        # and a little display shows that 1 = Dbmaj7 (Imaj7)

        # we need to add some things to be back end in order to get the
        # necessary data for this widget.
        #   - generate a chord scale with roman numerals representing degrees
        #       - uppercase = maj 3, lowercase = min3
        #       - use same accidental as numeric interval (b3 > bIII/biii)

        #       actually, now that I think about it, just use the interval scale
        #       function, then replace any numeral with a roman numeral:
        #
        #       scale = name_heptatonic_intervals(scale_type)
        #       scale_pattern = ["maj", "min", "min", "maj", ... etc]
        #       for i, interval_name in enumerate(scale):
        #           for char in interval_name:
        #               if char.is_digit():
        #                   roman = get_roman_numeral(int(char))
        #                   if scale_patern[i] == "maj":
        #                       roman = roman.upper()
        #                   if scale_pattern[i] == "min":
        #                       roman = roman.lower()
        #                   interval_name.replace(char, roman)

    def toggle_polyad(self) -> None:
        """Cycle the widget into the next polyad configuration."""
        i = functions.cycle_indices(self.polyad_options, self.current_polyad)
        self.current_polyad = self.polyad_options[i]
        self.polyad_toggle.config(text=self.current_polyad)

        # Part 1
        # Select number of notes -triad, tetrad --> Update display
        # select chord type -tertial, quartal   --> update display

        # Part 2
        # node display selector for the intervals in the polyad
        # These settings will be carried over when we change the
        # chord degree, but the names of the intervals might
        # change as we move through the chord scale. --> update display

        # Part 3
        # select chord degree (based on frozen scale settings)
        #       therefore, when the controller activates this widget, it
        #       should update the widget's knowledge of the base scale
        #
        # the intervals in the chord are shown according to the settings
        # in part 2, but the non-chord tones are displayed opaque or greyed out


        # in order for the intervals to cycle correctly with the chords, so that
        # the third of the chord (major or minor) will sill be a blue triangle or
        # whatever, we need to regard each chord's root as the tonic of a modal
        # centre. The 'true' centre of the scale will be whatever the frozen scale
        # form is (hence why we deny the user to change it). We can give the user
        # a toggle button to decide whether the intervals shown in the diagram are
        # those of the parent scale or the individual chords.
        #       therefore, we can take the settings for the relative perspective
        #       that the user sees in the node display controls
ABSTRACT = """

Arpeggio widget
    1. when the arpeggio widget is activated, the scaleform & position are 'frozen' and should appear greyed out until the scale widget is reactivated.
    2. the arpeggio widget has a drop down menu for each chord in the scale (chord is defined by its own sub-panel)
    3. when the chord is selected, we grey out any non-chord tones so the arpeggio is 'highlighted'
    4. the arpeggio widget has a node display selector, but only the notes in the chord will be options

    In order to do this...

    1. create a new diagram, load the current scale, load the selected chord
    2. change the diagram's interval map to that of the mode corresponding to the selected scale degree
    3. for all chord tones, make a node control panel
    4. for all non-chord tones, make a light grey circle

    but you left out... how does the controller know to use the new diagram instead of self.diagram?
    --> pass the dummy diagram back as part of the report to the callback...
    ... therefore, must have a separate callback from the normal on_display_change

   """

"""Widgets that make up the tkinter GUI of the FingeringDiagram app."""

from tkinter import E, EW, NW, SUNKEN, W, Canvas, Tk, StringVar, IntVar
from tkinter.font import Font
from tkinter.ttk import Button, Frame, OptionMenu, LabelFrame, Label
from typing import Any, Callable, cast

from data import (keywords,
                  annotations,
                  intervallic_canon)
from gui import config
from src import (interface,
                 nomenclature,
                 rendering)
from src.models import diagrams
# from src.models.diagrams import GuitarFingeringDiagram, get_interval_map, standard_fretboard
CANVAS_SIZE: int = 500

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
        self.scale = StringVar(self, value=keywords.DIATONIC)
        self.mode = StringVar(self, value=keywords.IONIAN)
        self.key = StringVar(self, "C")
        self.callback = callback

        self.select_scale = OptionMenu(
            self, self.scale, self.scale.get(), *keywords.HEPTATONIC_ORDER, command=self.change_state)
        self.select_mode = OptionMenu(
            self, self.mode, self.mode.get(), *keywords.MODAL_NAME_SERIES, command=self.change_state)
        self.select_key = OptionMenu(
            self, self.key, self.key.get(), *nomenclature.chromatic(), command=self.change_state)

        self.select_scale.grid(column=0, row=0)
        self.select_scale.config(width=15)
        self.select_mode.grid(column=1, row=0)
        self.select_mode.config(width=15)
        self.select_key.grid(column=2, row=0)
        self.select_key.config(width=10)

    def change_state(self, *args: StringVar) -> None:
        """Alert the controller about any change in state."""
        self.callback(self.report())

    def report(self) -> dict[str, str]:
        """Return a report about the current state of the widget."""
        return {keywords.SCALE_NAME: self.scale.get(),
                keywords.MODAL_NAME: self.mode.get(),
                keywords.KEYNOTE: self.key.get()}


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
        self.fingering_options: list[str] = config.FINGERING_TYPES
        self.current_fingering: str = config.FINGERING_TYPES[0]

        self.string_toggle: Button = Button(self,
                                            text=self.current_fingering,
                                            command=self.change_state)
        self.string_toggle.grid()

    def report(self) -> annotations.FingeringReport:
        """Return a report about the current state of the widget."""
        return cast(annotations.FingeringReport, {
            keywords.STRING: self.string,
            keywords.FINGERING: self.current_fingering}
        )

    def change_state(self, *args: StringVar) -> None:
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
                 shape: str = keywords.CIRCLE,
                 size: int = 2,
                 colour: str = keywords.BLACK,
                 text_colour: str = keywords.WHITE,
                 text_size: int = 14) -> None:

        Frame.__init__(self, master)
        self.callback: Callable[..., Any] = callback

        self.interval = interval

        self.shape_options: list[str] = config.DIAGRAM_SHAPES
        self.size_options: list[int] = config.DIAGRAM_NODE_SIZES
        self.text_size_options: list[int] = config.DIAGRAM_TEXT_SIZES
        self.colour_options: list[str] = config.COLOURS

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
            [(keywords.SHAPE, self.select_shape),
             (keywords.SHAPE_SIZE, self.select_size),
             (keywords.SHAPE_COLOUR, self.select_colour),
             (keywords.TEXT_COLOUR, self.select_text_colour),
             (keywords.TEXT_SIZE, self.select_text_size)]):

            label_ = Label(self, text=str.replace(
                label, "_", " ").capitalize())
            label_.grid(column=0, row=i, sticky="w")
            widget.grid(column=1, row=i, sticky="e")
            widget.config(width=15)

    def change_state(self, *args: StringVar) -> None:
        """Respond to any change of state by sending a report about the 
        current state to the controller's callback."""
        self.callback(self.report())

    def report(self) -> annotations.NodeDisplayReport:
        """Return a report about the current state of the widget."""
        return annotations.NodeDisplayReport(interval=self.interval,
                                             shape=self.shape.get(),
                                             size=self.size.get(),
                                             shape_colour=self.colour.get(),
                                             text_colour=self.text_colour.get(),
                                             text_size=self.text_size.get())


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
        label.grid(column=0, row=0, sticky=W)
        self.select_interval.grid(column=1, row=0, sticky=E)
        self.current_subwidget.grid(column=0, row=2, columnspan=2)

        self.config(text="Interval Controls",
                    borderwidth=5,
                    labelanchor=NW,
                    relief=SUNKEN,)
        
    def set_subwidget(self, interval: str) -> None:
        """Set the currently visible subwidget to the given interval."""
        self.current_interval.set(interval)
        self.display_subwidget()

    def rename_intervals(self, intervals: list[str]) -> None:
        """Rename the series of intervals that label the subwidgets."""
        self.intervals = intervals
        for i, interval in enumerate(intervals):
            self.subwidgets[i].interval = interval
        self.select_interval.set_menu(self.intervals[0], *self.intervals)  # type:ignore

    def display_subwidget(self, *args: StringVar) -> None:
        """Change which subwidget is currently being displayed, based on the 
        selected option in the dropdown menu."""
        self.current_subwidget.grid_forget()
        for x in self.subwidgets:
            if x.interval == self.current_interval.get():
                self.current_subwidget = x
        self.current_subwidget.grid(column=0, row=1, columnspan=2)

    def summarize(self) -> list[annotations.NodeDisplayReport]:
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

    def summarize(self) -> list[annotations.FingeringReport]:
        """Return a summary of the current state of all subwidgets
        controlled by this widget."""
        return [x.report() for x in self.subwidgets]


class FingerboardGridWidget(LabelFrame):
    """A large widget that represents a grid, in the cells of which are shapes
    representing notes, fingers, or intervals.

    This widget only ever displays information, it doesn't pass anything back to
    the controller."""

    def __init__(self, master: Tk | Frame | LabelFrame, diagram: diagrams.GuitarFingeringDiagram) -> None:

        LabelFrame.__init__(self, master)
        self.config(text="Fretboard Diagram")
        self.canvas: Canvas = Canvas(self, height=CANVAS_SIZE, width=CANVAS_SIZE, bg="white")

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

                if node.shape == keywords.CIRCLE:
                    x0, y0 = centre[0] - 15, centre[1] - 15
                    x1, y1 = centre[0] + 15, centre[1] + 15
                    self.canvas.create_oval(x0, y0, x1, y1,
                                            fill=node.shape_colour,
                                            tags="node_shape"
                                            )

                elif node.shape == keywords.SQUARE:
                    x0, y0 = centre[0] - 15, centre[1] - 15
                    x1, y1 = centre[0] + 15, centre[1] + 15
                    self.canvas.create_rectangle(x0, y0, x1, y1,
                                                 fill=node.shape_colour,
                                                 tags="node_shape"
                                                 )

                elif node.shape == keywords.INVERSE_TRIANGLE:
                    x0, y0 = centre[0] - 20, centre[1] - 10
                    x1, y1 = centre[0] + 20, centre[1] - 10
                    x2, y2 = centre[0], centre[1] + 20
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2,
                                               fill=node.shape_colour,
                                               tags="node_shape"
                                               )

                elif node.shape == keywords.TRIANGLE:
                    x0, y0 = centre[0] + 20, centre[1] + 15
                    x1, y1 = centre[0] - 20, centre[1] + 15
                    x2, y2 = centre[0], centre[1] - 20
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2,
                                               fill=node.shape_colour,
                                               tags="node_shape"
                                               )

                elif node.shape == keywords.DIAMOND:
                    x0, y0 = centre[0], centre[1] - 15
                    x1, y1 = centre[0] - 15, centre[1]
                    x2, y2 = centre[0], centre[1] + 15
                    x3, y3 = centre[0] + 15, centre[1]
                    self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                                               fill=node.shape_colour,
                                               tags="node_shape")

                else:
                    raise ValueError(
                        f"Unknown node setting: shape={node.shape}")

                font = Font(self, 
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


class DisplaySelector(LabelFrame):
    """A small widget that controls the display type."""

    def __init__(self, master: Tk | Frame | LabelFrame, callback: Callable[..., Any]) -> None:
        LabelFrame.__init__(self, master)
        self.callback = callback
        self.config(text="Select Display Mode")
        self.display_type = StringVar(self)
        self.display_options = [keywords.INTERVAL,
                                keywords.FINGER, keywords.NOTE_NAME, keywords.FRET]
        self.select_display = OptionMenu(
            self,
            self.display_type,
            self.display_options[0],
            *self.display_options,
            command=self.change_state)

        self.select_display.grid()

    def change_state(self, *args: StringVar) -> None:
        """Report any change of state to the controller."""
        self.callback(self.display_type.get())


class PositionSelector(LabelFrame):
    """A small widget that controls the current position."""

    def __init__(self, master: Tk | Frame | LabelFrame, positions: list[int], callback: Callable[..., Any]) -> None:
        LabelFrame.__init__(self, master)
        self.callback = callback
        self.config(text="Select Position")
        self.position = IntVar(self, value=5)
        self.position_options = positions
        self.select_position = OptionMenu(self,
                                          self.position,
                                          str(self.position.get()),
                                          *[str(x)
                                            for x in positions if 0 < x < 13],
                                          command=self.change_state)
        self.select_position.grid()

    def change_state(self, *args: StringVar) -> None:
        """Report any change of state to the controller."""
        self.callback(self.report())

    def set_position(self, position: int, positions: list[int]) -> None:
        """Set the current position. (Used when the scale has changed in such
        a way that the previous position is no longer legal)."""
        self.position.set(position)
        self.position_options = positions
        self.select_position.set_menu(str(position), *positions)  # type:ignore

    def report(self) -> int:
        """Report on the current state of the widget."""
        return self.position.get()


class FretboardDiagram(Frame):
    """Main widget for the fretboard diagram."""

    def __init__(self, master: Frame | Tk):
        Frame.__init__(self, master)

        self.diagram = diagrams.GuitarFingeringDiagram(
            5, diagrams.standard_fretboard(), 5)

        self.diagram.define_scale(rendering.render_plain(
            intervallic_canon.DIATONIC_SCALE))
        self.diagram.define_intervals(nomenclature.get_interval_map("C"))
        self.diagram.turn_on_names(rendering.render_plain(
            intervallic_canon.DIATONIC_SCALE))

        # Top bar
        self.scale_selector = ScaleSelectorWidget(
            self,
            self.on_scale_change)
        self.scale_selector.grid(column=0, row=0, sticky=W)

        self.position_selector = PositionSelector(self,
                                                  self.diagram.positions(rendering.render_plain(
                                                      intervallic_canon.DIATONIC_SCALE)),
                                                  self.on_position_change)
        self.position_selector.grid(column=1, row=0, sticky=W)

        self.display_type_selector = DisplaySelector(self,
                                                     self.on_display_mode_change)
        self.display_type_selector.grid(column=2, row=0, sticky=W)

        # Left large window (main diagram display)
        self.fingerboard_grid = FingerboardGridWidget(self, self.diagram)
        self.fingerboard_grid.grid(column=0, row=1, columnspan=2)

        # Centre narrow window
        self.fingering_panel = StringFingeringSelector(self,
                                                       self.on_fingering_change,
                                                       self.diagram.number_of_strings)
        self.fingering_panel.grid(column=2, row=1, sticky=EW)

        # Frame 4: Main Option Panel (RIGHT, STATE-BASED)
        self.mode_toggle: Button  # change state
        self.current_main_panel: Frame

        # Frame 4a: Scale Mode Panel (RIGHT, STATE)
        intervals = [v for k, v in self.diagram.interval_map.items()
                     if k in self.diagram.active_names]
        self.node_selector: IntervalDisplaySelector = IntervalDisplaySelector(
            self, self.on_node_option_change, intervals)
        self.node_selector.grid(column=3, row=1, sticky=EW)

        self.grid()

        # Display initial values
        self.scale_selector.change_state()
        for report in self.fingering_panel.summarize():
            self.diagram.apply_fingering(**report)

    def on_fingering_change(self, report: annotations.FingeringReport) -> None:
        """Receive a report about the change in fingering and modify the 
        diagram to reflect it"""
        self.diagram.apply_fingering(**report)
        self.fingerboard_grid.draw_diagram(self.diagram)

    def on_node_option_change(self, report: annotations.NodeDisplayReport) -> None:
        """Receive a report about the change to an interval node's
        display options and modify the diagram to reflect it."""
        self.diagram.apply_display_options(report)
        self.fingerboard_grid.draw_diagram(self.diagram)

    def on_scale_change(self, report: annotations.ScaleformReport) -> None:
        """Receive a report about the change to the main scale paradigm
        and modify the diagram to reflect it."""

        # Whenever the scale, mode, or keynote changes, we have to change
        # the active nodes to reflect the new notes and intervals.
        current_names: list[str] = list(set(self.diagram.active_names))
        positions: list[int] = self.diagram.positions(current_names)
        i: int = positions.index(self.diagram.position)

        # Define relevant scale information from the API response.
        data: dict[str, Any] = interface.render_heptatonic_form(**report)
        modalform: int = data[keywords.INTERVAL_STRUCTURE]
        keynote: str = data[keywords.KEYNOTE]
        note_names: list[str] = data[keywords.CHROMATIC_RENDERING]
        map_name_to_interval: dict[str, str] = nomenclature.get_interval_map(
            keynote, modalform)
        proper_names: list[str] = data[keywords.OPTIMAL_RENDERING]

        # Set the diagram to the new scale.
        self.diagram.define_scale(note_names)
        self.diagram.define_intervals(map_name_to_interval)
        self.diagram.turn_on_names(note_names)

        # Set the new position to the value of the index of the old position, 
        # in case the value of the old position is no longer a legal position.
        positions = self.diagram.positions(note_names)
        self.on_position_change(positions[i])
        self.position_selector.set_position(self.diagram.position, positions)

        # Configure nodes to display correct scale nomenclature
        self.diagram.clear_overrides()
        self.diagram.override_names(dict(zip(note_names, proper_names)))

        # The node selector will keep the same settings for each of the 7
        # intervals, but the intervals' names will be updated for the new
        # scale configuration.
        self.node_selector.rename_intervals(
            [v for k, v in map_name_to_interval.items() if k in note_names])
        
        # Restore previous node display settings for new interval names.
        for report_ in self.node_selector.summarize():
            self.diagram.apply_display_options(report_)
        self.node_selector.set_subwidget("1")

        self.fingerboard_grid.draw_diagram(self.diagram)

    def on_display_mode_change(self, report: str) -> None:
        """Receive a report about the change to the display mode
        and modify the diagram to reflect it."""
        self.diagram.apply_rendering_mode(report)
        self.fingerboard_grid.draw_diagram(self.diagram)

    def on_position_change(self, report: int) -> None:
        """Receive a report about the change to the position
        and modify the diagram to reflect it."""
        self.diagram.change_position(report)
        for report_ in self.fingering_panel.summarize():
            self.diagram.apply_fingering(**report_)

        self.fingerboard_grid.draw_diagram(self.diagram)

        # note: position change is clearing the saved proper names of notes
        # because it creates a new grid. pick up here next time.



ndnd = """

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



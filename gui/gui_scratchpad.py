
from tkinter import *
from tkinter.ttk import *
from typing import Any, Callable

from data.keywords import (BLACK, BLUE, CIRCLE, COLOUR,
                           DIAMOND, GREEN, INDEX, INTERVAL,
                           INVERSE_TRIANGLE, ORANGE, PINKY,
                           PURPLE, RED, SHAPE, SIZE, SQUARE,
                           TEXT_COLOUR, TEXT_SIZE, TRIANGLE,
                           WHITE, YELLOW)


class StringFingeringWidget(Frame):
    """A small widget that controls how a string will be fingered.
    
    A button is displayed and will cycle through a series of states
    when it is clicked. It reports any change of state to a callback
    function.
    """

    def __init__(self,
                 master: Frame | Tk,
                 update_callback: Callable[..., Any],
                 string: int
                 ) -> None:
        
        Frame.__init__(self, master)
        self.update: Callable[..., Any] = update_callback

        self.string = string
        self.fingering_options: list[str] = [INDEX, PINKY]
        self.current_fingering: str = INDEX

        self.string_toggle: Button = Button(self,
                                            text=self.current_fingering,
                                            command=self.change_state)
        self.string_toggle.pack()
        

    def change_state(self, *args) -> None:
        """Toggle the string's fingering into the next state, and inform the
        callback function that the user has made a change."""
        state: int = self.fingering_options.index(self.current_fingering)
        if state == len(self.fingering_options) - 1:
            self.current_fingering = self.fingering_options[0]
        else:
            self.current_fingering = self.fingering_options[state + 1]

        self.string_toggle.configure(text=self.current_fingering)
        self.update((self.string, self.current_fingering))


DIAGRAM_SHAPES: list[str] = [CIRCLE, TRIANGLE, INVERSE_TRIANGLE, SQUARE, DIAMOND]
COLOURS: list[str] = [BLACK, RED, BLUE, GREEN, ORANGE, YELLOW, PURPLE, WHITE]
DIAGRAM_NODE_SIZES: list[int] = [1, 2, 3, 4, 5]
DIAGRAM_TEXT_SIZES: list[int] = [10, 12, 14, 16, 18, 20]



class IntervalDisplayWidget(Frame):
    """A small widget that controls how an interval will be displayed in the 
    fingering diagram.
    
    The widget shows options for the shape, size, colour, text colour, and 
    text size for the individual interval nodes in the fretboard diagram.
    The user is able to select from pre-defined options in each category
    and any change of state is reported to a callback function."""


    def __init__(self, 
                 master: Frame | Tk,
                 update_callback: Callable[..., Any],
                 interval: str,
                 shape: str = CIRCLE,
                 size: int = 2,
                 colour: str = BLACK,
                 text_colour: str = WHITE,
                 text_size: int = 14) -> None:
        
        Frame.__init__(self, master)
        self.update: Callable[..., Any] = update_callback

        self.interval = interval
        
        self.shape_options: list[str] = DIAGRAM_SHAPES
        self.size_options: list[int] = DIAGRAM_NODE_SIZES
        self.text_size_options: list[int] = DIAGRAM_TEXT_SIZES
        self.colour_options: list[str] = COLOURS

        self.shape = StringVar(self, value=shape)
        self.size = IntVar(self, value=size)
        self.colour = StringVar(self, value=colour)
        self.text_colour = StringVar(self, value=text_colour)
        self.text_size =  IntVar(self, value=text_size)

        self.select_shape = OptionMenu(self, 
                                       self.shape, 
                                       self.shape.get(), 
                                       *self.shape_options, 
                                       command=self.change_state)
        self.select_size = OptionMenu(self, 
                                      self.size, 
                                      str(self.size.get()), 
                                      *[str(x) for x in self.size_options], 
                                      command=self.change_state)
        self.select_colour = OptionMenu(self, 
                                        self.colour, 
                                        self.colour.get(), 
                                        *self.colour_options, 
                                        command=self.change_state)
        self.select_text_colour = OptionMenu(self, 
                                             self.text_colour, 
                                             self.text_colour.get(), 
                                             *self.colour_options, 
                                             command=self.change_state)
        self.select_text_size = OptionMenu(self, 
                                           self.text_size, 
                                           str(self.text_size.get()), 
                                           *[str(x) for x in self.text_size_options], 
                                           command=self.change_state)


        for i, (label, widget) in enumerate([(SHAPE, self.select_shape),
                                           (SIZE, self.select_size),
                                           (COLOUR, self.select_colour),
                                           (TEXT_COLOUR, self.select_text_colour),
                                           (TEXT_SIZE, self.select_text_size)]):
            
            label_ = Label(self, text=label)
            label_.grid(column=0, row=i)
            widget.grid(column=1, row=i)



    def change_state(self, *args) -> None:
        """Respond to any change of state by sending a report about the 
        current state to the controller's callback."""
        self.update(self.__report())


    def __report(self) -> dict[str, str | int]:
        return {INTERVAL: self.interval,
                SHAPE: self.shape.get(), 
                SIZE: self.size.get(), 
                COLOUR: self.colour.get(), 
                TEXT_COLOUR: self.text_colour.get(),
                TEXT_SIZE: self.text_size.get()}


class IntervalControlSelector(Frame):
    """A widget that allows the user to select which interval display control
    panel is currently displayed.
    
    The widget shows a dropdown menu which, when an interval is selected, 
    causes an interval node control panel for that interval to appear below.
    It passes a callback function to all the control panels generated by
    the list of intervals provided."""

    def __init__(self, 
                 master: Frame | Tk, 
                 callback: Callable[..., Any], 
                 intervals: list[str]
                 ) -> None:
        

        Frame.__init__(self, master)
        self.callback =  callback
        self.intervals = intervals

        self.current_interval = StringVar(self, value=self.intervals[0])
        self.select_interval = OptionMenu(self, self.current_interval,
                                          self.current_interval.get(),
                                          *self.intervals,
                                          command=self.display_subwidget)

        self.subwidgets: list[IntervalDisplayWidget] = []
        for x in self.intervals:
            self.subwidgets.append(IntervalDisplayWidget(self, callback, x))

        self.current_subwidget: IntervalDisplayWidget = self.subwidgets[0]
        self.select_interval.grid(column=0, row=0)
        self.current_subwidget.grid(column=0, row=1)


    def display_subwidget(self, *args) -> None:
        """Change which subwidget is currently being displayed, based on the 
        selected option in the dropdown menu."""
        self.current_subwidget.grid_forget()
        for x in self.subwidgets:
            if x.interval == self.current_interval.get():
                self.current_subwidget = x
        self.current_subwidget.grid(column=0, row=1)



class TestMainWidget(Frame):
    """Test class to represent the widget in which the sub-widgets get created."""

    def __init__(self, 
                 number_of_subwidgets: int
                 ) -> None:
        Frame.__init__(self, Tk())
        self.number_of_subwidgets: int = number_of_subwidgets
        for x in range(self.number_of_subwidgets):
            w = StringFingeringWidget(self, self.update_fingering, x)
            w.pack()

        g = IntervalControlSelector(self, 
                                    self.update_node_options, 
                                    ["3", "5", "7", "9", "11"])
        g.pack()

        self.grid()


    def update_fingering(self, report: tuple[int, str]) -> None:
        """The main widget receives information from the subwidgets through 
        this callback, and can then use that information to update the diagram
        display widget."""
        print(f"The fingering of string {report[0]} was changed to {report[1]}")



    def update_node_options(self, report: dict[str, int | str]) -> None:
        """The main widget receives information from the subwidgets through 
        this callback, and can then use that information to update the diagram
        display widget."""
        print(f"The interval control panel was changed: {[str(k)+': '+str(v) for k, v in report.items()]}")
        

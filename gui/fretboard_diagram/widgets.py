"""Widgets that make up the GUI"""


from tkinter import *
from tkinter.ttk import *
from typing import Any, Callable

from gui.config import (DIAGRAM_NODE_SIZES,
                        DIAGRAM_SHAPES,
                        DIAGRAM_TEXT_SIZES,
                        COLOURS,
                        FINGERING_TYPES)

from data.keywords import (CURRENT_FINGERING, DIATONIC, IONIAN, SHAPE,
                           COLOUR,
                           SIZE, STRING,
                           TEXT_SIZE,
                           TEXT_COLOUR,
                           INTERVAL,
                           BLACK,
                           WHITE,
                           CIRCLE)


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
        
        self.scale = StringVar(self, value=DIATONIC)
        self.mode = StringVar(self, value=IONIAN)
        self.key = StringVar(self, "C")




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
        

    def change_state(self, *args) -> None:
        """Toggle the string's fingering into the next state, and inform the
        callback function that the user has made a change."""
        state: int = self.fingering_options.index(self.current_fingering)
        if state == len(self.fingering_options) - 1:
            self.current_fingering = self.fingering_options[0]
        else:
            self.current_fingering = self.fingering_options[state + 1]
        self.string_toggle.configure(text=self.current_fingering)
        self.callback({STRING: self.string, 
                       CURRENT_FINGERING: self.current_fingering})



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
        self.text_size =  IntVar(self, value=text_size)

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
            
            label_ = Label(self, text=str.replace(label, "_", " ").capitalize())
            label_.grid(column=0, row=i, sticky="w")
            widget.grid(column=1, row=i, sticky="e")
            widget.config(width=15)


    def change_state(self, *args) -> None:
        """Respond to any change of state by sending a report about the 
        current state to the controller's callback."""
        self.callback(self.__report())


    def __report(self) -> dict[str, str | int]:
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
        self.callback =  callback
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


    def display_subwidget(self, *args) -> None:
        """Change which subwidget is currently being displayed, based on the 
        selected option in the dropdown menu."""
        self.current_subwidget.grid_forget()
        for x in self.subwidgets:
            if x.interval == self.current_interval.get():
                self.current_subwidget = x
        self.current_subwidget.grid(column=0, row=1, columnspan=2)



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
    
        for x in range(number_of_strings):
            w = StringFingeringWidget(self, callback, x)
            l = Label(self, text=f"String {x}: ")
            l.grid(column=0, row=x, sticky="w")
            w.grid(column=1, row=x, sticky="e")



# class TestMainWidget(Frame):
#     """Test class to represent the widget in which the sub-widgets get created."""

#     def __init__(self,
#                  number_of_subwidgets: int
#                  ) -> None:

#         Frame.__init__(self, Tk())
#         self.number_of_subwidgets: int = number_of_subwidgets

#         f = StringFingeringSelector(self, self.update_fingering, 6)

#         f.pack(fill="both", anchor="center", ipadx=5, ipady=5, padx=5, pady=5)

#         g = IntervalDisplaySelector(self,
#                                     self.update_node_options,
#                                     ["3", "#5", "7", "#9", "#11"])
        
#         g.pack(fill="both", 
#                anchor="center", 
#                ipadx=5, 
#                ipady=5, 
#                padx=5, 
#                pady=5)
#         self.grid()


#     def update_fingering(self, report: tuple[int, str]) -> None:
#         """The main widget receives information from the subwidgets through 
#         this callback, and can then use that information to update the diagram
#         display widget."""
#         print(f"The fingering of string {report[0]} was changed to {report[1]}")


#     def update_node_options(self, report: dict[str, int | str]) -> None:
#         """The main widget receives information from the subwidgets through 
#         this callback, and can then use that information to update the diagram
#         display widget."""
#         print(f"The interval control panel was changed: {[str(k)+': '+str(v) for k, v in report.items()]}")
        

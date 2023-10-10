from tkinter import *
from tkinter import ttk

from src import interface
from data import keywords, constants


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, height=200, width=400)
        self.grid()
        self.create_widgets()
        self.vars = []
        self.master.title('Aristoxenus')
        

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)

        # Frame 1
        frame1 = ttk.Frame(self.notebook, height=100, width=300)
        frame1.grid()

        # Frame 1: choose scale, mode, and key, and display notes with best heptatonic name

        # Scales Dropdown Menu
        scales = keywords.HEPTATONIC_ORDER
        self.scale_selection = StringVar(self)
        self.scale_selection.set(scales[0])
        scales_ = ttk.OptionMenu(frame1, self.scale_selection, *scales, command=self.on_dropdown)
        scales_.grid(column=0, row=0)

        # Modes Dropdown Menu
        modes = keywords.MODAL_NAME_SERIES
        self.mode_selection = StringVar(self)
        self.mode_selection.set(modes[0])
        modes_ = ttk.OptionMenu(frame1, self.mode_selection, *modes, command=self.on_dropdown)
        modes_.grid(column=1, row=0)

        keynotes = constants.NATURALS + constants.ACCIDENTAL_NOTES
        self.key_selection = StringVar(self)
        self.key_selection.set(keynotes[0])
        keynotes_ = ttk.OptionMenu(frame1, self.key_selection, *keynotes, command=self.on_dropdown)
        keynotes_.grid(column=2, row=0)
        scale_notes = ' '.join(interface.render_heptatonic_form(self.scale_selection.get(), self.mode_selection.get(), self.key_selection.get())[keywords.OPTIMAL_RENDERING])
       
        
        self.textbox = ttk.Label(frame1, text=scale_notes)
        self.textbox.grid(column=0, row=2)

        self.notebook.add(frame1, text = "Window 1")
 

        # Frame 2
        frame2 = ttk.Frame(self.notebook, height=100, width=300)
        label2 = ttk.Label(frame2, text = "This is Window Two")
        label2.grid(column=1, row=1)
        frame2.grid()


        

        self.notebook.add(frame2, text = "Window 2")
 
        self.notebook.grid()


    def on_dropdown(self, *args):
        scale_notes = ' '.join(interface.render_heptatonic_form(self.scale_selection.get(), self.mode_selection.get(), self.key_selection.get())[keywords.OPTIMAL_RENDERING])
        self.textbox.config(text=scale_notes)


from tkinter import *
from tkinter import ttk

from src import interface
from data import keywords, constants


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, height=200, width=400)
        self.scale_selection = StringVar(self)
        self.mode_selection = StringVar(self)
        self.key_selection = StringVar(self)
        self.grid()
        self.create_widgets()
        self.vars = []
        self.master.title('Aristoxenus')
                

    def create_widgets(self):

        # Widget 1: Notebook
        self.notebook = ttk.Notebook(self)
        self.create_frame1()
        self.create_frame2()
        self.notebook.grid()


    def create_frame1(self):
        # Frame 1
        frame1 = ttk.Frame(self.notebook, height=100, width=300)
        frame1.grid()

        # FRAME 1: Generate heptatonic scales
        # ====================================================================
        #
        # FRAME 1 USER INPUT
        # --------------------------------------------------------------------
        #
        # Scales Dropdown Menu
        scales = keywords.HEPTATONIC_ORDER
        self.scale_selection.set(scales[0])
        scales_ = ttk.OptionMenu(frame1, self.scale_selection, scales[0], *scales, command=self.on_dropdown)
        scales_.grid(column=0, row=0)
        #
        # Modes Dropdown Menu
        modes = keywords.MODAL_NAME_SERIES
        self.mode_selection.set(modes[0])
        modes_ = ttk.OptionMenu(frame1, self.mode_selection, modes[0],  *modes, command=self.on_dropdown)
        modes_.grid(column=1, row=0)
        #
        # Keynote dropdown menu
        keynotes = constants.NATURALS + constants.ACCIDENTAL_NOTES
        self.key_selection.set(keynotes[0])
        keynotes_ = ttk.OptionMenu(frame1, self.key_selection, keynotes[0], *keynotes, command=self.on_dropdown)
        keynotes_.grid(column=2, row=0)
        #
        # FRAME 1 DISPLAY OUTPUT
        # --------------------------------------------------------------------
        #
        # Interface response
        scale_data = interface.render_heptatonic_form(self.scale_selection.get(), self.mode_selection.get(), self.key_selection.get())
        #
        # Basic Rendering
        ttk.Label(frame1, text='Chromatic rendering: ').grid(column=0, row=1)
        scale_notes = ' '.join(scale_data[keywords.CHROMATIC_RENDERING])
        self.scale_label = ttk.Label(frame1, text=scale_notes)
        self.scale_label.grid(column=1, row=1)
        #
        # Alphabetic Rendering
        ttk.Label(frame1, text='Alphabetic rendering: ').grid(column=0, row=2)
        alpha_notes = ' '.join(scale_data[keywords.ALPHABETIC_RENDERING])
        self.alpha_label = ttk.Label(frame1, text=alpha_notes)
        self.alpha_label.grid(column=1, row=2)
        #
        # Best Rendering
        ttk.Label(frame1, text='Optimal spelling: ').grid(column=0, row=3)
        best_notes = ' '.join(scale_data[keywords.OPTIMAL_RENDERING])
        self.best_label = ttk.Label(frame1, text=best_notes)
        self.best_label.grid(column=1, row=3)
        #
        # Best Keynote
        ttk.Label(frame1, text='Optimal keynote: ').grid(column=0, row=4)
        best_key = str(scale_data[keywords.OPTIMAL_KEYNOTE])
        self.best_key_label = ttk.Label(frame1, text=best_key)
        self.best_key_label.grid(column=1, row=4)
        #
        # Interval map
        ttk.Label(frame1, text='Interval map: ').grid(column=0, row=5)
        interval_map = ' '.join(scale_data[keywords.INTERVAL_SCALE])
        self.interval_map_label = ttk.Label(frame1, text=interval_map)
        self.interval_map_label.grid(column=1, row=5)

        self.notebook.add(frame1, text = "Heptatonic Scale Forms")


    def create_frame2(self):
 
        # Frame 2
        frame2 = ttk.Frame(self.notebook, height=100, width=300)
        label2 = ttk.Label(frame2, text = "This is Window Two")
        label2.grid(column=1, row=1)
        frame2.grid()

        self.notebook.add(frame2, text = "Window 2")
 
       


    def on_dropdown(self, *args):
        '''
        Update the display whenever a dropdown menu changes its selection.
        '''
        scale_data = interface.render_heptatonic_form(self.scale_selection.get(), self.mode_selection.get(), self.key_selection.get())

        scale_notes = ' '.join(scale_data[keywords.CHROMATIC_RENDERING])
        self.scale_label.config(text=scale_notes)
        alpha_notes = ' '.join(scale_data[keywords.ALPHABETIC_RENDERING])
        self.alpha_label.config(text=alpha_notes)
        best_notes = ' '.join(scale_data[keywords.OPTIMAL_RENDERING])
        self.best_label.config(text=best_notes)
        best_key = str(scale_data[keywords.OPTIMAL_KEYNOTE])
        self.best_key_label.config(text=best_key)
        interval_map = ' '.join(scale_data[keywords.INTERVAL_SCALE])
        self.interval_map_label.config(text=interval_map)



from tkinter import *
from tkinter import ttk

from data import (keywords,
                  constants)

from src import (interface)


class ScaleInfoPanel(ttk.Frame):
    

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.scale_selection = StringVar(self)
        self.mode_selection = StringVar(self)
        self.key_selection = StringVar(self)
        self.setup_dropdown_bar()
        self.setup_info_display()
        self.grid()

    def setup_dropdown_bar(self):

        menubar = ttk.Frame(self.master)

        # Scales Dropdown Menu
        scales = keywords.HEPTATONIC_ORDER
        self.scale_selection.set(scales[0])
        scales_ = ttk.OptionMenu(menubar, self.scale_selection, scales[0], *scales, command=self.on_selection)
        scales_.grid(column=0, row=0)
        scales_.config(width=15)
        #
        # Modes Dropdown Menu
        modes = keywords.MODAL_NAME_SERIES
        self.mode_selection.set(modes[0])
        modes_ = ttk.OptionMenu(menubar, self.mode_selection, modes[0],  *modes, command=self.on_selection)
        modes_.grid(column=1, row=0)
        modes_.config(width=20)
        #
        # Keynote dropdown menu
        keynotes = constants.NATURALS + constants.ACCIDENTAL_NOTES
        self.key_selection.set(keynotes[0])
        keynotes_ = ttk.OptionMenu(menubar, self.key_selection, keynotes[0], *keynotes, command=self.on_selection)
        keynotes_.grid(column=2, row=0)
        keynotes_.config(width=5)
        #
        # Separator
        separator = ttk.Separator(menubar, orient='horizontal')
        separator.grid(column=0, row=1, columnspan=3, sticky=NSEW)

        menubar.grid(column=0, row=0)


    def setup_info_display(self):
        infopanel = ttk.Frame()

        scale_data = self.scale_data
        #
        # Basic Rendering
        ttk.Label(infopanel, text='Chromatic rendering: ').grid(column=0, row=0, sticky=W)
        scale_notes = ' '.join(scale_data[keywords.CHROMATIC_RENDERING])
        self.scale_label = ttk.Label(infopanel, text=scale_notes)
        self.scale_label.grid(column=1, row=0, columnspan=2, sticky=W)
        #
        # Alphabetic Rendering
        ttk.Label(infopanel, text='Alphabetic rendering: ').grid(column=0, row=1, sticky=W)
        alpha_notes = ' '.join(scale_data[keywords.ALPHABETIC_RENDERING])
        self.alpha_label = ttk.Label(infopanel, text=alpha_notes)
        self.alpha_label.grid(column=1, row=1, columnspan=2, sticky=W)
        #
        # Best Rendering
        ttk.Label(infopanel, text='Optimal spelling: ').grid(column=0, row=2, sticky=W)
        best_notes = ' '.join(scale_data[keywords.OPTIMAL_RENDERING])
        self.best_label = ttk.Label(infopanel, text=best_notes)
        self.best_label.grid(column=1, row=2, columnspan=2, sticky=W)
        #
        # Best Keynote
        ttk.Label(infopanel, text='Optimal keynote: ').grid(column=0, row=3, sticky=W)
        best_key = str(scale_data[keywords.OPTIMAL_KEYNOTE])
        self.best_key_label = ttk.Label(infopanel, text=best_key)
        self.best_key_label.grid(column=1, row=3, columnspan=2, sticky=W)
        #
        # Interval map
        ttk.Label(infopanel, text='Interval map: ').grid(column=0, row=4, sticky=W)
        interval_map = ' '.join(scale_data[keywords.INTERVAL_SCALE])
        self.interval_map_label = ttk.Label(infopanel, text=interval_map)
        self.interval_map_label.grid(column=1, row=4, columnspan=2, sticky=W)
        #
        # Interval map
        ttk.Label(infopanel, text='Interval structure: ').grid(column=0, row=5, sticky=W)
        interval_structure = str(scale_data[keywords.INTERVAL_STRUCTURE])
        self.interval_structure_label = ttk.Label(infopanel, text=interval_structure)
        self.interval_structure_label.grid(column=1, row=5, columnspan=2, sticky=W)

        infopanel.grid(column=0, row=1)

        
    @property
    def scale_data(self):
        '''
        The dictionary of scale data returned by the endpoint for the current
        combination.
        '''
        s = self.scale_selection.get()
        m = self.mode_selection.get()
        k = self.key_selection.get()
        return interface.render_heptatonic_form(s, m, k)


    def on_selection(self, *args):
        '''
        Update the display whenever a dropdown menu changes its selection.
        '''
        scale_data = self.scale_data

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
        interval_structure = str(scale_data[keywords.INTERVAL_STRUCTURE])
        self.interval_structure_label.config(text=interval_structure)

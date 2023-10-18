from tkinter import Tk
from gui import scale_info_panel

master = Tk()
app = scale_info_panel.ScaleInfoPanel(master)
app.mainloop()
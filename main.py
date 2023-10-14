from tkinter import Tk
from gui import scale_info_panel

from src import nomenclature


# app = classes.Application()
# app.mainloop()


# from src import interface
# data = interface.render_heptatonic_form('altered', 'dorian', 'D#')

# for datum in data: 
#     print ( datum, ':', data[datum] )

# master = Tk()
# app = scale_info_panel.ScaleInfoPanel(master)
# app.mainloop()


x = nomenclature.encode_scientific_enharmonic('A4', 'G', 'below')
print(x)

print(nomenclature.decode_scientific_enharmonic(x))
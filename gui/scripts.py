from tkinter import *
from tkinter import ttk

window = Tk()
window.minsize(800, 500)
window.maxsize(800, 500)


ttk.Label(window, text='Main window', font=('Verdana', 10)).grid(column=0, row=0, padx=10, pady=10, ipadx=5, ipady=5)









window.mainloop()
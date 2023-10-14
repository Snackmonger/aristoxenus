
from tkinter import *
from tkinter import ttk


# Tkinter ttk style formatting


style = ttk.Style()

style.configure('BnW-Label',
                foreground='black',
                background='white')

label1 = ttk.Label(text='Test Label', style='BnW-Label')


root = Tk()

frame = ttk.Frame(root)
frame.pack()


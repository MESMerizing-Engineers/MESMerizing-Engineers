# TkTorq

import tkinter as tk
from tkinter import ttk
from TqTorq_PlotFrame import PlotFrame
from TqTorq_NavToolBarFrame import NavToolBarFrame
from TqTorq_AdjustFrame import AdjustFrame

class TkTorq(tk.Tk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class TkTorqNB(ttk.Notebook):
    def __init__(self, container):
        super().__init__(container)     
        self.grid(row=0, column=0, sticky='NSEW')  # This inserts notebook into tkinter window
        self.columnconfigure(0, weight=1)  # allows for vertical expansion
        self.rowconfigure(0, weight=1)  # allows for horizontal expansion
        self.TkTorqDict = {}  # empty dictionary to be used later


root = TkTorq()
NB = TkTorqNB(root)


plot_frame = PlotFrame(NB)
plot_frame.grid(row=0,
               column=0,
               sticky='NSEW'
               )

nav_frame = NavToolBarFrame(plot_frame)
nav_frame.grid(row=1,
               column=0,
               sticky='NSEW'
               )
adjust_frame = AdjustFrame(NB, plot_frame)
adjust_frame.grid(row=0,
               column=0,
               sticky='NSEW'
               )

NB.add(adjust_frame, text='Tab 1')
NB.add(plot_frame, text='Plot')
root.mainloop()


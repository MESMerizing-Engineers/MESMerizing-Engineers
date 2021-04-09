# TkTorq

import tkinter as tk
from tkinter import ttk
from TqTorq_PlotFrame_test import PlotFrame
from TqTorq_NavToolBarFrame_test import NavToolBarFrame
from Home_test import HomeFrame


from PIL import ImageTk,Image  # Decide if I need this everywhere



class TkTorq(tk.Tk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


class TkTorqNB(ttk.Notebook):
    def __init__(self, container):
        super().__init__(container)             
        self.grid(row=1, column=0, sticky='NSEW')  # This inserts notebook into tkinter window
        self.columnconfigure(0, weight=1)  # allows for vertical expansion
        self.rowconfigure(1, weight=1)  # allows for horizontal expansion
        self.TkTorqDict = {}  # empty dictionary to be used later


root = TkTorq()
root.title("MESMerizing Engineers") # Change the title of the window.


header = tk.Label(root,text='HAWKeye GUI',bg='royalblue',font=('courier',20,'bold'))
header.grid(row=0, column=0, sticky = 'EW')

NB = TkTorqNB(root)


plot_frame = PlotFrame(NB)
plot_frame.grid(row=1,
               column=0,
               sticky='NSEW'
               )

nav_frame = NavToolBarFrame(plot_frame)
nav_frame.grid(row=2,
               column=0,
               sticky='NSEW'
               )

#%%
home_frame = HomeFrame(NB, plot_frame)
home_frame.grid(row=1,
               column=0,
               sticky='NSEW'
               )
home_nav_frame = NavToolBarFrame(home_frame)
home_nav_frame.grid(row=2,
               column=0,
               sticky='NSEW'
               )
#%%



Settings_frame = PlotFrame(NB)
Settings_frame.grid(row=1,
               column=0,
               sticky='NSEW'
               )

Help_frame = PlotFrame(NB)
Help_frame.grid(row=1,
               column=0,
               sticky='NSEW'
               )

NB.add(home_frame, text='Home')
NB.add(plot_frame, text='Autonomous')
NB.add(Settings_frame, text='Settings')
NB.add(Help_frame, text='Help')
root.mainloop()


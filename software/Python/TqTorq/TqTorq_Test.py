# This is a test file

import tkinter as tk
import numpy as np
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()


PlotFrame = tk.Frame(master=root)
PlotFrame.grid(row=0, column=0, sticky='NSEW')
PlotFrame.columnconfigure(0, weight=1)
PlotFrame.rowconfigure(0, weight=1)

fig, ax = plt.subplots()
ax.plot(np.arange(100), np.sin(np.arange(100)))

canvas = FigureCanvasTkAgg(fig, master=PlotFrame)
canvas.draw()
canvas.get_tk_widget().grid(row=0,
                            column=0,
                            sticky='NSEW'
                            )

root.mainloop()
import tkinter as tk
import numpy as np
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.fig, self.ax = plt.subplots()
        #self.fig = plt.Figure()
        #self.ax = self.fig.add_subplot(111)
        #self.ax.plot(np.linspace(0,2*np.pi,1000),np.sin(np.linspace(0,2*np.pi,1000)))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,
                                         column=0,
                                         sticky='NSEW'
                                         )
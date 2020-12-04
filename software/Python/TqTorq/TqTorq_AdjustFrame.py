import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class AdjustFrame(ttk.Frame):
    def __init__(self, container, plot_frame):
        self.x = np.linspace(0, 2*np.pi, int(1E2))
        self.y = np.sin(self.x)
        self.x_new = self.x
        self.y_new = []
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        B1 = tk.Button(self,
                       text='Test Button',
                       command=lambda: B_Test(plot_frame))
        B1.grid(row=0,
                column=0,
                sticky='NSEW'
                )

        B2 = tk.Button(self,
                       text='Test Button',
                       command=lambda: Scale(plot_frame))
        B2.grid(row=0,
                column=1,
                sticky='NSEW'
                )
        def B_Test(plot_frame):
            plot_frame.ax = plt.plot(self.x, self.y)
            plot_frame.canvas.draw()
            plot_frame.canvas.get_tk_widget().grid(row=0, column=0)
        def Scale(plot_frame):

            if len(self.y_new) == 0:
                self.y_new = self.y
            else:
                self.y_new = self.y_new+1
            plot_frame.fig.clear()
            plot_frame.ax = plt.plot(self.x, self.y_new)
            plot_frame.canvas.draw()
            plot_frame.canvas.get_tk_widget().grid(row=0, column=0)

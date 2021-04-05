import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

class NavToolBarFrame(ttk.Frame):
    def __init__ (self,container):
        super().__init__(container)
        self.canvas = container.canvas
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas,self)
        self.toolbar.update()

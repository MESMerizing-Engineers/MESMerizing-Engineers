import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg


from PIL import ImageTk,Image  # Decide if I need this everywhere

class HomeFrame(ttk.Frame):
    def __init__(self, container, plot_frame):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        
#%% Primary Screen 

              
        self.fig = plt.Figure(figsize=[16,9])
        self.ax = self.fig.add_subplot(111)
        #self.img = mpimg.imread("CREO_proto.png")
        self.img = Image.open("map.png")   #.convert('LA') for grey scale
        #self.img.thumbnail((64, 64), Image.ANTIALIAS)  # resizes image in-place
        self.ax.imshow(self.img)
        self.ax.set_title('Primary Screen',weight='bold',fontsize=20,color='royalblue')
        self.ax.grid(color='royalblue',linestyle='-.')
        #self.ax.plot(np.linspace(0,2*np.pi,1000),np.sin(np.linspace(0,2*np.pi,1000)))
        
        self.fig.patch.set_facecolor('lightgrey')
        self.canvas = FigureCanvasTkAgg(self.fig, 
                                         master=self,
                                         )
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,
                                         rowspan=2,
                                         column=0,
                                         sticky='NSEW'
                                         )

#%% Secondary Screen
        
        self.fig2 = plt.Figure(figsize=[10,10])
        self.ax2 = self.fig2.add_subplot(111)
        self.img2 = Image.open("CREO_proto.png")   #.convert('LA') for grey scale
        self.ax2.imshow(self.img2)
        self.fig2.patch.set_facecolor('lightgrey')
        self.ax2.set_title('Secondary Screen',weight='bold',fontsize=20,color='royalblue')
        self.secondary = FigureCanvasTkAgg(self.fig2, 
                                         master=self,
                                         )
        self.secondary.draw()
        self.secondary.get_tk_widget().grid(row=0,
                                         columnspan=2,
                                         column=1,
                                         sticky='NSEW'
                                         )
        
#%% Media Controls
        

        
        Media_Frame = tk.Frame(self)
        Media_Frame.grid(row=1,
                         column=1,
                         sticky = "NSEW"
                         )
        Media_Frame.rowconfigure(0, weight=1)
        Media_Frame.columnconfigure(0, weight=1)
        
        Media_Label = tk.Label(Media_Frame,
                             text = 'Media Controls',
                             bg = 'royalblue',
                             font = ('courier',12,'bold')
                             )        
        Media_Label.grid(row=0,
                       column=0,
                       sticky='EW'
                       )



#### MEDIA Buttons
        primary_select = tk.Button(Media_Frame,
                       text='Select Primary Screen',
                       #command=lambda: B_Test(plot_frame)
                       )
        primary_select.grid(row = 1,
                column=0,
                sticky='EW'
                )
        
        
        secondary_select = tk.Button(Media_Frame,
                       text='Select Secondary Screen',
                       #command=lambda: B_Test(plot_frame)
                       )
        secondary_select.grid(row = 2,
                column=0,
                sticky='EW'
                )
        
        
        record_video = tk.Button(Media_Frame,
                       text='Record Video',
                       #command=lambda: B_Test(plot_frame)
                       )
        record_video.grid(row = 3,
                column=0,
                sticky='EW'
                )
        
        
        take_picture = tk.Button(Media_Frame,
                       text='Take Picture',
                       #command=lambda: B_Test(plot_frame)
                       )
        take_picture.grid(row = 4,
                column=0,
                sticky='EW'
                )  
        

        Save_Video = tk.Button(Media_Frame,
                       text='Save Video',
                       #command=lambda: B_Test(plot_frame)
                       )
        Save_Video.grid(row = 5,
                column=0,
                sticky='EW'
                )  
        

        Classify_Image = tk.Button(Media_Frame,
                       text='Classify Image',
                       #command=lambda: B_Test(plot_frame)
                       )
        Classify_Image.grid(row = 6,
                column=0,
                sticky='EW'
                )  
#%% Navigation Controls   
        
        NAV_Frame = tk.Frame(self)
        NAV_Frame.grid(row=1,
                         column=2,
                         sticky='NSEW'
                         )
        NAV_Frame.rowconfigure(5, weight=1)
        NAV_Frame.columnconfigure(0, weight=1)
        
        Nav_Label = tk.Label(NAV_Frame,
                             text = 'Navigation Controls',
                             bg = 'royalblue',
                             font = ('courier',12,'bold')
                             )        
        Nav_Label.grid(row = 0,
                       column = 0,
                       sticky='EW'
                       )
        

#### Navigation Buttons

        go_to_location = tk.Button(NAV_Frame,
                       text='Go To Location',
                       #command=lambda: Scale(plot_frame)
                       )
        go_to_location.grid(row = 1,
                column= 0,
                sticky='NSEW'
                )
        
        
        record_location = tk.Button(NAV_Frame,
                       text='Record Location',
                       #command=lambda: Scale(plot_frame)
                       )
        record_location.grid(row = 2,
                column= 0,
                sticky='NSEW'
                )


        remote_control = tk.Button(NAV_Frame,
                       text='Remote Control',
                       #command=lambda: Scale(plot_frame)
                       )
        remote_control.grid(row = 3,
                column= 0,
                sticky='NSEW'
                )


        return_to_base = tk.Button(NAV_Frame,
                       text='Return To Base',
                       #command=lambda: Scale(plot_frame)
                       )
        return_to_base.grid(row = 4,
                column= 0,
                sticky='NSEW'
                )


        E_stop = tk.Button(NAV_Frame,
                       text='Emergency Stop',
                       fg='red'
                       #command=lambda: Scale(plot_frame)
                       )
        E_stop.grid(row = 5,
                column= 0,
                #columnspan=1,
                sticky='NSEW'
                )
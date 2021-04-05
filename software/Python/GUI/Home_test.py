import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from PIL import ImageTk,Image  # Decide if I need this everywhere

class HomeFrame(ttk.Frame):
    def __init__(self, container, plot_frame):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
#%% Primary Screen 

      
        #self.fig, self.ax = plt.subplots()
        #self.primary = FigureCanvasTkAgg(self.fig, 
        #                                 master=self,
        #                                 width=300,
        #                                 height=300,
        #                                 )
        
        self.primary = tk.Canvas(self)
        self.img = ImageTk.PhotoImage(Image.open("CREO_proto.png"))    
        self.primary.create_image(0,0,anchor='nw', image=self.img)    
        self.primary.grid(row=0,
                          rowspan=2,
                          column=0,
                          sticky='NSEW'
                          )

#%% Secondary Screen

        self.secondary = tk.Canvas(self)  
        self.img2 = ImageTk.PhotoImage(Image.open("map.png"))    

         
        self.secondary.create_image(4,4,anchor='nw', image=self.img2)    

        self.secondary.grid(row=1,
                          columnspan=2,
                          column=1,
                          #sticky='NSEW'
                          )
#%% Media Controls
        

        
        Media_Frame = tk.Frame(self)
        Media_Frame.grid(row=0,
                         column=1,
                         sticky = "NSEW"
                         )
        Media_Frame.rowconfigure(0, weight=1)
        Media_Frame.columnconfigure(0, weight=1)
        
        Media_Label = tk.Label(Media_Frame,
                             text = 'Media Controls',
                             bg = 'royalblue'
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
        NAV_Frame.grid(row=0,
                         column=2,
                         sticky='NSEW'
                         )
        NAV_Frame.rowconfigure(4, weight=1)
        NAV_Frame.columnconfigure(0, weight=1)
        
        Nav_Label = tk.Label(NAV_Frame,
                             text = 'Navigation Controls',
                             bg = 'royalblue'
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


        E_stop = tk.Button(NAV_Frame,
                       text='Emergency Stop',
                       fg='red'
                       #command=lambda: Scale(plot_frame)
                       )
        E_stop.grid(row = 4,
                column= 0,
                columnspan=5,
                sticky='NSEW'
                )
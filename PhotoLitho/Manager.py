import tkinter as tk
from constants import style
from screens import *


class Manager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Control Panel")
        self.geometry("500x500")
        container = tk.Frame(self)
        container.pack(
            side="top",
            fill="both", 
            expand=True
            )
        container.configure(bg=style.BACKGROUND)  
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1) 

        self.frames = {}
        for F in (Home, Manual_mode, Jog_mode, Read_DXF):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Home)

    def show_frame(self, container):                        #This method  shows a frame for the given container 
        frame = self.frames[container]
        frame.tkraise()
        

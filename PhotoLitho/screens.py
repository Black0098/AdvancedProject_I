import sys
import os
import tkinter as tk 
from constants import style
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Modules.dxf_functions import *


class Home(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=style.BACKGROUND)

        self.init_widgets()

    def init_widgets(self):

        welcome = tk.Label( self, text="Home", justify="center", **style.STYLE_1)
        welcome.pack( side="top", fill="both", expand=True, pady= 22, padx= 11, )

        button1 = tk.Button(self, text="Botón 1", **style.STYLE_1, command=lambda: self.controller.show_frame(Manual_mode))
        button1.pack(pady=5)

        button2 = tk.Button(self, text="Botón 2", **style.STYLE_1, command=lambda: self.controller.show_frame(Jog_mode))
        button2.pack(pady=5)

        button3 = tk.Button(self, text="Botón 3", **style.STYLE_1, command=lambda: self.controller.show_frame(Read_DXF))
        button3.pack(pady=5)
                

            

class Manual_mode(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=style.BACKGROUND)

        self.init_widgets()
        
    def init_widgets(self):
        tk.Label(
            self,
            text="Manual Mode",
            justify="center",
            **style.STYLE_1
        ).pack(
            side="top",
            fill="both",
            expand=True,
            pady= 22,
            padx= 11,
        )

        tk.Button(
            self,
            text="Home",
            command=lambda: self.controller.show_frame(Home),
            **style.STYLE_1
        ).pack(
            side="top",
            fill="both",
            expand=True,
            pady= 22,
            padx= 11,
        )


class Read_DXF(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=style.BACKGROUND)

        self.init_widgets()
        
    def init_widgets(self):
        tk.Label(
            self,
            text="DXF File",
            justify="center",
            **style.STYLE_1
        ).pack(
            side="top",
            fill="both",
            expand=True,
            pady= 22,
            padx= 11,
        )

        tk.Button(self, text="Home", command=lambda: self.controller.show_frame(Home), **style.STYLE_1).pack(
            side="top",
            fill="both",
            expand=True,
            pady= 22,
            padx= 11,
        )

        tk.Button(self, text="Leer el DXF", command=DXF).pack(
            side="top",
            fill="both",
            expand=True,
            pady= 22,
            padx= 11,
        )



class Jog_mode(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=style.BACKGROUND)

        self.init_widgets()
        
    def init_widgets(self):
        tk.Label(
            self,
            text="JOG Mode",
            justify="center",
            **style.STYLE_1
        ).pack(
            side="top",
            fill="both",
            expand=True,
            pady= 22,
            padx= 11,
        )

        tk.Button(
            self,
            text="Home",
            command=lambda: self.controller.show_frame(Home),
            **style.STYLE_1
        ).pack(
            side="top",
            fill="both",
            expand=True,
            pady= 22,
            padx= 11,
        )

        


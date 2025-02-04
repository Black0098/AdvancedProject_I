import tkinter as tk
from constants import style
from screens import *


class Manager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Control Panel")
        self.geometry("900x600")

        # Barra lateral-------------------------------------------------------------------------
        self.sidebar = tk.Frame(self, width=50, bg="gray")
        self.sidebar.pack(side="left", fill="y")

        self.tooltips = {}  # Diccionario para almacenar los tooltips

        tool_buttons = [
            {"icon": "📁", "command": lambda: print("Herramienta seleccionada"), "tooltip": "Conectar con el controlador"},
            {"icon": "🔧", "command": lambda: print("Herramienta seleccionada"), "tooltip": "Herramientas"},
            {"icon": "📜", "command": lambda: print("Documentación abierta"), "tooltip": "Ver documentación"},
            {"icon": "📊", "command": lambda: print("Estadísticas mostradas"), "tooltip": "Ver estadísticas"},
            {"icon": "❓", "command": lambda: print("Ayuda abierta"), "tooltip": "Ayuda"},
        ]

        # Crear los botones y asignar tooltips
        for tool in tool_buttons:
            btn = tk.Button(self.sidebar, text=tool["icon"], font=("Arial", 14), command=tool["command"])
            btn.pack(pady=5, padx=5)

            # Asignar el tooltip
            btn.bind("<Enter>", lambda event, tool=tool: self.show_tooltip(event, tool["tooltip"]))
            btn.bind("<Leave>", self.hide_tooltip)



        # Contenedor de pantallas-------------------------------------------------------------------------
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
        
    def show_tooltip(self, event, tooltip_text):
        # Crear y mostrar el tooltip
        self.tooltip = tk.Label(self, text=tooltip_text, background=style.LIGHT_GREEN, relief="solid", bd=1.2)
        self.tooltip.place(x=event.x_root + 20, y=event.y_root + 20)  # Posicionar el tooltip cerca del cursor

    def hide_tooltip(self, event):
        # Eliminar el tooltip
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
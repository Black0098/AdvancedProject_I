import tkinter as tk
from constants import style
import os
from screens import *


class Manager(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Control Panel")
        self.geometry("1200x700")
        self.resizable(False, False)


# Barra lateral-------------------------------------------------------------------------
        self.sidebar = tk.Frame(self, width=40, bg="gray")
        self.sidebar.pack(side="left", fill="y")

        self.tooltips = {}  # Diccionario para almacenar los tooltips

        tool_buttons = [
            {"icon": "🛜", "command": self.connect_galil, "tooltip": "Conectar con el controlador"},
            {"icon": "📩", "command": self.load_dxf, "tooltip": "Cargar DXF"},
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


# Barra de estado en la parte inferior------------------------------------------------------------

        self.status_bar = tk.Label(self, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

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

# Metodos del manager-------------------------------------------------------------------------

    def show_frame(self, container):                        #This method  shows a frame for the given container 
        frame = self.frames[container]
        frame.tkraise()
        
    def show_tooltip(self, event, tooltip_text):
        # Crear y mostrar el tooltip
        self.tooltip = tk.Label(self, text=tooltip_text, background="lightgreen", relief="solid", bd=1.2)

        # Obtener la posición del cursor en coordenadas de pantalla
        x_root, y_root = self.winfo_pointerx(), self.winfo_pointery()

        # Convertir a coordenadas relativas dentro de la ventana
        x_local = x_root - self.winfo_rootx()
        y_local = y_root - self.winfo_rooty()

        self.tooltip.place(x=x_local + 20, y=y_local + 20)  # Posicionar el tooltip cerca del cursor

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def load_dxf(self):
        print('\n\n\n\n\nDXF ABIERTO')
        
        doc, file_name = DXF(name = True)
        model = doc.modelspace()

        (lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimensions, inserts, arcs) = GiveTypes(model, print_e=True)
        
        plot_linepaths, curvepaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimensions, inserts, arcs, 20, simu=True)
        linepaths, curvepaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimensions, inserts, arcs, 20, simu=False)

    
        self.doc = doc
        self.file_name = file_name
        self.model = model
        self.lines = lines
        self.polylines = polylines
        self.lwpolylines = lwpolylines
        self.splines = splines
        self.circles = circles
        self.texts = texts
        self.mtexts = mtexts
        self.hatchs = hatchs
        self.dimensions = dimensions
        self.inserts = inserts
        self.arcs = arcs
        self.linepaths = linepaths
        self.plot_linepaths = plot_linepaths
        self.curvepaths = curvepaths

        print("DXF cargado y funciones ejecutadas exitosamente.")
        file_name = os.path.basename(file_name)
        print("Archivo leido:", file_name)

        # Una vez definido, notificamos a Home (u otra pantalla) llamando a un método
        if hasattr(self.frames[Home], "update_plot_linepaths"):
            self.frames[Home].update_plot_linepaths(self.plot_linepaths)
        if hasattr(self.frames[Home], "update_file_name"):
            self.frames[Home].update_file_name(self.file_name)

    def connect_galil(self):
        metodo_conexion = "192.168.1.100"  
        self.g = driver_conection(metodo_conexion, self.update_driver_status)
        if self.g:
            give_info(self.g, self.update_driver_status)

    def update_driver_status(self, message):
        """Actualiza el texto de la barra de estado."""
        self.status_bar.config(text=message)

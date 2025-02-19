import sys
import os
import tkinter as tk 
from constants import style
import matplotlib
matplotlib.use('TkAgg')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from Modules import *


class Home(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=style.BACKGROUND)
        self.plot_linepaths = None  # Inicialmente sin datos
        self.fig = None
        self.canvas = None
        self.canvas_frame = None
        self.file_name = "DXF: No definido"

        self.init_widgets()

    def init_widgets(self):
        # Contenedor principal que distribuirá los widgets horizontalmente.
        main_frame = tk.Frame(self, bg=style.BACKGROUND)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame izquierdo para labels y demás widgets
        left_frame = tk.Frame(main_frame, bg=style.BACKGROUND)
        left_frame.pack(side="left", fill="both", expand=True)

        welcome = tk.Label(left_frame, text="Home", justify="center", **style.STYLE_1)
        welcome.pack(side="top", fill="both", expand=True, pady=22, padx=11)

        # Ejemplo de botón (descomenta y adapta según necesites)
        # button1 = tk.Button(left_frame, text="Botón 1", **style.STYLE_1, command=lambda: self.controller.show_frame(Manual_mode))
        # button1.pack(pady=5)

        self.file_label = tk.Label( left_frame, text="linepaths: No definido", **style.STYLE_1)
        self.file_label.pack(side="top", pady=10)

        # Frame derecho para el canvas con borde y relieve
        self.canvas_frame = tk.Frame(main_frame, bd=2, relief=tk.RIDGE, bg=style.BACKGROUND)
        self.canvas_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Crear la figura de Matplotlib y un ejemplo de gráfica.
        self.fig = plt.Figure(dpi=100)
        ax = self.fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.grid()
        ax.set_title(f"{self.file_name}")

        # Crear el canvas de Matplotlib y agregarlo al frame derecho
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)




# Metodos de Home-----------------------------------------------------------------------------------------------------------------------------------
    def update_plot_linepaths(self, plot_linepaths):
        """
        Actualiza la variable plot_linepaths y reinicia la animación.
        """
        self.plot_linepaths = plot_linepaths
        print("Home actualizó plot_linepaths")
        # Inicializa (o reinicializa) la animación con los nuevos datos
        self.init_animation()

    def update_file_name(self, file_name):
        self.file_name = file_name
        # Actualiza algún widget para mostrar el nombre del archivo
        self.file_label.config(text=f"Archivo: {file_name}")
        print("Home actualizo el nombre del archivo a:", file_name)

    def init_animation(self):
        """
        Inicializa (o reinicializa) la animación utilizando self.plot_linepaths.
        """
        if not self.plot_linepaths:
           return

        # Calcular un límite adecuado para la animación
        # Se toma el valor máximo absoluto entre todos los puntos
        lim = max(np.max(np.abs(np.array(trayectoria))) for trayectoria in self.plot_linepaths)

        # Llamamos a Plot_Animation para configurar la figura, la animación y las funciones
        self.fig, frames_totales, actualizar, reiniciar_animacion = Plot_Animation(self.plot_linepaths, lim + (lim*0.1))

        # Si ya existía un canvas (por ejemplo, en una actualización anterior), se elimina
        if self.canvas:
            self.canvas.get_tk_widget().destroy()


        # Crear el canvas de Matplotlib y agregarlo al frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Crear la animación utilizando FuncAnimation
        self.anim = FuncAnimation(
            self.fig,
            actualizar,
            frames=frames_totales,
            interval=50,
            blit=True,
            repeat=False,
            init_func=reiniciar_animacion
        )

        # Dibujar el canvas para que se actualice la visualización
        self.canvas.draw()
                    

                

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

        


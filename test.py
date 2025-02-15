
from Modules import *
import gclib
import winsound
import time 

#Controler definition -------------------------------------------------------------
g = gclib.py()
g = driver_conection('192.168.1.100')
give_info(g)

doc = ezdxf.readfile("DXFs\Poly.DXF")
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, curvepaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 20)




def reproducir_alarma(frecuencia=500, duracion=300):
    """
    Reproduce un beep que simula una alarma.
    
    Parámetros:
      - frecuencia: Frecuencia del sonido en Hertz (por defecto 2500 Hz).
      - duracion: Duración del sonido en milisegundos (por defecto 1000 ms).
    """
    winsound.Beep(frecuencia, duracion)

reproducir_alarma()

import matplotlib.pyplot as plt
import numpy as np

# Parámetros
r = 10
start_deg = 270
end_deg = 450  # 450° equivale a 90° (450-360)
angles_deg = np.linspace(start_deg, end_deg, 200)
angles_rad = np.deg2rad(angles_deg)

# Coordenadas del arco
x_arc = r * np.cos(angles_rad)
y_arc = r * np.sin(angles_rad)

# Dibujo del círculo completo para referencia
theta = np.linspace(0, 2*np.pi, 300)
x_circle = r * np.cos(theta)
y_circle = r * np.sin(theta)

# Graficar
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(x_circle, y_circle, 'k--', label="Círculo")
ax.plot(x_arc, y_arc, 'b-', lw=2, label="Arco")
ax.plot(r * np.cos(np.deg2rad(start_deg)), r * np.sin(np.deg2rad(start_deg)),
        'ro', label="Inicio (270°)")
ax.plot(r * np.cos(np.deg2rad(end_deg)), r * np.sin(np.deg2rad(end_deg)),
        'go', label="Fin (450°/90°)")

ax.set_aspect('equal')
ax.grid(True)
ax.legend()
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Arco de 270° a 450° en un círculo de radio 10")

plt.show()





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

x = mm_to_counts(-0.1)
y = mm_to_counts(0)
move_to_position(g, x, y, 1, relative=True)

close_conection(g)
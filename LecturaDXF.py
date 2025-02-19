from Modules import *
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import ezdxf
from matplotlib.animation import FuncAnimation






doc = DXF()                                 #selct the dxf
#doc = ezdxf.readfile("DXFs\CirculoYCuadrado.DXF")     #allways the same dxf
model = doc.modelspace()

allpaths = []
lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, curvepaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 20, simu = True)




print("\n HOLA \n")

for center, radius, angles in curvepaths:
    if angles == (0, 0):
        print(f'\ncirculo con centro en {center} y radio de {radius}')
    else:
        print(f'\narco con centro en {center} y radio de {radius}\nangulo inicial {angles[0]}\nangulo final {angles[1]}')


#-----------------------------------------------------------------------------Grafica-----------------------------------------------------------------------------------------------------
max_lim = max(array.max() for array in linepaths)
radio = 0.8  # Radio del círculo
n_puntos_por_tramo = 2  # Resolución de cada tramo
fig, frames_totales, actualizar, reiniciar_animacion = Plot_Animation(linepaths, max_lim+1)
anim = FuncAnimation(fig, actualizar, frames=frames_totales, interval=50, blit=True, repeat=False, init_func = reiniciar_animacion)
plt.show()


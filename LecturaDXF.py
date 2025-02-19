import ezdxf
import gclib
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Modules.dxf_functions import *
from Modules.Galil_functions import *




doc = DXF()                                 #selct the dxf
#doc = ezdxf.readfile("DXFs\LineaYPoly.DXF")     #allways the same dxf
model = doc.modelspace()


radio = 0.8  # Radio del círculo
n_puntos_por_tramo = 2  # Resolución de cada tramo

allpaths = []
lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)

allpaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 50)


max_lim = max(array.max() for array in allpaths)


print("\n \n", allpaths[1])


#-----------------------------------------------------------------------------Grafica-----------------------------------------------------------------------------------------------------



fig, frames_totales, actualizar, reiniciar_animacion = Plot_Animation(allpaths, max_lim)
anim = FuncAnimation(fig, actualizar, frames=frames_totales, interval=50, blit=True, repeat=False, init_func = reiniciar_animacion)
plt.show()


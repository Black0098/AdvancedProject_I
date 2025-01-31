import ezdxf
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Modules import *




#Galil connection----------------------------------------------------------------------------------------------------------------
#g = driver_conection('COM6')
#give_info(g)

#Dxf reading---------------------------------------------------------------------------------------------------------------------

allpaths = []
doc = ezdxf.readfile("DXFs\LineasYCirculos.DXF")     #allways the same dxf
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, centers, radii = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)

print(radii)











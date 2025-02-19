import ezdxf
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Modules import *
import math
import time
import winsound


#Phisical parameters------------------------------------------------------------------------------------------------------------
pen_diameter = 3 #mm
pen_r = pen_diameter/2

#Galil connection----------------------------------------------------------------------------------------------------------------
g = gclib.py()
g = driver_conection('192.168.1.100')
g.GTimeout(int(30e3))
c = g.GCommand
c('SP 150000,150000')

#Dxf reading---------------------------------------------------------------------------------------------------------------------

allpaths = []
#doc = ezdxf.readfile("DXFs\LineasYCirculos.DXF") 
doc = ezdxf.readfile("DXFs\HexagonoYCuadrado.DXF")
#doc = ezdxf.readfile("DXFs\Poly.DXF") 
#doc = ezdxf.readfile("DXFs\CirculoYCuadrado.DXF") 
#doc = ezdxf.readfile("DXFs\Arcs.DXF")

model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles_dxf, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, curvepaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles_dxf, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)



time.sleep(3)
reproducir_alarma()


scale = 0.001
curvepaths_0 = []
Vector_move(g, linepaths, curvepaths_0, scale)
Filled_Vector_move(g, linepaths, curvepaths, pen_diameter, scale)

close_conection(g)











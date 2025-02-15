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




#Galil connection----------------------------------------------------------------------------------------------------------------
g = gclib.py()
g = driver_conection('192.168.1.100')
g.GTimeout(int(30e3))
c = g.GCommand
c('SP 150000,150000')

#Dxf reading---------------------------------------------------------------------------------------------------------------------

allpaths = []
#doc = ezdxf.readfile("DXFs\LineasYCirculos.DXF") 
#doc = ezdxf.readfile("DXFs\HexagonoYCuadrado.DXF")
#doc = ezdxf.readfile("DXFs\Poly.DXF") 
#doc = ezdxf.readfile("DXFs\CirculoYCuadrado.DXF") 
doc = ezdxf.readfile("DXFs\Arcs.DXF")

model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles_dxf, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, curvepaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles_dxf, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)



time.sleep(3)
reproducir_alarma()

def draw_circles(g, center, radius, scale = 1):
    c = g.GCommand
    r = mm_to_counts(radius)
    x0, y0, z0 = map(mm_to_counts, center)
    move_to_position(g, (x0+r), y0, scale, relative=False)
    reproducir_alarma(1000, 400)
    print('\nPRENDE LÁSER!!!!!!!!!!!')
    setup_vector_mode(g)
    c(f'CR {r*scale}, 0, 360')
    c('VE')
    c('BGS')
    g.GMotionComplete('AB')
    reproducir_alarma(1000, 400)
    print('\nPARA LÁSER XXXXXXXXXXXX')

def draw_arcs(g, center, radius, angles, scale = 1):
    c = g.GCommand
    r = mm_to_counts(radius)
    x0, y0, z0 = map(mm_to_counts, center)
    a0, a1 = map(np.radians, angles)
    move_to_position(g, (x0 + r*np.cos(a0)), (y0 + r*np.sin(a0)), scale, relative=False)
    reproducir_alarma(1000, 400)
    print('\nPRENDE LÁSER!!!!!!!!!!!')
    setup_vector_mode(g)
    c(f'CR {r*scale}, {angles[0]}, {angles[1]-angles[0]}')
    c('VE')
    c('BGS')
    g.GMotionComplete('AB')
    reproducir_alarma(1000, 400)
    print('\nPARA LÁSER XXXXXXXXXXXX')





Vector_move(g, linepaths, scale=0.2)

for center, radius, angles in curvepaths:
    if angles == (0, 0):
        draw_circles(g, center, radius, scale=0.2)
        print(f'\ncirculo con centro en {center} y radio de {radius}')
    else:
        print(f'\narco con centro en {center} y radio de {radius}\nangulo inicial {angles[0]}\nangulo final {angles[1]}')
        draw_arcs(g, center, radius, angles, scale=0.2)














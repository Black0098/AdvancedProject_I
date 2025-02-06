import ezdxf
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Modules import *
import math
import time




#Galil connection----------------------------------------------------------------------------------------------------------------
#g = driver_conection('COM6')
#give_info(g)

#Dxf reading---------------------------------------------------------------------------------------------------------------------

allpaths = []
doc = ezdxf.readfile("DXFs\LineasYCirculos.DXF")     #allways the same dxf
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, centers, radii = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)



g = gclib.py()
g = driver_conection('192.168.1.100')
c = g.GCommand

c('SP 150000,150000,150000')

print(centers)

def rotate(g, deg, relative=False, wait = True):
    """
    Envía un comando al controlador para girar la máquina a una posición dada.
    
    Parámetros:
        g: Objeto controlador Galil.
        deg: angulo en 'counts'.
        relative: Si es True, usa movimiento relativo ('PR'); si es False, usa absoluto ('PA').
    """
    c = g.GCommand
    command_type = 'PR' if relative else 'PA'

    command = f'{command_type} , , {deg}'
    c(command)
    c('BG C')
    g.GMotionComplete('C') if wait else None
def dxf_circles(centers, radii, g):
    """
    Procesa una lista de entidades DXF y las traduce en movimientos de la máquina.

    Parámetros:
        centers: Lista de centros de los círculos.
        radii: Lista de radios de los círculos.
        g: Objeto controlador Galil.
    """
    for i, center in enumerate(centers):

        print(f'  -------------VA_AL_CENTRO_{i}-------------')
        r = mm_to_counts(radii[i])
        x, y, z = map(mm_to_counts, center)
        move_to_position(g, -x+r, -y,scale=0.5)
        print('start lasser')
        deg = deg_to_counts(360)
        rotate(g, deg, relative=True)
        print(f'\n -------------FINISH_{i}-------------')


'''
time_out  = int(30e3)
g.GTimeout(time_out)

c = g.GCommand
c('AC 256000,256000,256000')
c('DC 256000,256000,256000')
c('SP 150000,150000, 150000')
c('PA 0, 0')
c('BG AB')
g.GMotionComplete

print('ESPERA 5 sec')
time.sleep(5)


center_x, center_y = 10, 10
radius = 7
segments = 36
angle_inc = 360 / segments   # 10° por segmento

start_x = center_x + radius   # 30 + 7 = 37
start_y = center_y            # 30


move_to_position(g, mm_to_counts(start_x), mm_to_counts(start_y), scale= 1, relative=False)
c('AC 256000,256000,256000')
c('DC 556000,556000,556000')

angle_inc_rad = math.radians(angle_inc)
chord = 2 * radius * math.sin(angle_inc_rad / 2)

for i in range(segments):
    rotate(g, deg_to_counts(angle_inc), relative=True, wait=False)
    move_to_position(g, mm_to_counts(chord), scale= 1 , relative=True, wait = False)
    


'''
close_conection(g)








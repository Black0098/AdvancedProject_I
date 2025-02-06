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
doc = ezdxf.readfile("DXFs\LineasYCirculos.DXF") 
#doc = ezdxf.readfile("DXFs\LineaYPoly.DXF") 
   #allways the same dxf
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, centers, radii = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)

print(linepaths)

def Vector_move(g, linepaths, centers, radii):
    '''
    This function calculates the trajectory for lines, polylines, circles, and arcs.
    '''
    c = g.GCommand
    # Verificar si alguno de los parámetros es None
    if linepaths is None:
        linepaths = []
    if centers is None:
        centers = []
    if radii is None:
        radii = []

    for i, entity in enumerate(linepaths):
        if len(entity) == 2:  #  LINE
            draw_lines(g, entity)
            
        else: #POLOLINEA
            print(f'\n\n Es una PolilInea compuesta por {len(entity)} Puntos')
            draw_lines(g, entity)


def setup_vector_mode(g, VECTOR_SPEED  = 150000, VECTOR_ACCEL  = 1000000, VECTOR_DECEL  = 1000000):
    """Configura el modo vectorial en 2D (ejes A y B) y sus parámetros."""
    c = g.GCommand
    c('VM AB')                         # Inicializa el plano 2D para X, Y
    c(f'VS {VECTOR_SPEED}')            # Velocidad del vector
    c(f'VA {VECTOR_ACCEL}')            # Aceleración del vector
    c(f'VD {VECTOR_DECEL}')            # Desaceleración del vector
    
def draw_lines(g, entity):
    """
    Dibuja una entidad que puede ser línea (2 puntos) o polilínea (N puntos).
    - entity: lista de puntos [(x_mm, y_mm, z_mm), ...]
    - laser_on: indica si queremos encender/apagar láser con mensajes específicos.
    """
    c = g.GCommand
    x0, y0, z0 = map(mm_to_counts, entity[0])
    move_to_position(g, x0, y0, scale=1)
    time.sleep(2)
    print('\nPRENDE LÁSER!!!!!!!!!!!')
    setup_vector_mode()
    
    
    for i in range(1, len(entity)):
        x, y, z = map(mm_to_counts, entity[i])
        dx = x - x0
        dy = y - y0
        c(f'VP {dx}, {dy}') 
    c('VE')
    c('BGS')
    print('\nPARA LÁSER XXXXXXXXXXXX')







#g = gclib.py()
#g = driver_conection('192.168.1.100')
#c = g.GCommand








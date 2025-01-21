import ezdxf
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Modules.dxf_functions import *
from Modules.Galil_functions import *

#Simulated functions------------------------------------------------------------------------------------------------------------

def send_simulated_order(order):
    """
    Tells the driver what to do based on the Galil instructions

    """
    try: 
        if not isinstance(order, str):
            order = str(order)

        print(order)
        
        
    except Exception as e:
        print("Error al enviar un comando:", e)
        
def move_simulated_axis(axis, distance):
    '''moves the simulated axis to a specified distance'''
  
    try:
        order = f'PR{axis} = {distance}'    #Uses the PR command (position relative)
        send_simulated_order(order)
        send_simulated_order(f'BG{axis}')
        send_simulated_order(f'AM{axis}')
        print(f"Eje {axis} moviendose a {distance} \"unidades\".")
        
    except Exception as e:
        print("Error al mover el eje:", e)


#Galil connection----------------------------------------------------------------------------------------------------------------
#g = driver_conection('COM6')
#give_info(g)

#Dxf reading---------------------------------------------------------------------------------------------------------------------

allpaths = []
doc = ezdxf.readfile("DXFs\CirculoYCuadrado.DXF")     #allways the same dxf
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=False)
allpaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)

print('\n')
print(allpaths[4][4])

#print(f'\nMueve el eje X de {allpaths[0][0][0]} a {allpaths[0][0+1][0]}')

axisa = 'A'
axisb = 'B'


for i in range(len(allpaths)):
    if len(allpaths[:][i]) == 2:
        print(f'  -------------START_{i}-------------' )
        print('\n -------------FROM-------------' )
        move_simulated_axis(axisa, allpaths[i][0][0])
        move_simulated_axis(axisb, allpaths[i][0][1])



        print('start lasser')

        print('\n -------------TO-------------' )
        move_simulated_axis(axisa, allpaths[i][1][0])
        move_simulated_axis(axisb, allpaths[i][1][1])


        print('stop lasser')
        print(f'\n -------------FINISH_{i}-------------' )
    else:
        print(f'\n\n\nes un circulo compuesto por {len(allpaths[:][i])} lineas') 
        




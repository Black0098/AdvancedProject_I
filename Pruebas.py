import ezdxf
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Modules.dxf_functions import *
from Modules.Galil_functions import *



#Galil connection----------------------------------------------------------------------------------------------------------------
#g = driver_conection('COM6')
#give_info(g)

#Dxf reading---------------------------------------------------------------------------------------------------------------------

allpaths = []
doc = ezdxf.readfile("DXFs\CirculoYCuadrado.DXF")     #allways the same dxf
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=False)
allpaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)

print('\n PRUEBA DE ALLPATHS')
print(allpaths[4][4])

def mmtocounts(mm):
    counts = round(mm/3e-5)
    return counts




g = gclib.py()
g = driver_conection('192.168.1.100')
#g = driver_conection('COM4 -b 19200')
give_info(g)
g.GTimeout(int(30e3))
c = g.GCommand

x = mmtocounts(75-12)              # Posición final (en mm)
y = mmtocounts(75+16)



c(f'PR {x},{y}')
c('BG AB')


g.GMotionComplete('AB')
print('\n in center \n')

input('Press Enter to continue...')


for i in range(len(allpaths)):
    if len(allpaths[:][i]) == 2:
        print(f'  -------------START_{i}-------------' )
        print('\n -------------FROM-------------' )

        allpaths[i][0][0] = mmtocounts(allpaths[i][0][0])
        allpaths[i][0][1] = mmtocounts(allpaths[i][0][1])

        c(f'PR {0.1*allpaths[i][0][0]},{0.1*allpaths[i][0][1]}')
        c('BG AB')
        g.GMotionComplete('AB')

        print('start lasser')

        print('\n -------------TO-------------' )

        allpaths[i][1][0] = mmtocounts(allpaths[i][1][0])
        allpaths[i][1][1] = mmtocounts(allpaths[i][1][1])

        c(f'PR {0.1*allpaths[i][1][0]},{0.1*allpaths[i][1][1]}')
        c('BG AB')
        g.GMotionComplete('AB')


        print('stop lasser')
        print(f'\n -------------FINISH_{i}-------------' )

    else:
        print(f'\n\n\nes un circulo compuesto por {len(allpaths[:][i])} lineas') 
        for j in range(len(allpaths[:][i])-1):
            
            print(f'  -------------START_{i}_{j}-------------' )
            print('\n -------------FROM-------------' )

            allpaths[i][j][0] = mmtocounts(allpaths[i][j][0])
            allpaths[i][j][1] = mmtocounts(allpaths[i][j][1])

            c(f'PR {0.1*allpaths[i][j][0]},{0.1*allpaths[i][j][1]}')
            c('BG AB')
            g.GMotionComplete('AB')
            

            print('start lasser')

            print('\n -------------TO-------------' )

            allpaths[i][j+1][0] = mmtocounts(allpaths[i][j+1][0])
            allpaths[i][j+1][1] = mmtocounts(allpaths[i][j+1][1])

            c(f'PR {0.1*allpaths[i][j+1][0]},{0.1*allpaths[i][j+1][1]}')
            c('BG AB')
            g.GMotionComplete('AB')

            print('stop lasser')
            print(f'\n -------------FINISH_{i}_{j}-------------' )





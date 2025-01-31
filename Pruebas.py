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
doc = ezdxf.readfile("DXFs\Poly.DXF")     #allways the same dxf
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
allpaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)
def mmtocounts(mm):
    return round(round(mm, 5)/3e-5)

print('\n PRUEBA DE ALLPATHS')
print(allpaths[0][0])


g = driver_conection('192.168.1.100')
give_info(g)
time_out  = int(30e3)
c = g.GCommand
g.GTimeout(time_out)

input('\nPress Enter to continue...')
for i in range(len(allpaths[:][0])):

    allpaths[0][i][0] = mmtocounts(allpaths[0][i][0])
    allpaths[0][i][1] = mmtocounts(allpaths[0][i][1])

    print(f'PA {allpaths[0][i][0]}, {allpaths[0][i][1]}')
    c(f'PA {allpaths[0][i][0]}, {allpaths[0][i][1]}')
    c('BG AB')
    g.GMotionComplete('AB')


input('PRESS ENTER TO CLOSE')

close_conection(g)
    











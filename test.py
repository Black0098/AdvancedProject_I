
from Modules import *
import gclib
import time 

g = gclib.py()
g = driver_conection('192.168.1.100')
give_info(g)

doc = ezdxf.readfile("DXFs\Poly.DXF")
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, centers, radii = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 20)

def mmtocounts(mm):
    counts = round(mm/3e-5)
    return counts

def degtocounts(deg):
    return round(deg/8.05556e-5)

print(linepaths[0])

time.sleep(4)
c = g.GCommand

c('VM AB')
c('VS 150000')
c('VA 1000000')
c('VD 1000000')

for line in linepaths:  # Itera sobre cada línea en linepaths
    for point in line[1:]:  # Itera sobre cada punto dentro de la línea
        x, y, z = map(mm_to_counts, point)  # Convierte los valores
        
        c(f'VP {x}, {y}')

c('VE')
c('BGS')

close_conection(g)
#Prueba del modo vector HASMIR TE AMO


x = 10 #mm
y = 10 #mm



'''
def linear_move(g, x, y, g):
    c = g.GCommand
'''

'''
c('LMAB')
c('LI -333333,0')  #Specify first linear segment
c('LI -333333, -333333')  #Specify second linear segment
c('LE')         #End linear segments
c('VS 150000')    #Specify vector speed
c('BGS')        #Begin motion sequence 
'''



#c('CR 233333, 270, -180')
#c('VP 0 , 233333*2')
#c('CR 233333, 90, -180')



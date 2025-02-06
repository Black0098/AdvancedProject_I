
from Modules import *
import gclib
import winsound
import time 

#Controler definition -------------------------------------------------------------
g = gclib.py()
g = driver_conection('192.168.1.100')
give_info(g)

doc = ezdxf.readfile("DXFs\Poly.DXF")
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=True)
linepaths, centers, radii = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 20)




def reproducir_alarma(frecuencia=500, duracion=300):
    """
    Reproduce un beep que simula una alarma.
    
    Parámetros:
      - frecuencia: Frecuencia del sonido en Hertz (por defecto 2500 Hz).
      - duracion: Duración del sonido en milisegundos (por defecto 1000 ms).
    """
    winsound.Beep(frecuencia, duracion)

# Reproduce una alarma única
reproducir_alarma()

# O bien, reproduce la alarma tres veces con una pequeña pausa entre cada una
#
#reproducir_alarma()




'''

    for i, entity in enumerate(linepaths):
        if len(entity) == 2:  #  LINE
            x1, y1, z1 = map(mm_to_counts, entity[0])
            x2, y2, z2 = map(mm_to_counts, entity[1])
            move_to_position(g, x1, y1, scale=1)
            print('PRENDE LASSER!!!!!!!!!!!')
            c('VM AB')              #inicializa un plano 2d para x,y
            c('VS 150000')          #Velocidad del vector 
            c('VA 1000000')         #Aceleracion del vector
            c('VD 1000000')         #Desaceleracion del vector
            c(f'VP {x2-x1}, {y2-y1}')     #Establece la direccion a la que se dirige 
            c('VE')                 #Finaliza el vector 
            c('BGS')                #Inicia secuencia
            print('\nPARA LASER XXXXXXXXXXXX')
        else: #POLOLINEA
            print(f'\n\n Es una PolilInea compuesta por {len(entity)} Puntos')
            x0, y0, z1 = map(mm_to_counts, entity[0])
            move_to_position(g, x0, y0, scale=1)
            c('VM AB')              #inicializa un plano 2d para x,y
            c('VS 150000')          #Velocidad del vector 
            c('VA 1000000')         #Aceleracion del vector
            c('VD 1000000')         #Desaceleracion del vector
            for j, point in enumerate(entity):
                x, y, z = map(mm_to_counts, point)
                c(f'VP {x-x0}, {y-y0}')
            c('VE')
            c('BGS')
'''


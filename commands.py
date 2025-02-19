from Modules.DXF_Reading import *
from Modules.CNC_Logic import *
import time

g = gclib.py()

print('')
g = driver_conection('192.168.1.100')
give_info(g)

doc = DXF()
#doc = ezdxf.readfile("DXFs\CirculoYCuadrado.DXF")     #allways the same dxf
model = doc.modelspace()

lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs = GiveTypes(model, print_e=False)
linepaths, curvepaths = AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, 5)


x = 0          # Posición final (en mm)
y = 0
z = 0

xc= round(x/3e-5)  # Conversión de mm a unidades
yc= round(y/3e-5)  
zc= round(z/3e-5)  





time_out  = int(30e3)
c = g.GCommand


menu = bool
while menu:
    g.GTimeout(time_out)
    #c('AC 256000')
    #c('DC 256000')
    c('SP 150000,150000')

    print("-----------------------------------------------------------------------------------")
    print("\nBienvenido al panel de controlo V 0.01")
    print("Digite el numero correspondiente a la accion que desea realizar \n")
    sel = int(input(' 1. Regresar a Home \n 2. Comenzar lectura del DXF \n 3. Centro \n 4. Establece 0 global \n 5. Salir \n 6. Movimiento Libre \n' ))

    if sel == 1: 
        c('HM')
        c('BG AB')
        g.GMotionComplete('AB')
        print('\n En Home (Esto es necesario ya que actualmente no se tiene establecido una coordenada cero en el montaje) \n')
        
    elif sel == 2: 
        try :


            input('Presione enter para comenzar la rutina')
            Vector_move(g, linepaths, curvepaths, scale = 0.5)

        except Exception as e:

            print("Error al cumplir la rutina:", e)
            pass

    elif sel == 3:
        c(f'PA {0},{0}')
        c('BG AB')
        g.GMotionComplete('AB')
        print(f"\n En centro: {c('RP')}")

    elif sel == 4:
        c(f'PR {xc},{yc}')  #coordenadas hacia el centro (establecidas manualmente)
        c('BG AB')       
        g.GMotionComplete('AB')
            
        c('DPA = 0')
        c('DPB = 0')
            
        print(f'\n in center: {c('RP')} \n')

    elif sel == 5:
        close_conection(g)
        menu = False

    elif sel == 6:
        x = float(input('Digite la coordenada x: '))
        y = float(input('Digite la coordenada y: '))
        x = mm_to_counts(x)
        y = mm_to_counts(y)
        move_to_position(g, x, y, 1, relative=True)
        print(f'\n The global position Is: {c('PA ?, ?')} \n')

    
    else:
        print("por favor seleccione una opcion correcta")
        pass


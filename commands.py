from Modules.dxf_functions import *
from Modules.Galil_functions import *
import time

g = gclib.py()

print('')
#g = driver_conection('COM4 -b 19200')
g = driver_conection('192.168.1.100')
give_info(g)



x = 75-12              # Posición final (en mm)
y = 75+16
z = 0

xc= round(x/3e-5)  # Conversión de mm a unidades
yc= round(y/3e-5)  
zc= round(z/3e-5)  



ez_squarex = [5.0, 2.0225, 1.5451, -0.7725, -4.0451, -2.5, -4.0451, -0.7725, 1.5451, 2.0225]
ez_squarey = [0.0, 1.4695, 4.7553, 2.3776, 2.9389, 0.0, -2.9389, -2.3776, -4.7553, -1.4695]

ez_squarex = [x * 2 for x in ez_squarex]
ez_squarey = [y * 2 for y in ez_squarey]

def mmtocounts(mm):
    counts = round(mm/3e-5)
    return counts


time_out  = int(30e3)
c = g.GCommand
close_conection(g)

try:    



    g.GTimeout(time_out)
    #c('AC 256000')
    #c('DC 256000')
    c('SP 150000,150000')
    

    c(f'PR {xc},{yc}')
    c('BG AB')


    g.GMotionComplete('AB')
    print('\n in center \n')

    input('Press Enter to continue...')

    for i in range(len(ez_squarex)):
        ez_squarex[i] = mmtocounts(ez_squarex[i])
        ez_squarey[i] = mmtocounts(ez_squarey[i])

        c(f'PR {ez_squarex[i]},{ez_squarey[i]}')
        c('BG AB')
        g.GMotionComplete('AB')
        print(f'\n in {i} \n')


    c('HM')
    c('BG AB')
    g.GMotionComplete('AB')
    print('\n TODO MELO \n')

except Exception as e:

    print("Error al conectar:", e)
    pass

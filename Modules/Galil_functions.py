import gclib

def driver_conection(metodo_conexion):
    """
    Initializes a connection with the Galil driver.

    """
    g = gclib.py()
    try:
        g.GOpen(metodo_conexion)
        print("Conexion establecida con:", metodo_conexion)
        return g
    except Exception as e:
        print("Error al conectar:", e)
        return None
    
def close_conection(g):
    """
    Closes the connection with the driver

    """
    try:
        g.GClose()
        print("Conexion cerrada")
    except Exception as e:
        print("Error al cerrar la conexion:", e)

def give_info(g):
    """
    returns the info of the controller connected

    """
    try: 
        info = g.GInfo()
        print(info)
    except Exception as e:
        print("Error al dar informacion:", e)

def send_order(g, order):
    """
    Tells the driver what to do based on the Galil instructions

    """
    try: 
        if not isinstance(order, str):
            order = str(order)

        response = g.GCommand(order)
        return response
        
    except Exception as e:
        print("Error al enviar un comando:", e)
        return None

def move_axis(g, axis, distance, MC = True):

    """
    moves the axis to a specified distance

    """
    try:
        g.GTimeout(int(30e3))
        order = f'PR{axis} = {distance}'    #Uses the PR command (position relative)
        send_order(g, order)
        #send_order(g, f'BG{axis}')
        #if MC == True: send_order(g, f'MC')
        print(f"Eje {axis} moviéndose a {distance} \"unidades\".")
        
    except Exception as e:
        print("Error al mover el eje:", e)

def mmtocounts(mm):
    counts = round(mm/3e-5)
    return counts

def process_dxf(allpaths, g):
    
    c = g.GCommand 

    for i in range(len(allpaths)):
        if len(allpaths[:][i]) == 2: #This Case Verifyes if the entity is a LINE
            print(f'  -------------START_{i}-------------' )
            print('\n -------------FROM-------------' )

            allpaths[i][0][0] = mmtocounts(allpaths[i][0][0])
            allpaths[i][0][1] = mmtocounts(allpaths[i][0][1])

            c(f'PA {0.1*allpaths[i][0][0]},{0.1*allpaths[i][0][1]}')
            c('BG AB')
            g.GMotionComplete('AB')

            print('start lasser')

            print('\n -------------TO-------------' )

            allpaths[i][1][0] = mmtocounts(allpaths[i][1][0])
            allpaths[i][1][1] = mmtocounts(allpaths[i][1][1])

            c(f'PA {0.5*allpaths[i][1][0]},{0.5*allpaths[i][1][1]}')
            c('BG AB')
            g.GMotionComplete('AB')


            print('stop lasser')
            print(f'\n -------------FINISH_{i}-------------' )

        else:
            print(f'\n\n\n es una Polinline compuesta por:  {len(allpaths[:][i])} lineas') 

            
            for j in range(len(allpaths[:][i])):

                allpaths[i][j][0] = mmtocounts(allpaths[i][j][0])
                allpaths[i][j][1] = mmtocounts(allpaths[i][j][1])

                c(f'PA {0.5*allpaths[i][j][0]},{0.5*allpaths[i][j][1]}')
                c('BG AB')
                g.GMotionComplete('AB')
                   
                
    return
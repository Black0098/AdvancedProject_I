import gclib

def driver_conection(metodo_conexion):
    """
    Initializes a connection with the Galil driver.

    """
    g = gclib.py()
    try:
        g.GOpen(metodo_conexion)
        print("Conexión establecida con:", metodo_conexion)
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
        print("Conexión cerrada")
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

def move_axis(g, axis, distance):
    """
    moves the axis to a specified distance

    """
    try:
        order = f'PR{axis} = {distance}'    #Uses the PR command (position relative)
        send_order(g, order)
        send_order(g, f'BG{axis}')
        print(f"Eje {axis} moviéndose a {distance} \"unidades\".")
        
    except Exception as e:
        print("Error al mover el eje:", e)
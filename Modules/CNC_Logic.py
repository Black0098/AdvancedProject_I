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

def mm_to_counts(mm):
    """Convierte milimetros a 'counts."""
    return round(mm / 3e-5)

def deg_to_counts(deg):
    """Convierte grados a 'counts."""
    return round(deg/8.05556e-5)


def move_to_position(g, x, y=None, scale=1.0, relative=False, wait = True):
    """
    Envía un comando al controlador para mover la máquina a una posición dada.
    
    Parámetros:
        g: Objeto controlador Galil.
        x, y: Coordenadas en 'counts'.
        scale: Factor de escala para la posición.
        relative: Si es True, usa movimiento relativo ('PR'); si es False, usa absoluto ('PA').
    """
    c = g.GCommand

    command_type = 'PR' if relative else 'PA'

    if y is None:
        command = f'{command_type} {scale * x}'
    else:
        command = f'{command_type} {scale * x}, {scale * y}'
    
    c(command)
    c('BG AB')
    g.GMotionComplete('AB')
    g.GMotionComplete('C') if wait else None


def dxf_lines(linepaths, g):
    """
    Procesa una lista de entidades DXF y las traduce en movimientos de la máquina.

    Parámetros:
        allpaths: Lista de entidades DXF (líneas o polilíneas).
        g: Objeto controlador Galil.
    """
    for i, entity in enumerate(linepaths):
        if len(entity) == 2:  #  LINE
            print(f'  -------------START_{i}-------------')
            print('\n -------------FROM-------------')

            x1, y1, z1 = map(mm_to_counts, entity[0])
            move_to_position(g, x1, y1, scale=1)

            print('start lasser')

            print('\n -------------TO-------------')

            x2, y2, z2 = map(mm_to_counts, entity[1])
            move_to_position(g, x2, y2, scale=1)

            print('stop lasser')
            print(f'\n -------------FINISH_{i}-------------')

        else:  # POLYLINE
            print(f'\n\n\n Es una PolilInea compuesta por {len(entity)} líneas')

            for j, point in enumerate(entity):
                x, y, z = map(mm_to_counts, point)
                move_to_position(g, x, y, scale=1)
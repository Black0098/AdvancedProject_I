import gclib, math, numpy as np, time, winsound



def reproducir_alarma(frecuencia=500, duracion=300):
    """
    Reproduce un beep que simula una alarma.
    
    Parámetros:
      - frecuencia: Frecuencia del sonido en Hertz (por defecto 2500 Hz).
      - duracion: Duración del sonido en milisegundos (por defecto 1000 ms).
    """
    winsound.Beep(frecuencia, duracion)

def driver_conection(metodo_conexion, update_status=None):
    """
    Inicializa la conexión con el driver Galil.
    """
    g = gclib.py()
    try:
        g.GOpen(metodo_conexion)
        msg = f"Conexion establecida con: {metodo_conexion}"
        
        if update_status:
            update_status(msg)
        
        print(msg)
        return g
    except Exception as e:
        msg = f"Error al conectar: {e}"
        if update_status:
            update_status(msg)
        print(msg)
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

def give_info(g, update_status=None):
    """
    Retorna la información del controlador conectado.
    """
    try:
        info = g.GInfo()
        if update_status:
            update_status(info)
        print(info)
        
    except Exception as e:
        msg = f"Error al dar informacion: {e}"
        if update_status:
            update_status(msg)
        print(msg)

def mm_to_counts(mm):
    """Convierte milimetros a 'counts."""
    return round(mm / 3e-5)

def deg_to_counts(deg):
    """Convierte grados a 'counts."""
    return round(deg/8.05556e-5)

def fill_question():
    """
    Pregunta si la linea o el circulo necesita un relleno
    """
    while True:
        fill = input('desea rellenar el circulo? y/n\n')
        if fill == 'y' or fill == 'n':
            break
        else:
            print('respuesta incorrecta\n')
    return fill

def circle_fills(curvepaths):
    """
    Recorre `curvepaths` y pregunta si se debe rellenar el círculo antes de ejecutar los movimientos.
    Devuelve una lista con las respuestas de si se debe rellenar o no para cada círculo.
    """
    fills = []  # Lista que almacenará las respuestas de 'rellenar' para cada curva

    for center, radius, angles in curvepaths:
        if angles == (0, 0):  # Solo preguntamos por círculos
            print(f"Centro: {center}, Radio: {radius}")
            fill = fill_question()  # Preguntamos si se debe rellenar
            fills.append(fill) 
        else:
            
            fills.append('n')  # 'n' indica que no hay relleno para los arcos
            print(f'\narco con centro en {center} y radio de {radius}\nangulo inicial {angles[0]}\nangulo final {angles[1]}')
    
    return fills

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

def setup_vector_mode(g, VECTOR_SPEED  = 150000, VECTOR_ACCEL  = 1000000, VECTOR_DECEL  = 1000000):
    """Configura el modo vectorial en 2D (ejes A y B) y sus parámetros."""
    c = g.GCommand
    c('VM AB')                         # Inicializa el plano 2D para X, Y
    c(f'VS {VECTOR_SPEED}')            # Velocidad del vector
    c(f'VA {VECTOR_ACCEL}')            # Aceleración del vector
    c(f'VD {VECTOR_DECEL}')            # Desaceleración del vector
    
def draw_circles(g, center, radius, scale = 1):
    c = g.GCommand
    r = mm_to_counts(radius)
    x0, y0, z0 = map(mm_to_counts, center)
    move_to_position(g, (x0+r), y0, scale, relative=False)
    reproducir_alarma(1000, 400)
    print('\nPRENDE LÁSER!!!!!!!!!!!')
    setup_vector_mode(g)
    c(f'CR {r*scale}, 0, 360')
    c('VE')
    c('BGS')
    g.GMotionComplete('AB')
    reproducir_alarma(1000, 400)
    print('\nPARA LÁSER XXXXXXXXXXXX')

def draw_arcs(g, center, radius, angles, scale = 1):
    c = g.GCommand
    r = mm_to_counts(radius)
    rx = mm_to_counts(radius*math.cos(np.radians(angles[0])))
    ry = mm_to_counts(radius*math.sin(np.radians(angles[0])))
    x0, y0, z0 = map(mm_to_counts, center)
    newx = (x0 + rx)
    newy = (y0 + ry)

    move_to_position(g, newx, newy, scale, relative=False)
    reproducir_alarma(1000, 400)
    print('\nPRENDE LÁSER!!!!!!!!!!!')
    setup_vector_mode(g)
    c(f'CR {r*scale}, {angles[0]}, {angles[1]-angles[0]}')
    c('VE')
    c('BGS')
    g.GMotionComplete('AB')
    reproducir_alarma(1000, 400)
    print('\nPARA LÁSER XXXXXXXXXXXX')

def draw_lines(g, entity, scale = 1):
    """
    Dibuja una entidad que puede ser línea (2 puntos) o polilínea (N puntos).
    - entity: lista de puntos [(x_mm, y_mm, z_mm), ...]
    - laser_on: indica si queremos encender/apagar láser con mensajes específicos.
    """
    g.GTimeout(int(30e3))
    c = g.GCommand
    x0, y0, z0 = map(mm_to_counts, entity[0])
    move_to_position(g, x0, y0, scale)
    reproducir_alarma(1000,400)
    print('\nPRENDE LÁSER!!!!!!!!!!!')
    setup_vector_mode(g)
    
    
    for i in range(1, len(entity)):
        x, y, z = map(mm_to_counts, entity[i])
        dx = (x - x0)*scale
        dy = (y - y0)*scale
        c(f'VP {dx}, {dy}') 
    c('VE')
    c('BGS')
    g.GMotionComplete('AB')
    reproducir_alarma(1000,400)
    print('\nPARA LÁSER XXXXXXXXXXXX')

def Vector_move(g, linepaths, curvepaths, scale = 1):
    '''
    This function calculates the trajectory for lines, polylines, circles, and arcs.
    '''
    c = g.GCommand
    g.GTimeout(int(30e3))
    
    # Verificar si alguno de los parámetros es None
    if linepaths is None:
        linepaths = []
    if curvepaths is None:
        curvepaths = []

    for i, entity in enumerate(linepaths):
        if len(entity) == 2:  #  LINE
            draw_lines(g, entity, scale)
            
        else: #POLOLINEA
            print(f'\n\n Es una PolilInea compuesta por {len(entity)} Puntos')
            draw_lines(g, entity, scale)

    for center, radius, angles in curvepaths:
        if angles == (0, 0):
            draw_circles(g, center, radius, scale)
            print(f'\ncirculo con centro en {center} y radio de {radius}')
        else:
            print(f'\narco con centro en {center} y radio de {radius}\nangulo inicial {angles[0]}\nangulo final {angles[1]}')
            draw_arcs(g, center, radius, angles, scale)

def Filled_Vector_move(g, linepaths, curvepaths, beam_d, scale = 1):
    '''
    This function calculates the trajectory for lines, polylines, circles, and arcs.
    '''
    c = g.GCommand
    g.GTimeout(int(30e3))
    
    # Verificar si alguno de los parámetros es None
    if linepaths is None:
        linepaths = []
    if curvepaths is None:
        curvepaths = []

    for i, entity in enumerate(linepaths):
        if len(entity) == 2:  #  LINE
            draw_lines(g, entity, scale)
            
        else: #POLOLINEA
            print(f'\n\n Es una PolilInea compuesta por {len(entity)} Puntos')
            draw_lines(g, entity, scale)

    fills = circle_fills(curvepaths)
    for (center, radius, angles), fill in zip(curvepaths, fills):
        if angles == (0, 0):
            
            if fill == 'y':
                
                layers = int(radius * scale // beam_d)
                print(f'\n Numero de capas para reyenar el circulo: {layers}')
                
                for i in range(layers):
                    draw_circles(g, center, radius, scale)
                    radius -= beam_d
                
            else:
                draw_circles(g, center, radius, scale)
        else:
            draw_arcs(g, center, radius, angles, scale)


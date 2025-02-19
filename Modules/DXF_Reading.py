import ezdxf
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os


def GiveTypes(model, print_e = False):

    entity_types = []

    entity_data = {
    'LINE': None,
    'POLYLINES': None,
    'SPLINES': None,
    'CIRCLE': None,
    'TEXT': None,
    'MTEXT': None,
    'HATCH': None,
    'DIMENSION': None,
    'INSERT': None,
    'LWPOLYLINE': None,
    'ARC': None
    }

    #Create the list
    entities_by_type = defaultdict(list)

    #Classifies the entities
    for entity in model:
        entities_by_type[entity.dxftype()].append(entity)

    #Show the entity types
    if print_e:
        print("\nEntidades agrupadas por tipo:\n")
        for entity_type, entities in entities_by_type.items():
            print(f"{entity_type}: {len(entities)} entidades")
            entity_types.append(entity_type)
    else:
        entity_types = list(entities_by_type.keys())
        


    for types in entity_types:
        if types in entity_data:
            entity_data[types] = model.query(types)


    lines = entity_data['LINE']
    polylines = model.query('POLYLINE')
    lwpolylines = entity_data['LWPOLYLINE']
    splines = entity_data['SPLINES']
    circles = entity_data['CIRCLE']
    texts = entity_data['TEXT']
    mtexts = entity_data['MTEXT']
    hatchs = entity_data['HATCH']
    dimentions = entity_data['DIMENSION']
    inserts = entity_data['INSERT']
    arcs = entity_data['ARC']
        
    
    return lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs

def LinePath(lines, resolution):
    paths =[]
    for line in lines:
        start = np.array(line.dxf.start)
        end = np.array(line.dxf.end)
        path = np.linspace(start, end, resolution)
        paths.append(path)
    return paths

def CirclePath(circles, resolution):
    paths = []
    centers = []
    radii = []
    angles = []
    theta = np.linspace(0, 2 * np.pi, resolution)
    for circle in circles:
        center = np.array(circle.dxf.center)
        radius = np.array(circle.dxf.radius)
        #print(f'\n SOLO HAY {len(circles)}, ESTE ES EL {circle} CON COORDENADAS {center} Y RADIO {radius}')
        
        

        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        coordinates = np.stack((x, y, z), axis=-1)
        paths.append(coordinates)
        radii.append(round(radius.tolist(),5))
        centers.append(center.tolist())
        angles.append((0, 0))
    return paths, centers, radii, angles

def PolyPath (polylines):
    paths = []
    for polyline in range(len(polylines)):
        coords = np.array([(v.dxf.location.x, v.dxf.location.y, v.dxf.location.z) for v in polylines[polyline].vertices])
        paths.append(coords)
    return paths

def LwPolyPath (lwpolylines):
    paths = []
    for polyline in range(len(lwpolylines)):
        coords = np.array([(point[0], point[1], point[2]) for point in lwpolylines[polyline]])
        paths.append(coords)
    
    return paths

def ArcPath(arcs, resolution):
    paths = []
    angles = []
    centers = []
    radii = []

    for arc in arcs:

        if arc.dxf.end_angle < arc.dxf.start_angle:
            arc.dxf.end_angle += 360  

        start_angle = arc.dxf.start_angle
        end_angle = arc.dxf.end_angle
        theta = np.linspace(start_angle*(np.pi/180), end_angle*(np.pi/180), resolution)
    
        
        center = np.array(arc.dxf.center)
        radius = np.array(arc.dxf.radius)
        

        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        z = np.full_like(x, center[2])
        coordinates = np.stack((x, y, z), axis=-1)
        paths.append(coordinates)
        radii.append(round(radius.tolist(),5))
        centers.append(center.tolist())
        angles.append((start_angle, end_angle))

    return paths, centers, radii, angles

def AllPathSelect(lines, polylines, lwpolylines, splines, circles, texts, mtexts, hatchs, dimentions, inserts, arcs, circle_n, simu = False):
    allpaths = []
    centers = []
    radii = []
    angles = []

    if arcs is not None:
        arcpaths, arc_centers, arc_radii, arc_angles = ArcPath(arcs, circle_n)
        allpaths.extend(arcpaths) if simu else None
        centers.extend(arc_centers)
        radii.extend(arc_radii)
        angles.extend(arc_angles)

    if lines is not None:
        linepaths = LinePath(lines, 2)
        allpaths.extend(linepaths)

    if circles is not None:
        circlepaths, circle_centers, circle_radii, circle_angles = CirclePath(circles, circle_n)
        allpaths.extend(circlepaths) if simu else None
        centers.extend(circle_centers)
        radii.extend(circle_radii)
        angles.extend(circle_angles)

    if polylines is not None:
        polypaths = PolyPath(polylines)
        allpaths.extend(polypaths)

    if lwpolylines is not None:
        lwpolypaths = LwPolyPath(lwpolylines)
        allpaths.extend(lwpolypaths)

    curvepaths = list(zip(centers, radii, angles))
    return allpaths, curvepaths

def DXF(name = False):
    #global doc
    # Initialize tk
    root = tk.Tk()
    root.withdraw()  # Hide window
    
    # Open File explorer
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un archivo DXF",
        filetypes=[("Archivos DXF", "*.dxf"), ("Todos los archivos", "*.*")]
    )
    
    if ruta_archivo:
        try:
            # Read DXF
            doc = ezdxf.readfile(ruta_archivo)
            print(f"Archivo DXF cargado con éxito: {ruta_archivo}")

            if name:
                file_name = os.path.basename(ruta_archivo)
                return doc, file_name
            else:
                return doc
        
        except Exception as e:
            print(f"Error al leer el archivo DXF: {e}")
            doc = None
    else:
        print("No se selecciono ningun archivo.")
        doc = None


#----------------------------------------------------------------------------------------------------PLOT--------------------------------------------------------------------


def Plot_Animation(allpaths, lim):

    radio = 0.8

    # Crear figura y eje 2D
    fig, ax = plt.subplots()
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal')
    ax.grid()

    # Primer punto de la primera trayectoria (se ignora z)
    x0, y0, _ = allpaths[0][0]
    circle_plot, = ax.plot([], [], color='blue')

    # Líneas de todas las trayectorias
    linea_plots = [ax.plot([], [], color='red', linewidth=2)[0] for _ in allpaths]

    def generar_circulo(center, radius, num_points=50):
        # Genera un círculo en 2D en torno a center (solo x e y)
        theta = np.linspace(0, 2 * np.pi, num_points)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        return x, y

    def actualizar(frame):
        # Determinar en qué tramo estamos
        total_puntos = sum(len(t) for t in allpaths)
        punto_actual = frame % total_puntos
        segmento_actual = 0
        while punto_actual >= len(allpaths[segmento_actual]):
            punto_actual -= len(allpaths[segmento_actual])
            segmento_actual += 1

        # Actualizar el círculo en la posición actual (solo x, y)
        pos = allpaths[segmento_actual][punto_actual]
        x_circ, y_circ = generar_circulo(pos, radio)
        circle_plot.set_data(x_circ, y_circ)

        # Actualizar las líneas de cada trayectoria
        for i, linea_plot in enumerate(linea_plots):
            if i < segmento_actual:
                # Si ya pasó este segmento, mostramos toda la trayectoria
                puntos = np.vstack(allpaths[i])
                linea_plot.set_data(puntos[:, 0], puntos[:, 1])
            elif i == segmento_actual:
                # Si es el segmento actual, mostramos hasta el punto_actual
                puntos = np.vstack(allpaths[i][:punto_actual+1])
                linea_plot.set_data(puntos[:, 0], puntos[:, 1])
            else:
                # Segmentos futuros se dejan vacíos
                linea_plot.set_data([], [])
                
        return [circle_plot] + linea_plots

    def reiniciar_animacion():
        for linea_plot in linea_plots:
            linea_plot.set_data([], [])
        return [circle_plot] + linea_plots

    frames_totales = sum(len(t) for t in allpaths)
    return fig, frames_totales, actualizar, reiniciar_animacion
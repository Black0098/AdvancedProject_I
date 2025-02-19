import tkinter as tk 
from tkinter import filedialog
import ezdxf
#from Modules.dxf_functions import *
from Modules import *
doc = None


def DXF():
    global doc  
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
            print(f"Archivo DXF cargado con exito: {ruta_archivo}")
            print(doc)
        except Exception as e:
            print(f"Error al leer el archivo DXF: {e}")
            doc = None
    else:
        print("No se selecciono ningun archivo.")
        doc = None


app = tk.Tk()


app.geometry("500x500")                                                         #Set the window size
tk.Wm.wm_title(app, "Control Panel ")                                           #Set the window title
menu_bar = tk.Menu(app)
app.config(menu = menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)                                        #Set the menu
menu_bar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Abrir DXF", command=DXF)
   

                                  
app.mainloop()



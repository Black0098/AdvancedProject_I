import numpy as np
import matplotlib.pyplot as plt


valor = 1  # Valor inicial para entrar en el bucle
while valor != 0:
    try:

        valor = float(input("Digite o valor em mm (0 para sair): "))  # Convertir a float
        if valor != 0:  # Evitar realizar cálculos si el valor es 0
            trans = round(valor / 3e-5)
            print(f"\nLa Maquina Recive {trans}")
    except ValueError:
        print("Por favor, insira um número válido.")




import numpy as np
import matplotlib.pyplot as plt

'''
# Parámetros
accel = 10000   # Aceleración (unidades/s^2)
desacel = 10000   # Desaceleración (unidades/s^2)
vel = 200  # Velocidad máxima (unidades/s)
posicion = 1  # Posición final (en mm)
cuentas = round(posicion/3e-5)  # Conversión de mm a unidades




ac = 256000
dc = 256000
t = np.sqrt(2 * cuentas / ac)


# Cálculos de tiempos
t_total = np.sqrt(2 * cuentas / accel)  # Tiempo total de aceleración + desaceleración
t_accel = vel / accel  # Tiempo de aceleración
t_desacel = vel / desacel  # Tiempo de desaceleración
t_constante = t_total - t_accel - t_desacel  # Tiempo a velocidad constante

print(f" \nLa máquina recibe {cuentas} cuentas. \n Se desplazará {posicion} mm \n se demmorara {t_total} segundos\n") 

# Perfiles de tiempo para cada fase
t_acc = np.linspace(0, t_accel, 100)  # Tiempo de aceleración
t_const = np.linspace(t_accel, t_accel + t_constante, 100)  # Tiempo a velocidad constante
t_dcc = np.linspace(t_accel + t_constante, t_total, 100)  # Tiempo de desaceleración

# Perfiles de velocidad para cada fase
v_acc = accel * t_acc  # Velocidad en la fase de aceleración
v_const = np.full_like(t_const, vel)  # Velocidad constante
v_dcc = vel - desacel * (t_dcc - (t_accel + t_constante))  # Velocidad en la fase de desaceleración

# Unir los perfiles
t_total_profile = np.concatenate([t_acc, t_const, t_dcc])
v_total_profile = np.concatenate([v_acc, v_const, v_dcc])

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(t_total_profile, v_total_profile, label="Perfil de Velocidad")
plt.axvline(t_accel, color="gray", linestyle="--", label="Fin de Aceleración")
plt.axvline(t_accel + t_constante, color="black", linestyle="--", label="Inicio de Desaceleración")
plt.title("Perfil de Velocidad en Función del Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad (unidades/s)")
plt.legend()
plt.grid()
plt.show()
'''
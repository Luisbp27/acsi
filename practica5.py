import csv
import matplotlib.pyplot as plt

# Leemos el fichero con los datos
with open("data.txt", "r") as f:
    csv_reader = list(csv.reader(f, delimiter=" "))

# Eliminamos la cabecera de las columnas
csv_reader.pop(0)

# Declaramos la razón de visita y el tiempo de servicio
V = []
S = []

# Almacenamos los datos del fichero en los arrays correspondientes
for i in range(len(csv_reader)):
    V.append(float(csv_reader[i][0]))
    S.append(float(csv_reader[i][1]))

dispositivos = len(V)

# Array bidimensional que contendra los resultados obtenidos
resultados_sistema = []
resultados_dispositivos = []

# Almacenamos el input del usuario
N = int(input("Introduce el número de trabajos: "))
Z = int(input("Introduce el tiempo de reflexión: "))


def __main__(): 
    """ Algoritmo para el análisis del valor medio para redes de colas cerradas"""

    # Para todos los trabajos
    for n in range(1, N + 1):
        print(f"----- Job {n} -----")

        # Calculamos el tiempo de respuesta y la productividad del sistema
        R = formatear(calcularR(n))
        X = formatear(calcularX(n))

        resultados_sistema.append([n, R, X])

        # Para todos los dispositivos
        for i in range(dispositivos):
            Ri = formatear(calcularRi(n, i))
            Xi = formatear(calcularXi(n, i))
            Ni = formatear(calcularNi(n, i))
            Ui = formatear(calcularUi(n, i))

            resultados_dispositivos.append([i, Ri, Xi, Ni, Ui])

    # Almacenamos los resultados dels sistema en un fichero
    with open("resultados_sistema.txt", "w") as f:
        write = csv.writer(f)

        write.writerows(resultados_sistema)

    # Almacenamos los resultados dels sistema en un fichero
    with open("resultados_dispositivos.txt", "w") as f:
        write = csv.writer(f)

        write.writerows(resultados_dispositivos)

    # Almacenamos los valores del eje x para todas las graficas
    j = 0
    eje_x = [fila[j] for fila in resultados_sistema]

    # Almacenamos las cabeceras de los valores del eje y
    cabeceras = [
        "Tiempo de respuesta (s)", 
        "Productividad (trabajos/s)"]
        
    cabeceras_i = [ 
        "Tiempo de respuesta (s)",
        "Productividad (trabajos/s)",
        "Trabajos en la estación",
        "Utilización (%)"]

    # Graficamos los resultados del sistema
    for i in range(len(cabeceras)):
        plt.figure()

        # Obtenemos los valores del eje y
        eje_y = [fila[i + 1] for fila in resultados_sistema]

        # Graficamos los resultados
        plt.plot(eje_x, eje_y, marker = 'o', markersize = 3)

        # Añadimos las etiquetas
        plt.xlabel("Trabajos")
        plt.ylabel(f"{cabeceras[i]}")
        plt.title(f"{cabeceras[i]} del sistema")
        plt.savefig(f"grafica_sistema_{i}.png")

    # Graficamos los resultados de los dispositivos
    for i in range(len(cabeceras_i)):
        plt.figure()
        
        # Obtenemos los valores del eje y de cada dispositivo
        for j in range(dispositivos):
            eje_y = [fila[i + 1] for fila in resultados_dispositivos if fila[0] == j]

            # Graficamos los resultados
            plt.plot(eje_x, eje_y, label=f"Dispositivo {j}", marker = 'o', markersize = 3)

        # Añadimos las etiquetas
        plt.xlabel("Trabajos")
        plt.ylabel(f"{cabeceras_i[i]}")
        plt.title(f"{cabeceras_i[i]} de los dispositivos")
        plt.legend(loc='upper left')
        plt.savefig(f"grafica_{i}.png")

# Función para formatear los resultados
def formatear(x):
    return float(('%.4f' % x).rstrip('0').rstrip('.'))

# Función para calcular el tiempo de respuesta
def calcularR(n):
    return sum(V[i] * calcularRi(n, i) for i in range(dispositivos))

# Función para calcular la productividad del sistema
def calcularX(n):
    return n / (Z + calcularR(n))

# Función para calcular la productividad de un dispositivo
def calcularXi(n, i):
    return calcularX(n) * V[i]

# Función para calcular el número de trabajos de un dispositivo
def calcularNi(n, i):
    return (calcularX(n) * V[i] * calcularRi(n, i) if n != 0 else 0)

# Función para calcular el tiempo de respuesta de un dispositivo
def calcularRi(n, i):
    return (calcularNi(n - 1, i) + 1) * S[i]

# Función para calcular la utilización de un dispositivo
def calcularUi(n, i):
    return calcularX(n) * V[i] * S[i]


if __name__ == '__main__':
    __main__()

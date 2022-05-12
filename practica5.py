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
resultados = []

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

        # Para todos los dispositivos
        for i in range(dispositivos):
            Ri = formatear(calcularRi(n, i))
            Xi = formatear(calcularXi(n, i))
            Ni = formatear(calcularNi(n, i))
            Ui = formatear(calcularUi(n, i))

            if not i % 2 == 0:
                resultados.append([n, R, X, Ri, Xi, Ni, Ui])

    # Almacenamos los resultados en un fichero
    with open("resultados.txt", "w") as f:
        write = csv.writer(f)

        write.writerows(resultados)

    # Almacenamos los valores del eje x para todas las graficas
    j = 0
    eje_x = [fila[j] for fila in resultados]

    # Almacenamos las cabeceras de los valores del eje y
    cabeceras = [
        "Tiempo de respuesta del sistema (s)", 
        "Productividad del sistema (trabajos/s)", 
        "Tiempo de respuesta de los dispositivos (s)",
        "Productividad de los dispositivos (trabajos/s)",
        "Trabajos de los dispositivos",
        "Utilización de los dispositivos (%)"]

    # Graficamos los resultados
    for i in range(len(cabeceras)):
        plt.figure()
        eje_y = [fila[i] for fila in resultados]
        plt.plot(eje_x, eje_y)
        plt.xlabel("Trabajos")
        plt.ylabel(f"{cabeceras[i]}")
        plt.title(f"{cabeceras[i]} frente a los Trabajos")
        plt.savefig(f"{cabeceras[i]}.png")

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

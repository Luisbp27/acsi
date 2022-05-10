import csv
from importlib.machinery import FrozenImporter

def __main__():
    # Ri(N) = [Ni(N-1)+1] x Si
    # (N-1) es el número de trabajos

    with open ("data.txt", "r") as f:
        csv_reader = list(csv.reader(f, delimiter=" "))

    csv_reader.pop(0)
    Vi = []
    Si = []
    Ri = []
    R = []
    X = []
    N = []

    for i in range(len(csv_reader)):
        Vi.append(int(csv_reader[i][0]))
        Si.append(int(csv_reader[i][1]))

    dispositivos = len(Vi)
    N = input("Introduce el número de trabajos: ")
    Z = input("Introduce el tiempo de reflexión: ")

    for n in range(1, N):
        for i in range(dispositivos):
            Ri.append(calcularRi(N, csv_reader[i][1]))   

        R.append(calcularR(n, Ri, Vi))
        X.append(calcularX(n, Z, Vi, R[n]))

        for i in range(dispositivos):
            N.append(X[n], Vi[i], Si[i])

    print(R)
    # Imprimir id + ri + r + x + ni
    # Imprimir r y x como los datos más importantes

def calcularR(n, Ri, Vi): 
    if n != 0:
        return Ri[n - 1] + (Vi[n] * Ri[n])
    else:
        return Vi[n] * Ri[n]

def calcularX(n, Z, R):
    return n / (Z * R)

def calcularNi(X, Vi, Si):
    return X * Vi * Si

def calcularRi(N, Si):
    return (N * (N - 1) + 1) * Si

def calcularUi():
    pass

if __name__ == '__main__':
    __main__()
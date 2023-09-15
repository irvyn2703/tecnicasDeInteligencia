# Bibliotecas usadas
import numpy as np
import matplotlib.pyplot as plt

# Funcion que asigna valores aleatorios a los pesos y el bias
def setWb():
    global W, b
    # Inicialiazcion aleatoria de Pesos
    W = np.random.uniform(size=7)  # Numero de Pesos
    # Inicializacion aleatoria de bias
    b = np.random.uniform()

# Función con el algoritmo perceptrón
def train_and_track_error(patrones, s, W, b, numEpoc):
    a = np.zeros(10)  # Arreglo con las predicciones
    error = np.zeros(10)  # Arreglo con los errores
    errors = []  # Lista para almacenar los errores de cada época
    
    for epoca in range(numEpoc):  # Ciclo que itera según el número de épocas
        error_epoca = 0
        for q in range(len(patrones)):  # Ciclo que itera según el número de patrones
            a[q] = np.heaviside(np.dot(patrones[q], W) + b, 0)  # Cálculo de la predicción esperada del patrón i-ésimo
            error[q] = s[q] - a[q]  # Cálculo del error en la predicción i-ésima

            W += patrones[q] * error[q]  # Cálculo de los nuevos pesos
            b += error[q]  # Cálculo del nuevo bias
            
            error_epoca += np.abs(error[q])
        
        errors.append(error_epoca)
        
        if epoca % 30 == 0:
            print(f"Época {epoca}: Error total = {error_epoca}")
        
        if error_epoca == 0:
            break
    
    return errors

# Patrones de prueba
patrones = np.array([[1, 1, 1, 1, 1, 1, 0],  # 0
                     [0, 1, 1, 0, 0, 0, 0],  # 1
                     [1, 1, 0, 1, 1, 0, 1],  # 2
                     [1, 1, 1, 1, 0, 0, 1],  # 3
                     [0, 1, 1, 0, 0, 1, 1],  # 4
                     [1, 0, 1, 1, 0, 1, 1],  # 5
                     [1, 0, 1, 1, 1, 1, 1],  # 6
                     [1, 1, 1, 0, 0, 0, 0],  # 7
                     [1, 1, 1, 1, 1, 1, 1],  # 8
                     [1, 1, 1, 1, 0, 1, 1]])  # 9

# Salidas reales
np2 = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
s1 = np.array(np2)  # números pares

n5 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
s2 = np.array(n5)  # números < 5

npr = [0, 0, 1, 1, 0, 1, 0, 1, 0, 0]
s3 = np.array(npr)  # números primos

# Inicialiazción de Pesos
W = 0

# Inicialización de bias
b = 0

# Número de épocas
numEpoc = 150

errors1 = []
errors2 = []
errors3 = []

while True:
    print("Algoritmo perceptrón")
    print("Considerando que los números desde 0 a 9 están representados mediante el código de 7 segmentos de un "
          "display, entrene una neurona perceptrón para que reconozca...")
    print("1) Números pares")
    print("2) Números mayores a 5")
    print("3) Números primos")
    print("4) Salir")
    op = input("Elige una opción: ")

    if op == "1":
        print("Has elegido la Opción 1.")
        setWb()
        errors1 = train_and_track_error(patrones, s1, W, b, numEpoc)
    elif op == "2":
        print("Has elegido la Opción 2.")
        setWb()
        errors2 = train_and_track_error(patrones, s2, W, b, numEpoc)
    elif op == "3":
        print("Has elegido la Opción 3.")
        setWb()
        errors3 = train_and_track_error(patrones, s3, W, b, numEpoc)
    elif op == "4":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Por favor, elige una opción válida.")

# Gráfica de los errores a lo largo de las épocas
plt.plot(range(len(errors1)), errors1, label="Opción 1")
plt.plot(range(len(errors2)), errors2, label="Opción 2")
plt.plot(range(len(errors3)), errors3, label="Opción 3")
print(errors1)
print(errors2)
print(errors3)
plt.xlabel('Épocas')
plt.ylabel('Error total')
plt.legend()
plt.show()
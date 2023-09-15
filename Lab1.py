# Librerias usadas
import numpy as np
import random

# Funcion con el algoritmo perceptron
def perceptron(patrones, clases, W, b, numEpoc):
    a = np.zeros((8, 2))  # Arreglo con las predicciones
    error = np.zeros((8, 2))  # Arreglo con los errores
    for epoca in range(numEpoc):  # Ciclo que itera segun el numero de epocas
        for q in range(len(patrones)):  # Ciclo que itera segun el numero de patrones
            a[q] = np.heaviside(np.dot(patrones[q], W) + b, 0)  # Calulo de la prediccion esperada del patron i-esimo
            error[q] = clases[q] - a[q]  # Calculo del error en la predicción i-esima

            W += np.outer(patrones[q], error[q])  # Calculo de los nuevos pesos
            b += error[q]  # Calculo del nuevo bias

    # Clasificación final
    afinal = np.dot(patrones, W) + b
    salida_final = np.heaviside(afinal, 0)

    # Se muestran resultados en consola
    print("Patrones de entrada:\n", patrones)
    print("Clases reales:\n", clases)
    print("Clases predichas:\n", salida_final)

    # Graficacion


# Patrones de prueba
patrones = np.array([[0.7, 3], [1.5, 5],
                     [2.0, 9], [0.9, 11],
                     [4.2, 0], [2.2, 1],
                     [3.6, 7], [4.5, 6]])

# Clases reales
clases = np.array([[0, 0], [0, 0],
                   [0, 1], [0, 1],
                   [1, 0], [1, 0],
                   [1, 1], [1, 1]])

# Inicialiazcion aleatoria de Pesos
W = np.random.uniform(size=(2, 2)) # Numero de Pesos

# Inicializacion aletoria de bias
b = np.random.uniform(size=(1, 2))

# Numero de epocas
numEpoc = 50

# Se llama a la funcion perceptron
perceptron(patrones, clases, W, b, numEpoc)

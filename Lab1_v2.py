# Librerias usadas
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Función de activación (escalón unitario)
def activacion(x):
    return np.heaviside(x, 0)


def perceptron(patrones, clases, W, b, numEpoc):
    for epoch in range(numEpoc):
        print(epoch)
        # Calculo de las predicciones
        a = activacion(np.dot(patrones, W) + b)

        # Cálculo del error
        error = clases - a
        if(epoch % 5 == 0):
            print(error)

        # Actualización de pesos y bias
        W += np.dot(patrones.T, error)
        b += np.sum(error, axis=0, keepdims=True)

    # Clasificación final
    afinal = np.dot(patrones, W) + b
    salida_final = activacion(afinal)

    #print("Patrones de entrada:\n", patrones)
    #print("Clases reales:\n", clases)
    #print("Clases predichas:\n", salida_final)

    # Graficación de las líneas de decisión y los patrones de entrada
    plt.figure(figsize=(8, 6))

    # Graficar patrones de entrada
    for i, clase in enumerate(clases):
        if clase[0] == 0 and clase[1] == 0:  # Clase[0,0]
            plt.scatter(patrones[i, 0], patrones[i, 1], color='red', marker='o')  # Grafica patrones de clase [0,0]
        elif clase[0] == 0 and clase[1] == 1:  # Clase[0,1]
            plt.scatter(patrones[i, 0], patrones[i, 1], color='blue', marker='x')  # Grafica patrones de clase [0,1]
        elif clase[0] == 1 and clase[1] == 0:  # Clase[1,0]
            plt.scatter(patrones[i, 0], patrones[i, 1], color='green', marker='s')  # Grafica patrones de clase [1,0]
        elif clase[0] == 1 and clase[1] == 1:  # Clase[1,1]
            plt.scatter(patrones[i, 0], patrones[i, 1], color='purple', marker='^')  # Grafica patrones de clase [1,1]

    # Graficar líneas de decisión
    x_vals = np.linspace(-1, 5, 100)  # Crea arreglo de 100 valores equidistantes en el rango de -1 a 5
    for i in range(2):  # Dos iteraciones, una por cada linea de decision
        y_vals = -(W[0, i] * x_vals + b[0, i]) / W[1, i]  # Calculo de la linea de decision
        plt.plot(x_vals, y_vals, label=f'Línea de Decisión {i + 1}')  # Graficacion de la linea de decision

    plt.xlabel('Peso')
    plt.ylabel('Frecuencia de uso')
    plt.title('Líneas de Decisión y Patrones de Entrada')
    plt.legend()
    plt.grid()
    plt.show()


# Patrones
patrones = np.array([[0.7, 3, 1], [1.5, 5, 1], [2.0, 9, 1], [0.9, 11, 1], [4.2, 0, 1], [2.2, 1, 1], [3.6, 7, 1], [4.5, 6, 1]])

# Clases reales
clases = np.array([[0, 0], [0, 0], [0, 1], [0, 1], [1, 0], [1, 0], [1, 1], [1, 1]])

# Inicialiazcion aleatoria de Pesos
W = np.random.uniform(size=(2, 2))

# Inicializacion aletoria de bias
b = np.random.uniform(size=(1, 2))

# Epocas de entrenamiento
numEpoc = 71

# Se llama a la funcion perceptron
perceptron(patrones, clases, W, b, numEpoc)

# Obtención de la salida final
afinal = np.dot(patrones, W) + b
salida_final = activacion(afinal)

# Obtención de resultados estadísticos
clases_predichas = np.round(salida_final).astype(int)
precision = np.sum(clases == clases_predichas) / len(clases) * 100

# Creación de la tabla de resultados
data = {
    'Patrón': list(range(1, len(patrones) + 1)),
    'Clase Real': [f'{c[0]}, {c[1]}' for c in clases],
    'Clase Predicha': [f'{c[0]}, {c[1]}' for c in clases_predichas]
}
tabla_resultados = pd.DataFrame(data)

# Impresión de resultados estadísticos
print(f"Precision del modelo: {precision:.2f}%")

# Impresión de la tabla de resultados
print("\nTabla de Resultados:")
print(tabla_resultados)

# Gráfico de barras para comparar clases reales y predichas
plt.figure(figsize=(8, 6))
clases_bar = np.arange(len(clases))
plt.bar(clases_bar - 0.15, clases[:, 0], width=0.3, align='center', label='Real - Clase 1')
plt.bar(clases_bar + 0.15, clases[:, 1], width=0.3, align='center', label='Real - Clase 2')
plt.bar(clases_bar - 0.15, clases_predichas[:, 0], width=0.3, align='edge', label='Predicho - Clase 1', alpha=0.5)
plt.bar(clases_bar + 0.15, clases_predichas[:, 1], width=0.3, align='edge', label='Predicho - Clase 2', alpha=0.5)
plt.xlabel('Patrón')
plt.ylabel('Clase')
plt.title('Comparación entre Clases Reales y Predichas')
plt.xticks(clases_bar, [f'Patrón {i+1}' for i in clases_bar])
plt.legend()
plt.tight_layout()
plt.show()
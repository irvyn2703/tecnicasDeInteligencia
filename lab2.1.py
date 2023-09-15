"""
p1--w00---NEURONA0------  0  0  1  1
  W01  W10    B0
P2--w11---NEURONA1------  0  1  0  1
              B1
"""

# Librerias usadas
import numpy as np
import matplotlib.pyplot as plt


# Función de activación (escalón unitario)
def activacion(x):
    if (x > 0):
        return 1
    else:
        return 0


def perceptron(patrones, clases, w, b, numEpoc):
    # visualizamos w y b
    #print("w =", w)
    #print("b =", b)
    for epoch in range(numEpoc):
        # visualizamos el numero de epocas
        #print("epoca", epoch)
        for i in range(len(patrones)):
            # visualizamos el patron
            #print("patrones =", patrones[i])

            # Calculo de las predicciones por neurona
            pred0 = activacion((np.dot(patrones[i], w[0]) + b[0]))
            pred1 = activacion((np.dot(patrones[i], w[1]) + b[1]))

            # visualizamos las prediciones
            #print("pred0 =", pred0)
            #print("pred1 =", pred1)

            # Cálculo del error en cada neurona
            error0 = clases[i][0] - pred0
            error1 = clases[i][1] - pred1

            # visualizamos el error
            #print("esperamos =" + str(clases[i][0]) + str(clases[i][1]))
            #print("obtuvimos =" + str(pred0) + str(pred1))
            #print("error = " + str(error0) + str(error1))

            # Actualización de pesos
            w[0][0] = w[0][0] + (error0 * patrones[i][0])
            w[0][1] = w[0][1] + (error0 * patrones[i][1])
            w[1][0] = w[1][0] + (error1 * patrones[i][0])
            w[1][1] = w[1][1] + (error1 * patrones[i][1])

            # Actualización de pesos
            b[0] = b[0] + error0
            b[1] = b[1] + error1

            # visualizamos los nuevos pesos y bias
            #print("nuevo w = ", w)
            #print("nuevo b = ", b)

    # visualizamos los ultimos pesos y bias
    print("w = ", w)
    print("b = ", b)

    # graficamos
    plt.figure()
    # obtenemos las posiciones de nuestros patrones y las separamos segun su clasificacion
    for i in range(len(patrones)):
        if clases[i][0] == 0:
            if clases[i][1] == 0:
                # circulos verdes para la clase 00
                plt.plot(patrones[i][0], patrones[i][1], 'go',label='clase 00')
            else:
                # circulos rojos para la clase 01
                plt.plot(patrones[i][0], patrones[i][1], 'ro',label='clase 01')
        else:
            if clases[i][1] == 0:
                # circulos azules para la clase 10
                plt.plot(patrones[i][0], patrones[i][1], 'bo',label='clase 10')
            else:
                # circulos morados para la clase 10
                plt.plot(patrones[i][0], patrones[i][1], 'mo',label='clase 11')

    # creamos las fronteras de decision 
    # tamaño en el eje x de nuestras fronteras
    x = np.arange(0, 6, 1)
    # para crear la recta si w[0] * x + w[1] * y + b = 0 simplemente despejamos y en terminos de x
    # (w[0] * x) + (w[1] * y) + b = 0
    # (w[0] * x) + (w[1] * y) = -b
    # (w[0] * x)/w[1] + (w[1] * y)/w[1] = -b/w[1]
    # y = (-b/w[1]) - (w[0]/w[1]) * x
    plt.plot(x, ((-b[0] / w[0,1]) - (w[0,0] / w[0,1]) * x).flatten(),'c-')
    plt.plot(x, ((-b[1] / w[1,1]) - (w[1,0] / w[1,1]) * x).flatten(),'k-')

    plt.xlabel('Eje x')
    plt.ylabel('Eje y') 
    plt.title('Perceptron resultado')
    #plt.legend()
    plt.grid(True)
    plt.show()

# Patrones
patrones = np.array([[0.7, 3], [1.5, 5], [2.0, 9], [0.9, 11], [4.2, 0], [2.2, 1], [3.6, 7], [4.5, 6]])

# Clases reales de cada patron
clases = np.array([[0, 0], [0, 0], [0, 1], [0, 1], [1, 0], [1, 0], [1, 1], [1, 1]])

# Inicialiazcion aleatoria de Pesos
w = np.random.uniform(size=(2, 2))

# Inicializacion aletoria de bias
b = np.random.uniform(size=(2))

# Epocas de entrenamiento
numEpoc = 100

# Se llama a la funcion perceptron
perceptron(patrones, clases, w, b, numEpoc)
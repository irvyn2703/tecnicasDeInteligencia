# Librerias usadas
import numpy as np
import matplotlib.pyplot as plt

# Función de activación (escalón unitario)
def activacion(x):
    if x > 0:
        return 1
    else:
        return -1

def adaline(patrones, clases):
    R = np.zeros((patrones.shape[1], patrones.shape[1]))
    Q = len(patrones) # numero de patrones
    h1 = np.zeros(patrones.shape[1]) # el numero de h depende al numero de neuronas
    h2 = np.zeros(patrones.shape[1])

    for i in range(Q):
        R += np.outer(patrones[i], patrones[i]) # sumamos la multiplicacion de patron[i] por la transpuesta
    R = (1/Q) * R
    # print("Matriz R:\n " + str(R) + "\n")

    for i in range(Q):
        h1 += clases[i][0] * patrones[i] # es la suma de la clase real por el patron
    h1 = (1/Q) * h1 
    # print("h1:" + str(h1) + "\n")

    for i in range(Q):
        h2 += clases[i][1] * patrones[i]
    h2 = (1/Q) * h2    
    # print("h2:" + str(h2) + "\n")

    inversa = np.linalg.inv(R) # obtenemos la inversa
    # print("inversa:\n " + str(inversa) + "\n")

    x1 = np.dot(inversa, h1) # multiplicamos la inversa por h1 Xm = R^(-1)H
    print("x1:\n " + str(x1))

    x2 = np.dot(inversa, h2)
    print("x2:\n " + str(x2))

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
    plt.plot(x, ((-x1[2] / x1[1]) - (x1[0] / x1[1]) * x).flatten(),'c-')
    plt.plot(x, ((-x2[2] / x2[1]) - (x2[0] / x2[1]) * x).flatten(),'k-')

    plt.xlabel('Eje x')
    plt.ylabel('Eje y') 
    plt.title('Perceptron resultado')
    #plt.legend()
    plt.grid(True)
    plt.show()


# Patrones
patrones = np.array([[0.7, 3, 1], [1.5, 5, 1], [2.0, 9, 1], [0.9, 11, 1], [4.2, 0, 1], [2.2, 1, 1], [3.6, 7, 1], [4.5, 6, 1]])

# Clases reales de cada patron
clases = np.array([[-1, -1], [-1, -1], [-1, 1], [-1, 1], [1, -1], [1, -1], [1, 1], [1, 1]])

# Se llama a la funcion adaline
adaline(patrones, clases)

import pprint
import math
import numpy as np


def leer_datos():
    # Leer datos de aristas
    with open('aristas.txt', 'r') as file:
        aristas_data = [line.split(',') for line in file.readlines()]

    # Leer datos de vértices
    with open('vertices.txt', 'r') as file:
        vertices_data = [line.split(',') for line in file.readlines()]

    return aristas_data, vertices_data

def estacionesPosibles(x, y):
    posiblesEstaciones_set = set()

    for item in aristas:
        if (float(item[0]) <= x + margen) and (float(item[0]) >= x - margen):   
            if (float(item[1]) <= y + margen) and (float(item[1]) >= y - margen):
                tempx = float(item[2])
                tempy = float(item[3])
                distancia = float(item[4])
                tiempo = float(item[5])
                estacion = buscarEstacion(float(item[2]), float(item[3]))
                # Convertir datos a tupla y agregar al conjunto
                posiblesEstaciones_set.add((tempx, tempy, distancia, tiempo, estacion))

        if (float(item[2]) <= x + margen) and (float(item[2]) >= x - margen):   
            if (float(item[3]) <= y + margen) and (float(item[3]) >= y - margen):
                tempx = float(item[0])
                tempy = float(item[1])
                distancia = float(item[4])
                tiempo = float(item[5])
                estacion = buscarEstacion(float(item[0]), float(item[1]))
                # Convertir datos a tupla y agregar al conjunto
                posiblesEstaciones_set.add((tempx, tempy, distancia, tiempo, estacion))

    # Convertir conjunto a lista
    posiblesEstaciones = list(posiblesEstaciones_set)

    return posiblesEstaciones

def cambiarEstacion(x,y,estacionesPosibles):
    nuevoX = x
    nuevoY = y
    minimo = funcion_objetivo(x,y,estacionesPosibles[0],estacionesPosibles[0])
    f
    return nuevoX,nuevoY

def buscarEstacion(x,y):
    respuesta = None
    for item in vertices:
        if (float(item[0]) <= x + margen) and (float(item[0]) >= x - margen) :   
            if  (float(item[1]) <= y + margen) and (float(item[1]) >= y - margen):
                respuesta = item[2]
    return respuesta
    
def funcion_objetivo(x1,y1,x2,y2):
    # formula para conse4guir la longitud de una recta que conecta 2 puntos
    distancia = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distancia

# Función actualiza posicion 
def calcular_posiciones(lobos, lobo_alfa, lobo_beta, lobo_delta, dimension, iteracion, iteraciones, aptitud, func_objetivo):
    for i in range(len(lobos)): #ciclo para recorrer cada lobo de la manada
        #calculo del valor de A (formula de diapositivas)
        a = 2 * (iteracion / iteraciones) - 1
        A = 2 * a * np.random.rand(dimension) - a
        
        #calculo de C (formula de diapositivas)
        C = 2 * np.random.rand(dimension)
        
        #calculo de D (formula de diapositivas)
        D_alfa = np.abs(C * lobo_alfa - lobos[i])
        D_beta = np.abs(C * lobo_beta - lobos[i])
        D_delta = np.abs(C * lobo_delta - lobos[i])
        
        #calculo de posicion (formula de diapositivas)
        X_alfa = lobo_alfa - A * D_alfa
        X_beta = lobo_beta - A * D_beta
        X_delta = lobo_delta - A * D_delta

        #Calculo de posicion final (formula de diapositivas)
        aux = (X_alfa + X_beta + X_delta) / 3
        #print("posicion nueva 1:\n", aux)  # Imprimir la posicion nueva

        #aptitud nueva (FITNESS)
        apt = func_objetivo(aux[0], aux[1])
        #print("apt nueva:\n", apt)  # Imprimir la aptitud nueva

        #compamos las aptitudes para actualizar la posicion
        if apt < aptitud[i]:
            lobos[i] = aux #Actualizamos la posicion en la matriz
            aptitud[i] = apt #actualizamos la aptitud
            #print("aux:\n", aux)  # Imprimir la posicion nueva
            
    return lobos

# Implementación del algoritmo del Lobo Gris
def optimizador_lobo_gris(func_objetivo, dimension, tamano_poblacion, iteraciones, apt_obj):
    lobos = np.random.uniform(10, 753, (tamano_poblacion, dimension)) #Generación de la manada aleatoriamente (tam_poblacion filas, dimension columnas)***************************************************************
    estacionActual = []  # Lista para almacenar las coordenadas de la estación actual
    estacionesRecorridas = []  # Lista para almacenar las estaciones recorridas en cada iteración

    for i in range(tamano_poblacion):
        estacionActual.append((estacionA[0], estacionA[1]))  # Corregido para que sea una tupla
        estacionesRecorridas.append([buscarEstacion(estacionA[0], estacionA[1])][0])

    print("Matriz inicial de lobos:\n", lobos)  # Imprimir la matriz inicial de lobos

    global iteraciones_acierto, aciertos # Lista para guardar las iteraciones donde se alcanza la función objetivo
    iteraciones_acierto = []  
    aciertos = 0  # Contador de aciertos
    
    for iteracion in range(iteraciones):
        #calculo de aptitud para cada lobo (generacion de arreglo)
        aptitud = np.array([func_objetivo(lobo[0], lobo[1]) for lobo in lobos])
        #print("Valores de aptitud en la iteración {}:\n".format(iteracion), aptitud)  # Imprimir los valores de aptitud

        # Ordenar los índices de los lobos por aptitud
        indices_ordenados = np.argsort(aptitud)
        #print("Orden:\n", indices_ordenados)  # Imprimir orden de lobos

        # El lobo alfa es el mejor lobo
        indice_alfa = indices_ordenados[0]
        lobo_alfa = lobos[indice_alfa]
        #print("Lobo alfa en la iteración {}:\n".format(iteracion), lobo_alfa)  # Imprimir el lobo alfa

        # El lobo beta es el segundo mejor lobo
        indice_beta = indices_ordenados[1]
        lobo_beta = lobos[indice_beta]
        #print("Lobo beta en la iteración {}:\n".format(iteracion), lobo_beta)  # Imprimir el lobo beta

        # El lobo delta es el tercer mejor lobo
        indice_delta = indices_ordenados[2]
        lobo_delta = lobos[indice_delta]
        #print("Lobo delta en la iteración {}:\n".format(iteracion), lobo_delta)  # Imprimir el lobo delta

        lobos = calcular_posiciones(lobos, lobo_alfa, lobo_beta, lobo_delta, dimension, iteracion, iteraciones, aptitud, func_objetivo)
        print("Matriz inicial de lobos:\n", lobos)  # Imprimir la matriz inicial de la siguiente generacion de lobos

        if min(aptitud) <= apt_obj:  
            iteraciones_acierto.append(iteracion) #guardamos la iteracion 
        
        print("Iteración {}: Mejor valor de aptitud = {}".format(iteracion, min(aptitud)))

    mejor_indice = np.argmin(aptitud) #obtenemos la mejor aptitud
    mejor_lobo = lobos[mejor_indice] #mejor lobo
    mejor_aptitud = aptitud[mejor_indice]

    return mejor_lobo, mejor_aptitud



margen = 5 # las coordenadas de los vertices y las aristas no son iguales tienen un margen de 5 
aristas, vertices = leer_datos() # leemos los archivos

for i in range(len(vertices)):
    print("[ " + str(i+1) + " ] " + vertices[i][2])

# obtenemos los puntos A y B
teclado = int(input("selecciona la estacion de partida:  "))
estacionA = [float(vertices[teclado - 1][0]), float(vertices[teclado - 1][1])]

teclado = int(input("selecciona la estacion de partida:  "))
estacionB = [float(vertices[teclado - 1][0]), float(vertices[teclado - 1][1])]

estacionesRecorridas = []
for i in range(10):
        estacionesRecorridas.append([buscarEstacion(estacionA[0], estacionA[1]),0])


print(estacionesRecorridas[0][0])

#print(buscarEstacion(estacionA[0],estacionA[1]))
#print(buscarEstacion(estacionB[0],estacionB[1]))

#137.0,338.0,Tacubaya, 258.0,329.0,Centro Medico,
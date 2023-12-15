import pprint
import random
import math
import numpy as np
import statistics


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

def cambiarEstacion(x,y,estacionesP,opcion,estaciones):
    # si la opcion es 0 toma la ruta mas sercana al valor x y
    # en caso contrario toma cualquier otra ruta que no a revisado
    if len(estacionesP) > 0:
        nuevoX = estacionesP[0][0]
        nuevoY = estacionesP[0][1]
        minimo = funcion_objetivo(x,y,estacionesP[0][0],estacionesP[0][1])
        # busca la estacion mas cercana a la direccion x y
        iteracionMin = 0
        for i in range(len(estacionesP)):
            # usamos la funcion fitnes pero para obtener la distancia en la que el lobo se quiere mover y las estaciones que estan permitidas
            if minimo > funcion_objetivo(x,y,estacionesP[i][0],estacionesP[i][1]):
                    # obtenemos la estacion con una distancia corta a la eleccion del lobo
                    minimo = funcion_objetivo(x,y,estacionesP[i][0],estacionesP[i][1])
                    iteracionMin = i

        if opcion == 0:
            nuevoX = estacionesP[iteracionMin][0]
            nuevoY = estacionesP[iteracionMin][1]
        else:
            #tomamos cualquier ruta que no seleccionamos
            temp = 0
            #print(estaciones)
            for item in estaciones:
                if temp >= len(estacionesP):
                    if estacionesP[temp][4] != item:
                        nuevoX = estacionesP[temp][0]
                        nuevoY = estacionesP[temp][1]
                    else:
                        temp = temp + 1
    else:
        nuevoX = x
        nuevoY = y

    return nuevoX,nuevoY

def buscarEstacion(x,y):
    #devuelve el nombre de la estacion
    respuesta = None
    for item in vertices:
        if (float(item[0]) <= x + margen) and (float(item[0]) >= x - margen) :   
            if  (float(item[1]) <= y + margen) and (float(item[1]) >= y - margen):
                respuesta = item[2]
    return respuesta
    
def funcion_objetivo(x1,y1,x2,y2):
    # formula para conseguir la longitud de una recta que conecta 2 puntos
    distancia = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distancia

# Función actualiza posicion 
def calcular_posiciones(lobos, lobo_alfa, lobo_beta, lobo_delta, dimension, iteracion, iteraciones, aptitud, func_objetivo, estacionesR, numIntentos, indAlfa, indBeta, indDelta):
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
        # si es el 3 intento consecutivo del lobo de moverse y no lo consige selecciona cualquier otra ruta
        if numIntentos[i] < 3:
            aux[0], aux[1] = cambiarEstacion(aux[0],aux[1],estacionesPosibles(lobos[i][0],lobos[i][1]),0,estacionesR[i])
        else:
            #print("lobo " + str(i) + " cambiando de direccion ")
            aux[0], aux[1] = cambiarEstacion(aux[0],aux[1],estacionesPosibles(lobos[i][0],lobos[i][1]),1,estacionesR[i])

        #aptitud nueva (FITNESS)
        apt = func_objetivo(aux[0], aux[1], estacionB[0], estacionB[1])
        #print("apt nueva:\n", apt)  # Imprimir la aptitud nueva

        #compamos las aptitudes para actualizar la posicion
        # si la aptitud es menor o va 3 intentos sin moverse
        if apt < aptitud[i] or numIntentos[i] > 3:
            nueva_estacion = buscarEstacion(aux[0], aux[1])
            # Verifica si la nueva estación ya está en la lista
            # comprueba que no repita estaciones
            if nueva_estacion not in estacionesR[i]:
                lobos[i] = aux #Actualizamos la posicion en la matriz
                aptitud[i] = apt #actualizamos la aptitud
                # Agrega la nueva estación solo si no está en la lista
                estacionesR[i].append(nueva_estacion)
                numIntentos[i] = 0
        else:
            numIntentos[i] = numIntentos[i] + 1
            
    return lobos

# Implementación del algoritmo del Lobo Gris
def optimizador_lobo_gris(func_objetivo, dimension, tamano_poblacion, iteraciones, apt_obj):
    lobos = np.random.uniform(10, 753, (tamano_poblacion, dimension)) #Generación de la manada aleatoriamente (tam_poblacion filas, dimension columnas)***************************************************************
    estacionesRecorridas = []  # Lista para almacenar las estaciones recorridas en cada iteración
    numIntentos = []
    primerAcierto = False
    mejor_recorrido = []
    mejor_indice = 0 #obtenemos la mejor aptitud
    mejor_lobo = [] #mejor lobo
    mejor_aptitud = 0

    # iniciamos nuestras variables
    for i in range(tamano_poblacion):
        # iniciamos los lobos en el punto A
        estacionesRecorridas.append([buscarEstacion(estacionA[0], estacionA[1])])
        #iniciamos los intentos
        numIntentos.append(0)
        # movemos los lobos de estacion
        lobos[i][0], lobos[i][1] = cambiarEstacion(lobos[i][0],lobos[i][1],estacionesPosibles(estacionA[0],estacionA[1]),0,buscarEstacion(estacionA[0], estacionA[1]))
        # agregamos la nueva estacion
        nueva_estacion = buscarEstacion(lobos[i][0], lobos[i][1])
        estacionesRecorridas[i].append(nueva_estacion)


    #print("Matriz inicial de lobos:\n", lobos)  # Imprimir la matriz inicial de lobos
    
    for iteracion in range(iteraciones):         
        #calculo de aptitud para cada lobo (generacion de arreglo)
        aptitud = np.array([func_objetivo(lobo[0], lobo[1],estacionB[0], estacionB[1]) for lobo in lobos])
        #print("Valores de aptitud en la iteración {}:\n".format(iteracion), aptitud)  # Imprimir los valores de aptitud

        # Ordenar los índices de los lobos por aptitud
        indices_ordenados = np.argsort(aptitud)
        #print("Orden:\n", indices_ordenados)  # Imprimir orden de lobos

        # El lobo alfa es el mejor lobo
        indice_alfa = indices_ordenados[0]
        lobo_alfa = lobos[indice_alfa]
        #print("lobo alfa en la iteracion " + str(iteracion) + ": " + str(lobo_alfa) + " -- " + buscarEstacion(lobo_alfa[0],lobo_alfa[1]))

        # El lobo beta es el segundo mejor lobo
        indice_beta = indices_ordenados[1]
        lobo_beta = lobos[indice_beta]
        # print("lobo beta en la iteracion " + str(iteracion) + ": " + str(lobo_beta) + " -- " + buscarEstacion(lobo_beta[0],lobo_beta[1]))

        # El lobo delta es el tercer mejor lobo
        indice_delta = indices_ordenados[2]
        lobo_delta = lobos[indice_delta]
        # print("lobo delta en la iteracion " + str(iteracion) + ": " + str(lobo_beta) + " -- " + buscarEstacion(lobo_delta[0],lobo_delta[1]))

        lobos = calcular_posiciones(lobos, lobo_alfa, lobo_beta, lobo_delta, dimension, iteracion, iteraciones, aptitud, func_objetivo, estacionesRecorridas, numIntentos, indice_alfa, indice_beta, indice_delta)
        # print("Matriz inicial de lobos:\n", lobos)  # Imprimir la matriz inicial de la siguiente generacion de lobos

        if buscarEstacion(lobo_alfa[0],lobo_alfa[1]) == buscarEstacion(estacionB[0],estacionB[1]):  
            if primerAcierto == False:
                primerAcierto = True
                iteraciones_acierto.append(iteracion) #guardamos la iteracion 
                mejor_indice = np.argmin(aptitud) #obtenemos la mejor aptitud
                mejor_lobo = lobos[mejor_indice]
                mejor_aptitud = aptitud[mejor_indice]
                mejor_recorrido = estacionesRecorridas[mejor_indice]
                print(str(buscarEstacion(estacionA[0],estacionA[1])) + " -- " + str(buscarEstacion(estacionB[0],estacionB[1])))

    return mejor_lobo, mejor_aptitud, mejor_recorrido, primerAcierto


margen = 10 # las coordenadas de los vertices y las aristas no son iguales tienen un margen de 5 
aristas, vertices = leer_datos() # leemos los archivos


for i in range(len(vertices)):
    print("[ " + str(i+1) + " ] " + vertices[i][2])

# obtenemos los puntos A y B
teclado = int(input("selecciona la estacion de partida:  "))
estacionA = [float(vertices[teclado - 1][0]), float(vertices[teclado - 1][1])]

teclado = int(input("selecciona la estacion de partida:  "))
estacionB = [float(vertices[teclado - 1][0]), float(vertices[teclado - 1][1])]

# Parámetros del algoritmo<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< MODIFICAR AQUI <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
dimension = 2  #hay dos variables (x, y)
tamano_poblacion = 50
iteraciones = 50
ejec = 5
apt_obj = 0
iteraciones_acierto = []  
aciertos = 0  # Contador de aciertos

# Ejecutar el algoritmo
for i in range(ejec):
    mejor_solucion, mejor_aptitud, estaciones, acierto = optimizador_lobo_gris(funcion_objetivo, dimension, tamano_poblacion, iteraciones,apt_obj)
    # Verificar si hemos alcanzado la función objetivo
    if acierto == True:  
        aciertos += 1 #aumentamos los aciertos

if len(iteraciones_acierto) > 0:
    promedio_aciertos = (aciertos * 100)/ejec
    promedio_iteraciones = sum(iteraciones_acierto) / len(iteraciones_acierto)
    desviacion_estandar_iteraciones = np.std(iteraciones_acierto)

print("\nMejor solución encontrada:")
print("Lobo (x, y): ", mejor_solucion)
print("Valor de aptitud: ", mejor_aptitud)
print("Estaciones recorridas: ", estaciones)
print("\nParámetros utilizados:")
print("Población:", tamano_poblacion)
print("Iteraciones:", iteraciones)
print("Ejecuciones:", ejec)
print("Aptitud objetivo:", apt_obj)
if len(iteraciones_acierto) > 1:
    print("Estadísticas:")
    print("Promedio de aciertos: {}%".format(promedio_aciertos))
    print("Promedio de iteraciones: {}".format(statistics.mean(iteraciones_acierto)))
    print("Desviación estándar de iteraciones: {}".format(statistics.stdev(iteraciones_acierto)))
else:
    print("\nNo se logro llegar al valor optimo 7n7, ajuste sus parametros")
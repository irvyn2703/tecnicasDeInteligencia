"""Shubert: func = 2 (-10, 10) poblacion = 15 itera = 100 - 100 ejecuciones = 10 obj = -186
    Easom: func = 1 (-100, 100) obj = -1 poblacion = 10 iteracion = 7 ejec = 5
    Rosenbrock: func = 3 (-10, 10) obj = 0 poblacion = 10 iteracion = 100 ejec = 10"""

import numpy as np
import math

# Declarar una variable global
global func

# Función objetivo
def funcion_objetivo(x, y):
    if func == 1: # Función de Easom
        return math.floor(-np.cos(x) * np.cos(y) * np.exp(-((x - np.pi)**2 + (y - np.pi)**2))) #redondeamos a negativo con math.floor
    
    elif func == 2: #Funcion shubert
        sum1 = 0
        sum2 = 0
        for i in range(1,6):
          sum1 = sum1 + (i* np.cos(((i+1)*x) +i))
          sum2 = sum2 + (i* np.cos(((i+1)*y) +i))
          result = sum1 * sum2
        return result
    
    elif func == 3: # Función de Rosenbrock
        return round((1 - x)**2 + 100*(y - x**2)**2)

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
    lobos = np.random.uniform(-100, 100, (tamano_poblacion, dimension)) #Generación de la manada aleatoriamente (tam_poblacion filas, dimension columnas)***************************************************************
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

# Parámetros del algoritmo<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< MODIFICAR AQUI <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
dimension = 2  #hay dos variables (x, y)
tamano_poblacion = 10
iteraciones = 7
func = 1
ejec = 5
apt_obj = -1

# Ejecutar el algoritmo
for i in range(ejec):
    mejor_solucion, mejor_aptitud = optimizador_lobo_gris(funcion_objetivo, dimension, tamano_poblacion, iteraciones,apt_obj)
    # Verificar si hemos alcanzado la función objetivo
    if mejor_aptitud <= apt_obj:  
        aciertos += 1 #aumentamos los aciertos

if len(iteraciones_acierto) > 0:
    promedio_aciertos = (aciertos * 100)/ejec
    promedio_iteraciones = sum(iteraciones_acierto) / len(iteraciones_acierto)
    desviacion_estandar_iteraciones = np.std(iteraciones_acierto)

# Mostrar los resultados
if func == 1: # Función de Easom
    print("\nFUNCION EASOM:")
    
elif func == 2: #Funcion shubert
    print("\nFUNCION SHUBERT:")
    
elif func == 3: # Función de Rosenbrock
    print("\nFUNCION ROSENBROCK:")

print("\nMejor solución encontrada:")
print("Lobo (x, y):", mejor_solucion)
print("Valor de aptitud:", mejor_aptitud)
print("\nParámetros utilizados:")
print("Población:", tamano_poblacion)
print("Iteraciones:", iteraciones)
print("Ejecuciones:", ejec)
print("Aptitud objetivo:", apt_obj)
if len(iteraciones_acierto) > 0:
    print("Estadísticas:")
    #print("Promedio de aciertos: {}%".format(promedio_aciertos))
    print("Promedio de iteraciones: {}".format(promedio_iteraciones))
    print("Desviación estándar de iteraciones: {}".format(desviacion_estandar_iteraciones))
else:
    print("\nNo se logro llegar al valor optimo 7n7, ajuste sus parametros")



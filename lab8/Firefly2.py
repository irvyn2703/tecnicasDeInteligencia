import math
import random
import statistics


def algoritmo_luciernagas(fun, num_luciernagas, max_iteraciones, alpha, beta, gamma, deciOpt=6):
    # Función para evaluar la aptitud de una posición dada según la función seleccionada
    def evaluar_fitness(posicion):
        if fun == 2:  # Función de Easom
            return round(-math.cos(posicion[0])*math.cos(posicion[1])*math.exp(-(posicion[0]-math.pi)**2-(posicion[1]-math.pi)**2), deciOpt)
        elif fun == 4:  # Función de Shubert
            f1 = 0
            f2 = 0
            for i in range(1, 6):
                f1 += i * math.cos((i + 1) * posicion[0] + i)
                f2 += i * math.cos((i + 1) * posicion[1] + i)
            return round(f1 * f2, deciOpt)
        elif fun == 5:  # Función de Rosenbrock
            res_rosa = 0
            n = len(posicion)
            for i in range(n-1):
                res_rosa += (((1 - posicion[i]) ** 2) + 100 * ((posicion[i+1] - (posicion[i] ** 2)) ** 2))
            return round(res_rosa, deciOpt)

    # Función para mover una luciérnaga hacia otra luciérnaga
    def mover_luciernaga(posicion_actual, otra_posicion):
        r = random.uniform(0, 1)
        distancia = math.sqrt((posicion_actual[0] - otra_posicion[0])**2 + (posicion_actual[1] - otra_posicion[1])**2)
        beta_0 = 1.0
        intensidad = beta_0 * math.exp(-gamma * distancia**2)
        nueva_posicion = [
            posicion_actual[0] + alpha * (otra_posicion[0] - posicion_actual[0]) + intensidad * (r - 0.5),
            posicion_actual[1] + alpha * (otra_posicion[1] - posicion_actual[1]) + intensidad * (r - 0.5)
        ]
        return nueva_posicion

    # Inicializar luciérnagas aleatoriamente
    luciernagas = [[random.uniform(-10, 10), random.uniform(-10, 10)] for _ in range(num_luciernagas)]
    primerAcierto = True
    itera = -1
    acierto = 0
    comparar = 0

    # comparar varia segun la funcion que ocupemos
    if fun == 2:
        comparar = -1
    elif fun == 4:
        comparar = -186
    else:
        comparar = 0

    # Iterar a través de las generaciones del algoritmo
    for iteracion in range(max_iteraciones):
        # Iterar a través de cada luciérnaga
        for i in range(num_luciernagas):
            # Comparar con todas las demás luciérnagas
            for j in range(num_luciernagas):
                # Si la luciérnaga j es mejor que la luciérnaga i, entonces mueve i hacia j
                if evaluar_fitness(luciernagas[j]) < evaluar_fitness(luciernagas[i]):
                    luciernagas[i] = mover_luciernaga(luciernagas[i], luciernagas[j])
        # buscamos el mejor valor de la iteracion
        mejor_luciernaga = min(luciernagas, key=evaluar_fitness)
        mejor_fitness = evaluar_fitness(mejor_luciernaga)
        # si el valor es el que esperamos y es el primer acierto guardamos el numero de la iteracion
        if round(mejor_fitness) <= comparar and primerAcierto == True:
            itera = iteracion
            primerAcierto = False

    # Encontrar la mejor luciérnaga (aquella con la menor aptitud)
    mejor_luciernaga = min(luciernagas, key=evaluar_fitness)
    mejor_fitness = evaluar_fitness(mejor_luciernaga)
    #print(f"Mejor valor de aptitud: {mejor_fitness}")

    # si encontramos el valor deseado lo tomamos como acierto
    if round(mejor_fitness) <= comparar:
        acierto = 1

    return mejor_luciernaga, mejor_fitness, itera, acierto

# Ejemplo de uso:
opcion_fun = 5 # Elige la función (2 para Easom, 4 para Shubert, 5 para Rosenbrock)
num_luciernagas = 20 # Easom 25, Shubert 50 o mas, Rosenbrock 25
max_iteraciones = 50
alpha = 0.21
beta = 0.8
gamma = 0.6
iteraciones = []
aciertos = 0

# Ejecutar el algoritmo de luciérnagas
for i in range(100): # ejecutamos el algoritmo 100 veces
    mejor_posicion, mejor_fitness, tempItera, tempAcierto = algoritmo_luciernagas(opcion_fun, num_luciernagas, max_iteraciones, alpha, beta, gamma)
    # en tempItera tenemos el numero de la iteracion donde se encontro el resultado 
    if tempItera >= 0:# si nos llega un numero menor a 0 significa que no se encontro solucion
        iteraciones.append(tempItera) # guardamos la iteracion que encontro la solucion
    aciertos += tempAcierto # vamos guardando los aciertos

# Imprimir resultados
#print("iteraciones: " + str(iteraciones))
if opcion_fun == 2:
    print("Easom")
if opcion_fun == 4:
    print("Shubert")
if opcion_fun == 5:
    print("Rosenbrock")
print("Promedio de aciertos: " + str(aciertos) + "%")
print("Promedio de iteraciones: " + str(statistics.mean(iteraciones)))
print("Desviacion estandar: " + str(statistics.stdev(iteraciones)))


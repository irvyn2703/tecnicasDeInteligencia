import math
import random

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
    aciertos = 0
    numIteracion = []

    # Iterar a través de las generaciones del algoritmo
    for z in range(100):
        primerAcierto = True
        print("itento " + str(z))
        for iteracion in range(max_iteraciones):
            # Iterar a través de cada luciérnaga
            for i in range(num_luciernagas):
                # Comparar con todas las demás luciérnagas
                for j in range(num_luciernagas):
                    # Si la luciérnaga j es mejor que la luciérnaga i, entonces mueve i hacia j
                    if evaluar_fitness(luciernagas[j]) < evaluar_fitness(luciernagas[i]):
                        luciernagas[i] = mover_luciernaga(luciernagas[i], luciernagas[j])
            # Encontrar la mejor luciérnaga (aquella con la menor aptitud)
            mejor_luciernaga = min(luciernagas, key=evaluar_fitness)
            mejor_fitness = evaluar_fitness(mejor_luciernaga)
            if mejor_fitness == 0 and primerAcierto == True:
                numIteracion.append(iteracion)
                primerAcierto = False
        print("Mejor posición: " + str(mejor_luciernaga) + " | " + str(mejor_fitness))
        if(mejor_fitness == 0):
            aciertos = aciertos + 1

    return aciertos, numIteracion

# Ejemplo de uso:
opcion_fun = 2  # Elige la función (2 para Easom, 4 para Shubert, 5 para Rosenbrock)
num_luciernagas = 10
max_iteraciones = 50
alpha = 0.2
beta = 1.0
gamma = 1.0
numAciertos = 0
iteraciones = []


# Ejecutar el algoritmo de luciérnagas
numAciertos, iteraciones = algoritmo_luciernagas(opcion_fun, num_luciernagas, max_iteraciones, alpha, beta, gamma)

# Imprimir resultados
print("promedio de exito: " + str(numAciertos) + "%")
print("iteraciones: " + str(stas))


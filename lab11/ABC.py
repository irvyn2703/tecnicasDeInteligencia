import numpy as np
import statistics


# =========================================== Función principal ========================================================
def ABC(problem, num_dim, bounds, param, objetivo):
    funcion_fitness = problem  # Función que se va a optimizar
    dimension = (1, num_dim)  # Dimension del problema (para usarse al declarar listas)
    iteraciones = param['itermax']  # Numero de iteraciones
    tam_poblacion = param['npop']  # Tamano de la población de abejas
    xmin, xmax, a = bounds['xmin'], bounds['xmax'], 0.5  # Limites de los valores de la población
    lim = round(num_dim * tam_poblacion)  # Limite
    numIteracion = -1 # numero de la titeracion donde se consiguio el mejor resultado
    primeroAcierto = False

    # Se inicializa poblacion de abejas y arreglo para guardar los valores de la funcion objetivo
    mejor_solucion = {'loc': np.zeros(dimension), 'cost': np.inf}  # Arreglo que almacena los valores de la funcion objetivo (loc = [x1, x2], cost = y)
    food_source = [{'loc': np.zeros(num_dim), 'cost': np.inf} for _ in range(tam_poblacion)]

    # Se inicializa la poblacion de forma aleatoria, asi como actualizar los valores mejor_solucion
    for i in range(tam_poblacion):
        food_source[i]['loc'] = np.random.uniform(xmin, xmax, num_dim)
        food_source[i]['cost'] = funcion_fitness(food_source[i]['loc'])

        if food_source[i]['cost'] < mejor_solucion['cost']:
            mejor_solucion = food_source[i]

    # Se inicializa en 0 arreglo que guarda los trials y el arreglo almacena los mejores valores por iteracion
    trial = np.zeros(tam_poblacion)
    bestcost = np.zeros(iteraciones)

    # Loop principal de iteraciones
    for iter in range(iteraciones):
        # Employee Bee Phase
        for i in range(tam_poblacion):
            p = np.concatenate([np.arange(i), np.arange(i+1, tam_poblacion)])  # Lista de abejas diferentes a la actual
            partner = np.random.choice(p)  # Compañero selccionado aleatoriamente y distinta de la actual
            phi = a * np.random.uniform(-1, 1, num_dim)  # Genera un numero aleatoria entre -1 y 1

            # Genera nueva abeja con la abeja actual y su compañero, se comprueba que no sobrepase las cotas max y min
            newbee_loc = np.minimum(np.maximum(food_source[i]['loc'] + phi * (food_source[i]['loc'] - food_source[partner]['loc']), xmin), xmax)
            newbee_cost = funcion_fitness(newbee_loc)  # Calcula el valor fitness de la funcion objetivo

            # Greedy Selection
            if newbee_cost < food_source[i]['cost']:
                food_source[i] = {'loc': newbee_loc, 'cost': newbee_cost}
            else:
                trial[i] += 1

        # Actualiza los valores de acuerdo con la probabilidad de la misma forma que en la Employee Bee Phase
        # Onlooker Bee Phase
        fit = np.zeros(tam_poblacion)  # Inicializa valores en cero para el arreglo de valores fit
        for i in range(tam_poblacion):
            # Calcula valoresa fit si el valor fitness es mayor o menor a 0
            if food_source[i]['cost'] >= 0:
                fit[i] = 1 / (1 + food_source[i]['cost'])
            else:
                fit[i] = 1 + abs(food_source[i]['cost'])
        P = fit / sum(fit)  # Calcula la probabbilidad

        # Actualiza los valores de acuerdo con la probabilidad de la misma forma que en la Employee Bee Phase
        for j in range(tam_poblacion):
            i = np.random.choice(np.arange(tam_poblacion), p=P)
            p = np.concatenate([np.arange(i), np.arange(i+1, tam_poblacion)])
            partner = np.random.choice(p)
            phi = a * np.random.uniform(-1, 1, num_dim)
            newbee_loc = np.minimum(np.maximum(food_source[j]['loc'] + phi * (food_source[j]['loc'] - food_source[partner]['loc']), xmin), xmax)
            newbee_cost = funcion_fitness(newbee_loc)

            if newbee_cost < food_source[j]['cost']:
                food_source[j] = {'loc': newbee_loc, 'cost': newbee_cost}
            else:
                trial[j] += 1

        # Scout Bee Phase
        for i in range(tam_poblacion):
            # Si el numero de trial es mayor al limite genera un nuevo valor aletorio
            if trial[i] >= lim:
                food_source[i]['loc'] = np.random.uniform(xmin, xmax, num_dim)
                food_source[i]['cost'] = funcion_fitness(food_source[i]['loc'])
                trial[i] = 0

        # Encuentra la mejor solucion de la iteracion
        for i in range(tam_poblacion):
            if food_source[i]['cost'] < mejor_solucion['cost']:
                mejor_solucion = food_source[i]

        bestcost[iter] = mejor_solucion['cost']
        if (bestcost[iter] < objetivo + 0.001) and (primeroAcierto == False):
            print(f'\tIteration {iter+1} | Minimum cost = {bestcost[iter]}')
            numIteracion = iter + 1
            primeroAcierto = True

    bestbee = mejor_solucion  # Mejor individuo
    mincost = bestcost  # Historia de valores fitness por cada iteracion

    return bestbee, mincost, numIteracion
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
def easom(x):
    return -np.cos(x[0]) * np.cos(x[1]) * np.exp(-((x[0] - np.pi)**2 + (x[1] - np.pi)**2))


def shubert(x):
    result = 1
    for i in range(len(x)):
        term_sum = 0
        for j in range(1, 6):
            term_sum += j * np.cos((j + 1) * x[i] + j)
        result *= term_sum
    return -result


def rosenbrock(x):
    x = np.array(x)
    # Número de variables
    n = len(x)
    # Calcular la suma de la función de Rosenbrock
    sum_term = 0
    for i in range(n - 1):
        sum_term += 100 * (x[i + 1] - x[i]**2)**2 + (1 - x[i])**2

    return sum_term
# ----------------------------------------------------------------------------------------------------------------------


pf = 3  # 1 : Easom, 2 : Shubert, 3 : Rosenbrock
if pf == 1:
    funcion = easom
    dim = 2
    cotas_valores = {'xmin': -100, 'xmax': 100}
    objetivo = -1
elif pf == 2:
    funcion = shubert
    dim = 2
    cotas_valores = {'xmin': -10, 'xmax': 10}
    objetivo = -186
elif pf == 3:
    funcion = rosenbrock
    dim = 2
    cotas_valores = {'xmin': -10, 'xmax': 10}
    objetivo = 0
else:
    funcion = easom
    dim = 2
    cotas_valores = {'xmin': -100, 'xmax': 100}
    objetivo = -1


iteraciones_poblacion = {'itermax': 80, 'npop': 110}
iteraciones = []
aciertos = 0

# Llama al algoritmo ABC
for i in range(100):
    print("Ejecucion: " + str(i+1))
    mejor_resultado, fitness_historial, tempItearcion = ABC(funcion, dim, cotas_valores, iteraciones_poblacion, objetivo)
    if tempItearcion != -1:
        aciertos += 1
        iteraciones.append(tempItearcion)
    #print("Mejor solución encontrada:", mejor_resultado['loc'])
    #print("Valor de la función objetivo en la mejor solución:", mejor_resultado['cost'])

print()
if pf == 1:
    print("Easom")
if pf == 2:
    print("Shubert")
if pf == 3:
    print("Rosenbrock")
print("Promedio de aciertos: " + str(aciertos) + "%")
print("Promedio de iteraciones: " + str(statistics.mean(iteraciones)))
print("Desviacion estandar: " + str(statistics.stdev(iteraciones)))
    # Muestra la mejor solución encontrada
    # print(fitness_historial)

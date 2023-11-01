import random
import matplotlib.pyplot as plt

def inicializar_poblacion(num_pbl, j):
    global poblacion
    poblacion = [[random.randint(1, j) for _ in range(j)] + [0] for _ in range(num_pbl)]


def fitness(individuo):
    no_atacadas = 0

    for i in range(len(individuo) - 1):
        atacada = False

        for j in range(len(individuo) - 1):
            if i != j:
                # Verificar ataques en la misma columna
                if individuo[i] == individuo[j]:
                    atacada = True
                # Verificar ataques en la misma diagonal
                if abs(individuo[i] - individuo[j]) == abs(i - j):
                    atacada = True

        if not atacada:
            no_atacadas += 1
    individuo[-1] = no_atacadas  # Actualiza el valor de aptitud en el último elemento


def crossover(padre1, padre2):
    punto_de_cruce1 = random.randint(0, len(padre1) - 2)
    punto_de_cruce2 = random.randint(0, len(padre1) - 2)
    while punto_de_cruce1 == punto_de_cruce2:
        punto_de_cruce2 = random.randint(1, len(padre1) - 2)

    punto_de_cruce1, punto_de_cruce2 = min(punto_de_cruce1, punto_de_cruce2), max(punto_de_cruce1, punto_de_cruce2)

    hijo1 = padre1[:punto_de_cruce1] + padre2[punto_de_cruce1:punto_de_cruce2] + padre1[punto_de_cruce2:]
    hijo2 = padre2[:punto_de_cruce1] + padre1[punto_de_cruce1:punto_de_cruce2] + padre2[punto_de_cruce2:]
    return hijo1, hijo2

def pmx(parent1, parent2):
    n = len(parent1)  # Obtener la longitud de los padres
    corte = random.randint(0, n-1)  # Generar un punto de corte aleatorio
    child = [None] * n  # Crear un hijo vacío del mismo tamaño que los padres
    child[corte:] = parent1[corte:]  # Copiar la sección posterior del primer padre al hijo
    for i in range(corte, n):  # Recorrer la sección posterior del hijo
        if parent2[i] not in child:  # Si el valor del segundo padre no está en el hijo
            j = i  # Establecer un índice auxiliar
            while parent2[j] in child:  # Mientras el valor del segundo padre esté en el hijo
                j = parent1.index(parent2[j])  # Encontrar el índice correspondiente en el primer padre
            child[j] = parent2[i]  # Asignar el valor del segundo padre al hijo en la posición correspondiente
    for i in range(n):  # Para los valores restantes en el hijo
        if child[i] is None:  # Si el valor es nulo
            child[i] = parent2[i]  # Asignar el valor del segundo padre al hijo
    return child  # Devolver el hijo resultante del cruce PMX

def mutar(individuo, mutation_prob):
    if random.randint(1, 100) <= mutation_prob:
        cambio1, cambio2 = random.sample(range(len(individuo) - 2), 2)
        individuo[cambio1], individuo[cambio2] = individuo[cambio2], individuo[cambio1]


def reemplazar_poblacion(poblacion_actual, nueva_poblacion):
    poblacion_actual.sort(key=lambda x: x[-1], reverse=True)  # Ordena la población actual por aptitud (de mayor a menor)
    for i, nuevo_individuo in enumerate(nueva_poblacion):
        if nuevo_individuo[-1] > poblacion_actual[i][-1]:
            poblacion_actual[i] = nuevo_individuo  # Reemplaza si es mejor


def resultado_encontrado(pbl, nreinas_no_atacadas):  # Valor maximo de reinas que no se atacan
    return any(individuo[-1] == nreinas_no_atacadas for individuo in pbl)  # revisa la poblacion y busca el valor maximo


num_reinas = int(input("Ingrese el número de reinas: "))  # Indica el numero de reina que se colocaran en el tablero nxn
tamano_poblacion = int(input("Ingrese el tamaño de la población inicial: ")) # Indica el tamaño de la poblacion de individuos
probabilidad_mutacion = int(input("Ingrese la probabilidad de mutación (porcentaje): ")) # Indica la probabilidad (en porcentaje) de mutacion de cada individuo en la poblacion
umbral_reinicio = 5000  # int(input("Ingrese un umbral de reinicio: ")) # Inidica cuanas generaciones tienen que pasar para reinicar la poblacion
num_elite = 4

poblacion = [0]
filas = columnas = num_reinas  # Se asigna filas y columnas acorde al numero de reinas

inicializar_poblacion(tamano_poblacion, columnas)  # Se crea la matriz con la poblacion inicial y el numero de reinas
# print(poblacion)

for i in range(num_reinas):  # Se evalua la poblacion inicial
    fitness(poblacion[i])

poblacion = sorted(poblacion, key=lambda x: x[-1], reverse=True)  # Se ordena de la poblacion por fitness descendente
nueva_poblacion = []
generacion_actual = 0
while not resultado_encontrado(poblacion, num_reinas):
    generacion_actual += 1  # Actualiza el contador de generaciones

    if generacion_actual >= umbral_reinicio:
        # Realiza el reinicio aquí, por ejemplo, inicializa una nueva población
        inicializar_poblacion(tamano_poblacion, columnas)
        for i in range(num_reinas):  # Se evalua la poblacion inicial
            fitness(poblacion[i])
        poblacion = sorted(poblacion, key=lambda x: x[-1],
                           reverse=True)  # Se ordena de la poblacion por fitness descendente
        # Restablece el contador de generaciones
        generacion_actual = 0

    print("Generacion: ", generacion_actual)

    poblacion_elite = poblacion[:num_elite]
    nueva_poblacion = []
    # nueva_poblacion = poblacion_elite.copy()
    # Crossover con enfoque generacional
    for i in range(0, tamano_poblacion, 2):
        p1 = poblacion[i]
        p2 = poblacion[(i + 1) % filas]
        # if random.randint(1, 100) <= probabilidad_mutacion:
        h1, h2 = crossover(p1, p2)
        h1[-1] = 0
        h2[-1] = 0
        nueva_poblacion.extend([h1, h2])
        # else:
        # h1 = pmx(p1, p2)
        # h1[-1] = 0
        # nueva_poblacion.extend([h1])

    # Mutacion a la nueva poblacion
    for i in range(len(nueva_poblacion)):
        mutar(nueva_poblacion[i], probabilidad_mutacion)

    nueva_poblacion.extend(poblacion_elite)

    # Se evalua a la nueva poblacion
    for i in range(len(nueva_poblacion)):
        fitness(nueva_poblacion[i])

    # Se une la poblacion nueva y la actual
    poblacion.extend(nueva_poblacion)

    # Se ordena de la poblacion por fitness descendente
    poblacion = sorted(poblacion, key=lambda x: x[-1], reverse=True)
    poblacion_final = []
    for individuo in poblacion:
        if individuo not in poblacion_final and len(poblacion_final) < tamano_poblacion:
            poblacion_final.append(individuo)

    # Se elimina a la poblacion con fitness mas bajo hasta alcanzar el tamaño de poblacione stablecido
    poblacion = poblacion_final

    print("Población Final (de mayor a menor):")
    for individuo in poblacion:
        print(individuo[:-1], f"Fitness: {individuo[columnas]}")
    print()

    nueva_poblacion = []
    poblacion_final = []
    poblacion_elite = []

# print("Población Final (de mayor a menor):")
# for individuo in poblacion:
#     print(individuo[:-1], f"Fitness: {individuo[columnas]}")
# print()

print("Resultado Final")
print(poblacion[0][:-1], "Fitness: " + str(poblacion[0][-1]))
print()

# Función para dibujar el tablero con líneas de cuadrícula
def dibujar_tablero(poblacion):
    n = len(poblacion) 
    tablero = [[0 for _ in range(n)] for _ in range(n)] 
    for i in range(n):  
        tablero[i][poblacion[i] - 1] = 1  

    fig, ax = plt.subplots()  
    ax.matshow(tablero, cmap='binary')  

    for i in range(n + 1):  
        ax.axhline(i - 0.5, color='black', linewidth=2)  
        ax.axvline(i - 0.5, color='black', linewidth=2)  

    plt.show()  

# Llamar a la función dibujar_tablero con la población de reinas encontrada
dibujar_tablero(poblacion[0][:-1])


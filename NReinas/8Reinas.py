import random
import math
import matplotlib.pyplot as plt
import numpy as np

filas = 4
columnas = 8

# Crear una matriz inicialmente llena de números aleatorios del 1 al 8
# y también mantener un valor de fitness inicializado en 0 para cada individuo
poblacion = [[random.randint(1, 8) for _ in range(columnas)] + [0] for _ in range(filas)]
nueva_poblacion = []

# Función para aplicar la mutación a un individuo
def mutar(individuo, mutation_prob):
    if random.randint(1, 10) < mutation_prob:
        print(individuo, end=" ")
        cambio1 = random.randint(1, 8)
        cambio2 = random.randint(1, 8)
        while cambio1 == cambio2:
            cambio1 = random.randint(1, 8)
        aux = individuo[cambio1]
        individuo[cambio1] = individuo[cambio2]
        individuo[cambio2] = aux
        print(" ==> " + str(individuo))


def crossover(padre1, padre2):
    # Elegir dos puntos de cruce aleatorios diferentes
    punto_de_cruce1 = random.randint(1, len(padre1) - 1)
    punto_de_cruce2 = random.randint(1, len(padre1) - 1)
    
    # Asegurarse de que los puntos de cruce sean diferentes
    while punto_de_cruce1 == punto_de_cruce2:
        punto_de_cruce2 = random.randint(1, len(padre1) - 1)

    # Ordenar los puntos de cruce
    punto_de_cruce1, punto_de_cruce2 = min(punto_de_cruce1, punto_de_cruce2), max(punto_de_cruce1, punto_de_cruce2)

    # Realizar el cruce de dos puntos
    hijo1 = padre1[:punto_de_cruce1] + padre2[punto_de_cruce1:punto_de_cruce2] + padre1[punto_de_cruce2:]
    hijo2 = padre2[:punto_de_cruce1] + padre1[punto_de_cruce1:punto_de_cruce2] + padre2[punto_de_cruce2:]
    
    return hijo1, hijo2

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

    # agregamos su valor fitness
    individuo[columnas] = no_atacadas
    """  <-- visualizar el tablero -->
    print(individuo[:-1])
    for i in range(columnas):
        for j in range(columnas):
            if individuo[i] == j + 1:
                print("*", end=" ")
            else:
                print("-", end=" ")
        print()
    
    print("Reinas sin atacar en este individuo: " + str(no_atacadas))
    print()
    """

def resultadoEncontrado(individuos):
    temp = False
    for i in range(len(individuos)):
        if individuos[i][columnas] == 8:
            temp = True
    return temp

# evaluamos nuestra poblacion inicial
print(poblacion)
for i in range(filas):
    fitness(poblacion[i])

# Ordenar la población de mayor a menor fitness
poblacion = sorted(poblacion, key=lambda x: x[columnas], reverse=True)
print("Población ordenada por fitness (de mayor a menor):")
for individuo in poblacion:
    print(individuo[:-1], f"Fitness: {individuo[columnas]}")
print()

w = False
while w == False:
    # realizamos parejas para cruzarlas
    for i in range(filas):
        padre1 = poblacion[i]
        padre2 = poblacion[(i + 1) % filas]  # Escoge el siguiente individuo en el anillo
        hijo1, hijo2 = crossover(padre1, padre2)
        nueva_poblacion.extend([hijo1, hijo2])

    # nueva poblacion
    print("Nueva población después del cruce:")
    for individuo in nueva_poblacion:
        print(individuo)
    print()

    # realizamos mutaciones
    print("Mutaciones")
    for i in range(len(nueva_poblacion)):
        mutar(nueva_poblacion[i],5)
    print()

    # combinamos las poblaciones
    poblacion.extend(nueva_poblacion)

    # limpiamos la poblacion de hijos
    nueva_poblacion = []

    # evaluamos 
    for i in range(len(poblacion)):
        fitness(poblacion[i])

    # Ordenar la población de mayor a menor fitness
    poblacion = sorted(poblacion, key=lambda x: x[columnas], reverse=True)

    print("Población ordenada por fitness (de mayor a menor):")
    for individuo in poblacion:
        print(individuo[:-1], f"Fitness: {individuo[columnas]}")
    print()

    # Mantener solo los mejores 3 individuos y alguno de los peores pra mantener la diversidad
    numTemp = 0
    mejores_individuos = [] 
    for individuo in poblacion:
        if individuo not in mejores_individuos and numTemp < 4:
            mejores_individuos.append(individuo)
            numTemp += 1
    print("poblacion sobreviviente")
    for individuo in mejores_individuos:
        print(individuo[:-1], f"Fitness: {individuo[columnas]}")
    print()

    # poblacion ahora contiene solo los 4 mejores individuos
    poblacion = mejores_individuos

    w = resultadoEncontrado(poblacion)

print("Resultado Final")
print(poblacion[0][:-1], "Fitness: " + str(poblacion[0][8]))
print()


import random

minPoblacion = -5 # valor minimo de la poblacion
maxPoblacion = 5 # valor maximo de la poblacion
tamPoblacion = 5 # tamaño de la poblacion
c1 = 1.5 
c2 = 1.5
dimProblema = 2
w = 0.9
maxIteracion = 20 # num de iteraciones
r1 = random.uniform(0, 1) # numero aleatorio entre el 0 y 1
r2 = random.uniform(0, 1) # numero aleatorio entre el 0 y 1
velocidad = [[random.uniform(0, 1) for _ in range(2)] for _ in range(tamPoblacion)] # inicializamos una matriz aleatoria del tamaño de la poblacion
position = [[random.uniform(minPoblacion, maxPoblacion) for _ in range(2)] for _ in range(tamPoblacion)] # inicializamos una matriz aleatoria del tamaño de la poblacion
positionBest = position # mejores posiciones al inicio son las mismas que las posiociones
mejorPosition = 0
fitnessPuntos = [[0, 0] for _ in range(tamPoblacion)] #[x][0] --> valor fitness de la iteracion [x][1] valor fitness de la mejor position

# ------------------------------------------------- funciones -----------------------------------------
def fitness(x,y):
    return x**2 - x*y + y**2 + 2*x + 4*y + 3 # formula fitness

def bestPosition():
    best_value = fitnessPuntos[0][1]  # Suponemos que el primer valor es el mejor inicialmente
    best_index = 0  # Índice del mejor valor

    for i in range(0, tamPoblacion):
        if (fitnessPuntos[i][1] > best_value):
            best_value = fitnessPuntos[i][1]
            best_index = i

    return best_index

def actualizacionVelocidad(velocidad,position,bestPosition,bestPunto):
    nuevoValor = w*velocidad + c1*r1*(bestPosition - position) + c2*r2*(bestPunto - position)
    return nuevoValor

def actualizarPosition(position,velocidad):
    temp = position + velocidad
    if (temp <= maxPoblacion) and (temp >= minPoblacion):
        return temp
    else:
        return position
    
def actualizarMejoresPuntos():
    for i in range(0,tamPoblacion):
        if(fitnessPuntos[i][0] > fitnessPuntos[i][1]):
            print("cambio: " + str(positionBest[i][0]) + " " + str(positionBest[i][1]) + " a " + str(position[i][0]) + " " + str(position[i][1])) 
            positionBest[i][0] = position[i][0]
            positionBest[i][1] = position[i][1]
            fitnessPuntos[i][1] = fitnessPuntos[i][0]

# inicio del PSO
for z in range(1, maxIteracion + 1):
    print("iteracion : " + str(z))
    # calculamos el valor fitness y mostramos la poblacion
    for i in range (0, tamPoblacion):
        fitnessPuntos[i][0] = fitness(position[i][0], position[i][1])
        print(str(velocidad[i][0]) + "," + str(velocidad[i][1]) + "  ||  " +str(position[i][0]) + "," + str(position[i][1]) + " = " + str(fitnessPuntos[i][0]))

    # actualizamos los puntos
    print("")
    actualizarMejoresPuntos()

    # obtenemos el mejor punto
    print("")
    mejorPosition = bestPosition()
    print("mejor posicion = " + str(positionBest[mejorPosition][0]) + "," + str(positionBest[mejorPosition][1]) + " - " + str(fitnessPuntos[mejorPosition][1]))

    #actualizamos velocidades y posiciones
    for i in range(0, tamPoblacion):
        velocidad[i][0] = actualizacionVelocidad(velocidad[i][0], position[i][0],positionBest[i][0],positionBest[mejorPosition][0])
        velocidad[i][1] = actualizacionVelocidad(velocidad[i][1], position[i][1],positionBest[i][1],positionBest[mejorPosition][1])
        position[i][0] = actualizarPosition(position[i][0], velocidad[i][0])
        position[i][1] = actualizarPosition(position[i][1], velocidad[i][1])
    print("\n")

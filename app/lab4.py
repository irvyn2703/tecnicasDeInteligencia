# Bibliotecas usadas
import random
import json
import numpy as np
import matplotlib.pyplot as plt


# Red neuronal usando algoritmo perceptron
class AlgoritmoPerceptron:
    # Constructor de la clase
    def __init__(self):
        self.min_val = None  # Valor minimo posible de los pesos sinapticos
        self.max_val = None  # Valor maximo posible de los pesos sinapticos
        self.numEpoc = None  # Numero de epocas de entrenamiento
        self.graf4 = None  # Epocas que se grafican (true / false)
        self.cantidadp = None  # Cantidad de puntos generados por region
        self.W = None  # Pesos sinapticos (Contendrá los pesos finales)
        self.b = None  # sesgo (contendrá el sesgo final)
        self.learning_rate = None  # Learning rate
        self.p1 = None  # [p1x1, p1y1] Punto1 limite de region1
        self.p2 = None  # [p1x2, p1y2] Punto2 limite de region1
        self.p3 = None  # [p2x1, p2y1] Punto1 limite de region2
        self.p4 = None  # [p2x2, p2y2] Punto2 limite de region2
        self.patrones_entrenamiento = None  # Arreglo de patrones de entrenamiento
        self.clases_entrenamiento = None  # Arreglo de salidas esperadas de entrenamiento
        self.us_al = None  # Define si se generan datos aleatorios o por el usuario para reconocimiento (true/false)
        self.patrones_gen = None  # Patrones (puntos) dados por el usuario o aleatorios para reconocomiento
        self.clases_gen = None  # Arreglos de salidas esperadas para datos de generalizacion
        self.pesos_guardados = None  # Se guardan 4 pesos uniformemente distribuidos

    # Funcion para asignar valores a los parametros ingresados por el usuario
    def set_parametros(self, min_val, max_val, val_g, num_epoc, ln, cantidadp, p1, p2, p3, p4):
        self.min_val = min_val
        self.max_val = max_val
        self.numEpoc = num_epoc
        self.learning_rate = ln
        self.graf4 = val_g
        self.cantidadp = cantidadp
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    # Retorna los parametros ingreasdos por el usuario
    def get_parametros(self):
        return self.min_val, self.max_val, self.numEpoc, self.learning_rate, self.graf4, self.cantidadp, self.p1, self.p2, self.p3, self.p4

    # Asigna valores aleatorios a los pesos y el bias
    def set_w_b(self):
        # Inicialiazcion aleatoria de Pesos en el rango de valores min_val a max_val
        self.W = np.random.uniform(self.min_val, self.max_val, size=2)
        # Inicializacion aletoria de bias
        self.b = np.random.uniform()

    # Genera una lista de puntos aleatorios dados dos puntos, retornar arreglos con puntos aleatorios
    def generar_puntos_aleatorios_en_dos_regiones(self):
        def generar_puntos_en_region(punto1, punto2, cantidad):  # Genera datos aleatorios en una region
            x1, y1 = min(punto1[0], punto2[0]), min(punto1[1], punto2[1])
            x2, y2 = max(punto1[0], punto2[0]), max(punto1[1], punto2[1])

            puntos_generados = []
            for _ in range(cantidad):
                x = random.uniform(x1, x2)
                y = random.uniform(y1, y2)
                puntos_generados.append((x, y))

            return puntos_generados

        puntos_region1 = generar_puntos_en_region(self.p1, self.p2, self.cantidadp)
        puntos_region2 = generar_puntos_en_region(self.p3, self.p4, self.cantidadp)

        return puntos_region1, puntos_region2

    # Define el conjunto de entradas y de salidas esperadas para los datos de entrenamiento
    def set_patrones_salidas(self, p_region1, p_region2):
        self.patrones_entrenamiento = np.array(p_region1 + p_region2)
        # Calcular la cantidad de patrones en cada región
        num_patrones_region1 = len(p_region1)
        num_patrones_region2 = len(p_region2)

        # Crear las listas de clases (etiquetas) con valores 0.0 y 1.0
        self.clases_entrenamiento = np.append(np.zeros(num_patrones_region1), np.ones(num_patrones_region2))

    # Define el conjunto de entradas y de salidas esperadas para los datos de generalizacion
    def set_patrones_salidas_gen(self, p_region1, p_region2):
        self.patrones_gen = np.array(p_region1 + p_region2)
        # Contar la cantidad de patrones en cada región
        num_patrones_region1 = len(p_region1)
        num_patrones_region2 = len(p_region2)

        # Crear las listas de clases (etiquetas) con valores 0.0 y 1.0
        self.clases_gen = np.append(np.zeros(num_patrones_region1), np.ones(num_patrones_region2))

    # Funcion con el algoritmo perceptron
    def entrenamiento_perceptron(self):
        self.pesos_guardados = {}
        intervalo = (self.numEpoc - 1) // 2
        for epoca in range(self.numEpoc):
            # Calculo de las predicciones
            a = np.heaviside(np.dot(self.patrones_entrenamiento, self.W) + self.b, 0)

            # Cálculo del error
            error = self.clases_entrenamiento - a

            # Actualización de pesos y bias
            self.W += np.dot(self.patrones_entrenamiento.T, error) * self.learning_rate
            self.b += np.sum(error, axis=0, keepdims=True)

            # Guarda pesos y bias de la epoca dependiendo del usuario (4 epocas o solo 2, inicial y final)
            if self.graf4:  # Si el usuario quiere ver las lineas de decision en 4 etapas
                if epoca == 0 or epoca == self.numEpoc - 1 or (epoca - 1) % intervalo == 0:
                    # Si la época actual es la primera, última o está en un punto de guardado uniforme
                    self.pesos_guardados[epoca] = (self.W.copy(), self.b.copy())
            else:  # Si el usuario quiere ver las lineas de decision inicial y final
                # Si la epoca es la primera o la ultima
                if epoca == 0 or epoca == self.numEpoc - 1:
                    self.pesos_guardados[epoca] = (self.W.copy(), self.b.copy())

        # # # Se muestran resultados en consola
        # print("Patrones de entrada (entrenamiento):\n", self.patrones_entrenamiento)
        # print("Clases reales (entrenamiento):\n", self.clases_entrenamiento)
        # # print("Clases predichas:\n", salida_final)
        # # print("Error (entrenamiento): \n", error)
        # print("Pesos(Final): \n", self.W)
        # print("Sesgo(Final): \n", self.b)

    # Grafica los resultados de entrenamiento
    def graficacion(self):
        # Crear una figura y ejes
        fig, ax = plt.subplots()

        # Establecer los límites de los ejes x e y
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)

        # Establecer las etiquetas de los ejes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        # Coloca líneas de los ejes en el origen (0,0)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Grafica patrones de entrenamiento
        for i, c in enumerate(self.clases_entrenamiento):
            if c == 0:
                plt.scatter(self.patrones_entrenamiento[i, 0], self.patrones_entrenamiento[i, 1], color='red',
                            marker='o')
            elif c == 1:
                plt.scatter(self.patrones_entrenamiento[i, 0], self.patrones_entrenamiento[i, 1], color='blue',
                            marker='x')

        # Grafica regiones delimitadas por el usuario
        # Dibujar el rectángulo para resaltar la región 1
        rect_x1 = [self.p1[0], self.p2[0], self.p2[0], self.p1[0], self.p1[0]]
        rect_y1 = [self.p1[1], self.p1[1], self.p2[1], self.p2[1], self.p1[1]]
        ax.fill(rect_x1, rect_y1, 'r', alpha=0.3, label='Región A')

        # Dibujar el rectángulo para resaltar la región 2
        rect_x2 = [self.p3[0], self.p4[0], self.p4[0], self.p3[0], self.p3[0]]
        rect_y2 = [self.p3[1], self.p3[1], self.p4[1], self.p4[1], self.p3[1]]
        ax.fill(rect_x2, rect_y2, 'b', alpha=0.3, label='Región B')

        # Grafica lineas de decision
        x_vals = np.linspace(-6, 5, 100)
        for clave, valor in self.pesos_guardados.items():
            wb = self.pesos_guardados[clave]
            w = wb[0]
            b = wb[1]
            y_vals = -(w[0] * x_vals + b[0]) / w[1]
            plt.plot(x_vals, y_vals, label=f'Frontera Epoca {clave + 1}')

        # Agregar etiquetas a los ejes y leyenda y guarda la grafica
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.legend(loc='lower left')
        plt.savefig('static/img/imageGrafica2.png')
        # Mostrar la gráfica
        # plt.show()

    # define que tipo de datos se usan en la generalizacion, (dados por el usuario o generados aleatoriamente)
    def set_recon_us(self, us_al, us_r1=0, us_r2=0):
        if us_al:
            self.set_patrones_salidas_gen(us_r1, us_r2)
        else:
            us_r1r, us_r2r = self.generar_puntos_aleatorios_en_dos_regiones()
            self.set_patrones_salidas_gen(us_r1r, us_r2r)

    # Calcula el porcentaje de reconocimiento/generalizacion, retorna resultado calculado
    def calcula_recon_gen(self, patrones, salidas):
        afinal = np.dot(patrones, self.W) + self.b
        salida_final = np.heaviside(afinal, 0)  # prediccion final
        error = salidas - salida_final  # calcula error final
        # Se muestran resultados en consola
        # print("Patrones de entrada:\n", patrones)
        # print("Clases reales:\n", salidas)
        # print("Clases predichas:\n", salida_final)
        # print("Error: \n", error)
        # print("Pesos(Final): \n", self.W)
        # print("Sesgo(Final): \n", self.b)
        cont = 0
        for i in range(len(error)):  # Ciclo para conocer numero de patrones correctamente clasificados
            if error[i] == 0:
                cont += 1
        res = (cont / len(patrones)) * 100
        return res

    # Llama a la funcion que calcula el porcentaje de reconocimiento/generalizacion, retorna resultados de ambos datos
    def get_recon_gen(self):
        # print("Datos de reconocimiento: \n")
        reconocimiento = self.calcula_recon_gen(self.patrones_entrenamiento,
                                                self.clases_entrenamiento)  # Datos de entrenamiento
        # print("Datos de generalizacion: \n")
        generalizacion = self.calcula_recon_gen(self.patrones_gen,
                                                self.clases_gen)  # Nuevos datos (usuario o aleatorio)
        return reconocimiento, generalizacion
"""

min_val = 0.1
max_val = 1
val_g = False
num_epoc = 50
ln = 0.1
cantidadp = 5
us_al = False
p1 = [-8.0, 6.0]
p2 = [-4.0, 4.0]
p3 = [-2.0, 4.0]
p4 = [0.0, 0.0]

# r1_us_prueba = [[], [], [], [], []]
# r2_us_prueba = [[], [], [], [], []]

per1 = AlgoritmoPerceptron()
per1.set_parametros(min_val, max_val, val_g, num_epoc, ln, cantidadp, p1, p2, p3, p4)
per1.set_w_b()
r1, r2 = per1.generar_puntos_aleatorios_en_dos_regiones()
per1.set_patrones_salidas(r1, r2)
per1.entrenamiento_perceptron()
per1.graficacion()
# per1.set_recon_us(False)
# # print("Patrones para generalizacion aleatorios: \n", per1.patrones_gen)
# # print("Clases para generalizacion aleatorios: \n", per1.clases_gen)
# recon, gen = per1.get_recon_gen()
# # print("Reconocimiento: \n", recon)
# # print("Generalizacion: \n", gen)
"""

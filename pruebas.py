import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

class PerceptronGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz Gráfica del Perceptrón")

        # Crear y configurar el marco principal
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Organizar botones en una columna vertical con margen
        buttons = [
            ("Agregar Áreas", self.mostrar_menu_areas),
            ("Fronteras y Épocas", self.mostrar_menu_fronteras_epocas),
            ("Parámetros", self.mostrar_menu_parametros),
            ("Agregar Puntos", self.mostrar_menu_agregar_puntos),
            ("Graficar", self.graficar)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(self.main_frame, text=text, command=command).grid(column=0, row=i, pady=5)

    def mostrar_menu_areas(self):
        # Crear una ventana emergente para ingresar las áreas
        areas_window = tk.Toplevel(self.root)
        areas_window.title("Agregar Áreas")

        ttk.Label(areas_window, text="px1:").grid(column=0, row=0)
        px1_entry = ttk.Entry(areas_window)
        px1_entry.grid(column=1, row=0)

        ttk.Label(areas_window, text="px2:").grid(column=0, row=1)
        px2_entry = ttk.Entry(areas_window)
        px2_entry.grid(column=1, row=1)

        ttk.Label(areas_window, text="px3:").grid(column=0, row=2)
        px3_entry = ttk.Entry(areas_window)
        px3_entry.grid(column=1, row=2)

        ttk.Label(areas_window, text="px4:").grid(column=0, row=3)
        px4_entry = ttk.Entry(areas_window)
        px4_entry.grid(column=1, row=3)

        ttk.Label(areas_window, text="py1:").grid(column=2, row=0)
        py1_entry = ttk.Entry(areas_window)
        py1_entry.grid(column=3, row=0)

        ttk.Label(areas_window, text="py2:").grid(column=2, row=1)
        py2_entry = ttk.Entry(areas_window)
        py2_entry.grid(column=3, row=1)

        ttk.Label(areas_window, text="py3:").grid(column=2, row=2)
        py3_entry = ttk.Entry(areas_window)
        py3_entry.grid(column=3, row=2)

        ttk.Label(areas_window, text="py4:").grid(column=2, row=3)
        py4_entry = ttk.Entry(areas_window)
        py4_entry.grid(column=3, row=3)

        # Botón para guardar los valores en variables globales
        ttk.Button(areas_window, text="Guardar", command=lambda: self.guardar_areas(px1_entry.get(), px2_entry.get(), px3_entry.get(), px4_entry.get(), py1_entry.get(), py2_entry.get(), py3_entry.get(), py4_entry.get())).grid(column=0, row=4, columnspan=4)

    def guardar_areas(self, px1, px2, px3, px4, py1, py2, py3, py4):
        # Validar que los valores sean números válidos antes de guardarlos en variables globales
        try:
            px1 = float(px1)
            px2 = float(px2)
            px3 = float(px3)
            px4 = float(px4)
            py1 = float(py1)
            py2 = float(py2)
            py3 = float(py3)
            py4 = float(py4)
            PerceptronGUI.px1 = px1
            PerceptronGUI.px2 = px2
            PerceptronGUI.px3 = px3
            PerceptronGUI.px4 = px4
            PerceptronGUI.py1 = py1
            PerceptronGUI.py2 = py2
            PerceptronGUI.py3 = py3
            PerceptronGUI.py4 = py4
        except ValueError:
            pass

    def mostrar_menu_fronteras_epocas(self):
        # Crear una ventana emergente para ingresar el número de fronteras y épocas
        fe_window = tk.Toplevel(self.root)
        fe_window.title("Fronteras y Épocas")

        ttk.Label(fe_window, text="Número de Fronteras (2-4):").grid(column=0, row=0)
        num_fronteras_entry = ttk.Entry(fe_window)
        num_fronteras_entry.grid(column=1, row=0)

        ttk.Label(fe_window, text="Número de Épocas (>=1):").grid(column=0, row=1)
        num_epocas_entry = ttk.Entry(fe_window)
        num_epocas_entry.grid(column=1, row=1)

        # Botón para guardar los valores en variables globales
        ttk.Button(fe_window, text="Guardar", command=lambda: self.guardar_fronteras_epocas(num_fronteras_entry.get(), num_epocas_entry.get())).grid(column=0, row=2, columnspan=2)

    def guardar_fronteras_epocas(self, num_fronteras, num_epocas):
        # Validar que los valores sean números válidos antes de guardarlos en variables globales
        try:
            num_fronteras = int(num_fronteras)
            num_epocas = int(num_epocas)
            if 2 <= num_fronteras <= 4:
                PerceptronGUI.numFronteras = num_fronteras
            if num_epocas >= 1:
                PerceptronGUI.numEpocas = num_epocas
        except ValueError:
            pass

    def mostrar_menu_parametros(self):
        # Crear una ventana emergente para ingresar el coeficiente y el intervalo
        parametros_window = tk.Toplevel(self.root)
        parametros_window.title("Parámetros")

        ttk.Label(parametros_window, text="Coeficiente (>0):").grid(column=0, row=0)
        coeficiente_entry = ttk.Entry(parametros_window)
        coeficiente_entry.grid(column=1, row=0)

        ttk.Label(parametros_window, text="Intervalo (>0):").grid(column=0, row=1)
        intervalo_entry = ttk.Entry(parametros_window)
        intervalo_entry.grid(column=1, row=1)

        # Botón para guardar los valores en variables globales
        ttk.Button(parametros_window, text="Guardar", command=lambda: self.guardar_parametros(coeficiente_entry.get(), intervalo_entry.get())).grid(column=0, row=2, columnspan=2)

    def guardar_parametros(self, coeficiente, intervalo):
        # Validar que los valores sean números válidos antes de guardarlos en variables globales
        try:
            coeficiente = float(coeficiente)
            intervalo = float(intervalo)
            if coeficiente > 0:
                self.coeficiente = coeficiente
            if intervalo > 0:
                self.intervalo = intervalo
        except ValueError:
            pass

    def mostrar_menu_agregar_puntos(self):
        # Crear una ventana emergente para ingresar una coordenada x, y
        puntos_window = tk.Toplevel(self.root)
        puntos_window.title("Agregar Puntos")

        ttk.Label(puntos_window, text="Coordenada X:").grid(column=0, row=0)
        x_entry = ttk.Entry(puntos_window)
        x_entry.grid(column=1, row=0)

        ttk.Label(puntos_window, text="Coordenada Y:").grid(column=0, row=1)
        y_entry = ttk.Entry(puntos_window)
        y_entry.grid(column=1, row=1)

        # Botón para agregar el punto a la lista y en la variable global puntosUser
        ttk.Button(puntos_window, text="Agregar", command=lambda: self.agregar_punto(x_entry.get(), y_entry.get())).grid(column=0, row=2, columnspan=2)

    def agregar_punto(self, x, y):
        # Validar que x y y sean números válidos antes de agregarlos a la lista de puntos y a la variable global puntosUser
        try:
            x = float(x)
            y = float(y)
            self.puntos.append((x, y))
            PerceptronGUI.puntosUser.append((x, y))
        except ValueError:
            pass

    def graficar(self):
        # Realizar la gráfica utilizando los valores ingresados
        if self.puntos:
            # Crear una gráfica simple (puedes personalizarla según tus necesidades)
            x_vals = [p[0] for p in self.puntos]
            y_vals = [p[1] for p in self.puntos]
            plt.scatter(x_vals, y_vals)
            plt.xlabel("Coordenada X")
            plt.ylabel("Coordenada Y")
            plt.title("Gráfica de Puntos")
            plt.grid()
            plt.show()
        else:
            tk.messagebox.showinfo("Información", "Agrega puntos antes de graficar.")

def main():
    root = tk.Tk()
    app = PerceptronGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

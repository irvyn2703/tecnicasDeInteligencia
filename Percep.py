import numpy as np
import matplotlib.pyplot as plt

# Datos de entrada (p) y objetivos (t)
p = np.array([[0.7, 1.5, 2.0, 0.9, 4.2, 2.2, 3.6, 4.5],
              [3, 5, 9, 11, 0, 1, 7, 6]])
t = np.array([[0, 0, 0, 0, 1, 1, 1, 1],
              [0, 0, 1, 1, 0, 0, 1, 1]])

# Inicialización de pesos y sesgos
w = 2 * np.random.rand(2, 2) - 1
b = 2 * np.random.rand(2, 1) - 1


# Entrenamiento del perceptrón
for Epocas in range(30):
    for q in range(8):
        e = t[:, q].reshape(2, 1) - np.heaviside(np.dot(w, p[:, q].reshape(2, 1)) + b, 1)
        w = w + np.dot(e, p[:, q].reshape(1, 2))
        b = b + e

# Muestra el error final
print(e)

# Gráfica para verificar visualmente
plt.figure()
plt.plot(p[0, :2], p[1, :2], 'bx')
plt.plot(p[0, 2:4], p[1, 2:4], 'bo')
plt.plot(p[0, 4:6], p[1, 4:6], 'kx')
plt.plot(p[0, 6:], p[1, 6:], 'ko')
p1 = np.arange(0, 6, 0.01)
plt.plot(p1, (-b[0] / w[0, 1] - (w[0, 0] / w[0, 1]) * p1).flatten())
plt.plot(p1, (-b[1] / w[1, 1] - (w[1, 0] / w[1, 1]) * p1).flatten())
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Perceptron Training')
plt.legend(['Class 1', 'Class 2', 'Decision Boundary 1', 'Decision Boundary 2'])
plt.grid(True)
plt.show()

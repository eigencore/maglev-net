import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Parámetros del sistema
m = 0.068          # kg
Ke = 6.53e-5       # N·m²/A²
R = 10             # Ohm
L = 0.4125         # H
g = 9.81           # m/s²
a0 = 0.007         # m (posición nominal)
i0 = np.sqrt((m * g * a0**2) / Ke)  # A (corriente de equilibrio)

print(f"Corriente de equilibrio i0 = {i0:.4f} A")

# Modelo linealizado - Matrices del espacio de estados
A = np.array([
    [0, 1, 0],
    [(Ke * i0**2) / (m * a0**3), 0, (Ke * i0) / (m * a0**2)],
    [0, 0, -R/L]
])

B = np.array([
    [0],
    [0], 
    [1/L]
])

C = np.eye(3)  # Matriz identidad 3x3

D = np.zeros((C.shape[0], B.shape[1]))  # Matriz de ceros

print("\nMatrices del sistema:")
print(f"Matriz A:\n{A}")
print(f"\nMatriz B:\n{B}")
print(f"\nMatriz C:\n{C}")
print(f"\nMatriz D:\n{D}")

# Crear el sistema en espacio de estados usando scipy
sistema = signal.StateSpace(A, B, C, D)

print(f"\nSistema en espacio de estados creado:")
print(f"Orden del sistema: {sistema.nstates}")
print(f"Número de entradas: {sistema.ninputs}")
print(f"Número de salidas: {sistema.noutputs}")

# Análisis de estabilidad - Valores propios
eigenvalues = np.linalg.eigvals(A)
print(f"\nValores propios del sistema:")
for i, eigenval in enumerate(eigenvalues):
    if np.isreal(eigenval):
        print(f"λ{i+1} = {eigenval.real:.4f}")
    else:
        print(f"λ{i+1} = {eigenval.real:.4f} + {eigenval.imag:.4f}j")

# Verificar estabilidad
stable = all(np.real(eigenval) < 0 for eigenval in eigenvalues)
print(f"\nEl sistema es {'estable' if stable else 'inestable'}")

# Ejemplo de simulación de respuesta al escalón
t = np.linspace(0, 2, 1000)  # Vector de tiempo de 0 a 2 segundos
tout, yout = signal.step(sistema, T=t)

# Graficar la respuesta (opcional - descomenta para visualizar)
"""
plt.figure(figsize=(12, 8))
for i in range(3):
    plt.subplot(3, 1, i+1)
    plt.plot(tout, yout[:, i])
    plt.title(f'Respuesta al escalón - Estado {i+1}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel(f'Estado {i+1}')
    plt.grid(True)

plt.tight_layout()
plt.show()
"""
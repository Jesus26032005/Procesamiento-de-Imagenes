import numpy as np
import cv2

# --- Ejemplo: matriz imagen pequeña (reemplaza con tus valores reales) ---
imagen_matriz = np.array([
    [180, 180, 179, 179, 245, 10, 10],
    [179, 181, 178, 245, 245, 10, 10],
    [179, 180, 170, 245, 10, 8, 15],
    [182, 180, 38, 159, 7, 14, 16],
    [201, 200, 247, 6, 3, 0, 2],
    [240, 245, 110, 12, 9, 1, 3],
    [125, 125, 121, 218, 225, 12, 9]
], dtype=np.float32)  # ajusta según tus datos

# Si tienes una imagen en archivo:
# imagen = cv2.imread('diapositiva_recortada.png', cv2.IMREAD_GRAYSCALE).astype(np.float32)

# --- Máscaras de la diapositiva ---
h1 = np.ones((3,3), dtype=np.float32)      # todos 1
h2 = -1 * np.ones((3,3), dtype=np.float32) # todos -1
h2[1,1] = 4                                # centro 8

# --- Correlación con filter2D (cv2.filter2D hace correlación por defecto) ---
corr_h1 = cv2.filter2D(imagen_matriz, ddepth=-1, kernel=h1, borderType=cv2.BORDER_CONSTANT)
corr_h2 = cv2.filter2D(imagen_matriz, ddepth=-1, kernel=h2, borderType=cv2.BORDER_CONSTANT)

# --- Convolución: rotamos el kernel 180° y aplicamos filter2D (o usar scipy.signal.convolve2d) ---
h1_rot = np.flip(h1, (0,1))
h2_rot = np.flip(h2, (0,1))

conv_h1 = cv2.filter2D(imagen_matriz, ddepth=-1, kernel=h1_rot, borderType=cv2.BORDER_CONSTANT)
conv_h2 = cv2.filter2D(imagen_matriz, ddepth=-1, kernel=h2_rot, borderType=cv2.BORDER_CONSTANT)

# --- Mostrar resultados por consola ---
np.set_printoptions(linewidth=200, precision=1, suppress=True)
print("Imagen (entrada):\n", imagen_matriz, "\n")
print("Correlacion con h1:\n", corr_h1, "\n")
print("Convolucion con h1:\n", conv_h1, "\n")
print("Correlacion con h2:\n", corr_h2, "\n")
print("Convolucion con h2:\n", conv_h2, "\n")

# Importar librerías necesarias
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
# 1. Lectura de imagen con Pillow
# 2. Lectura de imagen con OpenCV
imagen_cv = cv2.imread("Practica1/images.jpg")
imagen_cv_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)

# 3. Visualización de modelos de color
# RGB
r, g, b = cv2.split(imagen_cv_rgb)
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(r, cmap="Reds")
plt.title("Canal R")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(g, cmap="Greens")
plt.title("Canal G")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(b, cmap="Blues")
plt.title("Canal B")
plt.axis("off")
plt.suptitle("Modelo RGB")

plt.show()
# HSV
imagen_hsv = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(imagen_hsv)
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(h, cmap="hsv")
plt.title("Canal H")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(s, cmap="gray")
plt.title("Canal S")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(v, cmap="gray")
plt.title("Canal V")
plt.axis("off")
plt.suptitle("Modelo HSV")
plt.show()
# CMY (simulado, ya que OpenCV no lo soporta directamente)
imagen_cmy = 255 - imagen_cv_rgb
c, m, y = cv2.split(imagen_cmy)
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(c, cmap="Blues")
plt.title("Canal C")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(m, cmap="Purples")
plt.title("Canal M")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(y, cmap="Oranges")
plt.title("Canal Y")
plt.axis("off")
plt.suptitle("Modelo CMY (simulado)")
plt.show()
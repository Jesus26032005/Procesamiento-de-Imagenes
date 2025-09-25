# Importar librerías necesarias
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 2. Lectura de imagen con OpenCV
imagen_cv = cv2.imread("images.jpg")
imagen_cv_rgb = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(5, 5))
plt.title("Imagen con OpenCV (RGB)")
plt.imshow(imagen_cv_rgb)
plt.axis("off")
plt.show()

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
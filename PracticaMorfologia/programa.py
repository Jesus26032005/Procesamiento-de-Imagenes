import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen en escala de grises
imagen = cv2.imread('PracticaMorfologia/bolillo.jpg', cv2.IMREAD_GRAYSCALE)
# Mostrar la imagen original
plt.imshow(imagen, cmap='gray')
plt.title('Imagen Original')
plt.show()

### EROSION DE LA IMAGEN
# Definir el kernel para la erosión
kernel = np.ones((5,5), np.uint8)
# Aplicar la operación de erosión
imagen_erosionada = cv2.erode(imagen, kernel, iterations = 1) 
# Mostrar la imagen erosionada
plt.imshow(imagen_erosionada, cmap='gray')
plt.title('Imagen Erosionada')
plt.show()

### DILATACION DE LA IMAGEN
# Aplicar la operación de dilatación
imagen_dilatada = cv2.dilate(imagen, kernel, iterations = 1)
# Mostrar la imagen dilatada
plt.imshow(imagen_dilatada, cmap='gray')
plt.title('Imagen Dilatada')
plt.show()


### APERTURA DE LA IMAGEN
# Aplicar la operación de apertura
imagen_apertura = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)
# Mostrar la imagen con apertura
plt.imshow(imagen_apertura, cmap='gray')
plt.title('Imagen con Apertura')
plt.show()


### CIERRE DE LA IMAGEN
# Aplicar la operación de cierre
imagen_cierre = cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, kernel)
# Mostrar la imagen con cierre
plt.imshow(imagen_cierre, cmap='gray')
plt.title('Imagen con Cierre')
plt.show()
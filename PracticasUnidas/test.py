import cv2
import numpy as np
import matplotlib.pyplot as plt

# Implementación validada de la Entropía de Kapur
def entropia_kapur(histograma, total_pixeles):
    max_entropia = -1
    umbral_optimo = 0
    for t in range(256):
        # Dividir el histograma en dos clases
        clase1 = histograma[:t]
        clase2 = histograma[t:]
        
        # Sumas de conteos (proporcionales a probabilidades P1 y P2)
        sum_c1 = np.sum(clase1)
        sum_c2 = np.sum(clase2)
        
        # Evitar división por cero
        if sum_c1 == 0 or sum_c2 == 0:
            continue
            
        # Probabilidades a priori
        p1 = sum_c1 / total_pixeles
        p2 = sum_c2 / total_pixeles
        
        # Calcular la entropía de cada clase
        # Se filtra para evitar log(0)
        prob1 = clase1 / sum_c1
        prob1 = prob1[prob1 > 0]
        entropia1 = -np.sum(prob1 * np.log(prob1))

        prob2 = clase2 / sum_c2
        prob2 = prob2[prob2 > 0]
        entropia2 = -np.sum(prob2 * np.log(prob2))
        
        # Entropía total (criterio de Kapur)
        entropia_total = p1 * entropia1 + p2 * entropia2
        print("Entropía total:", entropia_total)
        print(max_entropia)

        if entropia_total > max_entropia:
            max_entropia = entropia_total
            umbral_optimo = t
            
    return umbral_optimo

#Simulación de carga y procesamiento
imagen = cv2.imread('Imagenes/bolillomoho.jpg', cv2.IMREAD_GRAYSCALE)
total_pixeles = imagen.shape[0] * imagen.shape[1]
histograma, _ = np.histogram(imagen, bins=256, range=(0, 256))
umbral_kapur = entropia_kapur(histograma, total_pixeles)

print("Umbral de Kapur:", umbral_kapur)
imagen_kapur = (imagen > umbral_kapur).astype(np.uint8) * 255
plt.imshow(imagen_kapur, cmap='gray')
plt.show()
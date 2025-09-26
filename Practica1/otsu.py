import cv2
import numpy as np

def otsu_manual(imagen):
    hist_norm = hist / hist.sum()

    # 3. Inicializar variables
    var_max = 0
    mejor_umbral = 0

    # 4. Recorrer todos los posibles umbrales (0–255)
    for t in range(256):
        # Pesos (probabilidad total de cada grupo)
        w0 = hist_norm[:t+1].sum()   # clase 0 (<= t)
        w1 = hist_norm[t+1:].sum()   # clase 1 (> t)

        if w0 == 0 or w1 == 0:
            continue

        mu0 = np.dot(np.arange(0, t+1), hist_norm[:t+1]) / w0
        mu1 = np.dot(np.arange(t+1, 256), hist_norm[t+1:]) / w1
        var_between = w0 * w1 * (mu0 - mu1) ** 2
        if var_between > var_max:
            var_max = var_between
            mejor_umbral = t
    return mejor_umbral


# ===========================
# EJEMPLO DE USO
# ===========================
# Cargar imagen en escala de grises
imagen = cv2.imread("foto.jpg", 0)

# Calcular umbral óptimo con Otsu (manual)
umbral = otsu_manual(imagen)
print("Umbral óptimo según Otsu =", umbral)

# Aplicar binarización con el umbral encontrado
_, binarizada = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY)

# Guardar resultado
cv2.imwrite("binarizada_otsu_manual.jpg", binarizada)

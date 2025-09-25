import numpy as np

# Matriz A
A = np.array([
    [170, 125,   1,  85, 224, 255, 239,  15],
    [218, 118,  98,   1, 200, 254,  35,  97],
    [ 41, 101,  98,  11, 210, 200,  35,  95],
    [ 23,  15,   7, 147, 208, 200, 200,  16],
    [  4,   6,  13,  20, 210, 210,  22,  22],
    [ 10,   4,  20,  20, 226, 23,  23,  22],
    [ 10,  12,  19,  21, 226, 226,  22,  23],
    [  1,  18, 125,  22, 226, 104,   9,   9]
])

# Aplanamos la matriz porque ocupamos que se lea de manera lineal
pixels = A.flatten()
# Número total de pixeles xd
N = len(pixels)
print(N)
# contamos ocurrencias de cada valor de pixel, unico es el valor del pixel y counts es el número de ocurrencias
unico, conteo = np.unique(pixels, return_counts=True)
P = conteo / N  # Probabilidad a todos los valores

# Media
sumatotal= np.sum(pixels)
media=np.sum(pixels) / N

media, resultadoMedia = np.sum(unico * P), unico * P
entropia, resultadoEntropia = -np.sum(P * np.log2(P)), P * np.log2(P)
varianza, resultadoAcontar = np.sum(((unico - media) ** 2) * P),  ((unico - media) ** 2) * P
asimetria, resultadoAsimetria = np.sum(((unico - media) ** 3) * P),  ((unico - media) ** 3) * P
energia, resultadoEnergia = np.sum(P ** 2), P ** 2

varianzaSimple = np.sqrt(varianza)

print(f"Media: {media}, Entropia: {entropia}, Varianza: {varianza}, Desviación Estándar: {varianzaSimple}, Asimetría: {asimetria}, Energía: {energia}")
# print(f"Media desglosada:")
# # for i in range(len(unico)):
# #     print(f"Valor: {unico[i]}, P: {P[i]}, Aporte a la media: {resultadoMedia[i]}")
print(f"Entropía desglosada:")
for i in range(len(unico)):
    print(f"Valor: {unico[i]}, P: {P[i]}, Aporte a la entropía: {resultadoEntropia[i]}")
# print(f"Varianza desglosada:")
# for i in range(len(unico)):
#     print(f"Valor: {unico[i]}, P: {P[i]}, Aporte a la varianza: {resultadoAcontar[i]}")
# print(f"Asimetría desglosada:")
# for i in range(len(unico)):
#     print(f"Valor: {unico[i]}, P: {P[i]}, Aporte a la asimetría: {resultadoAsimetria[i]}")
# print(f"Energía desglosada:")
# for i in range(len(unico)):
#     print(f"Valor: {unico[i]}, P: {P[i]}, Aporte a la energía: {resultadoEnergia[i]}")
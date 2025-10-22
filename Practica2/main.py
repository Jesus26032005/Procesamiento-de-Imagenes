"""
Practica2 - Pseudocolores y mapas personalizados
Autores:
    - Zaddkiel de Jesus Martinez Alor
Autores Adicionales:
    - María Elena Cruz Meza
        Creador de la mayor parte del código, a excepcion de la creacion de los mapas de colores personalizados.
Descripción:
    Script de ejemplo que carga una imagen en escala de grises y muestra
    diferentes pseudocolores (colormaps) aplicados a la misma. Se incluyen
    mapas de color predefinidos de OpenCV (JET, HOT, OCEAN) y colormaps
    personalizados creados con Matplotlib.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
# ---------------------------
# Carga de la imagen (gris)
# ---------------------------
# Se carga la imagen en escala de grises. Ajusta la ruta si es necesario.
imagen_gris = cv2.imread('Practica2/imagenCabezaZadd.jpg', cv2.IMREAD_GRAYSCALE)
if imagen_gris is None:
    # Mensaje claro para el usuario y salida segura
    print("Error al cargar la imagen: 'Practica2/imagenCabezaZadd.jpg' no encontrada.")
    exit(1)
# ---------------------------
# Colormaps OpenCV (rapidez)
# ---------------------------
# OpenCV proporciona tablas predefinidas de color que mapean valores
# escala de grises [0..255] a colores BGR. Aquí se generan algunas versiones
# rápidas para comparación.
imagen_jet = cv2.applyColorMap(imagen_gris, cv2.COLORMAP_JET)
imagen_hot = cv2.applyColorMap(imagen_gris, cv2.COLORMAP_HOT)
imagen_ocean = cv2.applyColorMap(imagen_gris, cv2.COLORMAP_OCEAN)
# ---------------------------
# Colormaps personalizados (Matplotlib)
# ---------------------------
# Definimos listas de colores como tuplas RGB normalizadas en [0, 1].
# LinearSegmentedColormap.from_list crea un colormap interpolando
# entre estos colores.
colores_pastel = [
    (1.0, 0.8, 0.9),  # rosa claro
    (0.8, 1.0, 0.8),  # verde menta
    (0.8, 0.9, 1.0),  # azul lavanda
    (1.0, 1.0, 0.8),  # amarillo suave
    (0.9, 0.8, 1.0)   # violeta claro
]
# 'N=256' indica la resolución interna del mapa (256 niveles). No es
# obligatorio pero es común para mapas continuos.
mapa_pastel = LinearSegmentedColormap.from_list("PastelMap", colores_pastel, N=256)


coloresTron = [
    (0/255, 14/255, 82/255),   # oscuro
    (0/255, 27/255, 145/255),  # medio
    (122/255, 147/255, 255/255)  # claro
]
mapa_tron = LinearSegmentedColormap.from_list("TronMap", coloresTron, N=256)


coloresTronAres = [
    (64/255, 0/255, 32/255),   # oscuro
    (130/255, 0/255, 7/255),   # medio
    (255/255, 207/255, 208/255)  # claro (normalizado correctamente)
]
mapa_tron_ares = LinearSegmentedColormap.from_list("TronAresMap", coloresTronAres, N=256)

coloresDivisiones = [
    (176/255, 0/255, 167/255),  # violeta
    (0/255, 176/255, 47/255),   # verde
    (176/255, 91/255, 0/255)    # naranja
]
# Aquí utilizamos N=3 porque queremos 3 bandas discretas (sin interpolación
# fina entre ellas)
mapa_divisiones = LinearSegmentedColormap.from_list("DivisionesMap", coloresDivisiones, N=3)

coloresArcoiris = [
    (148/255, 0/255, 211/255),  # violeta
    (75/255, 0/255, 130/255),   # índigo
    (0/255, 0/255, 255/255),    # azul
    (0/255, 130/255, 20/255),   # verde
    (240/255, 240/255, 0/255),  # amarillo
    (240/255, 120/255, 0/255),  # naranja
    (255/255, 0/255, 0/255)     # rojo
]
mapa_arcoiris = LinearSegmentedColormap.from_list("ArcoirisMap", coloresArcoiris, N=7)

# ---------------------------
# Visualización con Matplotlib
# ---------------------------
# Creamos una figura con 4 filas x 2 columnas para comparar los resultados.
fig, axs = plt.subplots(4, 2, figsize=(10, 8))

# Escala de grises (imagen original)
axs[0, 0].imshow(imagen_gris, cmap='gray')
axs[0, 0].set_title('Escala de grises')

# OpenCV -> BGR a RGB para Matplotlib
axs[0, 1].imshow(cv2.cvtColor(imagen_jet, cv2.COLOR_BGR2RGB))
axs[0, 1].set_title('Pseudocolor: JET')

axs[1, 0].imshow(cv2.cvtColor(imagen_hot, cv2.COLOR_BGR2RGB))
axs[1, 0].set_title('Pseudocolor: HOT')

# Uso de un colormap de Matplotlib directamente sobre la imagen en gris.
# Matplotlib mappea los valores escala-de-grises (0..255) a colores.
axs[1, 1].imshow(imagen_gris, cmap=mapa_pastel)
axs[1, 1].set_title('Pseudocolor: Pastel (Matplotlib)')

axs[2, 0].imshow(imagen_gris, cmap=mapa_tron)
axs[2, 0].set_title('Pseudocolor: Tron (Matplotlib)')

axs[2, 1].imshow(imagen_gris, cmap=mapa_tron_ares)
axs[2, 1].set_title('Pseudocolor: Tron Ares (Matplotlib)')

axs[3, 0].imshow(imagen_gris, cmap=mapa_divisiones)
axs[3, 0].set_title('Pseudocolor: Divisiones (Matplotlib)')

axs[3, 1].imshow(imagen_gris, cmap=mapa_arcoiris)
axs[3, 1].set_title('Pseudocolor: Arcoiris (Matplotlib)')

# Quitar ejes para una visualización más limpia
for ax in axs.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()

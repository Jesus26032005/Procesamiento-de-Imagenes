"""
===============================================================================
                            DERECHOS DE AUTOR
===============================================================================
© 2025 - Práctica 2 Minireto- "Mejoramiento de una imagen"

Autores:
Dominguez Jimenez Ana Andrea
Miranda Ferreyra Uriel
Salas Velazquez Orlando
Martinez Alor Zaddkiel de Jesus
Urbina Garcidueñas Luis Jesus

Materia: Procesamiento De Imagenes
Semestre: Cuarto Semestre
Institución: Escuela Superior de Cómputo, Instituto Politécnico Nacional

Este código es de uso académico y está protegido por derechos de autor.
Prohibida su reproducción parcial o total sin autorización del autor.

Fecha de creación: Noviembre 2025
Versión: 1.0
===============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('Agg')

class HistogramUtils:
    @staticmethod
    def calculate_histogram(image):
        if len(image.shape) == 3:
            # Imagen a color
            colors = ('b', 'g', 'r')
            histograms = []
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                histograms.append((color, hist))
            return histograms
        else:
            # Imagen en escala de grises
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            return [('gray', hist)]
    
    @staticmethod
    def plot_histogram(histograms, title="Histograma"):
        fig, ax = plt.subplots(figsize=(6, 4))
        
        for color, hist in histograms:
            ax.plot(hist, color=color, label=color.upper())
        
        ax.set_title(title)
        ax.set_xlabel('Niveles de intensidad')
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        return fig
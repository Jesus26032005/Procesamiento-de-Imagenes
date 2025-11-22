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

class LinearFilters:
    @staticmethod
    def average_filter(image, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        return cv2.filter2D(image, -1, kernel)
    
    @staticmethod
    def weighted_average_filter(image, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.float32)
        center = kernel_size // 2
        kernel[center, center] = kernel_size * 2
        kernel /= kernel.sum()
        return cv2.filter2D(image, -1, kernel)
    
    @staticmethod
    def gaussian_filter(image, kernel_size=3, sigma=1.0):
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    
    @staticmethod
    def Bilateral_filter(image, diameter=9, sigma_color=75, sigma_space=75):
        return cv2.bilateralFilter(image, diameter, sigma_color, sigma_space)
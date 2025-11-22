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
from scipy import ndimage
import scipy.stats

class NonLinearFilters:
    @staticmethod
    def median_filter(image, kernel_size=3):
        return cv2.medianBlur(image, kernel_size)
    
    @staticmethod
    def mode_filter(image, kernel_size=3):
        def _mode_filter_2d(channel):
            def mode_func(x):
                values, counts = np.unique(x, return_counts=True)
                return values[np.argmax(counts)]
            return ndimage.generic_filter(
                channel, 
                mode_func, 
                size=kernel_size
            )
        
        if len(image.shape) == 3:
            channels = []
            for i in range(3):
                channels.append(_mode_filter_2d(image[:,:,i]))
            return np.stack(channels, axis=2)
        else:
            return _mode_filter_2d(image)
        
    @staticmethod
    def max_filter(image, kernel_size=3):
        return cv2.dilate(image, np.ones((kernel_size, kernel_size)))
    
    @staticmethod
    def min_filter(image, kernel_size=3):
        return cv2.erode(image, np.ones((kernel_size, kernel_size)))
    
    @staticmethod
    def adaptive_median_filter(image, max_window_size=7):
        def process_pixel(i, j):
            window_size = 3
            while window_size <= max_window_size:
                half = window_size // 2
                window = image[
                    max(0, i-half):min(image.shape[0], i+half+1),
                    max(0, j-half):min(image.shape[1], j+half+1)
                ]
                
                # Calcular Z_min, Z_max y Z_med
                if len(image.shape) == 3:
                    vectors = window.reshape(-1, 3).astype(float)
                    N = len(vectors) 

                    magnitudes = np.sum(vectors, axis=1) 
                    z_min = vectors[np.argmin(magnitudes)].astype(np.uint8)
                    z_max = vectors[np.argmax(magnitudes)].astype(np.uint8)

                    min_distance_sum = float('inf')
                    z_med = np.zeros(3, dtype=np.uint8)

                    for k in range(N):
                        actual_vector = vectors[k]
                        distances = np.linalg.norm(vectors - actual_vector, axis=1)
                        distance_sum = np.sum(distances)
                        
                        if distance_sum < min_distance_sum:
                            min_distance_sum = distance_sum
                            z_med = actual_vector.astype(np.uint8) 
                else:
                    z_min = np.min(window)
                    z_max = np.max(window)
                    z_med = np.median(window)
                
                isEqual = False
                if len(image.shape) == 3: isEqual = np.array_equal(z_med, z_min) or np.array_equal(z_med, z_max)
                else: isEqual = z_med == z_min or z_med == z_max

                if isEqual:
                    window_size += 2
                    if window_size > max_window_size:
                        return z_med
                else:
                    current_pixel= image[i, j]
                    if len(image.shape) == 3:
                        if np.array_equal(current_pixel, z_min) or np.array_equal(current_pixel, z_max):
                            return z_med
                        else:
                            return current_pixel
                    else:
                        if z_min < current_pixel < z_max:
                            return current_pixel
                        else:
                            return z_med
            return image[i, j]
        
        if len(image.shape) == 3:
            result = np.zeros_like(image)
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    result[i, j] = process_pixel(i, j)
            return result
        else:
            result = np.zeros_like(image)
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    result[i, j] = process_pixel(i, j)
            return result
    
    @staticmethod
    def contraharmonic_mean_filter(image, kernel_size=3, Q=1.5):
        def contraharmonic_mean(channel):
            kernel = np.ones((kernel_size, kernel_size))
            padding = kernel_size // 2
            
            padded = np.pad(channel.astype(np.float64), padding, mode='reflect')
            result = np.zeros_like(channel, dtype=np.float64)
            
            for i in range(channel.shape[0]):
                for j in range(channel.shape[1]):
                    window = padded[i:i+kernel_size, j:j+kernel_size]
                    
                    numerator = np.sum(window ** (Q + 1))
                    denominator = np.sum(window ** Q)
                    
                    if denominator != 0:
                        result[i, j] = numerator / denominator
                    else:
                        result[i, j] = channel[i, j]
            
            return np.clip(result, 0, 255).astype(np.uint8)
        
        if len(image.shape) == 3:
            channels = []
            for i in range(3):
                channels.append(contraharmonic_mean(image[:, :, i]))
            return np.stack(channels, axis=2)
        else:
            return contraharmonic_mean(image)
        
    @staticmethod
    def weighted_median_filter(image, kernel_size=3, weights=None):
        if weights is None:
            center = kernel_size // 2
            y, x = np.ogrid[-center:kernel_size-center, -center:kernel_size-center]
            weights = np.exp(-(x**2 + y**2) / (2*(center/2)**2))
            weights = weights / weights.sum() * kernel_size**2
            weights = np.round(weights).astype(int)
        
        def weighted_median(channel):
            padding = kernel_size // 2
            padded = np.pad(channel, padding, mode='reflect')
            result = np.zeros_like(channel)
            
            for i in range(channel.shape[0]):
                for j in range(channel.shape[1]):
                    window = padded[i:i+kernel_size, j:j+kernel_size]
                    
                    weighted_list = []
                    for w_i in range(kernel_size):
                        for w_j in range(kernel_size):
                            weight = weights[w_i, w_j]
                            pixel_value = window[w_i, w_j]
                            weighted_list.extend([pixel_value] * weight)
                    
                    result[i, j] = np.median(weighted_list)
            
            return result.astype(np.uint8)
        
        if len(image.shape) == 3:
            channels = []
            for i in range(3):
                channels.append(weighted_median(image[:, :, i]))
            return np.stack(channels, axis=2)
        else:
            return weighted_median(image)
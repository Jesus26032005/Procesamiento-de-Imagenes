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
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from Filtros.Filtros_Lineales import LinearFilters
from Filtros.Filtros_NoLineales import NonLinearFilters
from Utilidades.Histograma import HistogramUtils

class ImageModel:
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.history = []
        self.linear_filters = LinearFilters()
        self.nonlinear_filters = NonLinearFilters()
        self.histogram_utils = HistogramUtils()
    
    def load_image(self, file_path):
        try:
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                raise ValueError("No se pudo cargar la imagen")
            
            self.current_image = self.original_image.copy()
            self.history = [self.current_image.copy()]
            return True
        except Exception as e:
            raise e
    
    def convert_to_grayscale(self):
        if self.current_image is not None:
            if len(self.current_image.shape) == 3:
                self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            self._add_to_history()
            return True
        return False
    
    def add_salt_pepper_noise(self, amount=0.05):
        if self.current_image is not None:
            noisy_image = self.current_image.copy()
            
            salt_mask = np.random.random(noisy_image.shape[:2]) < amount/2
            if len(noisy_image.shape) == 3:
                noisy_image[salt_mask] = [255, 255, 255]
            else:
                noisy_image[salt_mask] = 255
            
            pepper_mask = np.random.random(noisy_image.shape[:2]) < amount/2
            if len(noisy_image.shape) == 3:
                noisy_image[pepper_mask] = [0, 0, 0]
            else:
                noisy_image[pepper_mask] = 0
            
            self.current_image = noisy_image
            self._add_to_history()
            return True
        return False
    
    def add_gaussian_noise(self, mean=0, sigma=25):
        if self.current_image is not None:
            noisy_image = self.current_image.copy().astype(np.float64)
            
            gaussian_noise = np.random.normal(mean, sigma, noisy_image.shape)
            noisy_image += gaussian_noise
            
            noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
            self.current_image = noisy_image
            self._add_to_history()
            return True
        return False
    
    def apply_average_filter(self, kernel_size=3):
        if self.current_image is not None:
            self.current_image = self.linear_filters.average_filter(
                self.current_image, kernel_size
            )
            self._add_to_history()
            return True
        return False
    
    def apply_weighted_average_filter(self, kernel_size=3):
        if self.current_image is not None:
            self.current_image = self.linear_filters.weighted_average_filter(
                self.current_image, kernel_size
            )
            self._add_to_history()
            return True
        return False
    
    def apply_gaussian_filter(self, kernel_size=3, sigma=1.0):
        if self.current_image is not None:
            self.current_image = self.linear_filters.gaussian_filter(
                self.current_image, kernel_size, sigma
            )
            self._add_to_history()
            return True
        return False
    
    def apply_median_filter(self, kernel_size=3):
        if self.current_image is not None:
            self.current_image = self.nonlinear_filters.median_filter(
                self.current_image, kernel_size
            )
            self._add_to_history()
            return True
        return False
    
    def apply_mode_filter(self, kernel_size=3):
        if self.current_image is not None:
            self.current_image = self.nonlinear_filters.mode_filter(
                self.current_image, kernel_size
            )
            self._add_to_history()
            return True
        return False
    
    def apply_max_filter(self, kernel_size=3):
        if self.current_image is not None:
            self.current_image = self.nonlinear_filters.max_filter(
                self.current_image, kernel_size
            )
            self._add_to_history()
            return True
        return False
    
    def apply_min_filter(self, kernel_size=3):
        if self.current_image is not None:
            self.current_image = self.nonlinear_filters.min_filter(
                self.current_image, kernel_size
            )
            self._add_to_history()
            return True
        return False
    
    def apply_bilateral_filter(self, d=9, sigma_color=75, sigma_space=75):
        if self.current_image is not None:
            self.current_image = self.linear_filters.Bilateral_filter(
                self.current_image, d, sigma_color, sigma_space
            )
            self._add_to_history()
            return True
        return False
    
    def apply_adaptive_median_filter(self, max_window_size=7):
        if self.current_image is not None:
            self.current_image = self.nonlinear_filters.adaptive_median_filter(
                self.current_image, max_window_size
            )
            self._add_to_history()
            return True
        return False
    
    def apply_contraharmonic_mean_filter(self, kernel_size=3, Q=1.5):
        if self.current_image is not None:
            self.current_image = self.nonlinear_filters.contraharmonic_mean_filter(
                self.current_image, kernel_size, Q
            )
            self._add_to_history()
            return True
        return False
    
    def apply_weighted_median_filter(self, kernel_size=3, weights=None):
        if self.current_image is not None:
            self.current_image = self.nonlinear_filters.weighted_median_filter(
                self.current_image, kernel_size, weights
            )
            self._add_to_history()
            return True
        return False
    
    def get_histogram(self):
        return self.histogram_utils.calculate_histogram(self.current_image)
    
    def reset_to_original(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self._add_to_history()
            return True
        return False
    
    def _add_to_history(self):
        if self.current_image is not None:
            self.history.append(self.current_image.copy())
    
    def get_image_for_display(self, max_size=(400, 400)):
        if self.current_image is None:
            return None
        
        if len(self.current_image.shape) == 3:
            image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = self.current_image
        
        height, width = image_rgb.shape[:2]
        if height > max_size[0] or width > max_size[1]:
            scale = min(max_size[0]/height, max_size[1]/width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image_resized = cv2.resize(image_rgb, (new_width, new_height))
        else:
            image_resized = image_rgb
        
        if len(image_resized.shape) == 2:
            pil_image = Image.fromarray(image_resized)
        else:
            pil_image = Image.fromarray(image_resized.astype('uint8'))
        
        return ImageTk.PhotoImage(pil_image)
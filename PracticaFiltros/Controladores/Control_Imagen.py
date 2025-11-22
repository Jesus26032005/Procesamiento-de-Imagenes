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

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Modelos.Modelo_Imagen import ImageModel
from Vistas.Vista_Principal import MainView

class ImageController:
    def __init__(self, root):
        self.model = ImageModel()
        self.view = MainView(root, self)
        self.root = root
    
    def load_image(self):
        file_path = self.view.get_file_path()
        if file_path:
            try:
                success = self.model.load_image(file_path)
                if success:
                    self.update_display()
                else:
                    self.view.show_error("No se pudo cargar la imagen")
            except Exception as e:
                self.view.show_error(f"Error al cargar imagen: {str(e)}")
    
    def convert_to_grayscale(self):
        if self.model.convert_to_grayscale():
            self.update_display()
        else:
            self.view.show_error("No hay imagen cargada")
    
    def add_noise(self, noise_type):
        if noise_type == "salt_pepper":
            self.model.add_salt_pepper_noise()
            self.update_display()
        elif noise_type == "gaussian":
            self.model.add_gaussian_noise()
            self.update_display()
        else:
            self.view.show_error("No hay imagen cargada")
    
    def apply_linear_filter(self, filter_type):
        filter_methods = {
            "average": self.model.apply_average_filter,
            "weighted_average": self.model.apply_weighted_average_filter,
            "gaussian": self.model.apply_gaussian_filter,
            "bilateral": self.model.apply_bilateral_filter
        }
        
        if filter_type in filter_methods:
            if filter_methods[filter_type]():
                self.update_display()
            else:
                self.view.show_error("Error, no hay imagen cargada")
        else:
            self.view.show_error("Tipo de filtro lineal no reconocido")

    def apply_nonlinear_filter(self, filter_type):
        filter_methods = {
            "median": self.model.apply_median_filter,
            "mode": self.model.apply_mode_filter,
            "max": self.model.apply_max_filter,
            "min": self.model.apply_min_filter,
            "adaptive_median": self.model.apply_adaptive_median_filter,
            "contraharmonic_mean": self.model.apply_contraharmonic_mean_filter,
            "weighted_median": self.model.apply_weighted_median_filter
        }
        
        if filter_type in filter_methods:
            if filter_methods[filter_type]():
                self.update_display()
            else:
                self.view.show_error("Error, no hay imagen cargada")
        else:
            self.view.show_error("Tipo de filtro no lineal no reconocido")
    
    def reset_image(self):
        if self.model.reset_to_original():
            self.update_display()
        else:
            self.view.show_error("No hay imagen cargada")
    
    def update_display(self):
        photo_image = self.model.get_image_for_display()
        self.view.update_image_display(photo_image)
        
        histograms = self.model.get_histogram()
        self.view.update_histogram(histograms)
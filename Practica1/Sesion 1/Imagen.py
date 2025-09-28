"""
===============================================================================
                            DERECHOS DE AUTOR
===============================================================================
© 2025 - Práctica 1: Modelos de Color
Autor: Zaddkiel de Jesus Martinez Alor,Herrera Monroy Abraham Andre, Marcelino Lopez Jessica
Materia: Procesamiento De Imagenes
Semestre: Cuarto Semestre
Institución: Escuela Superior de Cómputo, Instituto Politécnico Nacional

Descripción: 
Aplicación de interfaz gráfica para visualización y análisis de diferentes 
modelos de color (RGB, HSV, CMY) usando ttkbootstrap, OpenCV y matplotlib.

Este código es de uso académico y está protegido por derechos de autor.
Prohibida su reproducción parcial o total sin autorización del autor.

Fecha de creación: Septiembre 2025
Versión: 1.0
===============================================================================
"""


# Importación de la librería PIL (Python Imaging Library) para manejo de imágenes
# Se importa Image con alias ImagenPillow, ImageTk para mostrar imágenes en tkinter,
# y UnidentifiedImageError para capturar errores de archivos no válidos
from PIL import Image as ImagenPillow, ImageTk, UnidentifiedImageError

# Importación de messagebox de tkinter para mostrar ventanas de error
from tkinter import messagebox

# Importación de OpenCV para procesamiento avanzado de imágenes
import cv2

# Importación de NumPy para manejo de arrays numéricos (matrices de píxeles)
import numpy as np

# Definición de la clase Imagen que manejará las operaciones con imágenes
class Imagen:
    # Constructor de la clase que inicializa los atributos
    def __init__(self, ruta=None):
        # Atributo para almacenar la imagen en formato OpenCV (numpy array)
        self.imagenCv = None
        # Atributo para almacenar la imagen en formato PIL
        self.imagenPil = None
        # Atributo para almacenar la ruta del archivo de imagen
        self.ruta = ruta

    # Método para cargar y procesar una imagen desde la ruta especificada
    def iniciarImagen(self):
        # Bloque try-except para manejo de errores al cargar la imagen
        try:
            # Abre la imagen desde la ruta usando PIL y la convierte a formato RGB
            self.imagenPil = ImagenPillow.open(self.ruta).convert("RGB")
            
            # Convierte la imagen PIL a un array de NumPy para uso con OpenCV
            self.imagenCv = np.array(self.imagenPil)
            
            # Define las dimensiones máximas para redimensionar la imagen (ancho, alto)
            max_dimension = (1400, 600)
            
            # Crea una copia de la imagen PIL para no modificar la original
            imagenAuxiliada = self.imagenPil.copy()
            
            # Redimensiona la imagen manteniendo la proporción usando algoritmo LANCZOS
            # (algoritmo de alta calidad para redimensionamiento)
            imagenAuxiliada.thumbnail(max_dimension, ImagenPillow.LANCZOS)

            # Convierte la imagen redimensionada a formato PhotoImage para mostrar en tkinter
            return ImageTk.PhotoImage(imagenAuxiliada)
            
        # Captura error cuando no se encuentra el archivo en la ruta especificada
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró la imagen en la ruta especificada.")
            return False
            
        # Captura error cuando el archivo no es una imagen válida o reconocible
        except UnidentifiedImageError:
            messagebox.showerror("Error", "El archivo seleccionado no es una imagen válida.")
            return False
            
        # Captura errores del sistema operativo (archivo dañado, formato no soportado)
        except OSError:
            messagebox.showerror("Error", "Error al abrir la imagen, archivo dañado o formato no soportado.")
            return False
            
        # Captura error cuando no se tienen permisos para acceder al archivo
        except PermissionError:
            messagebox.showerror("Error", "No se tienen los permisos necesarios para abrir la imagen.")
            return False 
            
        # Captura error cuando no hay suficiente memoria RAM para cargar la imagen
        except MemoryError:
            messagebox.showerror("Error", "No hay suficiente memoria para cargar la imagen.")
            return False 
            
        # Captura cualquier otro error no contemplado anteriormente
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado de tipo: {e}")
            return False
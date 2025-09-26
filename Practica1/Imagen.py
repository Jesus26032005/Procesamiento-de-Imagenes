"""
===============================================================================
                            DERECHOS DE AUTOR
===============================================================================
© 2025 - Práctica 1: Clase Imagen - Procesamiento de Imágenes
Autor: Zaddkiel de Jesús Martínez Alor
Materia: Procesamiento De Imagenes
Semestre: Cuarto Semestre
Institución: Escuela Superior de Cómputo, Instituto Politécnico Nacional

Descripción: 
Clase personalizada para el manejo y procesamiento de imágenes utilizando
PIL (Python Imaging Library), OpenCV y NumPy. Proporciona funcionalidades
para cargar la imagen de momento.

Este código es de uso académico y está protegido por derechos de autor.
Prohibida su reproducción parcial o total sin autorización del autor.

Fecha de creación: Septiembre 2025
Versión: 1.0
===============================================================================
"""

# Importación de PIL: Image como ImagenPillow para manipulación básica, ImageTk para integración con tkinter,
# UnidentifiedImageError para manejo de errores de archivos no válidos como imagen
from PIL import Image as ImagenPillow, ImageTk, UnidentifiedImageError
# Importación de messagebox desde tkinter para mostrar ventanas emergentes de error y notificación
from tkinter import messagebox
# Importación de NumPy para operaciones matemáticas eficientes con arrays multidimensionales
import numpy as np
# Importación de OpenCV para procesamiento avanzado de imágenes y visión computacional
import cv2

# Definición de la clase Imagen para encapsular operaciones de carga y procesamiento de imágenes
class Imagen:
    # Constructor de la clase - inicializa una instancia con una ruta de archivo opcional
    def __init__(self, ruta=None):
        # Atributo para almacenar la imagen en formato OpenCV (array NumPy) - utilizado para procesamiento
        self.imagenCv = None
        # Atributo para almacenar la imagen en formato PIL - utilizado para operaciones básicas y conversiones
        self.imagenPil = None
        # Atributo para almacenar la ruta del archivo de imagen - referencia al archivo original
        self.ruta = ruta

    # Método principal para cargar y procesar la imagen desde el archivo especificado
    def iniciarImagen(self):
        # Inicio del bloque try-except para manejo robusto de errores durante la carga
        try:
            # Carga de la imagen usando PIL y conversión forzada a modo RGB (3 canales de color)
            # Esto asegura compatibilidad independientemente del formato original (RGBA, L, etc.)
            self.imagenPil = ImagenPillow.open(self.ruta).convert("RGB")
            # Conversión de la imagen PIL a array NumPy para compatibilidad con OpenCV
            # np.array crea una representación matricial de la imagen para procesamiento matemático
            self.imagenCv = np.array(self.imagenPil)
            # Definición de dimensiones máximas para redimensionamiento (ancho: 1400px, alto: 600px)
            # Esto optimiza el rendimiento y evita problemas de memoria con imágenes muy grandes
            max_dimension = (1400, 600)
            # Creación de una copia de la imagen PIL para evitar modificar la original
            imagenAuxiliada = self.imagenPil.copy()
            # Redimensionamiento proporcional de la imagen:
            # El método thumbnail() ajusta la imagen para que quepa dentro de las dimensiones máximas dadas,
            # manteniendo la proporción (no la deforma) y modificando la imagen directamente en el mismo objeto.
            # Se suele usar con el filtro Image.LANCZOS, que ofrece alta calidad al reducir imágenes.
            # Hacerlo manualmente implicaría: Obtener el tamaño actual de la imagen (ancho y alto). Calcular la proporción de escala usando el tamaño máximo permitido usando la formula min(max_dimension[0]/ancho_actual, max_dimension[1]/alto_actual). Redimensionar con resize((nuevo_ancho, nuevo_alto), filtro).
            # Sobre los filtros de redimensionamiento:
            # - Image.NEAREST: usa el píxel más cercano, es rápido pero pixelado (baja calidad).
            # - Image.BILINEAR: promedia 4 píxeles vecinos, resultado más suave.
            # - Image.BICUBIC: usa 16 píxeles vecinos (interpolación cúbica), mejor calidad que BILINEAR.
            # - Image.LANCZOS: el más preciso para reducir, mantiene mayor detalle y bordes limpios.
            imagenAuxiliada.thumbnail(max_dimension, ImagenPillow.LANCZOS)

            # Conversión final a formato PhotoImage de tkinter para mostrar en la interfaz gráfica
            return ImageTk.PhotoImage(imagenAuxiliada)
        # Manejo específico de FileNotFoundError - cuando la ruta del archivo no existe
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró la imagen en la ruta especificada.")
            return False
        # Manejo específico de UnidentifiedImageError - cuando PIL no puede identificar el formato de imagen
        except UnidentifiedImageError:
            messagebox.showerror("Error", "El archivo seleccionado no es una imagen válida.")
            return False
        # Manejo específico de OSError - errores del sistema operativo (archivo corrupto, formato no soportado)
        except OSError:
            messagebox.showerror("Error", "Error al abrir la imagen, archivo dañado o formato no soportado.")
            return False
        # Manejo específico de PermissionError - cuando no hay permisos de lectura para el archivo
        except PermissionError:
            messagebox.showerror("Error", "No se tienen los permisos necesarios para abrir la imagen.")
            return False 
        # Manejo específico de MemoryError - cuando la imagen es demasiado grande para la memoria disponible
        except MemoryError:
            messagebox.showerror("Error", "No hay suficiente memoria para cargar la imagen.")
            return False 
        # Manejo genérico de cualquier otra excepción no contemplada específicamente
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado de tipo: {e}")
            return False

    def obtenerImagenGris(self, modo= "Tk"):
        # Verificación de que la imagen en formato OpenCV esté cargada
        try:
            if self.imagenCv is not None:
                alto,ancho = self.imagenCv.shape[0], self.imagenCv.shape[1]
                imagenGris = np.zeros((alto, ancho), dtype=np.uint8)
                for i in range(alto):
                    for j in range(ancho):
                        # Cálculo del valor de gris usando la fórmula ponderada:
                        # Gris = 0.299*R + 0.587*G + 0.114*B
                        gris = int(0.299 * self.imagenCv[i, j, 0] + 0.587 * self.imagenCv[i, j, 1] + 0.114 * self.imagenCv[i, j, 2])

                        imagenGris[i, j] = gris
                if modo == "Tk":
                    imagenGrisPillow = ImagenPillow.fromarray(imagenGris)
                    imagenGrisPillow.thumbnail((1400,600), ImagenPillow.LANCZOS)
                    return ImageTk.PhotoImage(imagenGrisPillow)
                else:
                    return imagenGris
            else:
                messagebox.showerror("Error", "La imagen no ha sido cargada correctamente.")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado de tipo: {e}")
            return None
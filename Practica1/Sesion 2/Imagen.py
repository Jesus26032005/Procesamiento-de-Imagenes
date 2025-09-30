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

# Definición de la clase Imagen que maneja las operaciones con imágenes
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
    
    # Método para convertir la imagen a escala de grises usando fórmula estándar
    def obtenerImagenGris(self, modo= "TK"):
        # Bloque try-except para manejo de errores durante la conversión
        try:
            # Verifica si la imagen OpenCV ha sido cargada correctamente
            if self.imagenCv is not None:
                # Obtiene las dimensiones de la imagen (alto, ancho)
                alto,ancho = self.imagenCv.shape[0], self.imagenCv.shape[1]
                # Crea una matriz vacía para almacenar la imagen en escala de grises
                # dtype=np.uint8 significa valores enteros de 0 a 255
                imagenGris = np.zeros((alto, ancho), dtype=np.uint8)
                # Itera a través de cada fila de la imagen
                for i in range(alto):
                    # Itera a través de cada columna de la imagen
                    for j in range(ancho):
                        # Aplica la fórmula estándar de conversión a escala de grises:
                        # Gris = 0.299*Rojo + 0.587*Verde + 0.114*Azul
                        # Esta fórmula pondera los colores según la sensibilidad del ojo humano
                        gris = int(0.299 * self.imagenCv[i, j, 0] + 0.587 * self.imagenCv[i, j, 1] + 0.114 * self.imagenCv[i, j, 2])

                        # Asigna el valor de gris calculado al píxel correspondiente
                        imagenGris[i, j] = gris
                # Verifica el modo de retorno solicitado
                if modo == "TK":
                    # Convierte el array NumPy a imagen PIL
                    imagenGrisPillow = ImagenPillow.fromarray(imagenGris)
                    # Redimensiona la imagen para visualización (1400x600 máximo)
                    imagenGrisPillow.thumbnail((1400,600), ImagenPillow.LANCZOS)
                    # Retorna la imagen como PhotoImage para usar en tkinter
                    return ImageTk.PhotoImage(imagenGrisPillow)
                else:
                    # Retorna el array NumPy directamente para procesamiento posterior
                    return imagenGris
            else:
                # Muestra error si la imagen no ha sido cargada
                messagebox.showerror("Error", "La imagen no ha sido cargada correctamente.")
            return None
        # Captura cualquier error durante el procesamiento
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado de tipo: {e}")
            return None

    # Método para calcular el histograma de una imagen en escala de grises
    def histogramaGris(self):
        # Obtiene la imagen en escala de grises como array NumPy (modo "Data")
        imagenGris = self.obtenerImagenGris(modo="Data")
        # Calcula los valores únicos y sus frecuencias en la imagen
        # np.unique retorna: valores únicos (0-255) y cuántas veces aparece cada uno
        valor, frecuencia = np.unique(imagenGris, return_counts=True)
        # Retorna una tupla con los valores de intensidad y sus frecuencias
        return valor, frecuencia

    # Método para calcular histogramas de los canales de color RGB por separado
    def histogramaColor(self):
        # Verifica si la imagen OpenCV ha sido cargada correctamente
        if self.imagenCv is not None:
            # Separa la imagen en sus tres canales de color usando OpenCV
            canalR, canalG, canalB = cv2.split(self.imagenCv)
            # Calcula valores únicos y frecuencias para el canal Rojo
            valorR, frecuenciaR = np.unique(canalR, return_counts=True)
            # Calcula valores únicos y frecuencias para el canal Verde
            valorG, frecuenciaG = np.unique(canalG, return_counts=True)
            # Calcula valores únicos y frecuencias para el canal Azul
            valorB, frecuenciaB = np.unique(canalB, return_counts=True)
            # Retorna una tupla con tres tuplas, cada una conteniendo (valores, frecuencias) para R, G, B
            return (valorR, frecuenciaR), (valorG, frecuenciaG), (valorB, frecuenciaB)

    # Método para obtener histograma de escala de grises (implementación incompleta)
    def obtenerHistogramaGris(self):
        # Verifica si la imagen OpenCV ha sido cargada correctamente
        if self.imagenCv is not None:
            # Obtiene las dimensiones de la imagen (alto, ancho)
            alto, ancho = self.imagenCv.shape[0], self.imagenCv.shape[1]
            # NOTA: Este método parece estar incompleto - falta la implementación
            pass

    def calcularPropiedadesImagenRGB(self):
        # Verifica si la imagen OpenCV ha sido cargada correctamente
        if self.imagenCv is not None:
            # Separa la imagen en sus tres canales de color usando OpenCV
            canalR, canalG, canalB = cv2.split(self.imagenCv)
            resultadosPorCanal = []
            # Calcula propiedades estadísticas para cada canal de color
            for canal in [canalR, canalG, canalB]:
                # Aplanar la matriz para análisis lineal
                pixels = canal.flatten()
                N = len(pixels)  # Número total de píxeles
                unico, conteo = np.unique(pixels, return_counts=True)
                probabilidad = conteo / N
                media = np.sum(unico * probabilidad)
                entropia = -np.sum(probabilidad * np.log2(probabilidad))
                varianza = np.sum(((unico - media) ** 2) * probabilidad)
                asimetria = np.sum(((unico - media) ** 3) * probabilidad)
                energia = np.sum(probabilidad ** 2)
                listaPropiedades = [media, entropia, varianza, asimetria, energia]
                resultadosPorCanal.append(listaPropiedades)
            return resultadosPorCanal
    
    def calcularPropiedadesImagenGris(self):
        if self.imagenCv is not None:
            matrizGris = self.obtenerImagenGris(modo="Data")
            pixels = matrizGris.flatten()
            N = len(pixels)
            unico, conteo = np.unique(pixels, return_counts=True)
            probabilidad = conteo / N
            media = np.sum(unico * probabilidad)
            entropia = -np.sum(probabilidad * np.log2(probabilidad))
            varianza = np.sum(((unico - media) ** 2) * probabilidad)
            asimetria = np.sum(((unico - media) ** 3) * probabilidad)
            energia = np.sum(probabilidad ** 2)
            return [media, entropia, varianza, asimetria, energia]
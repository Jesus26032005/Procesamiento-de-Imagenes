from PIL import Image
import numpy as np
from Utilities.ImagenData import ImagenData
import cv2
from PIL import ImageTk
from scipy import ndimage
from scipy.signal import find_peaks

# Diccionario de mensajes de error comunes al cargar imágenes
MENSAJES_ERROR = {
    FileNotFoundError: "No se encontró la imagen en la ruta especificada.",
    OSError: "Error al abrir la imagen, archivo dañado o formato no soportado.",
    PermissionError: "No se tienen los permisos necesarios para abrir la imagen.",
    MemoryError: "No hay suficiente memoria para cargar la imagen."
}

class ProcesadorImagen:

    @staticmethod
    def cargar_imagen(ruta: str):
        try:
            imagen_pillow = Image.open(ruta)
            imagen_cv = np.array(imagen_pillow)
            # Redimensionar para ajustar a la interfaz (opcional, hardcoded a 1400x600)
            imagen_cv= cv2.resize(imagen_cv, (1400, 600))
            imagen_copia_modified = imagen_cv.copy()
            return ImagenData(imagen_cv, imagen_copia_modified, imagen_cv.shape[0], imagen_cv.shape[1], 'rgb')
        except tuple(MENSAJES_ERROR.keys()) as e:
            return MENSAJES_ERROR[type(e)]
        except Exception as e:
            return "Error inesperado al cargar la imagen."

    @staticmethod
    def reiniciar_imagen(imagen: ImagenData):
        imagen.imagen_modified = imagen.imagen_cv.copy()
        imagen.tipo = 'rgb'
        return (ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified))

    @staticmethod
    def guardar_imagen(imagen: np.ndarray, ruta: str):
        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
        cv2.imwrite(ruta, imagen)
    
    def convertir_imagen_tk(imagen: np.ndarray):
        max_dimension = (1400, 600)
        imagen_pil = Image.fromarray(imagen)
        imagen_pil.thumbnail(max_dimension, Image.LANCZOS)
        return ImageTk.PhotoImage(imagen_pil)
    
    @staticmethod
    def convertir_escala_grises(imagen: ImagenData):
        imagen_auxiliar_gris = cv2.cvtColor(imagen.imagen_modified, cv2.COLOR_BGR2GRAY)
        imagen.tipo = 'gris'
        imagen.imagen_modified = cv2.merge([imagen_auxiliar_gris, imagen_auxiliar_gris, imagen_auxiliar_gris])
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def calcular_histograma_gris(imagen: np.ndarray):
        datos_aplanados = imagen[:, :, 0].flatten()
        valor, frecuencia = np.unique(datos_aplanados, return_counts=True)
        return valor, frecuencia
    
    @staticmethod
    def calcular_histograma_color(imagen: np.ndarray):
        canales = cv2.split(imagen)
        histogramaValores = list()
        for i in canales:
            valor, frecuencia = np.unique(i, return_counts=True)
            histogramaValores.append([valor, frecuencia])
        return histogramaValores

    def determinarTipo(tipo_imagen_1: str, tipo_imagen_2: str):
        """
        Determina el tipo resultante de una operación entre dos imágenes.
        Prioriza RGB sobre Gris y Gris sobre Binaria.
        
        Args:
            tipo_imagen_1 (str): Tipo de la primera imagen.
            tipo_imagen_2 (str): Tipo de la segunda imagen.
            
        Returns:
            str: Tipo resultante ('rgb', 'gris', 'binaria').
        """
        if tipo_imagen_1 == 'rgb' or tipo_imagen_2 == 'rgb':
            return 'rgb'
        if tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'gris':
            return 'gris'
        if tipo_imagen_1 == 'binaria' and tipo_imagen_2 == 'binaria':
            return 'binaria'
        if (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'binaria') or (tipo_imagen_1 == 'binaria' and tipo_imagen_2 == 'gris'):
            return 'gris'
        # Caso redundante pero explícito para combinaciones con RGB
        if (tipo_imagen_1 == 'rgb' and tipo_imagen_2 == 'binaria') or (tipo_imagen_1 == 'binaria' and tipo_imagen_2 == 'rgb') or (tipo_imagen_1 == 'rgb' and tipo_imagen_2 == 'gris') or (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'rgb'):
            return 'rgb'

    @staticmethod
    def aplicar_morfologia(tipo_morfologia, imagen: ImagenData):
        if tipo_morfologia == 'Cierre':
            ProcesadorImagen.cierre(imagen)
        elif tipo_morfologia == 'Dilatacion':
            ProcesadorImagen.dilatar(imagen)
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    def cierre(imagen: ImagenData):
        kernel = np.ones((9,9), np.uint8)
        imagen_cierre = cv2.morphologyEx(imagen.imagen_modified[:, :, 0], cv2.MORPH_CLOSE, kernel)
        imagen.imagen_modified = cv2.merge((imagen_cierre, imagen_cierre, imagen_cierre))

    def dilatar(imagen: ImagenData):
        kernel = np.ones((3,3), np.uint8)
        imagen_dilatada = cv2.dilate(imagen.imagen_modified[:, :, 0], kernel, iterations = 1)
        imagen.imagen_modified = cv2.merge((imagen_dilatada, imagen_dilatada, imagen_dilatada))

    @staticmethod
    def not_logico(imagen_1: ImagenData):
        cv2.bitwise_not(imagen_1.imagen_modified, imagen_1.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)

    @staticmethod
    def binarizar_inversa_fijo(imagen: ImagenData, umbral: int):
        imagen_auxiliar = imagen.imagen_modified[:, :, 0]
        _, imagen_auxiliar = cv2.threshold(imagen_auxiliar, umbral, 255, cv2.THRESH_BINARY_INV)
        imagen.imagen_modified = cv2.merge([imagen_auxiliar, imagen_auxiliar, imagen_auxiliar])
        imagen.tipo = 'binaria'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    @staticmethod
    def sumar_imagenes(imagen: ImagenData):
        imagen.tipo = 'final'
        cv2.add(imagen.imagen_modified, imagen.imagen_cv, imagen.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)




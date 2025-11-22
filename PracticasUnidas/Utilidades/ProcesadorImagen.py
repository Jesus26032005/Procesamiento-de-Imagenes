from PIL import Image
import numpy as np
from Utilidades.ImagenData import ImagenData
import cv2
from PIL import ImageTk

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
            imagen_cv= cv2.resize(imagen_cv, (1400, 600))
            imagen_copia_modified = imagen_cv.copy()
            return ImagenData(imagen_cv, imagen_copia_modified, imagen_cv.shape[0], imagen_cv.shape[1], 'color')
        except tuple(MENSAJES_ERROR.keys()) as e:
            return MENSAJES_ERROR[type(e)]
        except Exception as e:
            return "Error inesperado al cargar la imagen."

    @staticmethod
    def reiniciar_imagen(imagen: ImagenData):
        imagen.imagen_modified = imagen.imagen_cv.copy()
        imagen.tipo = 'color'
        return (ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified))

    @staticmethod
    def guardar_imagen(imagen: np.ndarray, ruta: str):
        try:
            cv2.imwrite(ruta, imagen)
            return True
        except Exception as e:
            return "Error al guardar la imagen."
    
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
        return (ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified), 
        ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified))
    
    @staticmethod
    def binarizar_metodo_fijo(imagen: ImagenData, umbral: int):
        imagen_auxiliar = imagen.imagen_modified[:, :, 0]
        _, imagen_auxiliar = cv2.threshold(imagen_auxiliar, umbral, 255, cv2.THRESH_BINARY)
        imagen.imagen_modified = cv2.merge([imagen_auxiliar, imagen_auxiliar, imagen_auxiliar])
        imagen.tipo = 'binario'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def binarizar_metodo_otsu(imagen: ImagenData):
        imagen_auxiliar = imagen.imagen_modified[:, :, 0]
        _, imagen_auxiliar = cv2.threshold(imagen_auxiliar, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        imagen.imagen_modified = cv2.merge([imagen_auxiliar, imagen_auxiliar, imagen_auxiliar])
        imagen.tipo = 'binario'
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
        if tipo_imagen_1 == 'color' or tipo_imagen_2 == 'color':
            return 'color'
        if tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'gris':
            return 'gris'
        if tipo_imagen_1 == 'binario' and tipo_imagen_2 == 'binario':
            return 'binario'
        if (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'binario') or (tipo_imagen_1 == 'binario' and tipo_imagen_2 == 'gris'):
            return 'gris'
        if (tipo_imagen_1 == 'color' and tipo_imagen_2 == 'binario') or (tipo_imagen_1 == 'binario' and tipo_imagen_2 == 'color') or (tipo_imagen_1 == 'color' and tipo_imagen_2 == 'gris') or (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'color'):
            return 'color'

    @staticmethod
    def sumar_escalar(imagen: ImagenData, valor: int):
        cv2.add(imagen.imagen_modified, valor, imagen.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def restar_escalar(imagen: ImagenData, valor: int):
        cv2.subtract(imagen.imagen_modified, valor, imagen.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def multiplicar_escalar(imagen: ImagenData, valor: int):
        cv2.multiply(imagen.imagen_modified, valor, imagen.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def operaciones_aritmeticas_entre_imagenes(imagen_1: ImagenData, imagen_2: ImagenData, operacion: str):
        imagen_1.tipo = ProcesadorImagen.determinarTipo(imagen_1.tipo, imagen_2.tipo)
        if operacion == 'suma':
            ProcesadorImagen.sumar_imagenes(imagen_1, imagen_2)
        if operacion == 'resta':
            ProcesadorImagen.restar_imagenes(imagen_1, imagen_2)
        if operacion == 'multiplicacion':
            ProcesadorImagen.multiplicar_imagenes(imagen_1, imagen_2)
        return (ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(imagen_1.imagen_modified))

    def sumar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.add(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    def restar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.subtract(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    def multiplicar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.multiply(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    @staticmethod
    def operaciones_logicas_entre_imagenes(imagen_1: ImagenData, imagen_2: ImagenData, operacion: str):
        imagen_1.tipo = ProcesadorImagen.determinarTipo(imagen_1.tipo, imagen_2.tipo)
        if operacion == 'or':
            ProcesadorImagen.or_logico(imagen_1, imagen_2)
        if operacion == 'and':
            ProcesadorImagen.and_logico(imagen_1, imagen_2)
        if operacion == 'xor':
            ProcesadorImagen.xor_logico(imagen_1, imagen_2)
        return (ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(imagen_1.imagen_modified))
    
    def or_logico(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.bitwise_or(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)

    def and_logico(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.bitwise_and(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)

    def xor_logico(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.bitwise_xor(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)

    @staticmethod
    def not_logico(imagen_1: ImagenData):
        cv2.bitwise_not(imagen_1.imagen_modified, imagen_1.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)
    
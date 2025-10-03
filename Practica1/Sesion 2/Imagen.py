# Importación de librerías necesarias para el procesamiento de imágenes
from PIL import Image as ImagenPillow, ImageTk, UnidentifiedImageError  # PIL para manejo de imágenes y conversión a formato Tkinter
from tkinter import messagebox  # Para mostrar mensajes de error en la interfaz gráfica
import cv2  # OpenCV para operaciones avanzadas de procesamiento de imágenes
import numpy as np  # NumPy para operaciones matemáticas con arrays

class Imagen:
    """
    Clase para el manejo y procesamiento de imágenes digitales.
    Incluye métodos para conversión de formatos, análisis estadístico y umbralización.
    """
    def __init__(self, ruta=None):
        """
        Constructor de la clase Imagen.
        Inicializa todas las propiedades de la imagen en None.
        """
        self.imagenCv = None  # Almacena la imagen en formato OpenCV (array de NumPy)
        self.imagenGris= None  # Almacena la versión en escala de grises de la imagen
        self.canalesRGB = None  # Almacena los canales R, G y B por separado
        self.alto = None  # Altura de la imagen en píxeles
        self.ancho = None  # Ancho de la imagen en píxeles
        self.ruta = ruta  # Ruta del archivo de imagen

    def convertirImagenTK(self, imagenCV):
        """
        Convierte una imagen en formato OpenCV a formato PhotoImage de Tkinter.
        Redimensiona la imagen para que quepa en la interfaz gráfica.
        """
        max_dimension = (1400, 600)  # Define el tamaño máximo permitido para mostrar en la interfaz
        imagenPil = ImagenPillow.fromarray(imagenCV)  # Convierte el array de NumPy a formato PIL
        imagenPil.thumbnail(max_dimension, ImagenPillow.LANCZOS)  # Redimensiona manteniendo proporción con interpolación LANCZOS
        return ImageTk.PhotoImage(imagenPil)  # Convierte a formato PhotoImage para mostrar en Tkinter

    def iniciarImagen(self):
        """
        Carga una imagen desde la ruta especificada y la prepara para su procesamiento.
        Maneja múltiples tipos de errores que pueden ocurrir durante la carga.
        """
        try:
            imagenPil = ImagenPillow.open(self.ruta).convert("RGB")  # Abre la imagen y la convierte a formato RGB
            self.imagenCv = np.array(imagenPil)  # Convierte la imagen PIL a array de NumPy para OpenCV
            self.alto, self.ancho = self.imagenCv.shape[0], self.imagenCv.shape[1]  # Obtiene las dimensiones de la imagen
            max_dimension = (1400, 600)  # Define el tamaño máximo para la vista previa
            imagenAuxiliada = imagenPil.copy()  # Crea una copia para no modificar la imagen original
            imagenAuxiliada.thumbnail(max_dimension, ImagenPillow.LANCZOS)  # Redimensiona la copia
            return ImageTk.PhotoImage(imagenAuxiliada)  # Retorna la imagen en formato Tkinter
        except FileNotFoundError:  # Error cuando no se encuentra el archivo
            messagebox.showerror("Error", "No se encontró la imagen en la ruta especificada.")
            return False
        except UnidentifiedImageError:  # Error cuando el archivo no es una imagen válida
            messagebox.showerror("Error", "El archivo seleccionado no es una imagen válida.")
            return False
        except OSError:  # Error de sistema operativo (archivo dañado, formato no soportado)
            messagebox.showerror("Error", "Error al abrir la imagen, archivo dañado o formato no soportado.")
            return False
        except PermissionError:  # Error de permisos de acceso al archivo
            messagebox.showerror("Error", "No se tienen los permisos necesarios para abrir la imagen.")
            return False 
        except MemoryError:  # Error cuando no hay suficiente memoria RAM
            messagebox.showerror("Error", "No hay suficiente memoria para cargar la imagen.")
            return False 
        except Exception as e:  # Captura cualquier otro error no previsto
            messagebox.showerror("Error", f"Ocurrió un error inesperado de tipo: {e}")
            return False
    
    def obtenerImagenGris(self):
        """
        Convierte la imagen a color a escala de grises usando la fórmula estándar de luminancia.
        Formula: Gris = 0.299*R + 0.587*G + 0.114*B
        """
        if self.imagenCv is not None:  # Verifica que la imagen esté cargada
            self.imagenGris = np.zeros((self.alto, self.ancho), dtype=np.uint8)  # Crea matriz vacía para imagen en grises
            for i in range(self.alto):  # Recorre todas las filas de la imagen
                for j in range(self.ancho):  # Recorre todas las columnas de la imagen
                    # Aplica la fórmula de conversión a escala de grises (ponderación por luminancia)
                    valorGris = int(0.299 * self.imagenCv[i, j, 0] + 0.587 * self.imagenCv[i, j, 1] + 0.114 * self.imagenCv[i, j, 2])
                    self.imagenGris[i, j] = valorGris  # Asigna el valor calculado al píxel correspondiente
            return self.convertirImagenTK(self.imagenGris)  # Convierte y retorna la imagen para mostrar en Tkinter
    
    def histogramaGris(self):
        """
        Calcula el histograma de la imagen en escala de grises.
        Retorna los valores únicos de intensidad y sus frecuencias.
        """
        valor, frecuencia = np.unique(self.imagenGris, return_counts=True)  # Obtiene valores únicos y sus conteos
        return valor, frecuencia  # Retorna tupla con valores de intensidad y sus frecuencias

    def histogramaColor(self):
        """
        Calcula el histograma para cada canal de color (R, G, B) por separado.
        Retorna una lista con las tuplas (valores, frecuencias) de cada canal.
        """
        self.canalesRGB = cv2.split(self.imagenCv)  # Separa la imagen en sus canales R, G y B
        listaValores = []  # Lista para almacenar los histogramas de cada canal
        if self.imagenCv is not None:  # Verifica que la imagen esté cargada
            for canal in self.canalesRGB:  # Itera sobre cada canal (R, G, B)
                valor, frecuencia = np.unique(canal, return_counts=True)  # Calcula histograma del canal actual
                listaValores.append((valor, frecuencia))  # Agrega la tupla a la lista
            return listaValores  # Retorna la lista con los histogramas de los tres canales

    def calcularPropiedadesImagenRGB(self):
        """
        Calcula propiedades estadísticas para cada canal RGB:
        media, entropía, varianza, asimetría y energía.
        """
        resultadosPorCanal = []  # Lista para almacenar las propiedades de cada canal
        for canal in self.canalesRGB:  # Itera sobre cada canal RGB
            pixels = canal.flatten()  # Convierte la matriz 2D del canal en un vector 1D
            N = len(pixels)  # Número total de píxeles en el canal
            unico, conteo = np.unique(pixels, return_counts=True)  # Obtiene valores únicos y sus conteos
            probabilidad = conteo / N  # Calcula la probabilidad de cada valor de intensidad
            media = float(np.sum(unico * probabilidad))  # Calcula la media ponderada
            entropia = float(-np.sum(probabilidad * np.log2(probabilidad)))  # Calcula la entropía (medida de información)
            varianza = float(np.sum(((unico - media) ** 2) * probabilidad))  # Calcula la varianza
            asimetria = float(np.sum(((unico - media) ** 3) * probabilidad))  # Calcula la asimetría (skewness)
            energia = float(np.sum(probabilidad ** 2))  # Calcula la energía (uniformidad)
            listaPropiedades = [media, entropia, varianza, asimetria, energia]  # Agrupa todas las propiedades
            resultadosPorCanal.append(listaPropiedades)  # Agrega las propiedades del canal a la lista
        return resultadosPorCanal  # Retorna lista con propiedades de los tres canales
    
    def calcularPropiedadesImagenGris(self):
        """
        Calcula las mismas propiedades estadísticas pero para la imagen en escala de grises.
        Retorna: [media, entropía, varianza, asimetría, energía]
        """
        pixels = self.imagenGris.flatten()  # Convierte la imagen en grises a vector 1D
        N = len(pixels)  # Número total de píxeles
        unico, conteo = np.unique(pixels, return_counts=True)  # Obtiene valores únicos y conteos
        probabilidad = conteo / N  # Calcula probabilidades de cada intensidad
        media = np.sum(unico * probabilidad)  # Calcula la media
        entropia = -np.sum(probabilidad * np.log2(probabilidad))  # Calcula la entropía
        varianza = np.sum(((unico - media) ** 2) * probabilidad)  # Calcula la varianza
        asimetria = np.sum(((unico - media) ** 3) * probabilidad)  # Calcula la asimetría
        energia = np.sum(probabilidad ** 2)  # Calcula la energía
        return [media, entropia, varianza, asimetria, energia]  # Retorna lista con todas las propiedades
    
    def umbralizarFijoImagen(self, umbral):
        """
        Aplica umbralización fija a la imagen en escala de grises.
        Convierte píxeles >= umbral a blanco (255) y < umbral a negro (0).
        """
        # Aplica umbralización: si el valor del píxel >= umbral entonces 255, sino 0
        imagenUmbralizada = np.where(self.imagenGris >= umbral, 255, 0).astype(np.uint8)
        return self.convertirImagenTK(imagenUmbralizada)  # Convierte y retorna imagen binarizada
    
    def calcularVecindad(self, x, y):
        """
        Calcula la vecindad 5x5 alrededor del píxel en posición (x,y).
        Excluye el píxel central y maneja los bordes de la imagen.
        """
        listaVecindad = []  # Lista para almacenar los valores de los píxeles vecinos
        for i in range(x-2, x+3):  # Recorre filas desde x-2 hasta x+2 (ventana 5x5)
            for j in range(y-2, y+3):  # Recorre columnas desde y-2 hasta y+2
                # Verifica que las coordenadas estén dentro de los límites de la imagen
                if (0 <= i) and (0 <= j) and (i < self.alto) and (j < self.ancho):
                    if not (i == x and j == y):  # Excluye el píxel central de la vecindad
                        listaVecindad.append(self.imagenGris[i, j])  # Agrega el valor del píxel vecino
        return listaVecindad  # Retorna la lista con los valores de los píxeles vecinos

    def umbralizarAdaptativoImagen(self, C):
        """
        Aplica umbralización adaptativa usando el promedio de la vecindad local.
        El umbral para cada píxel es: promedio_vecindad - C
        """
        imagenUmbralizada = np.zeros((self.alto, self.ancho), dtype=np.uint8)  # Crea imagen vacía para resultado
        for i in range(1, self.alto - 1):  # Recorre filas evitando bordes (necesita vecindad completa)
            for j in range(1, self.ancho - 1):  # Recorre columnas evitando bordes
                vecindad = self.calcularVecindad(i, j)  # Obtiene los píxeles vecinos al píxel actual
                umbralLocal = np.mean(vecindad) - C  # Calcula umbral local: promedio de vecinos - constante C
                if self.imagenGris[i, j] >= umbralLocal:  # Compara píxel actual con umbral local
                    imagenUmbralizada[i, j] = 255  # Si >= umbral, asigna blanco (255)
                else:
                    imagenUmbralizada[i, j] = 0  # Si < umbral, asigna negro (0)
        return self.convertirImagenTK(imagenUmbralizada)  # Convierte y retorna imagen umbralizada
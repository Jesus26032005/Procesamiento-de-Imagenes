from PIL import Image as ImagenPillow, ImageTk, UnidentifiedImageError
from tkinter import messagebox
import cv2
import numpy as np

class Imagen:
    def __init__(self, ruta=None):
        self.imagenCv = None
        self.imagenGris= None
        self.canalesRGB = None
        self.alto = None
        self.ancho = None
        self.ruta = ruta

    def convertirImagenTK(self, imagenCV):
        max_dimension = (1400, 600)
        imagenPil = ImagenPillow.fromarray(imagenCV)
        imagenPil.thumbnail(max_dimension, ImagenPillow.LANCZOS)
        return ImageTk.PhotoImage(imagenPil)

    def iniciarImagen(self):
        try:
            imagenPil = ImagenPillow.open(self.ruta).convert("RGB")
            self.imagenCv = np.array(imagenPil)
            max_dimension = (1400, 600)
            imagenAuxiliada = imagenPil.copy()
            imagenAuxiliada.thumbnail(max_dimension, ImagenPillow.LANCZOS)
            return ImageTk.PhotoImage(imagenAuxiliada)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró la imagen en la ruta especificada.")
            return False
        except UnidentifiedImageError:
            messagebox.showerror("Error", "El archivo seleccionado no es una imagen válida.")
            return False
        except OSError:
            messagebox.showerror("Error", "Error al abrir la imagen, archivo dañado o formato no soportado.")
            return False
        except PermissionError:
            messagebox.showerror("Error", "No se tienen los permisos necesarios para abrir la imagen.")
            return False 
        except MemoryError:
            messagebox.showerror("Error", "No hay suficiente memoria para cargar la imagen.")
            return False 
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado de tipo: {e}")
            return False
    
    def obtenerImagenGris(self):
        if self.imagenCv is not None:
            self.alto, self.ancho = self.imagenCv.shape[0], self.imagenCv.shape[1]
            self.imagenGris = np.zeros((self.alto, self.ancho), dtype=np.uint8)
            for i in range(self.alto):
                for j in range(self.ancho):
                    valorGris = int(0.299 * self.imagenCv[i, j, 0] + 0.587 * self.imagenCv[i, j, 1] + 0.114 * self.imagenCv[i, j, 2])
                    self.imagenGris[i, j] = valorGris
            return self.convertirImagenTK(self.imagenGris)
    
    def histogramaGris(self):
        valor, frecuencia = np.unique(self.imagenGris, return_counts=True)
        return valor, frecuencia

    def histogramaColor(self):
        self.canalesRGB = cv2.split(self.imagenCv)
        listaValores = []
        if self.imagenCv is not None:
            for canal in self.canalesRGB:
                valor, frecuencia = np.unique(canal, return_counts=True)
                listaValores.append((valor, frecuencia))
            return listaValores

    def calcularHistograma(self, matriz):
        histograma = []
        for canal in matriz:
            valor, frecuencia = np.unique(canal, return_counts=True)
            histograma.append((valor, frecuencia))
        return histograma

    def calcularPropiedadesImagenRGB(self):
        resultadosPorCanal = []
        for canal in self.canalesRGB:
            pixels = canal.flatten()
            N = len(pixels)
            unico, conteo = np.unique(pixels, return_counts=True)
            probabilidad = conteo / N
            media = float(np.sum(unico * probabilidad))
            entropia = float(-np.sum(probabilidad * np.log2(probabilidad)))
            varianza = float(np.sum(((unico - media) ** 2) * probabilidad))
            asimetria = float(np.sum(((unico - media) ** 3) * probabilidad))
            energia = float(np.sum(probabilidad ** 2))
            listaPropiedades = [media, entropia, varianza, asimetria, energia]
            resultadosPorCanal.append(listaPropiedades)
        return resultadosPorCanal
    
    def calcularPropiedadesImagenGris(self):
        pixels = self.imagenGris.flatten()
        N = len(pixels)
        unico, conteo = np.unique(pixels, return_counts=True)
        probabilidad = conteo / N
        media = np.sum(unico * probabilidad)
        entropia = -np.sum(probabilidad * np.log2(probabilidad))
        varianza = np.sum(((unico - media) ** 2) * probabilidad)
        asimetria = np.sum(((unico - media) ** 3) * probabilidad)
        energia = np.sum(probabilidad ** 2)
        return [media, entropia, varianza, asimetria, energia]
    
    def umbralizarFijoImagen(self, umbral):
        imagenUmbralizada = np.where(self.imagenGris >= umbral, 255, 0).astype(np.uint8)
        return self.convertirImagenTK(imagenUmbralizada)
    
    def calcularVecindad(self, x, y):
        listaVecindad = []
        for i in range(x-2, x+3):
            for j in range(y-2, y+3):
                if (0 <= i) and (0 <= j) and (i < self.alto) and (j < self.ancho):
                    if not (i == x and j == y):  # si NO quieres el centro
                        listaVecindad.append(self.imagenGris[i, j])
        return listaVecindad

    def umbralizarAdaptativoImagen(self, C):
        imagenUmbralizada = np.zeros((self.alto, self.ancho), dtype=np.uint8)
        for i in range(1, self.alto - 1):
            for j in range(1, self.ancho - 1):
                vecindad = self.calcularVecindad(i, j)
                umbralLocal = np.mean(vecindad) - C
                if self.imagenGris[i, j] >= umbralLocal:
                    imagenUmbralizada[i, j] = 255
                else:
                    imagenUmbralizada[i, j] = 0
        return self.convertirImagenTK(imagenUmbralizada)
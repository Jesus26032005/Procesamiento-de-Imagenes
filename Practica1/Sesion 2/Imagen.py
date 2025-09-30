from PIL import Image as ImagenPillow, ImageTk, UnidentifiedImageError
from tkinter import messagebox
import cv2
import numpy as np

class Imagen:
    def __init__(self, ruta=None):
        self.imagenCv = None
        self.imagenGris= None
        self.alto = None
        self.ancho = None
        self.ruta = ruta

    def iniciarImagen(self):
        try:
            self.imagenPil = ImagenPillow.open(self.ruta).convert("RGB")
            self.imagenCv = np.array(self.imagenPil)
            max_dimension = (1400, 600)
            imagenAuxiliada = self.imagenPil.copy()
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
    
    def obtenerImagenGris(self, modo= "TK"):
        try:
            if self.imagenCv is not None:
                alto,ancho = self.imagenCv.shape[0], self.imagenCv.shape[1]
                imagenGris = np.zeros((alto, ancho), dtype=np.uint8)
                for i in range(alto):
                    for j in range(ancho):
                        gris = int(0.299 * self.imagenCv[i, j, 0] + 0.587 * self.imagenCv[i, j, 1] + 0.114 * self.imagenCv[i, j, 2])

                        imagenGris[i, j] = gris
                if modo == "TK":
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

    def histogramaGris(self):
        imagenGris = self.obtenerImagenGris(modo="Data")
        valor, frecuencia = np.unique(imagenGris, return_counts=True)
        return valor, frecuencia

    def histogramaColor(self):
        if self.imagenCv is not None:
            canalR, canalG, canalB = cv2.split(self.imagenCv)
            valorR, frecuenciaR = np.unique(canalR, return_counts=True)
            valorG, frecuenciaG = np.unique(canalG, return_counts=True)
            valorB, frecuenciaB = np.unique(canalB, return_counts=True)
            return (valorR, frecuenciaR), (valorG, frecuenciaG), (valorB, frecuenciaB)

    def obtenerHistogramaGris(self):
        if self.imagenCv is not None:
            alto, ancho = self.imagenCv.shape[0], self.imagenCv.shape[1]
            pass

    def calcularPropiedadesImagenRGB(self):
        if self.imagenCv is not None:
            canalR, canalG, canalB = cv2.split(self.imagenCv)
            resultadosPorCanal = []
            for canal in [canalR, canalG, canalB]:
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
    
    def umbralizarFijoImagen(self, umbral):
        pass
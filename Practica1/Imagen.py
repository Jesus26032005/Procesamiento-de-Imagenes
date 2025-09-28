from PIL import Image as ImagenPillow, ImageTk, UnidentifiedImageError
from tkinter import messagebox
import cv2
import numpy as np

class Imagen:
    def __init__(self, ruta=None):
        self.imagenCv = None
        self.imagenPil = None
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

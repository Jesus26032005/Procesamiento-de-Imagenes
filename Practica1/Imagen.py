from PIL import Image as ImagenPillow, ImageTk, UnidentifiedImageError
from tkinter import messagebox
import numpy as np
import cv2

class Imagen:
    def __init__(self, ruta=None):
        self.imagenCv = None
        self.imagenPil = None
        self.ruta = ruta

    def iniciarImagen(self):
        try:
            # Cargar la imagen usando Pillow
            self.imagenPil = ImagenPillow.open(self.ruta).convert("RGB")
            # Convertir la imagen a un array de NumPy y luego a formato OpenCV
            self.imagenCv = np.array(self.imagenPil)
            # Cambiamos el tamaño de la imagen si es muy grande
            max_dimension = (1400, 600)
            imagenAuxiliada = self.imagenPil.copy()
            imagenAuxiliada.thumbnail(max_dimension, ImagenPillow.LANCZOS)
            # Convertir la imagen a formato compatible con Tkinter
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

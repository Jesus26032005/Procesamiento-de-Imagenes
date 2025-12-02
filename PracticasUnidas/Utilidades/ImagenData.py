from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class ImagenData:
    """
    Clase de datos (Data Class) que almacena la información de una imagen.
    
    Attributes:
        imagen_cv (np.ndarray): La imagen original cargada (matriz NumPy).
        imagen_modified (np.ndarray): La versión modificada de la imagen (matriz NumPy).
        alto (int): Altura de la imagen en píxeles.
        ancho (int): Ancho de la imagen en píxeles.
        tipo (str): Tipo de la imagen actual ('rgb', 'gris', 'binaria'). Por defecto 'rgb'.
    """
    imagen_cv: np.ndarray
    imagen_modified: np.ndarray
    alto: int
    ancho: int
    tipo: str = 'rgb'
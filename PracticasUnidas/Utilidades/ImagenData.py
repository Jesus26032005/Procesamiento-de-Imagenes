from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class ImagenData:
    """
    Clase de datos que representa una imagen en la aplicación.
    Almacena la imagen original (OpenCV), la modificada, dimensiones y tipo.
    """
    imagen_cv: np.ndarray
    imagen_modified: np.ndarray
    alto: int
    ancho: int
    tipo: str = 'rgb'
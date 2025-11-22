from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class ImagenData:
    imagen_cv: np.ndarray
    imagen_modified: np.ndarray
    alto: int
    ancho: int
    tipo: str = 'color'
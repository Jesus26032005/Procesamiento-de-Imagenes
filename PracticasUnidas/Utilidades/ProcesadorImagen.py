from PIL import Image
import numpy as np
from Utilidades.ImagenData import ImagenData
import cv2
from PIL import ImageTk
from scipy import ndimage

MENSAJES_ERROR = {
    FileNotFoundError: "No se encontró la imagen en la ruta especificada.",
    OSError: "Error al abrir la imagen, archivo dañado o formato no soportado.",
    PermissionError: "No se tienen los permisos necesarios para abrir la imagen.",
    MemoryError: "No hay suficiente memoria para cargar la imagen."
}
from PIL import Image
import numpy as np
from Utilidades.ImagenData import ImagenData
import cv2
from PIL import ImageTk
from scipy import ndimage

MENSAJES_ERROR = {
    FileNotFoundError: "No se encontró la imagen en la ruta especificada.",
    OSError: "Error al abrir la imagen, archivo dañado o formato no soportado.",
    PermissionError: "No se tienen los permisos necesarios para abrir la imagen.",
    MemoryError: "No hay suficiente memoria para cargar la imagen."
}

class ProcesadorImagen:
    """
    Clase utilitaria que contiene métodos estáticos para el procesamiento de imágenes.
    Incluye carga, guardado, conversión, operaciones aritméticas/lógicas, ruido y filtros.
    """
    @staticmethod
    def cargar_imagen(ruta: str):
        """
        Carga una imagen desde la ruta especificada.
        
        Args:
            ruta (str): Ruta del archivo de imagen.
            
        Returns:
            ImagenData or str: Objeto ImagenData si es exitoso, mensaje de error si falla.
        """
        try:
            imagen_pillow = Image.open(ruta)
            imagen_cv = np.array(imagen_pillow)
            imagen_cv= cv2.resize(imagen_cv, (1400, 600))
            imagen_copia_modified = imagen_cv.copy()
            return ImagenData(imagen_cv, imagen_copia_modified, imagen_cv.shape[0], imagen_cv.shape[1], 'rgb')
        except tuple(MENSAJES_ERROR.keys()) as e:
            return MENSAJES_ERROR[type(e)]
        except Exception as e:
            return "Error inesperado al cargar la imagen."

    @staticmethod
    def reiniciar_imagen(imagen: ImagenData):
        """
        Restaura la imagen modificada a su estado original.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            
        Returns:
            tuple: Imagen TK restaurada e histograma.
        """
        imagen.imagen_modified = imagen.imagen_cv.copy()
        imagen.tipo = 'rgb'
        return (ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified))

    @staticmethod
    def guardar_imagen(imagen: np.ndarray, ruta: str):
        """
        Guarda la imagen en la ruta especificada.
        
        Args:
            imagen (np.ndarray): Matriz de la imagen.
            ruta (str): Ruta de destino.
        """
        cv2.imwrite(ruta, imagen)
    
    def convertir_imagen_tk(imagen: np.ndarray):
        """
        Convierte una imagen numpy a un objeto PhotoImage de Tkinter para mostrar en la UI.
        Redimensiona la imagen para ajustar a la vista.
        
        Args:
            imagen (np.ndarray): Matriz de la imagen.
            
        Returns:
            ImageTk.PhotoImage: Imagen lista para Tkinter.
        """
        max_dimension = (1400, 600)
        imagen_pil = Image.fromarray(imagen)
        imagen_pil.thumbnail(max_dimension, Image.LANCZOS)
        return ImageTk.PhotoImage(imagen_pil)
    
    @staticmethod
    def convertir_escala_grises(imagen: ImagenData):
        """
        Convierte la imagen a escala de grises.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            
        Returns:
            ImageTk.PhotoImage: Imagen en grises para Tkinter.
        """
        imagen_auxiliar_gris = cv2.cvtColor(imagen.imagen_modified, cv2.COLOR_BGR2GRAY)
        imagen.tipo = 'gris'
        imagen.imagen_modified = cv2.merge([imagen_auxiliar_gris, imagen_auxiliar_gris, imagen_auxiliar_gris])
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def binarizar_metodo_fijo(imagen: ImagenData, umbral: int):
        """
        Binariza la imagen usando un umbral fijo.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            umbral (int): Valor del umbral (0-255).
            
        Returns:
            ImageTk.PhotoImage: Imagen binarizada para Tkinter.
        """
        imagen_auxiliar = imagen.imagen_modified[:, :, 0]
        _, imagen_auxiliar = cv2.threshold(imagen_auxiliar, umbral, 255, cv2.THRESH_BINARY)
        imagen.imagen_modified = cv2.merge([imagen_auxiliar, imagen_auxiliar, imagen_auxiliar])
        imagen.tipo = 'binario'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def binarizar_metodo_otsu(imagen: ImagenData):
        """
        Binariza la imagen usando el método de Otsu.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            
        Returns:
            ImageTk.PhotoImage: Imagen binarizada para Tkinter.
        """
        imagen_auxiliar = imagen.imagen_modified[:, :, 0]
        _, imagen_auxiliar = cv2.threshold(imagen_auxiliar, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        imagen.imagen_modified = cv2.merge([imagen_auxiliar, imagen_auxiliar, imagen_auxiliar])
        imagen.tipo = 'binario'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    @staticmethod
    def calcular_histograma_gris(imagen: np.ndarray):
        """
        Calcula el histograma de una imagen en escala de grises.
        
        Args:
            imagen (np.ndarray): Matriz de la imagen.
            
        Returns:
            tuple: Arrays de valores y frecuencias.
        """
        datos_aplanados = imagen[:, :, 0].flatten()
        valor, frecuencia = np.unique(datos_aplanados, return_counts=True)
        return valor, frecuencia
    
    @staticmethod
    def calcular_histograma_color(imagen: np.ndarray):
        """
        Calcula el histograma de una imagen a color (por canal).
        
        Args:
            imagen (np.ndarray): Matriz de la imagen.
            
        Returns:
            list: Lista de [valores, frecuencias] por canal.
        """
        canales = cv2.split(imagen)
        histogramaValores = list()
        for i in canales:
            valor, frecuencia = np.unique(i, return_counts=True)
            histogramaValores.append([valor, frecuencia])
        return histogramaValores

    def determinarTipo(tipo_imagen_1: str, tipo_imagen_2: str):
        """
        Determina el tipo de imagen resultante de una operación entre dos imágenes.
        
        Args:
            tipo_imagen_1 (str): Tipo de la primera imagen.
            tipo_imagen_2 (str): Tipo de la segunda imagen.
            
        Returns:
            str: Tipo resultante ('rgb', 'gris', 'binario').
        """
        if tipo_imagen_1 == 'rgb' or tipo_imagen_2 == 'rgb':
            return 'rgb'
        if tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'gris':
            return 'gris'
        if tipo_imagen_1 == 'binario' and tipo_imagen_2 == 'binario':
            return 'binario'
        if (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'binario') or (tipo_imagen_1 == 'binario' and tipo_imagen_2 == 'gris'):
            return 'gris'
        if (tipo_imagen_1 == 'rgb' and tipo_imagen_2 == 'binario') or (tipo_imagen_1 == 'binario' and tipo_imagen_2 == 'rgb') or (tipo_imagen_1 == 'rgb' and tipo_imagen_2 == 'gris') or (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'rgb'):
            return 'rgb'

    @staticmethod
    def sumar_escalar(imagen: ImagenData, valor: int):
        """
        Suma un valor escalar a la imagen.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            valor (int): Valor a sumar.
            
        Returns:
            ImageTk.PhotoImage: Imagen resultante para Tkinter.
        """
        cv2.add(imagen.imagen_modified, valor, imagen.imagen_modified)
        if imagen.tipo == 'binaria':
            imagen.tipo = 'gris'

        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def restar_escalar(imagen: ImagenData, valor: int):
        """
        Resta un valor escalar a la imagen.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            valor (int): Valor a restar.
            
        Returns:
            ImageTk.PhotoImage: Imagen resultante para Tkinter.
        """
        cv2.subtract(imagen.imagen_modified, valor, imagen.imagen_modified)
        if imagen.tipo == 'binaria':
            imagen.tipo = 'gris'

        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def multiplicar_escalar(imagen: ImagenData, valor: int):
        """
        Multiplica la imagen por un valor escalar.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            valor (int): Valor multiplicador.
            
        Returns:
            ImageTk.PhotoImage: Imagen resultante para Tkinter.
        """
        cv2.multiply(imagen.imagen_modified, valor, imagen.imagen_modified)
        if imagen.tipo == 'binaria':
            imagen.tipo = 'gris'
            
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def operaciones_aritmeticas_entre_imagenes(imagen_1: ImagenData, imagen_2: ImagenData, operacion: str):
        """
        Realiza operaciones aritméticas entre dos imágenes.
        
        Args:
            imagen_1 (ImagenData): Primera imagen.
            imagen_2 (ImagenData): Segunda imagen.
            operacion (str): Tipo de operación ('suma', 'resta', 'multiplicacion').
            
        Returns:
            ImageTk.PhotoImage: Imagen resultante para Tkinter.
        """
        imagen_1.tipo = ProcesadorImagen.determinarTipo(imagen_1.tipo, imagen_2.tipo)
        if operacion == 'suma':
            ProcesadorImagen.sumar_imagenes(imagen_1, imagen_2)
        if operacion == 'resta':
            ProcesadorImagen.restar_imagenes(imagen_1, imagen_2)
        if operacion == 'multiplicacion':
            ProcesadorImagen.multiplicar_imagenes(imagen_1, imagen_2)
        
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)

    def sumar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        """
        Suma dos imágenes pixel a pixel.
        """
        cv2.add(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    def restar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        """
        Resta la segunda imagen de la primera pixel a pixel.
        """
        cv2.subtract(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    def multiplicar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        """
        Multiplica dos imágenes pixel a pixel.
        """
        cv2.multiply(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    @staticmethod
    def operaciones_logicas_entre_imagenes(imagen_1: ImagenData, imagen_2: ImagenData, operacion: str):
        """
        Realiza operaciones lógicas entre dos imágenes.
        
        Args:
            imagen_1 (ImagenData): Primera imagen.
            imagen_2 (ImagenData): Segunda imagen.
            operacion (str): Tipo de operación ('or', 'and', 'xor').
            
        Returns:
            ImageTk.PhotoImage: Imagen resultante para Tkinter.
        """
        imagen_1.tipo = ProcesadorImagen.determinarTipo(imagen_1.tipo, imagen_2.tipo)
        if operacion == 'or':
            ProcesadorImagen.or_logico(imagen_1, imagen_2)
        if operacion == 'and':
            ProcesadorImagen.and_logico(imagen_1, imagen_2)
        if operacion == 'xor':
            ProcesadorImagen.xor_logico(imagen_1, imagen_2)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)
    
    def or_logico(imagen_1: ImagenData, imagen_2: ImagenData):
        """
        Aplica OR lógico entre dos imágenes.
        """
        cv2.bitwise_or(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)

    def and_logico(imagen_1: ImagenData, imagen_2: ImagenData):
        """
        """
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        imagen.imagen_modified = cv2.filter2D(imagen.imagen_modified, -1, kernel)
    
    def aplicar_filtro_promediador_pesado(imagen: ImagenData, kernel_size=3):
        """
        Aplica filtro promediador ponderado.
        """
        kernel = np.ones((kernel_size, kernel_size), np.float32)
        center = kernel_size // 2
        kernel[center, center] = kernel_size * 2
        kernel /= kernel.sum()
        imagen.imagen_modified = cv2.filter2D(imagen.imagen_modified, -1, kernel)
    
    def aplicar_filtro_gaussiano(imagen: ImagenData, kernel_size=3, sigma=1.0):
        """
        Aplica filtro gaussiano.
        """
        imagen.imagen_modified = cv2.GaussianBlur(imagen.imagen_modified, (kernel_size, kernel_size), sigma)
    
    def aplicar_filtro_bilateral(imagen: ImagenData, diameter=9, sigma_color=75, sigma_space=75):
        """
        Aplica filtro bilateral.
        """
        imagen.imagen_modified = cv2.bilateralFilter(imagen.imagen_modified, diameter, sigma_color, sigma_space)

    def aplicar_filtro_mediana(imagen: ImagenData, kernel_size=3):
        """
        Aplica filtro de mediana.
        """
        imagen.imagen_modified = cv2.medianBlur(imagen.imagen_modified, kernel_size)
    
    def aplicar_filtro_moda(imagen: ImagenData, kernel_size=3):
        """
        Aplica filtro de moda.
        """
        def _modafiltro2D(channel):
            def funcionModa(x):
                values, counts = np.unique(x, return_counts=True)
                return values[np.argmax(counts)]
            return ndimage.generic_filter(
                channel, 
                funcionModa, 
                size=kernel_size
            )
        
        if imagen.tipo == 'rgb':
            channels = []
            for i in range(3):
                channels.append(_modafiltro2D(imagen.imagen_modified[:,:,i]))
            imagen.imagen_modified = np.stack(channels, axis=2)
        else:
            imagen.imagen_modified = _modafiltro2D(imagen.imagen_modified)
        
    def aplicar_filtro_maximo(imagen: ImagenData, kernel_size=3):
        """
        Aplica filtro de máximo (dilatación).
        """
        imagen.imagen_modified = cv2.dilate(imagen.imagen_modified, np.ones((kernel_size, kernel_size)))
    
    def aplicar_filtro_minimo(imagen: ImagenData, kernel_size=3):
        """
        Aplica filtro de mínimo (erosión).
        """
        imagen.imagen_modified = cv2.erode(imagen.imagen_modified, np.ones((kernel_size, kernel_size)))
    
    def aplicar_filtro_adaptativo(imagen: ImagenData, max_window_size=7):
        """
        Aplica filtro de mediana adaptativa.
        """
        def process_pixel(i, j):
            window_size = 3
            while window_size <= max_window_size:
                half = window_size // 2
                window = imagen.imagen_modified[
                    max(0, i-half):min(imagen.imagen_modified.shape[0], i+half+1),
                    max(0, j-half):min(imagen.imagen_modified.shape[1], j+half+1)
                ]
                
                if imagen.tipo == 'rgb':
                    vectors = window.reshape(-1, 3).astype(float)
                    N = len(vectors) 

                    magnitudes = np.sum(vectors, axis=1) 
                    z_min = vectors[np.argmin(magnitudes)].astype(np.uint8)
                    z_max = vectors[np.argmax(magnitudes)].astype(np.uint8)

                    min_distance_sum = float('inf')
                    z_med = np.zeros(3, dtype=np.uint8)

                    for k in range(N):
                        actual_vector = vectors[k]
                        distances = np.linalg.norm(vectors - actual_vector, axis=1)
                        distance_sum = np.sum(distances)
                        
                        if distance_sum < min_distance_sum:
                            min_distance_sum = distance_sum
                            z_med = actual_vector.astype(np.uint8) 
                else:
                    z_min = np.min(window)
                    z_max = np.max(window)
                    z_med = np.median(window)
                
                isEqual = False
                if imagen.tipo == 'rgb': isEqual = np.array_equal(z_med, z_min) or np.array_equal(z_med, z_max)
                else: isEqual = z_med == z_min or z_med == z_max

                if isEqual:
                    window_size += 2
                    if window_size > max_window_size:
                        return z_med
                else:
                    current_pixel= imagen.imagen_modified[i, j]
                    if imagen.tipo == 'rgb':
                        if np.array_equal(current_pixel, z_min) or np.array_equal(current_pixel, z_max):
                            return z_med
                        else:
                            return current_pixel
                    else:
                        if z_min < current_pixel < z_max:
                            return current_pixel
                        else:
                            return z_med
            return imagen.imagen_modified[i, j]
        
        if imagen.tipo == 'rgb':
            result = np.zeros_like(imagen.imagen_modified)
            for i in range(imagen.imagen_modified.shape[0]):
                for j in range(imagen.imagen_modified.shape[1]):
                    result[i, j] = process_pixel(i, j)
            imagen.imagen_modified = result
        else:
            result = np.zeros_like(imagen.imagen_modified)
            for i in range(imagen.imagen_modified.shape[0]):
                for j in range(imagen.imagen_modified.shape[1]):
                    result[i, j] = process_pixel(i, j)
            imagen.imagen_modified = result
    
    def aplicar_filtro_contraharmonico(imagen: ImagenData, kernel_size=3, Q=1.5):
        """
        Aplica filtro de media contraarmónica.
        """
        def contraharmonic_mean(channel):
            kernel = np.ones((kernel_size, kernel_size))
            padding = kernel_size // 2
            
            padded = np.pad(channel.astype(np.float64), padding, mode='reflect')
            result = np.zeros_like(channel, dtype=np.float64)
            
            for i in range(channel.shape[0]):
                for j in range(channel.shape[1]):
                    window = padded[i:i+kernel_size, j:j+kernel_size]
                    
                    numerator = np.sum(window ** (Q + 1))
                    denominator = np.sum(window ** Q)
                    
                    if denominator != 0:
                        result[i, j] = numerator / denominator
                    else:
                        result[i, j] = channel[i, j]
            
            return np.clip(result, 0, 255).astype(np.uint8)
        
        if imagen.tipo == 'rgb':
            channels = []
            for i in range(3):
                channels.append(contraharmonic_mean(imagen.imagen_modified[:, :, i]))
            imagen.imagen_modified = np.stack(channels, axis=2)
        else:
            imagen.imagen_modified = contraharmonic_mean(imagen.imagen_modified)

    def aplicar_filtro_mediana_ponderada(imagen: ImagenData, kernel_size=3, weights=None):
        """
        Aplica filtro de mediana ponderada.
        """
        if weights is None:
            center = kernel_size // 2
            y, x = np.ogrid[-center:kernel_size-center, -center:kernel_size-center]
            weights = np.exp(-(x**2 + y**2) / (2*(center/2)**2))
            weights = weights / weights.sum() * kernel_size**2
            weights = np.round(weights).astype(int)
        
        def weighted_median(channel):
            padding = kernel_size // 2
            padded = np.pad(channel, padding, mode='reflect')
            result = np.zeros_like(channel)
            
            for i in range(channel.shape[0]):
                for j in range(channel.shape[1]):
                    window = padded[i:i+kernel_size, j:j+kernel_size]
                    
                    weighted_list = []
                    for w_i in range(kernel_size):
                        for w_j in range(kernel_size):
                            weight = weights[w_i, w_j]
                            pixel_value = window[w_i, w_j]
                            weighted_list.extend([pixel_value] * weight)
                    
                    result[i, j] = np.median(weighted_list)
            
            return result.astype(np.uint8)
        
        if imagen.tipo == 'rgb':
            channels = []
            for i in range(3):
                channels.append(weighted_median(imagen.imagen_modified[:, :, i]))
            imagen.imagen_modified = np.stack(channels, axis=2)
        else:
            imagen.imagen_modified = weighted_median(imagen.imagen_modified)
    
    def aplicar_filtro_sobel(imagen: ImagenData, kernel_size=3):
        """
        Aplica filtro de Sobel para detección de bordes.
        """
        imagen_gris= imagen.imagen_modified[:, :, 0]
        sobel_x = cv2.Sobel(imagen_gris, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(imagen_gris, cv2.CV_64F, 0, 1, ksize=kernel_size)
        bordes = cv2.magnitude(sobel_x, sobel_y)
        bordes_final = np.clip(bordes, 0, 255).astype(np.uint8)
        imagen.imagen_modified = cv2.merge((bordes_final, bordes_final, bordes_final))

        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    def aplicar_filtro_Prewitt(imagen: ImagenData):
        """
        Aplica filtro de Prewitt para detección de bordes.
        """
        imagen_gris = imagen.imagen_modified[:, :, 0]
        kernel_prewitt_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        kernel_prewitt_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

        bordes_prewitt_x = cv2.filter2D(imagen_gris, cv2.CV_64F, kernel_prewitt_x)
        bordes_prewitt_y = cv2.filter2D(imagen_gris, cv2.CV_64F, kernel_prewitt_y)
        abs_x = cv2.convertScaleAbs(bordes_prewitt_x)
        abs_y = cv2.convertScaleAbs(bordes_prewitt_y)
        bordes_prewitt = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
        
        imagen.imagen_modified = cv2.merge((bordes_prewitt, bordes_prewitt, bordes_prewitt))
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    def aplicar_filtro_robert(imagen: ImagenData):
        """
        Aplica filtro de Roberts para detección de bordes.
        """
        imagen_gris = imagen.imagen_modified[:, :, 0]
        kernel_robert_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
        kernel_robert_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        
        bordes_robert_x = cv2.filter2D(imagen_gris, cv2.CV_64F, kernel_robert_x)
        bordes_robert_y = cv2.filter2D(imagen_gris, cv2.CV_64F, kernel_robert_y)
        abs_x = cv2.convertScaleAbs(bordes_robert_x)
        abs_y = cv2.convertScaleAbs(bordes_robert_y)
        bordes_robert = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
        
        imagen.imagen_modified = cv2.merge((bordes_robert, bordes_robert, bordes_robert))
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    def aplicar_filtro_canny(imagen: ImagenData, valor_umbral_minimo, valor_umbral_maximo):
        """
        Aplica filtro de Canny para detección de bordes.
        """
        imagen_gris = imagen.imagen_modified[:, :, 0]
        bordes_canny = cv2.Canny(imagen_gris, valor_umbral_minimo, valor_umbral_maximo)
        imagen.imagen_modified = cv2.merge((bordes_canny, bordes_canny, bordes_canny))
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
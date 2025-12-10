from PIL import Image
import numpy as np
from Utilidades.ImagenData import ImagenData
import cv2
from PIL import ImageTk
from scipy import ndimage
from scipy.signal import find_peaks

# Diccionario de mensajes de error comunes al cargar imágenes
MENSAJES_ERROR = {
    FileNotFoundError: "No se encontró la imagen en la ruta especificada.",
    OSError: "Error al abrir la imagen, archivo dañado o formato no soportado.",
    PermissionError: "No se tienen los permisos necesarios para abrir la imagen.",
    MemoryError: "No hay suficiente memoria para cargar la imagen."
}

class ProcesadorImagen:
    """
    Clase utilitaria que contiene métodos estáticos para el procesamiento de imágenes.
    Incluye carga, guardado, conversión, filtros, operaciones aritméticas/lógicas, segmentación y ajustes de brillo.
    """
    
    @staticmethod
    def cargar_imagen(ruta: str):
        """
        Carga una imagen desde la ruta especificada.
        
        Args:
            ruta (str): Ruta del archivo de imagen.
            
        Returns:
            ImagenData or str: Objeto ImagenData si es exitoso, o mensaje de error.
        """
        try:
            imagen_pillow = Image.open(ruta)
            imagen_cv = np.array(imagen_pillow)
            # Redimensionar para ajustar a la interfaz (opcional, hardcoded a 1400x600)
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
            tuple: Imagen TK restaurada y su histograma.
        """
        imagen.imagen_modified = imagen.imagen_cv.copy()
        imagen.tipo = 'rgb'
        return (ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified))

    @staticmethod
    def guardar_imagen(imagen: np.ndarray, ruta: str):
        """
        Guarda la imagen en disco.
        
        Args:
            imagen (np.ndarray): Matriz de la imagen.
            ruta (str): Ruta de destino.
        """
        cv2.imwrite(ruta, imagen)
    
    def convertir_imagen_tk(imagen: np.ndarray):
        """
        Convierte una matriz numpy (imagen OpenCV) a un objeto PhotoImage de Tkinter para mostrar en la GUI.
        
        Args:
            imagen (np.ndarray): Matriz de la imagen.
            
        Returns:
            ImageTk.PhotoImage: Objeto de imagen para Tkinter.
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
            ImageTk.PhotoImage: Imagen TK en escala de grises.
        """
        imagen_auxiliar_gris = cv2.cvtColor(imagen.imagen_modified, cv2.COLOR_BGR2GRAY)
        imagen.tipo = 'gris'
        # Mantenemos 3 canales para compatibilidad visual, aunque sean iguales
        imagen.imagen_modified = cv2.merge([imagen_auxiliar_gris, imagen_auxiliar_gris, imagen_auxiliar_gris])
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def binarizar_metodo_fijo(imagen: ImagenData, umbral: int):
        """
        Binariza la imagen usando un umbral fijo.
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            umbral (int): Valor de corte (0-255).
            
        Returns:
            ImageTk.PhotoImage: Imagen TK binarizada.
        """
        imagen_auxiliar = imagen.imagen_modified[:, :, 0]
        _, imagen_auxiliar = cv2.threshold(imagen_auxiliar, umbral, 255, cv2.THRESH_BINARY)
        imagen.imagen_modified = cv2.merge([imagen_auxiliar, imagen_auxiliar, imagen_auxiliar])
        imagen.tipo = 'binaria'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def binarizar_metodo_otsu(imagen: ImagenData):
        """
        Binariza la imagen usando el método de Otsu (umbral automático).
        
        Args:
            imagen (ImagenData): Objeto de datos de la imagen.
            
        Returns:
            ImageTk.PhotoImage: Imagen TK binarizada.
        """
        imagen_auxiliar = imagen.imagen_modified[:, :, 0]
        _, imagen_auxiliar = cv2.threshold(imagen_auxiliar, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        imagen.imagen_modified = cv2.merge([imagen_auxiliar, imagen_auxiliar, imagen_auxiliar])
        imagen.tipo = 'binaria'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    @staticmethod
    def calcular_histograma_gris(imagen: np.ndarray):
        """
        Calcula el histograma para una imagen en escala de grises.
        
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
        Calcula el histograma para cada canal de una imagen a color.
        
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
        Determina el tipo resultante de una operación entre dos imágenes.
        Prioriza RGB sobre Gris y Gris sobre Binaria.
        
        Args:
            tipo_imagen_1 (str): Tipo de la primera imagen.
            tipo_imagen_2 (str): Tipo de la segunda imagen.
            
        Returns:
            str: Tipo resultante ('rgb', 'gris', 'binaria').
        """
        if tipo_imagen_1 == 'rgb' or tipo_imagen_2 == 'rgb':
            return 'rgb'
        if tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'gris':
            return 'gris'
        if tipo_imagen_1 == 'binaria' and tipo_imagen_2 == 'binaria':
            return 'binaria'
        if (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'binaria') or (tipo_imagen_1 == 'binaria' and tipo_imagen_2 == 'gris'):
            return 'gris'
        # Caso redundante pero explícito para combinaciones con RGB
        if (tipo_imagen_1 == 'rgb' and tipo_imagen_2 == 'binaria') or (tipo_imagen_1 == 'binaria' and tipo_imagen_2 == 'rgb') or (tipo_imagen_1 == 'rgb' and tipo_imagen_2 == 'gris') or (tipo_imagen_1 == 'gris' and tipo_imagen_2 == 'rgb'):
            return 'rgb'

    @staticmethod
    def sumar_escalar(imagen: ImagenData, valor: int):
        """Suma un valor escalar a cada pixel de la imagen."""
        cv2.add(imagen.imagen_modified, valor, imagen.imagen_modified)
        if imagen.tipo == 'binaria':
            imagen.tipo = 'gris'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def restar_escalar(imagen: ImagenData, valor: int):
        """Resta un valor escalar a cada pixel de la imagen."""
        cv2.subtract(imagen.imagen_modified, valor, imagen.imagen_modified)
        if imagen.tipo == 'binaria':
            imagen.tipo = 'gris'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def multiplicar_escalar(imagen: ImagenData, valor: int):
        """Multiplica cada pixel de la imagen por un valor escalar."""
        cv2.multiply(imagen.imagen_modified, valor, imagen.imagen_modified)
        if imagen.tipo == 'binaria':
            imagen.tipo = 'gris'
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def operaciones_aritmeticas_entre_imagenes(imagen_1: ImagenData, imagen_2: ImagenData, operacion: str):
        """
        Realiza operaciones aritméticas (suma, resta, mult) entre dos imágenes.
        Ajusta el tipo de la imagen resultante.
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
        cv2.add(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    def restar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.subtract(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    def multiplicar_imagenes(imagen_1: ImagenData, imagen_2: ImagenData):
        cv2.multiply(imagen_1.imagen_modified, imagen_2.imagen_modified, imagen_1.imagen_modified)

    @staticmethod
    def operaciones_logicas_entre_imagenes(imagen_1: ImagenData, imagen_2: ImagenData, operacion: str):
        """
        Realiza operaciones lógicas (OR, AND, XOR) entre dos imágenes.
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
        """Invierte los bits de la imagen (negativo)."""
        cv2.bitwise_not(imagen_1.imagen_modified, imagen_1.imagen_modified)
        return ProcesadorImagen.convertir_imagen_tk(imagen_1.imagen_modified)
    
    @staticmethod
    def agregar_ruido_sal_pimienta(imagen: ImagenData):
        """
        Agrega ruido de tipo 'Sal y Pimienta' a la imagen.
        """
        cantidad= 0.05
        copiaAux = imagen.imagen_modified.copy()
        numeroPixeles= int(cantidad * imagen.ancho * imagen.alto)

        # Sal (blanco)
        coordenadas = [np.random.randint(0, i - 1, numeroPixeles) for i in copiaAux.shape[:2]]
        copiaAux[coordenadas[0], coordenadas[1]] = 255 
        # Pimienta (negro)
        coordenadas = [np.random.randint(0, i - 1, numeroPixeles) for i in copiaAux.shape[:2]]
        copiaAux[coordenadas[0], coordenadas[1]] = 0
        imagen.imagen_modified = copiaAux
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def agregar_ruido_gaussiano(imagen: ImagenData):
        """
        Agrega ruido Gaussiano a la imagen.
        """
        imagen_ruido = None
        if imagen.tipo == 'binaria':
            imagen.tipo = 'gris'
        media = 0
        sigma = 25
        if imagen.tipo== 'gris' or imagen.tipo== 'binaria':
            dimensiones = imagen.imagen_modified.shape[:2]
        else:
            dimensiones = imagen.imagen_modified.shape

        gauss = np.random.normal(media, sigma, dimensiones).astype(np.int16)

        if imagen.tipo == 'gris' or imagen.tipo == 'binaria':
            imagen_ruido = imagen.imagen_modified.copy()
            for i in range(3):
                canal_ruidoso = imagen.imagen_modified[:, :, i].astype(np.int16) + gauss
                imagen_ruido[:, :, i] = np.clip(canal_ruidoso, 0, 255).astype(np.uint8)
        else:
            imagen_ruido = imagen.imagen_modified.astype(np.int16) + gauss
            imagen_ruido = np.clip(imagen_ruido, 0, 255).astype(np.uint8)

        imagen.imagen_modified = imagen_ruido
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def aplicar_filtro(filtro, imagen: ImagenData, valor_umbral_minimo = None, valor_umbral_maximo = None):
        """
        Aplica un filtro espacial o de frecuencia seleccionado.
        """
        if filtro == 'Filtro Promediador':
            ProcesadorImagen.aplicar_filtro_promediador(imagen)
        elif filtro == 'Filtro Promediador Pesado':
            ProcesadorImagen.aplicar_filtro_promediador_pesado(imagen)
        elif filtro == 'Filtro Gaussiano':
            ProcesadorImagen.aplicar_filtro_gaussiano(imagen)
        elif filtro == 'Filtro Bilateral':
            ProcesadorImagen.aplicar_filtro_bilateral(imagen)
        elif filtro == 'Filtro de Mediana':
            ProcesadorImagen.aplicar_filtro_mediana(imagen)
        elif filtro == 'Filtro de Moda':
            ProcesadorImagen.aplicar_filtro_moda(imagen)
        elif filtro == 'Filtro de Maximo':
            ProcesadorImagen.aplicar_filtro_maximo(imagen)
        elif filtro == 'Filtro de Minimo':
            ProcesadorImagen.aplicar_filtro_minimo(imagen)
        elif filtro == 'Filtro Bilateral':
            ProcesadorImagen.aplicar_filtro_bilateral(imagen)
        elif filtro == 'Filtro de Mediana Adaptativa':
            ProcesadorImagen.aplicar_filtro_adaptativo(imagen)
        elif filtro == 'Filtro de Media Contraharmonica':
            ProcesadorImagen.aplicar_filtro_contraharmonico(imagen)
        elif filtro == 'Filtro de Mediana Ponderada':
            ProcesadorImagen.aplicar_filtro_mediana_ponderada(imagen)
        elif filtro == 'Filtro de Sobel':
            ProcesadorImagen.aplicar_filtro_sobel(imagen)
        elif filtro == 'Filtro de Prewitt':
            ProcesadorImagen.aplicar_filtro_Prewitt(imagen)
        elif filtro == 'Filtro de Roberts':
            ProcesadorImagen.aplicar_filtro_roberts(imagen)
        elif filtro == 'Filtro de Canny':
            ProcesadorImagen.aplicar_filtro_canny(imagen, valor_umbral_minimo, valor_umbral_maximo)
        elif filtro == 'Filtro Laplaciano':
            ProcesadorImagen.aplicar_filtro_laplaciano(imagen)
        elif filtro == 'Filtro Laplaciano 8':
            ProcesadorImagen.aplicar_filtro_laplaciano_8(imagen)
            
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    def aplicar_filtro_promediador(imagen: ImagenData, kernel_size=3):
        """Filtro de suavizado promediador (media aritmética)."""
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        imagen.imagen_modified = cv2.filter2D(imagen.imagen_modified, -1, kernel)
    
    def aplicar_filtro_promediador_pesado(imagen: ImagenData, kernel_size=3):
        """Filtro de suavizado promediador ponderado (más peso al centro)."""
        kernel = np.ones((kernel_size, kernel_size), np.float32)
        center = kernel_size // 2
        kernel[center, center] = kernel_size * 2
        kernel /= kernel.sum()
        imagen.imagen_modified = cv2.filter2D(imagen.imagen_modified, -1, kernel)
    
    def aplicar_filtro_gaussiano(imagen: ImagenData, kernel_size=3, sigma=1.0):
        """Filtro Gaussiano para suavizado."""
        imagen.imagen_modified = cv2.GaussianBlur(imagen.imagen_modified, (kernel_size, kernel_size), sigma)
    
    def aplicar_filtro_bilateral(imagen: ImagenData, diameter=9, sigma_color=75, sigma_space=75):
        """Filtro Bilateral (suaviza preservando bordes)."""
        imagen.imagen_modified = cv2.bilateralFilter(imagen.imagen_modified, diameter, sigma_color, sigma_space)

    def aplicar_filtro_mediana(imagen: ImagenData, kernel_size=3):
        """Filtro de Mediana (efectivo para ruido sal y pimienta)."""
        imagen.imagen_modified = cv2.medianBlur(imagen.imagen_modified, kernel_size)
    
    def aplicar_filtro_moda(imagen: ImagenData, kernel_size=3):
        """Filtro de Moda (valor más frecuente en la vecindad)."""
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
        """Filtro de Máximo (dilatación)."""
        imagen.imagen_modified = cv2.dilate(imagen.imagen_modified, np.ones((kernel_size, kernel_size)))
    
    def aplicar_filtro_minimo(imagen: ImagenData, kernel_size=3):
        """Filtro de Mínimo (erosión)."""
        imagen.imagen_modified = cv2.erode(imagen.imagen_modified, np.ones((kernel_size, kernel_size)))
    
    def aplicar_filtro_adaptativo(imagen: ImagenData, max_window_size=7):
        """Filtro de Mediana Adaptativa (ajusta el tamaño de ventana según el ruido local)."""
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
        """Filtro de Media Contraharmónica (útil para ruido sal o pimienta dependiendo de Q)."""
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
        """Filtro de Mediana Ponderada."""
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
        """Filtro de Sobel para detección de bordes."""
        imagen_gris= imagen.imagen_modified[:, :, 0]
        sobel_x = cv2.Sobel(imagen_gris, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(imagen_gris, cv2.CV_64F, 0, 1, ksize=kernel_size)
        bordes = cv2.magnitude(sobel_x, sobel_y)
        bordes_final = np.clip(bordes, 0, 255).astype(np.uint8)
        imagen.imagen_modified = cv2.merge((bordes_final, bordes_final, bordes_final))

        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    def aplicar_filtro_Prewitt(imagen: ImagenData):
        """Filtro de Prewitt para detección de bordes."""
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

    def aplicar_filtro_roberts(imagen: ImagenData):
        """Filtro de Roberts para detección de bordes."""
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
        """Filtro de Canny para detección de bordes óptima."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        bordes_canny = cv2.Canny(imagen_gris, valor_umbral_minimo, valor_umbral_maximo)
        imagen.imagen_modified = cv2.merge((bordes_canny, bordes_canny, bordes_canny))
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def aplicar_filtro_laplaciano(imagen: ImagenData):
        """
        Aplica filtro Laplaciano en el dominio espacial (segunda derivada).
        """
        imagen_gris = imagen.imagen_modified[:, :, 0]
        laplaciano = cv2.Laplacian(imagen_gris, cv2.CV_64F)
        abs_laplaciano = cv2.convertScaleAbs(laplaciano)
        
        imagen.imagen_modified = cv2.merge((abs_laplaciano, abs_laplaciano, abs_laplaciano))
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def aplicar_filtro_laplaciano_8(imagen: ImagenData):
        """
        Aplica filtro Laplaciano considerando 8 vecinos (diagonales incluidas).
        """
        imagen_gris = imagen.imagen_modified[:, :, 0]
        
        laplacian_kernel_8 = np.array([[1, 1, 1],
                                       [1, -8, 1],
                                       [1, 1, 1]], dtype=np.float32)
        
        laplacian = cv2.filter2D(imagen_gris, cv2.CV_32F, laplacian_kernel_8)
        
        abs_laplacian = cv2.convertScaleAbs(laplacian)
        
        imagen.imagen_modified = cv2.merge((abs_laplacian, abs_laplacian, abs_laplacian))
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def aplicar_filtro_kirsch(imagen: ImagenData):
        """
        Aplica filtro Kirsch (detección de bordes direccional).
        """
        imagen_gris = imagen.imagen_modified[:, :, 0]
        kirsch_kernels = [
            np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]], dtype=np.float32),
            np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]], dtype=np.float32),
            np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]], dtype=np.float32),
            np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]], dtype=np.float32),
            np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]], dtype=np.float32),
            np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]], dtype=np.float32),
            np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]], dtype=np.float32),
            np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]], dtype=np.float32)
        ]
        
        max_response = np.zeros_like(imagen_gris, dtype=np.float32)
        for kernel in kirsch_kernels:
            response = cv2.filter2D(imagen_gris, cv2.CV_32F, kernel)
            max_response = np.maximum(max_response, response)
        
        abs_kirsch = cv2.convertScaleAbs(max_response)
        imagen.imagen_modified = cv2.merge((abs_kirsch, abs_kirsch, abs_kirsch))
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    @staticmethod
    def aplicar_segmentacion(metodo_segmentacion,imagen: ImagenData, umbral1, umbral2):
        """
        Aplica algoritmos de segmentación.
        """
        if metodo_segmentacion == "otsu":
            #Solo en este caso se aplica un return debido a que este metodo regresa la imagen binarizada
            return ProcesadorImagen.binarizar_metodo_otsu(imagen)
        elif metodo_segmentacion == "Metodo de entropía de Kapur":
            ProcesadorImagen.aplicar_segmentacion_entropia_kapur(imagen)
        elif metodo_segmentacion == "Método de mínimo de histograma":
            ProcesadorImagen.aplicar_segmentacion_minimo_histograma(imagen)
        elif metodo_segmentacion == "Método de la media":
            ProcesadorImagen.aplicar_segmentacion_media(imagen)
        elif metodo_segmentacion == "Método de dos umbrales":
            ProcesadorImagen.aplicar_segmentacion_dos_umbrales(imagen, umbral1, umbral2)
        elif metodo_segmentacion == "Método de umbral de banda":
            ProcesadorImagen.aplicar_segmentacion_umbral_banda(imagen, umbral1, umbral2)

        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)
    
    def aplicar_segmentacion_entropia_kapur(imagen: ImagenData):
        """Segmentación basada en la entropía de Kapur."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        histograma, _ = np.histogram(imagen_gris, bins=256, range=(0, 256))
        total_pixeles = imagen_gris.size

        max_entropia = -1
        umbral_optimo = 0

        for t in range(256):
            clase1 = histograma[:t]
            clase2 = histograma[t:]
            p1 = np.sum(clase1) / total_pixeles
            p2 = np.sum(clase2) / total_pixeles
            if p1 == 0 or p2 == 0:
                continue
            entropia1 = -np.sum((clase1 / np.sum(clase1)) * np.log(clase1 / np.sum(clase1) + 1e-10))
            entropia2 = -np.sum((clase2 / np.sum(clase2)) * np.log(clase2 / np.sum(clase2) + 1e-10))

            entropia_total = p1 * entropia1 + p2 * entropia2
            if entropia_total > max_entropia:
                max_entropia = entropia_total
                umbral_optimo = t

        imagen_kapur = (imagen_gris > umbral_optimo).astype(np.uint8) * 255
        imagen.imagen_modified = cv2.merge((imagen_kapur, imagen_kapur, imagen_kapur))
        imagen.tipo = "binaria"

    def aplicar_segmentacion_minimo_histograma(imagen: ImagenData):
        """Segmentación buscando el mínimo entre dos picos del histograma."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        histograma, _ = np.histogram(imagen_gris, bins=256, range=(0, 256))
        picos, _ = find_peaks(histograma, distance=20)
        # Si no encuentra suficientes picos, podría fallar o necesitar fallback.
        # Asumimos que encuentra al menos 2 para el rango.
        if len(picos) >= 2:
            minimo = np.argmin(histograma[picos[0]:picos[1]]) + picos[0]
        else:
            minimo = 127 # Fallback simple
            
        imagen_minimo = (imagen_gris > minimo).astype(np.uint8) * 255
        imagen.imagen_modified = cv2.merge((imagen_minimo, imagen_minimo, imagen_minimo))
        imagen.tipo = "binaria"
    
    def aplicar_segmentacion_media(imagen: ImagenData):
        """Segmentación usando la media de intensidad como umbral."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        umbral = np.mean(imagen_gris)
        imagen_media = (imagen_gris > umbral).astype(np.uint8) * 255
        imagen.imagen_modified = cv2.merge((imagen_media, imagen_media, imagen_media))
        imagen.tipo = "binaria"

    def aplicar_segmentacion_dos_umbrales(imagen: ImagenData, umbral1, umbral2):
        """Segmentación con dos umbrales (multinivel)."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_multi_umbrales = np.zeros_like(imagen_gris)
        imagen_multi_umbrales[imagen_gris < umbral1] = 0
        imagen_multi_umbrales[(imagen_gris >= umbral1) & (imagen_gris < umbral2)] = 127
        imagen_multi_umbrales[imagen_gris >= umbral2] = 255
        imagen.imagen_modified = cv2.merge((imagen_multi_umbrales, imagen_multi_umbrales, imagen_multi_umbrales))
        imagen.tipo = "gris"

    def aplicar_segmentacion_umbral_banda(imagen: ImagenData, umbral1, umbral2):
        """Segmentación por banda (mantiene solo lo que está entre umbrales)."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_umbral_banda = np.zeros_like(imagen_gris)
        imagen_umbral_banda[(imagen_gris >= umbral1) & (imagen_gris <= umbral2)] = 255
        imagen.imagen_modified = cv2.merge((imagen_umbral_banda, imagen_umbral_banda, imagen_umbral_banda))
        imagen.tipo = "binaria"

    @staticmethod
    def aplicar_ajuste_brillo(metodo_ajuste_brillo,imagen: ImagenData, valor):
        """
        Aplica técnicas de ajuste de brillo y contraste.
        """
        if metodo_ajuste_brillo == "Ecualización uniforme":
            ProcesadorImagen.ecualizacion_uniforme(imagen)
        if metodo_ajuste_brillo == "Ecualización exponencial":
            ProcesadorImagen.ecualizacion_exponencial(imagen)
        if metodo_ajuste_brillo == "Ecualización Rayleigh":
            ProcesadorImagen.ecualizacion_rayleigh(imagen)
        if metodo_ajuste_brillo == "Ecualización hipercúbica":
            ProcesadorImagen.ecualizacion_hipercubica(imagen, valor)
        if metodo_ajuste_brillo == "Ecualización logarítmica hiperbólica":
            ProcesadorImagen.ecualizacion_logaritmica_hiperbolica(imagen)
        if metodo_ajuste_brillo == "Función exponencial":
            ProcesadorImagen.funcion_exponencial(imagen, valor)
        if metodo_ajuste_brillo == "Corrección gamma":
            ProcesadorImagen.correccion_gamma(imagen, valor)

        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    def ecualizacion_uniforme(imagen: ImagenData):
        """Ecualización de histograma estándar."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_ecualizada = cv2.equalizeHist(imagen_gris)
        imagen.imagen_modified = cv2.merge((imagen_ecualizada, imagen_ecualizada, imagen_ecualizada))

    def ecualizacion_exponencial(imagen: ImagenData):
        """Ecualización con distribución exponencial."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_exponenciada = np.uint8(255 * (1 - np.exp(-imagen_gris / 255)))
        imagen.imagen_modified = cv2.merge((imagen_exponenciada, imagen_exponenciada, imagen_exponenciada))

    def ecualizacion_rayleigh(imagen: ImagenData):
        """Ecualización con distribución Rayleigh."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_rayleigh = np.uint8(255 * np.sqrt(imagen_gris / 255))
        imagen.imagen_modified = cv2.merge((imagen_rayleigh, imagen_rayleigh, imagen_rayleigh))

    def ecualizacion_hipercubica(imagen: ImagenData, potencia=4):
        """Ajuste de brillo hipercúbico."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_hipercubica = np.uint8(255 * (imagen_gris / 255) ** potencia)
        imagen.imagen_modified = cv2.merge((imagen_hipercubica, imagen_hipercubica, imagen_hipercubica))

    def ecualizacion_logaritmica_hiperbolica(imagen: ImagenData):
        """Ajuste logarítmico hiperbólico."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_logaritmica = np.uint8(255 * np.log1p(imagen_gris) / np.log1p(255))
        imagen.imagen_modified = cv2.merge((imagen_logaritmica, imagen_logaritmica, imagen_logaritmica))

    def funcion_exponencial(imagen: ImagenData, potencia=2):
        """Ajuste de brillo exponencial."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_exponencial = np.uint8(255 * (imagen_gris / 255) ** potencia)
        imagen.imagen_modified = cv2.merge((imagen_exponencial, imagen_exponencial, imagen_exponencial))

    def correccion_gamma(imagen: ImagenData, gamma=1.5):
        """Corrección Gamma."""
        imagen_gris = imagen.imagen_modified[:, :, 0]
        imagen_gamma = np.power(imagen_gris / 255.0, gamma) * 255
        imagen_gamma = np.uint8(imagen_gamma)
        imagen.imagen_modified = cv2.merge((imagen_gamma, imagen_gamma, imagen_gamma))

    @staticmethod
    def aislar_moho_resta_canales(imagen: ImagenData):
        """
        Segmentación específica para aislar moho en pan mediante resta de canales.
        Lógica: El moho suele ser azul/verdoso y el pan rojizo/tostado.
        """
        # 1. Separar la imagen en sus 3 canales base (Blue, Green, Red)
        # OpenCV carga las imágenes en orden BGR
        canal_rojo, canal_verde, canal_azul = cv2.split(imagen.imagen_modified)
        
        # 2. Aplicar la aritmética: Azul - Rojo
        # El pan tiene mucho Rojo, así que: (poco azul) - (mucho rojo) = 0 (Negro)
        # El moho tiene mucho Azul, así que: (mucho azul) - (poco rojo) = Positivo (Gris)
        diferencia = cv2.subtract(canal_azul, canal_rojo)
        
        # 5. Reconstruir para mostrar en Tkinter
        imagen.imagen_modified = cv2.merge([diferencia, diferencia, diferencia])
        imagen.tipo = 'gris'
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    @staticmethod
    def etiquetar_y_medir_moho(imagen: ImagenData):
        matriz_objetos = []
        mascara = imagen.imagen_modified[:, :, 0]
        imagen_visual = imagen.imagen_cv.copy() 

        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area_total = 0
        perimetro_total = 0

        objetos_detectados = 0
        for i, contorno in enumerate(contornos, start=1):
            vector_datos = []
            vector_datos.append(i)
            
            area = cv2.contourArea(contorno)
            area = round(area, 2)
            vector_datos.append(area)

            perimetro = cv2.arcLength(contorno, True)
            perimetro = round(perimetro, 2)
            vector_datos.append(perimetro)
            objetos_detectados += 1
            area_total += area
            perimetro_total += perimetro

            matriz_objetos.append(vector_datos)
            
            x, y, w, h = cv2.boundingRect(contorno)
            M = cv2.moments(contorno)
            cX, cY = 0, 0
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

            cv2.drawContours(imagen_visual, [contorno], -1, (0, 255, 0), 2)

            texto_id = f"#{i}"
            cv2.putText(imagen_visual, texto_id, (cX - 10, cY), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (255, 0, 0), 2)



        cv2.rectangle(imagen_visual, (0, 0), (300, 150), (0, 0, 0), -1)
        cv2.putText(imagen_visual, f"Total Manchas: {objetos_detectados}", (10, 25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(imagen_visual, f"Area Total: {area_total:.2f}", (10, 75), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(imagen_visual, f"Perimetro Total: {perimetro_total:.2f}", (10, 125), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        imagen.imagen_modified = imagen_visual
        imagen.tipo = 'componentes'
        
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified), matriz_objetos

    @staticmethod
    def aplicar_morfologia(tipo_morfologia, imagen: ImagenData):
        """
        Aplica una operación de morfología a la imagen.
        
        Args:
            tipo_morfologia (str): Nombre de la operación de morfología.
            imagen (ImagenData): Imagen a la que se le aplica la operación.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """

        if tipo_morfologia == 'Erosión':
            ProcesadorImagen.erosionar(imagen)
        elif tipo_morfologia == 'Dilatación':
            ProcesadorImagen.dilatar(imagen)
        elif tipo_morfologia == 'Apertura':
            ProcesadorImagen.apertura(imagen)
        elif tipo_morfologia == 'Cierre':
            ProcesadorImagen.cierre(imagen)
        return ProcesadorImagen.convertir_imagen_tk(imagen.imagen_modified)

    @staticmethod
    def erosionar(imagen: ImagenData):
        kernel = np.ones((5,5), np.uint8)
        imagen_erosionada = cv2.erode(imagen.imagen_modified[:, :, 0], kernel, iterations = 1) 
        imagen.imagen_modified = cv2.merge((imagen_erosionada, imagen_erosionada, imagen_erosionada))

    @staticmethod
    def dilatar(imagen: ImagenData):
        kernel = np.ones((5,5), np.uint8)
        imagen_dilatada = cv2.dilate(imagen.imagen_modified[:, :, 0], kernel, iterations = 1)
        imagen.imagen_modified = cv2.merge((imagen_dilatada, imagen_dilatada, imagen_dilatada))

    @staticmethod
    def apertura(imagen: ImagenData):
        kernel = np.ones((5,5), np.uint8)
        imagen_apertura = cv2.morphologyEx(imagen.imagen_modified[:, :, 0], cv2.MORPH_OPEN, kernel)
        imagen.imagen_modified = cv2.merge((imagen_apertura, imagen_apertura, imagen_apertura))

    @staticmethod
    def cierre(imagen: ImagenData):
        kernel = np.ones((5,5), np.uint8)
        imagen_cierre = cv2.morphologyEx(imagen.imagen_modified[:, :, 0], cv2.MORPH_CLOSE, kernel)
        imagen.imagen_modified = cv2.merge((imagen_cierre, imagen_cierre, imagen_cierre))

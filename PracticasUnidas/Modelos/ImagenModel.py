from Utilidades.ProcesadorImagen import ProcesadorImagen

"""
Modelo de la aplicación.
Gestiona el estado de las imágenes y delega el procesamiento a la clase ProcesadorImagen.
"""

class ImageModel:
    """
    Clase Modelo que almacena las imágenes cargadas y gestiona las operaciones sobre ellas.
    Actúa como intermediario entre el Controlador y la utilidad de procesamiento de imágenes.
    """
    def __init__(self):
        """
        Inicializa el modelo con dos espacios para imágenes (imagen1 e imagen2).
        Inicialmente están vacíos (None).
        """
        self.imagen1 = None
        self.imagen2 = None

    def checar_existencia_imagen(self, numero_imagen):
        """
        Verifica si una imagen específica está cargada en el modelo.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
            
        Returns:
            bool: True si la imagen existe, False en caso contrario.
        """
        if numero_imagen == 1:
            if self.imagen1 is None:
                return False 
            return True
        elif numero_imagen == 2:
            if self.imagen2 is None:
                return False 
            return True
    
    def crear_imagen(self, ruta, numero_imagen):
        """
        Carga una imagen desde una ruta y la almacena en el modelo.
        
        Args:
            ruta (str): Ruta del archivo de imagen.
            numero_imagen (int): Identificador de la imagen (1 o 2).
            
        Returns:
            tuple or str: Tupla con la imagen TK y su histograma si es exitoso, o mensaje de error.
        """
        # Validación: Para cargar la imagen 2, la imagen 1 debe existir (regla de negocio opcional)
        if numero_imagen == 2 and self.imagen1 is None:
            return "La imagen 1 no está cargada."
            
        resultadoCreacion = ProcesadorImagen.cargar_imagen(ruta)
        
        # Si hubo un error al cargar (retorna string), se propaga el error
        if isinstance(resultadoCreacion, str):
            return resultadoCreacion
            
        if numero_imagen == 1:
            self.imagen1 = resultadoCreacion
        elif numero_imagen == 2:
            self.imagen2 = resultadoCreacion
            
        # Retorna la representación visual (TK) y el histograma inicial
        return (ProcesadorImagen.convertir_imagen_tk(resultadoCreacion.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(resultadoCreacion.imagen_modified))

    def _determinarImagen(self, numero_imagen):
        """
        Método auxiliar para obtener la instancia de imagen correspondiente al número.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
            
        Returns:
            ImagenData: Objeto con los datos de la imagen.
        """
        if numero_imagen == 1:
            return self.imagen1
        elif numero_imagen == 2:
            return self.imagen2

    def reiniciar_imagen(self, numero_imagen):
        """
        Reinicia la imagen a su estado original.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
            
        Returns:
            tuple: Imagen TK reiniciada y su histograma.
        """
        return ProcesadorImagen.reiniciar_imagen(self._determinarImagen(numero_imagen))

    def guardar_imagen(self, numero_imagen):
        """
        Guarda la imagen actual en disco.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        imagen = self._determinarImagen(numero_imagen)
        ProcesadorImagen.guardar_imagen(imagen)

    def convertir_escala_grises(self, numero_imagen):
        """
        Convierte la imagen a escala de grises.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
            
        Returns:
            tuple: Imagen TK en grises y su histograma.
        """
        histograma = None
        imagen = self._determinarImagen(numero_imagen)

        # Calcula el histograma antes o después de la conversión según la lógica deseada
        # Aquí parece que se calcula sobre la imagen modificada (que será gris)
        # Nota: La implementación original calculaba histograma gris ANTES de convertir? 
        # Revisando lógica original: 
        # histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        # return (ProcesadorImagen.convertir_escala_grises(imagen), histograma)
        # Esto parece asumir que ya es gris o se calcula sobre lo que será. 
        # Corrección lógica: Primero convertimos, luego calculamos histograma o al revés si la función 'convertir' modifica in-place.
        # ProcesadorImagen.convertir_escala_grises modifica in-place el objeto imagen.
        
        imagen_tk = ProcesadorImagen.convertir_escala_grises(imagen)
        histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)

        return (imagen_tk, histograma)

    def binarizar_imagen(self, numero_imagen, metodo: str, umbral: int = None):
        """
        Binariza la imagen usando un método específico (fijo u Otsu).
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
            metodo (str): Método de binarización ('fijo' u 'otsu').
            umbral (int, optional): Valor umbral para el método fijo.
            
        Returns:
            list: Lista con la imagen TK binarizada y None (histograma no aplica igual para visualización estándar).
        """
        histograma = None
        imagen = self._determinarImagen(numero_imagen)
        if metodo == 'fijo':
            return [ProcesadorImagen.binarizar_metodo_fijo(imagen, umbral), None]
        if metodo == 'otsu':
            return [ProcesadorImagen.binarizar_metodo_otsu(imagen), None]
        
    def realizar_operacion_aritmetica_escalar(self, numero_imagen, operacion: str, valor: int):
        """
        Realiza una operación aritmética escalar sobre la imagen.
        
        Args:
            numero_imagen (int): Identificador de la imagen.
            operacion (str): Tipo de operación ('suma', 'resta', 'multiplicacion').
            valor (int): Valor escalar.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        imagen = self._determinarImagen(numero_imagen)
        histograma = None

        if operacion == 'suma':
            resultado_operacion = ProcesadorImagen.sumar_escalar(imagen, valor)
        if operacion == 'resta':
            resultado_operacion = ProcesadorImagen.restar_escalar(imagen, valor)
        if operacion == 'multiplicacion':
            resultado_operacion = ProcesadorImagen.multiplicar_escalar(imagen, valor)
        
        # Recalcular histograma según el tipo resultante
        if imagen.tipo == 'rgb':
            histograma = ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified)
        elif imagen.tipo == 'gris':
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        return (resultado_operacion, histograma, imagen.tipo)
    
    def realizar_operacion_aritmetica_entre_imagenes(self, numero_imagen_1, numero_imagen_2, operacion: str):
        """
        Realiza una operación aritmética entre dos imágenes.
        
        Args:
            numero_imagen_1 (int): Identificador de la primera imagen.
            numero_imagen_2 (int): Identificador de la segunda imagen.
            operacion (str): Tipo de operación.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        histograma = None
        imagen_1 = self._determinarImagen(numero_imagen_1)
        imagen_2 = self._determinarImagen(numero_imagen_2)
        resultado_operacion = ProcesadorImagen.operaciones_aritmeticas_entre_imagenes(imagen_1, imagen_2, operacion)
        
        if imagen_1.tipo == 'rgb':
            histograma = ProcesadorImagen.calcular_histograma_color(imagen_1.imagen_modified)
        elif imagen_1.tipo == 'gris':
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen_1.imagen_modified)
        
        return (resultado_operacion, histograma, imagen_1.tipo)
    
    def realizar_operacion_logica_entre_imagenes(self, numero_imagen_1, numero_imagen_2, operacion: str):
        """
        Realiza una operación lógica entre dos imágenes.
        
        Args:
            numero_imagen_1 (int): Identificador de la primera imagen.
            numero_imagen_2 (int): Identificador de la segunda imagen.
            operacion (str): Tipo de operación.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        histograma = None
        imagen_1 = self._determinarImagen(numero_imagen_1)
        imagen_2 = self._determinarImagen(numero_imagen_2)
        resultado_operacion = ProcesadorImagen.operaciones_logicas_entre_imagenes(imagen_1, imagen_2, operacion)
        
        if imagen_1.tipo == 'rgb':
            histograma = ProcesadorImagen.calcular_histograma_color(imagen_1.imagen_modified)
        elif imagen_1.tipo == 'gris':
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen_1.imagen_modified)
        return (resultado_operacion, histograma, imagen_1.tipo)
    
    def operacion_not(self, numero_imagen):
        """
        Aplica la operación NOT a la imagen.
        
        Args:
            numero_imagen (int): Identificador de la imagen.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        histograma = None
        imagen = self._determinarImagen(numero_imagen)
        resultado_operacion =  ProcesadorImagen.not_logico(imagen)

        if imagen.tipo == 'rgb':
            histograma = ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified)
        elif imagen.tipo == 'gris':
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        return (resultado_operacion, histograma, imagen.tipo)

    def agregar_ruido(self, tipo_ruido, numero_imagen):
        """
        Agrega ruido a la imagen.
        
        Args:
            tipo_ruido (str): Tipo de ruido ('sal y pimienta', 'gaussiano').
            numero_imagen (int): Identificador de la imagen.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        histograma = None
        imagen = self._determinarImagen(numero_imagen)

        if tipo_ruido == "sal y pimienta":
            resultado_operacion = ProcesadorImagen.agregar_ruido_sal_pimienta(imagen)
        elif tipo_ruido == "gaussiano":
            resultado_operacion = ProcesadorImagen.agregar_ruido_gaussiano(imagen)

        if imagen.tipo == 'rgb':
            histograma = ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified)
        elif imagen.tipo == 'gris':
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        return (resultado_operacion, histograma, imagen.tipo)

    def aplicar_filtro(self, filtro, numero_imagen, valor_umbral_minimo = None, valor_umbral_maximo = None):
        """
        Aplica un filtro a la imagen.
        
        Args:
            filtro (str): Nombre del filtro.
            numero_imagen (int): Identificador de la imagen.
            valor_umbral_minimo (int, optional): Umbral mínimo (para Canny) o Radio (D0) para filtros de frecuencia.
            valor_umbral_maximo (int, optional): Umbral máximo (para Canny).
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        histograma = None
        imagen = self._determinarImagen(numero_imagen)
    
        resultado_operacion = ProcesadorImagen.aplicar_filtro(filtro, imagen, valor_umbral_minimo, valor_umbral_maximo)

        if imagen.tipo == 'rgb':
            histograma = ProcesadorImagen.calcular_histograma_color(imagen.imagen_modified)
        elif imagen.tipo == 'gris':
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
            
        return (resultado_operacion, histograma, imagen.tipo)

    def determinar_tipo_imagen(self, numero_imagen):
        """
        Devuelve el tipo de la imagen (e.g., 'rgb', 'gris').
        
        Args:
            numero_imagen (int): Identificador de la imagen.
            
        Returns:
            str: Tipo de imagen.
        """
        imagen = self._determinarImagen(numero_imagen)
        return imagen.tipo

    def aplicar_segmentacion(self, tipo_segmentacion, numero_imagen, valor_umbral_1 = None, valor_umbral_2 = None):
        """
        Aplica un filtro de segmentacion a la imagen.
        
        Args:
            tipo_segmentacion (str): Nombre del filtro.
            numero_imagen (int): Identificador de la imagen.
            valor_umbral_1 (int, optional): Primer umbral.
            valor_umbral_2 (int, optional): Segundo umbral.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        histograma = None
        imagen = self._determinarImagen(numero_imagen)

        if tipo_segmentacion == "Método de segmentación por resta canales":
            resultado_operacion = ProcesadorImagen.aislar_moho_resta_canales(imagen)
            return (resultado_operacion, histograma, imagen.tipo)

        resultado_operacion = ProcesadorImagen.aplicar_segmentacion(tipo_segmentacion, imagen, valor_umbral_1, valor_umbral_2)
        
        if tipo_segmentacion == "Método de dos umbrales":
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        else:
            histograma = None

        return (resultado_operacion, histograma, imagen.tipo)

    def aplicar_ajuste_brillo(self, tipo_ajuste, numero_imagen, valor_operacion= None):
        """
        Aplica un ajuste de brillo a la imagen.
        
        Args:
            tipo_ajuste (str): Nombre del ajuste.
            numero_imagen (int): Identificador de la imagen.
            valor_operacion (int, optional): Valor de la operacion.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        imagen = self._determinarImagen(numero_imagen)

        resultado_operacion = ProcesadorImagen.aplicar_ajuste_brillo(tipo_ajuste, imagen, valor_operacion)
        histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        return (resultado_operacion, histograma, imagen.tipo)
    
    def aplicar_etiquetado_y_contornos(self, numero_imagen):
        """
        Aplica etiquetado de componentes conexos y detección de contornos.
        
        Args:
            numero_imagen (int): Identificador de la imagen.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        imagen = self._determinarImagen(numero_imagen)
        resultado_operacion, matriz_objetos = ProcesadorImagen.etiquetar_y_medir_moho(imagen)
        histograma = None
        return (resultado_operacion, histograma, imagen.tipo, matriz_objetos)

    def aplicar_morfologia(self, tipo_morfologia, numero_imagen):
        """
        Aplica una operación de morfología a la imagen.
        
        Args:
            tipo_morfologia (str): Nombre de la operación de morfología.
            numero_imagen (int): Identificador de la imagen.
            
        Returns:
            tuple: Imagen resultante, histograma y tipo de imagen.
        """
        imagen = self._determinarImagen(numero_imagen)
        imagen_modificada = ProcesadorImagen.aplicar_morfologia(tipo_morfologia, imagen)
        
        if imagen.tipo == 'gris':
            histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        else:
            histograma = None
        return (imagen_modificada, histograma, imagen.tipo)
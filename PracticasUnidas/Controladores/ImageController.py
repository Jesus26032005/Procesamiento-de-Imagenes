from Modelos.ImagenModel import ImageModel
from Vistas.mainWindow import MainWindow 

"""
Controlador principal de la aplicación.
Maneja la interacción entre la vista (MainWindow) y el modelo (ImageModel).
"""

class ImageController:
    """
    Clase Controlador que gestiona la lógica de la aplicación y la comunicación
    entre la interfaz de usuario y el modelo de datos.
    """
    def __init__(self, model, view):
        """
        Inicializa el controlador con el modelo y la vista.
        Conecta los eventos de los botones de la interfaz.
        
        Args:
            model (ImageModel): Instancia del modelo de la imagen.
            view (MainWindow): Instancia de la ventana principal.
        """
        self.model = model
        self.view = view
        
        # Conectar los eventos de las diferentes secciones de la interfaz
        self.conectar_eventos_basicos()
        self.conectar_eventos_operaciones()
        self.conectar_eventos_filtros()
        self.conectar_eventos_segmentacion()
        self.conectar_eventos_ajuste_brillo()
        self.conectar_eventos_morfologia()

    def conectar_eventos_basicos(self):
        """
        Conecta los eventos de los botones de la pestaña principal (Cargar, Guardar, Reiniciar, etc.).
        Asigna las funciones correspondientes a cada botón.
        """
        self.tabulador_main = self.view.tabulator_main
        
        # Eventos para cargar imágenes
        self.tabulador_main.button_cargar_img1.config(command= lambda: self.cargar_imagen(1))
        self.tabulador_main.button_cargar_img2.config(command= lambda: self.cargar_imagen(2))
        
        # Eventos para reiniciar imágenes
        self.tabulador_main.button_reiniciar_img1.config(command= lambda: self.reiniciar_imagen(1))
        self.tabulador_main.button_reiniciar_img2.config(command= lambda: self.reiniciar_imagen(2))
        
        # Eventos para conversión a escala de grises
        self.tabulador_main.button_convertir_grises_img1.config(command= lambda: self.convertir_grises(1))
        self.tabulador_main.button_convertir_grises_img2.config(command= lambda: self.convertir_grises(2))
        
        # Eventos para binarización fija
        self.tabulador_main.button_binarizar_fijo_img1.config(command= lambda: self.binarizar_fijo(1))
        self.tabulador_main.button_binarizar_fijo_img2.config(command= lambda: self.binarizar_fijo(2))
        
        # Eventos para binarización Otsu
        self.tabulador_main.button_binarizar_otsu_img1.config(command= lambda: self.binarizar_otsu(1))
        self.tabulador_main.button_binarizar_otsu_img2.config(command= lambda: self.binarizar_otsu(2))
        
        # Eventos para guardar imágenes
        self.tabulador_main.button_guardar_img1.config(command= lambda: self.guardar_imagen(1))
        self.tabulador_main.button_guardar_img2.config(command= lambda: self.guardar_imagen(2))

    def conectar_eventos_operaciones(self):
        """
        Conecta los eventos de los botones de la pestaña de operaciones aritméticas y lógicas.
        """
        self.tabulator_operations = self.view.tabulator_operations
        
        # Operaciones aritméticas escalares para Imagen 1
        self.tabulator_operations.boton_sumar_escalar_img1.config(command= lambda: self.operacion_aritmetica_escalar("suma", 1))
        self.tabulator_operations.boton_restar_escalar_img1.config(command= lambda: self.operacion_aritmetica_escalar("resta", 1))
        self.tabulator_operations.boton_multiplicar_escalar_img1.config(command= lambda: self.operacion_aritmetica_escalar("multiplicacion", 1))

        # Operaciones aritméticas entre imágenes (Img1 vs Img2)
        self.tabulator_operations.boton_sumar_entre_img1.config(command= lambda: self.operacion_aritmetica_entre_imagenes("suma", 1, 2))
        self.tabulator_operations.boton_restar_entre_img1.config(command= lambda: self.operacion_aritmetica_entre_imagenes("resta", 1, 2))
        self.tabulator_operations.boton_multiplicar_entre_img1.config(command= lambda: self.operacion_aritmetica_entre_imagenes("multiplicacion", 1, 2))

        # Operaciones lógicas para Imagen 1
        self.tabulator_operations.boton_or_logico_img1.config(command= lambda: self.operacion_logica_entre_imagenes("or", 1, 2))
        self.tabulator_operations.boton_and_logico_img1.config(command= lambda: self.operacion_logica_entre_imagenes("and", 1, 2))
        self.tabulator_operations.boton_not_logico_img1.config(command= lambda: self.operacion_not(1))
        self.tabulator_operations.boton_xor_logico_img1.config(command= lambda: self.operacion_logica_entre_imagenes("xor", 1, 2))

        # Operaciones aritméticas escalares para Imagen 2
        self.tabulator_operations.boton_sumar_escalar_img2.config(command= lambda: self.operacion_aritmetica_escalar("suma", 2))
        self.tabulator_operations.boton_restar_escalar_img2.config(command= lambda: self.operacion_aritmetica_escalar("resta", 2))
        self.tabulator_operations.boton_multiplicar_escalar_img2.config(command= lambda: self.operacion_aritmetica_escalar("multiplicacion", 2))

        # Operaciones aritméticas entre imágenes (Img2 vs Img1)
        self.tabulator_operations.boton_sumar_entre_img2.config(command= lambda: self.operacion_aritmetica_entre_imagenes("suma", 2, 1))
        self.tabulator_operations.boton_restar_entre_img2.config(command= lambda: self.operacion_aritmetica_entre_imagenes("resta", 2, 1))
        self.tabulator_operations.boton_multiplicar_entre_img2.config(command= lambda: self.operacion_aritmetica_entre_imagenes("multiplicacion", 2, 1))

        # Operaciones lógicas para Imagen 2
        self.tabulator_operations.boton_or_logico_img2.config(command= lambda: self.operacion_logica_entre_imagenes("or", 2, 1))
        self.tabulator_operations.boton_and_logico_img2.config(command= lambda: self.operacion_logica_entre_imagenes("and", 2, 1))
        self.tabulator_operations.boton_not_logico_img2.config(command= lambda: self.operacion_not(2))
        self.tabulator_operations.boton_xor_logico_img2.config(command= lambda: self.operacion_logica_entre_imagenes("xor", 2, 1))

        # Operaciones extra (Etiquetado y contornos)
        self.tabulator_operations.boton_extra_img1.config(command = lambda: self.aplicar_etiquetado_y_contornos(1))
        self.tabulator_operations.boton_extra_img2.config(command= lambda: self.aplicar_etiquetado_y_contornos(2))

    def conectar_eventos_filtros(self):
        """
        Conecta los eventos de los botones de la pestaña de filtros y ruido.
        """
        self.tabulator_filters= self.view.tabulator_filters
        
        # Ruido Sal y Pimienta
        self.tabulator_filters.boton_agregar_ruido_sal_y_pimienta_Img1.config(command= lambda: self.agregar_ruido("sal y pimienta",1))
        self.tabulator_filters.boton_agregar_ruido_sal_y_pimienta_Img2.config(command= lambda: self.agregar_ruido("sal y pimienta",2))
        
        # Ruido Gaussiano
        self.tabulator_filters.boton_agregar_ruido_gaussiano_Img1.config(command= lambda: self.agregar_ruido("gaussiano",1))
        self.tabulator_filters.boton_agregar_ruido_gaussiano_Img2.config(command= lambda: self.agregar_ruido("gaussiano",2))
        
        # Aplicar Filtros seleccionados
        self.tabulator_filters.boton_aplicar_filtro_Img1.config(command= lambda: self.aplicar_filtro(1))
        self.tabulator_filters.boton_aplicar_filtro_Img2.config(command= lambda: self.aplicar_filtro(2))

    def conectar_eventos_segmentacion(self):
        """
        Conecta los eventos de los botones de la pestaña de segmentación.
        """
        self.tabulator_segmentation = self.view.tabulator_segmentation
        
        # Segmentación Otsu
        self.tabulator_segmentation.boton_segmentacion_otsu_img1.config(command= lambda: self.aplicar_segmentacion("otsu",1))
        self.tabulator_segmentation.boton_segmentacion_otsu_img2.config(command= lambda: self.aplicar_segmentacion("otsu",2))
        
        # Segmentación Entropía de Kapur
        self.tabulator_segmentation.boton_segmentacion_entropia_kapur_img1.config(command= lambda: self.aplicar_segmentacion("Metodo de entropía de Kapur",1))
        self.tabulator_segmentation.boton_segmentacion_entropia_kapur_img2.config(command= lambda: self.aplicar_segmentacion("Metodo de entropía de Kapur",2))
        
        # Segmentación Mínimo Histograma
        self.tabulator_segmentation.boton_minimo_histograma_img1.config(command= lambda: self.aplicar_segmentacion("Método de mínimo de histograma",1))
        self.tabulator_segmentation.boton_minimo_histograma_img2.config(command= lambda: self.aplicar_segmentacion("Método de mínimo de histograma",2))
        
        # Segmentación Media
        self.tabulator_segmentation.boton_segmentacion_media_img1.config(command= lambda: self.aplicar_segmentacion("Método de la media",1))
        self.tabulator_segmentation.boton_segmentacion_media_img2.config(command= lambda: self.aplicar_segmentacion("Método de la media",2))
        
        # Segmentación Dos Umbrales
        self.tabulator_segmentation.boton_segmentacion_dos_umbrales_img1.config(command= lambda: self.aplicar_segmentacion("Método de dos umbrales",1))
        self.tabulator_segmentation.boton_segmentacion_dos_umbrales_img2.config(command= lambda: self.aplicar_segmentacion("Método de dos umbrales",2))
        
        # Segmentación Umbral de Banda
        self.tabulator_segmentation.boton_segmentacion_umbral_banda_img1.config(command= lambda: self.aplicar_segmentacion("Método de umbral de banda",1))
        self.tabulator_segmentation.boton_segmentacion_umbral_banda_img2.config(command= lambda: self.aplicar_segmentacion("Método de umbral de banda",2))
        
        # Segmentación Resta de Canales (Moho)
        self.tabulator_segmentation.boton_segmentacion_moho_hsv_img1.config(command= lambda: self.aplicar_segmentacion("Método de segmentación por resta canales",1))
        self.tabulator_segmentation.boton_segmentacion_moho_hsv_img2.config(command= lambda: self.aplicar_segmentacion("Método de segmentación por resta canales",2))

    def conectar_eventos_ajuste_brillo(self):
        """
        Conecta los eventos de los botones de la pestaña de ajuste de brillo.
        """
        self.tabulator_brightness = self.view.tabulator_brightness
        
        # Ecualización Uniforme
        self.tabulator_brightness.boton_ecualizacion_uniforme_img1.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización uniforme",1))
        self.tabulator_brightness.boton_ecualizacion_uniforme_img2.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización uniforme",2))
        
        # Ecualización Exponencial
        self.tabulator_brightness.boton_ecualizacion_exponencial_img1.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización exponencial",1))
        self.tabulator_brightness.boton_ecualizacion_exponencial_img2.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización exponencial",2))
        
        # Ecualización Rayleigh
        self.tabulator_brightness.boton_ecualizacion_Rayleigh_img1.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización Rayleigh",1))
        self.tabulator_brightness.boton_ecualizacion_Rayleigh_img2.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización Rayleigh",2))
        
        # Ecualización Hipercúbica
        self.tabulator_brightness.boton_ecualizacion_hipercubica_img1.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización hipercúbica",1))
        self.tabulator_brightness.boton_ecualizacion_hipercubica_img2.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización hipercúbica",2))
        
        # Ecualización Logarítmica Hiperbólica
        self.tabulator_brightness.boton_ecualizacion_logaritmica_hiperbolica_img1.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización logarítmica hiperbólica",1))
        self.tabulator_brightness.boton_ecualizacion_logaritmica_hiperbolica_img2.config(command= lambda: self.aplicar_ajuste_brillo("Ecualización logarítmica hiperbólica",2))
        
        # Función Exponencial
        self.tabulator_brightness.boton_funcion_exponencial_img1.config(command= lambda: self.aplicar_ajuste_brillo("Función exponencial",1))
        self.tabulator_brightness.boton_funcion_exponencial_img2.config(command= lambda: self.aplicar_ajuste_brillo("Función exponencial",2))
        
        # Corrección Gamma
        self.tabulator_brightness.boton_correccion_gamma_img1.config(command= lambda: self.aplicar_ajuste_brillo("Corrección gamma",1))
        self.tabulator_brightness.boton_correccion_gamma_img2.config(command= lambda: self.aplicar_ajuste_brillo("Corrección gamma",2))

    def conectar_eventos_morfologia(self):
        self.tabulator_morphology = self.view.tabulator_morphology
        # Erosión
        self.tabulator_morphology.boton_erosion_img1.config(command= lambda: self.aplicar_morfologia("Erosión",1))
        self.tabulator_morphology.boton_erosion_img2.config(command= lambda: self.aplicar_morfologia("Erosión",2))
        
        # Dilatación
        self.tabulator_morphology.boton_dilatacion_img1.config(command= lambda: self.aplicar_morfologia("Dilatación",1))
        self.tabulator_morphology.boton_dilatacion_img2.config(command= lambda: self.aplicar_morfologia("Dilatación",2))
        
        # Apertura
        self.tabulator_morphology.boton_apertura_img1.config(command= lambda: self.aplicar_morfologia("Apertura",1))
        self.tabulator_morphology.boton_apertura_img2.config(command= lambda: self.aplicar_morfologia("Apertura",2))
        
        # Cierre
        self.tabulator_morphology.boton_cierre_img1.config(command= lambda: self.aplicar_morfologia("Cierre",1))
        self.tabulator_morphology.boton_cierre_img2.config(command= lambda: self.aplicar_morfologia("Cierre",2))
        
        # Frontera
        self.tabulator_morphology.boton_frontera_img1.config(command= lambda: self.aplicar_morfologia("Frontera",1))
        self.tabulator_morphology.boton_frontera_img2.config(command= lambda: self.aplicar_morfologia("Frontera",2))
        
        # Hit or miss
        self.tabulator_morphology.boton_hit_or_miss_img1.config(command= lambda: self.aplicar_morfologia("Hit or miss",1))
        self.tabulator_morphology.boton_hit_or_miss_img2.config(command= lambda: self.aplicar_morfologia("Hit or miss",2))
        
        # Adelgazamiento
        self.tabulator_morphology.boton_adelgazamiento_img1.config(command= lambda: self.aplicar_morfologia("Adelgazamiento",1))
        self.tabulator_morphology.boton_adelgazamiento_img2.config(command= lambda: self.aplicar_morfologia("Adelgazamiento",2))
        
        # Suavizado morfológico
        self.tabulator_morphology.boton_suavizado_morfologico_img1.config(command= lambda: self.aplicar_morfologia("Suavizado morfológico",1))
        self.tabulator_morphology.boton_suavizado_morfologico_img2.config(command= lambda: self.aplicar_morfologia("Suavizado morfológico",2))
        
        # Gradiente por erosión
        self.tabulator_morphology.boton_grad_erosion_img1.config(command= lambda: self.aplicar_morfologia("Gradiente por erosión",1))
        self.tabulator_morphology.boton_grad_erosion_img2.config(command= lambda: self.aplicar_morfologia("Gradiente por erosión",2))
        
        # Gradiente por dilatación
        self.tabulator_morphology.boton_grad_dilatacion_img1.config(command= lambda: self.aplicar_morfologia("Gradiente por dilatación",1))
        self.tabulator_morphology.boton_grad_dilatacion_img2.config(command= lambda: self.aplicar_morfologia("Gradiente por dilatación",2))
        
        # Gradiente simétrico
        self.tabulator_morphology.boton_grad_simetrico_img1.config(command= lambda: self.aplicar_morfologia("Gradiente simétrico",1))
        self.tabulator_morphology.boton_grad_simetrico_img2.config(command= lambda: self.aplicar_morfologia("Gradiente simétrico",2))
        
        # Top-hat
        self.tabulator_morphology.boton_tophat_img1.config(command= lambda: self.aplicar_morfologia("Top-hat",1))
        self.tabulator_morphology.boton_tophat_img2.config(command= lambda: self.aplicar_morfologia("Top-hat",2))
        
        # Black-hat
        self.tabulator_morphology.boton_blackhat_img1.config(command= lambda: self.aplicar_morfologia("Black-hat",1))
        self.tabulator_morphology.boton_blackhat_img2.config(command= lambda: self.aplicar_morfologia("Black-hat",2))

    def cargar_imagen(self, numero_imagen):
        """
        Maneja la carga de una imagen desde el sistema de archivos.
        Solicita al usuario la ruta del archivo y actualiza el modelo y la vista.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        rutaArchivo = self.tabulador_main.pedir_ruta_archivo()
        if rutaArchivo:
            imagen_creada = self.model.crear_imagen(rutaArchivo, numero_imagen)
            # Si la creación es exitosa, devuelve una tupla (imagen, histograma)
            if isinstance(imagen_creada, tuple):
                self.view.mostrar_imagen_cargada([imagen_creada[0], imagen_creada[0]], imagen_creada[1], numero_imagen)
            else:
                # Si hay error, devuelve un mensaje string
                self.view.mostrar_mensaje(imagen_creada, "error")
        else:
            self.view.mostrar_mensaje("No se seleccionó ninguna imagen.", "info")

    def guardar_imagen(self, numero_imagen):
        """
        Maneja el guardado de la imagen actual en el sistema de archivos.
        Verifica si hay una imagen cargada antes de intentar guardar.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        rutaArchivo = self.tabulador_main.pedir_ruta_archivo_guardar()
        if rutaArchivo:
            self.model.guardar_imagen(numero_imagen)
        else:
            self.view.mostrar_mensaje("No se seleccionó ninguna imagen.", "info")

    def reiniciar_imagen(self, numero_imagen):
        """
        Reinicia la imagen a su estado original (como fue cargada).
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        imagen_reiniciada = self.model.reiniciar_imagen(numero_imagen)
        self.view.actualizar_imagen(imagen_reiniciada[0], imagen_reiniciada[1], numero_imagen, "rgb")
    
    def convertir_grises(self, numero_imagen):
        """
        Convierte la imagen seleccionada a escala de grises.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return
            
        imagen_convertida = self.model.convertir_escala_grises(numero_imagen)
        self.view.actualizar_imagen(imagen_convertida[0], imagen_convertida[1], numero_imagen, "gris")
    
    def binarizar_fijo(self, numero_imagen):
        """
        Aplica binarización con un umbral fijo ingresado por el usuario.
        Requiere que la imagen esté previamente en escala de grises.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return
        
        valorUmbral = None
        imagen = self.model._determinarImagen(numero_imagen)
        if imagen.tipo != 'gris':
            self.view.mostrar_mensaje("La imagen debe estar en escala de grises.", "error")
            return

        valorUmbral = self.tabulador_main.aviso_binarizar_fijo()
        if valorUmbral:
            imagen_binarizada = self.model.binarizar_imagen(numero_imagen, "fijo", valorUmbral)
            self.view.actualizar_imagen(imagen_binarizada[0], imagen_binarizada[1], numero_imagen, "binaria")

    def binarizar_otsu(self, numero_imagen):
        """
        Aplica binarización utilizando el método de Otsu para calcular el umbral automáticamente.
        Requiere que la imagen esté previamente en escala de grises.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return
        
        imagen = self.model._determinarImagen(numero_imagen)
        if imagen.tipo != 'gris':
            self.view.mostrar_mensaje("La imagen debe estar en escala de grises.", "error")
            return
        imagen_binarizada = self.model.binarizar_imagen(numero_imagen, "otsu")
        self.view.actualizar_imagen(imagen_binarizada[0], imagen_binarizada[1], numero_imagen, "binaria")

    def operacion_aritmetica_escalar(self, operacion, numero_imagen):
        """
        Realiza operaciones aritméticas (suma, resta, multiplicación) con un valor escalar.
        Valida que el valor ingresado sea correcto (entero o flotante según corresponda).
        
        Args:
            operacion (str): Tipo de operación ('suma', 'resta', 'multiplicacion').
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return
        
        if numero_imagen == 1:
            valor = self.tabulator_operations.campo_entrada_valor_img1.get()
        else:
            valor = self.tabulator_operations.campo_entrada_valor_img2.get()

        if operacion == 'suma' or operacion == 'resta':
            try:
                valor = int(valor)
            except ValueError:
                self.view.mostrar_mensaje("El valor debe ser un número entero.", "error")
                return
        else:
            try:
                valor = float(valor)
            except ValueError:
                self.view.mostrar_mensaje("El valor debe ser un número.", "error")
                return

        imagen_operada = self.model.realizar_operacion_aritmetica_escalar(numero_imagen, operacion, valor)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen, imagen_operada[2])
        
    def operacion_aritmetica_entre_imagenes(self, operacion, numero_imagen_1, numero_imagen_2):
        """
        Realiza operaciones aritméticas entre dos imágenes.
        Verifica que ambas imágenes estén cargadas.
        
        Args:
            operacion (str): Tipo de operación ('suma', 'resta', 'multiplicacion').
            numero_imagen_1 (int): Identificador de la primera imagen.
            numero_imagen_2 (int): Identificador de la segunda imagen.
        """
        if not self.model.checar_existencia_imagen(numero_imagen_1) and not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada ninguna imagen, se requieren dos imágenes", "info")
            return
        
        if not self.model.checar_existencia_imagen(numero_imagen_1) or not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada una imagen, se requieren dos imágenes", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen_1) == 'componentes' or self.model.determinar_tipo_imagen(numero_imagen_2) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return
        
        imagen_operada = self.model.realizar_operacion_aritmetica_entre_imagenes(numero_imagen_1, numero_imagen_2, operacion)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen_1, imagen_operada[2])
    
    def operacion_logica_entre_imagenes(self, operacion, numero_imagen_1, numero_imagen_2):
        """
        Realiza operaciones lógicas (AND, OR, XOR) entre dos imágenes.
        Verifica que ambas imágenes estén cargadas.
        
        Args:
            operacion (str): Tipo de operación ('and', 'or', 'xor').
            numero_imagen_1 (int): Identificador de la primera imagen.
            numero_imagen_2 (int): Identificador de la segunda imagen.
        """
        if not self.model.checar_existencia_imagen(numero_imagen_1) and not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada ninguna imagen, se requieren dos imágenes", "info")
            return
        
        if not self.model.checar_existencia_imagen(numero_imagen_1) or not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada una imagen, se requieren dos imágenes", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen_1) == 'componentes' or self.model.determinar_tipo_imagen(numero_imagen_2) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return
        
        imagen_operada = self.model.realizar_operacion_logica_entre_imagenes(numero_imagen_1, numero_imagen_2, operacion)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen_1, imagen_operada[2])
    
    def operacion_not(self, numero_imagen):
        """
        Aplica la operación lógica NOT (inversión) a una imagen.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return

        imagen_operada = self.model.operacion_not(numero_imagen)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen, imagen_operada[2])

    def agregar_ruido(self, tipo_ruido, numero_imagen):
        """
        Agrega ruido a la imagen seleccionada.
        
        Args:
            tipo_ruido (str): Tipo de ruido ('sal y pimienta', 'gaussiano').
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return

        imagen_operada = self.model.agregar_ruido(tipo_ruido, numero_imagen)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen, imagen_operada[2])

    def aplicar_filtro(self, numero_imagen):
        """
        Aplica un filtro seleccionado a la imagen.
        Maneja validaciones específicas para ciertos filtros (tiempo de proceso, tipo de imagen, parámetros extra).
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        valor_umbral_minimo = None
        valor_umbral_maximo = None
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        filtro = None
        if numero_imagen == 1:
            filtro = self.tabulator_filters.lista_opciones_filtros_Img1.get()
        else:
            filtro = self.tabulator_filters.lista_opciones_filtros_Img2.get()

        if not filtro:
            self.view.mostrar_mensaje("No se selecciono un filtro", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return

        # Advertencia para filtros lentos
        if filtro in ["Filtro Bilateral", "Filtro de Mediana Adaptativa", "Filtro de Media Contraharmonica", "Filtro de Mediana Ponderada"]:
            self.view.mostrar_mensaje("Aviso: El filtro seleccionado requiere de una mayor cantidad de tiempo de procesado, por tanto se recomienda que si el programa deje de responder, espere hasta que el filtro termine de procesar la imagen", "info")            
        
        # Validación para filtros que requieren escala de grises
        if filtro in ["Filtro de Sobel", "Filtro de Prewitt", "Filtro de Roberts", "Filtro de Canny", "Filtro Kirsch", "Filtro Laplaciano", "Filtro Ideal Pasa Bajo", "Filtro Ideal Pasa Alto"]:
            if self.model.determinar_tipo_imagen(numero_imagen) != 'gris':
                self.view.mostrar_mensaje("El filtro seleccionado requiere que la imagen sea en escala de grises", "info")
                return
        
        # Parámetros extra para Canny
        if filtro == "Filtro de Canny":
            valor_umbral_minimo, valor_umbral_maximo = self.view.tabulator_filters.pedir_valor_canny()
            if not valor_umbral_minimo or not valor_umbral_maximo:
                self.view.mostrar_mensaje("No se ingresaron valores validos", "info")
                return

        imagen_operada = self.model.aplicar_filtro(filtro, numero_imagen, valor_umbral_minimo, valor_umbral_maximo)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen, imagen_operada[2])

    def aplicar_segmentacion(self, tipo_segmentacion, numero_imagen):
        """
        Aplica un método de segmentación a la imagen.
        Solicita umbrales si el método lo requiere.
        
        Args:
            tipo_segmentacion (str): Nombre del método de segmentación.
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        valor_umbral_1 = None
        valor_umbral_2 = None

        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) != 'gris' and tipo_segmentacion != "Método de segmentación por resta canales":
            self.view.mostrar_mensaje("El segmento seleccionado requiere que la imagen sea en escala de grises", "info")
            return

        if tipo_segmentacion == "Método de umbral de banda" or tipo_segmentacion == "Método de dos umbrales":
            if tipo_segmentacion == "Método de umbral de banda":
                valor_umbral_1, valor_umbral_2 = self.view.tabulator_segmentation.pedir_valor_umbrales("umbral de banda")
            else:
                valor_umbral_1, valor_umbral_2 = self.view.tabulator_segmentation.pedir_valor_umbrales("dos umbrales")
            
            if valor_umbral_1==None or valor_umbral_2==None:
                self.view.mostrar_mensaje("No se ingresaron valores validos", "info")
                return

        imagen_segmentada = self.model.aplicar_segmentacion(tipo_segmentacion, numero_imagen, valor_umbral_1, valor_umbral_2)
        self.view.actualizar_imagen(imagen_segmentada[0], imagen_segmentada[1], numero_imagen, imagen_segmentada[2])

    def aplicar_ajuste_brillo(self, tipo_ajuste,numero_imagen):
        """
        Aplica ajuste de brillo o ecualización a la imagen.
        
        Args:
            tipo_ajuste (str): Tipo de ajuste de brillo.
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) != 'gris':
            self.view.mostrar_mensaje("El ajuste de brillo requiere que la imagen sea en escala de grises", "info")
            return

        valor_operacion = None
        if tipo_ajuste in ["Ecualización hipercúbica", "Función exponencial", "Corrección gamma"]:
            valor_operacion = self.view.tabulator_brightness.pedir_valor_operacion(tipo_ajuste)
            if not valor_operacion:
                self.view.mostrar_mensaje("No se ingresaron valores validos", "info")
                return

        imagen_ajustada = self.model.aplicar_ajuste_brillo(tipo_ajuste, numero_imagen, valor_operacion)
        self.view.actualizar_imagen(imagen_ajustada[0], imagen_ajustada[1], numero_imagen, imagen_ajustada[2])

    def aplicar_etiquetado_y_contornos(self, numero_imagen):
        """
        Aplica etiquetado de componentes conexos y detección de contornos.
        Requiere que la imagen sea binaria.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return


        if self.model.determinar_tipo_imagen(numero_imagen) != 'binaria':
            self.view.mostrar_mensaje("El etiquetado y contornos requiere que la imagen sea binaria", "info")
            return

        imagen_etiquetada = self.model.aplicar_etiquetado_y_contornos(numero_imagen)
        self.view.actualizar_imagen(imagen_etiquetada[0], imagen_etiquetada[1], numero_imagen, imagen_etiquetada[2])
        self.view.tabulator_operations.mostrar_datos_objetos(imagen_etiquetada[3])

    def aplicar_morfologia(self, tipo_morfologia, numero_imagen):
        """
        Aplica operaciones morfológicas (erosión, dilatación, apertura, cierre).
        Requiere que la imagen sea binaria.
        
        Args:
            numero_imagen (int): Identificador de la imagen (1 o 2).
            tipo_morfologia (str): Tipo de morfología ('erosionar', 'dilatar', 'apertura', 'cierre').
        """
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) == 'componentes':
            self.view.mostrar_mensaje("La imagen se encuentra etiqueta por tanto no es posible realizar ninguna operacion, reinicie la imagen para continuar", "info")
            return

        if self.model.determinar_tipo_imagen(numero_imagen) not in ['binaria', 'gris']:
            self.view.mostrar_mensaje("La morfologia requiere que la imagen sea binaria o en escala de grises", "info")
            return

        if tipo_morfologia in ['Adelgazamiento', 'Hit or miss', 'Frontera'] and self.model.determinar_tipo_imagen(numero_imagen) != 'binaria':
            self.view.mostrar_mensaje("La morfologia requiere que la imagen sea binaria", "info")
            return

        imagen_morfologica = self.model.aplicar_morfologia(tipo_morfologia, numero_imagen)
        self.view.actualizar_imagen(imagen_morfologica[0], imagen_morfologica[1], numero_imagen, imagen_morfologica[2])
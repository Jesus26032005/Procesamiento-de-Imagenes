from Modelos.ImagenModel import ImageModel
from Vistas.mainWindow import MainWindow 

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.conectar_eventos_basicos()
        self.conectar_eventos_operaciones()
        self.conectar_eventos_filtros()

    def conectar_eventos_basicos(self):
        self.tabulador_main = self.view.tabulator_main
        self.tabulador_main.button_cargar_img1.config(command= lambda: self.cargar_imagen(1))
        self.tabulador_main.button_cargar_img2.config(command= lambda: self.cargar_imagen(2))
        self.tabulador_main.button_reiniciar_img1.config(command= lambda: self.reiniciar_imagen(1))
        self.tabulador_main.button_reiniciar_img2.config(command= lambda: self.reiniciar_imagen(2))
        self.tabulador_main.button_convertir_grises_img1.config(command= lambda: self.convertir_grises(1))
        self.tabulador_main.button_convertir_grises_img2.config(command= lambda: self.convertir_grises(2))
        self.tabulador_main.button_binarizar_fijo_img1.config(command= lambda: self.binarizar_fijo(1))
        self.tabulador_main.button_binarizar_fijo_img2.config(command= lambda: self.binarizar_fijo(2))
        self.tabulador_main.button_binarizar_otsu_img1.config(command= lambda: self.binarizar_otsu(1))
        self.tabulador_main.button_binarizar_otsu_img2.config(command= lambda: self.binarizar_otsu(2))
        self.tabulador_main.button_guardar_img1.config(command= lambda: self.guardar_imagen(1))
        self.tabulador_main.button_guardar_img2.config(command= lambda: self.guardar_imagen(2))

    def conectar_eventos_operaciones(self):
        self.tabulator_operations = self.view.tabulator_operations
        self.tabulator_operations.boton_sumar_escalar_img1.config(command= lambda: self.operacion_aritmetica_escalar("suma", 1))
        self.tabulator_operations.boton_restar_escalar_img1.config(command= lambda: self.operacion_aritmetica_escalar("resta", 1))
        self.tabulator_operations.boton_multiplicar_escalar_img1.config(command= lambda: self.operacion_aritmetica_escalar("multiplicacion", 1))

        self.tabulator_operations.boton_sumar_entre_img1.config(command= lambda: self.operacion_aritmetica_entre_imagenes("suma", 1, 2))
        self.tabulator_operations.boton_restar_entre_img1.config(command= lambda: self.operacion_aritmetica_entre_imagenes("resta", 1, 2))
        self.tabulator_operations.boton_multiplicar_entre_img1.config(command= lambda: self.operacion_aritmetica_entre_imagenes("multiplicacion", 1, 2))

        self.tabulator_operations.boton_or_logico_img1.config(command= lambda: self.operacion_logica_entre_imagenes("or", 1, 2))
        self.tabulator_operations.boton_and_logico_img1.config(command= lambda: self.operacion_logica_entre_imagenes("and", 1, 2))
        self.tabulator_operations.boton_not_logico_img1.config(command= lambda: self.operacion_not(1))
        self.tabulator_operations.boton_xor_logico_img1.config(command= lambda: self.operacion_logica_entre_imagenes("xor", 1, 2))

        self.tabulator_operations.boton_sumar_escalar_img2.config(command= lambda: self.operacion_aritmetica_escalar("suma", 2))
        self.tabulator_operations.boton_restar_escalar_img2.config(command= lambda: self.operacion_aritmetica_escalar("resta", 2))
        self.tabulator_operations.boton_multiplicar_escalar_img2.config(command= lambda: self.operacion_aritmetica_escalar("multiplicacion", 2))

        self.tabulator_operations.boton_sumar_entre_img2.config(command= lambda: self.operacion_aritmetica_entre_imagenes("suma", 2, 1))
        self.tabulator_operations.boton_restar_entre_img2.config(command= lambda: self.operacion_aritmetica_entre_imagenes("resta", 2, 1))
        self.tabulator_operations.boton_multiplicar_entre_img2.config(command= lambda: self.operacion_aritmetica_entre_imagenes("multiplicacion", 2, 1))

        self.tabulator_operations.boton_or_logico_img2.config(command= lambda: self.operacion_logica_entre_imagenes("or", 2, 1))
        self.tabulator_operations.boton_and_logico_img2.config(command= lambda: self.operacion_logica_entre_imagenes("and", 2, 1))
        self.tabulator_operations.boton_not_logico_img2.config(command= lambda: self.operacion_not(2))
        self.tabulator_operations.boton_xor_logico_img2.config(command= lambda: self.operacion_logica_entre_imagenes("xor", 2, 1))

    def conectar_eventos_filtros(self):
        self.tabulator_filters= self.view.tabulator_filters
        self.tabulator_filters.boton_agregar_ruido_sal_y_pimienta_Img1.config(command= lambda: self.agregar_ruido("sal y pimienta",1))
        self.tabulator_filters.boton_agregar_ruido_sal_y_pimienta_Img2.config(command= lambda: self.agregar_ruido("sal y pimienta",2))
        self.tabulator_filters.boton_agregar_ruido_gaussiano_Img1.config(command= lambda: self.agregar_ruido("gaussiano",1))
        self.tabulator_filters.boton_agregar_ruido_gaussiano_Img2.config(command= lambda: self.agregar_ruido("gaussiano",2))
        self.tabulator_filters.boton_aplicar_filtro_Img1.config(command= lambda: self.aplicar_filtro(1))
        self.tabulator_filters.boton_aplicar_filtro_Img2.config(command= lambda: self.aplicar_filtro(2))

    def cargar_imagen(self, numero_imagen):
        rutaArchivo = self.tabulador_main.pedir_ruta_archivo()
        if rutaArchivo:
            imagen_creada = self.model.crear_imagen(rutaArchivo, numero_imagen)
            if isinstance(imagen_creada, tuple):
                self.view.mostrar_imagen_cargada([imagen_creada[0], imagen_creada[0]], imagen_creada[1], numero_imagen)
            else:
                self.view.mostrar_mensaje(imagen_creada, "error")
        else:
            self.view.mostrar_mensaje("No se seleccionó ninguna imagen.", "info")

    def guardar_imagen(self, numero_imagen):
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        rutaArchivo = self.tabulador_main.pedir_ruta_archivo_guardar()
        if rutaArchivo:
            self.model.guardar_imagen(numero_imagen)
        else:
            self.view.mostrar_mensaje("No se seleccionó ninguna imagen.", "info")

    def reiniciar_imagen(self, numero_imagen):
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        imagen_reiniciada = self.model.reiniciar_imagen(numero_imagen)
        self.view.actualizar_imagen(imagen_reiniciada[0], imagen_reiniciada[1], numero_imagen, "rgb")
    
    def convertir_grises(self, numero_imagen):
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        imagen_convertida = self.model.convertir_escala_grises(numero_imagen)
        self.view.actualizar_imagen(imagen_convertida[0], imagen_convertida[1], numero_imagen, "gris")
    
    def binarizar_fijo(self, numero_imagen):
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
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
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        imagen = self.model._determinarImagen(numero_imagen)
        if imagen.tipo != 'gris':
            self.view.mostrar_mensaje("La imagen debe estar en escala de grises.", "error")
            return
        imagen_binarizada = self.model.binarizar_imagen(numero_imagen, "otsu")
        self.view.actualizar_imagen(imagen_binarizada[0], imagen_binarizada[1], numero_imagen, "binaria")

    def operacion_aritmetica_escalar(self, operacion, numero_imagen):
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
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
        if not self.model.checar_existencia_imagen(numero_imagen_1) and not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada ninguna imagen, se requieren dos imágenes", "info")
            return
        
        if not self.model.checar_existencia_imagen(numero_imagen_1) or not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada una imagen, se requieren dos imágenes", "info")
            return
        
        imagen_operada = self.model.realizar_operacion_aritmetica_entre_imagenes(numero_imagen_1, numero_imagen_2, operacion)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen_1, imagen_operada[2])
    
    def operacion_logica_entre_imagenes(self, operacion, numero_imagen_1, numero_imagen_2):
        if not self.model.checar_existencia_imagen(numero_imagen_1) and not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada ninguna imagen, se requieren dos imágenes", "info")
            return
        
        if not self.model.checar_existencia_imagen(numero_imagen_1) or not self.model.checar_existencia_imagen(numero_imagen_2):
            self.view.mostrar_mensaje("No se tiene cargada una imagen, se requieren dos imágenes", "info")
            return
        
        imagen_operada = self.model.realizar_operacion_logica_entre_imagenes(numero_imagen_1, numero_imagen_2, operacion)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen_1, imagen_operada[2])
    
    def operacion_not(self, numero_imagen):
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return
        
        imagen_operada = self.model.operacion_not(numero_imagen)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen, imagen_operada[2])

    def agregar_ruido(self, tipo_ruido, numero_imagen):
        if not self.model.checar_existencia_imagen(numero_imagen):
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        imagen_operada = self.model.agregar_ruido(tipo_ruido, numero_imagen)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen, imagen_operada[2])

    def aplicar_filtro(self, numero_imagen):
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

        if filtro in ["Filtro Bilateral", "Filtro de Mediana Adaptativa", "Filtro de Media Contraharmonica", "Filtro de Mediana Ponderada"]:
            self.view.mostrar_mensaje("Aviso: El filtro seleccionado requiere de una mayor cantidad de tiempo de procesado, por tanto se recomienda que si el programa deje de responder, espere hasta que el filtro termine de procesar la imagen", "info")            
        
        if filtro in ["Filtro de Sobel", "Filtro de Prewitt", "Filtro de Roberts", "Filtro de Canny", "Filtro Kirsch", "Filtro Laplaciano"]:
            if self.model.determinar_tipo_imagen(numero_imagen) != 'gris':
                self.view.mostrar_mensaje("El filtro seleccionado requiere que la imagen sea en escala de grises", "info")
                return
        
        if filtro == "Filtro de Canny":
            valor_umbral_minimo, valor_umbral_maximo = self.view.tabulator_filters.pedir_valor_canny()
            if not valor_umbral_minimo or not valor_umbral_maximo:
                self.view.mostrar_mensaje("No se ingresaron valores validos", "info")
                return

        imagen_operada = self.model.aplicar_filtro(filtro, numero_imagen, valor_umbral_minimo, valor_umbral_maximo)
        self.view.actualizar_imagen(imagen_operada[0], imagen_operada[1], numero_imagen, imagen_operada[2])
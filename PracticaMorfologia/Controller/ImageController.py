from Model.ImagenModel import ImageModel
from View.mainWindow import MainWindow 

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.conectar_eventos()

    def conectar_eventos(self):
        self.view.boton_cargar_imagen.config(command= self.cargar_imagen)
        self.view.boton_reiniciar_imagen.config(command= self.reiniciar_imagen)
        self.view.boton_guardar_imagen.config(command= self.guardar_imagen)

        self.view.boton_convertir_grises.config(command= self.convertir_grises)
        self.view.boton_morfologia_cierre.config(command= lambda: self.aplicar_morfologia("Cierre"))
        self.view.boton_morfologia_dilatacion.config(command= lambda: self.aplicar_morfologia("Dilatacion"))
        self.view.boton_operacion_not.config(command = self.operacion_not)
        self.view.boton_binarizacion_fija.config(command = self.binarizar_fijo)
        self.view.boton_sumar_con_imagen_original.config(command = self.sumar_con_imagen_original)

    def cargar_imagen(self):
        rutaArchivo = self.view.pedir_ruta_archivo()
        if rutaArchivo:
            imagen_creada = self.model.crear_imagen(rutaArchivo)
            if isinstance(imagen_creada, tuple):
                self.view.mostrar_imagen_cargada([imagen_creada[0], imagen_creada[0]], imagen_creada[1],)
            else:
                self.view.mostrar_mensaje(imagen_creada, "error")
        else:
            self.view.mostrar_mensaje("No se seleccionó ninguna imagen.", "info")

    def reiniciar_imagen(self):
        if not self.model.checar_existencia_imagen():
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        imagen_reiniciada = self.model.reiniciar_imagen()
        self.view.actualizar_imagen(imagen_reiniciada[0], imagen_reiniciada[1], "rgb")
    
    def guardar_imagen(self):
        if not self.model.checar_existencia_imagen():
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        rutaArchivo = self.view.pedir_ruta_archivo_guardar()
        if rutaArchivo:
            self.model.guardar_imagen(rutaArchivo)
        else:
            self.view.mostrar_mensaje("No se seleccionó ninguna imagen.", "info")

    def convertir_grises(self):
        if not self.model.checar_existencia_imagen():
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
            
        imagen_convertida = self.model.convertir_escala_grises()
        self.view.actualizar_imagen(imagen_convertida[0], imagen_convertida[1], imagen_convertida[2])

    def aplicar_morfologia(self, tipo_morfologia):
        if not self.model.checar_existencia_imagen():
            self.view.mostrar_mensaje("No se tiene cargada la imagen", "info")
            return

        if self.model.determinar_tipo_imagen() not in ['gris','binaria']:
            self.view.mostrar_mensaje("La operación requiere que la imagen sea gris o binaria", "info")
            return

        imagen_morfologica = self.model.aplicar_morfologia(tipo_morfologia)
        self.view.actualizar_imagen(imagen_morfologica[0], imagen_morfologica[1], imagen_morfologica[2])

    def operacion_not(self):
        if not self.model.checar_existencia_imagen():
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return

        if self.model.determinar_tipo_imagen() not in ['gris']:
            self.view.mostrar_mensaje("La operación requiere que la imagen sea binaria", "info")
            return

        histograma = None
        imagen_not = self.model.operacion_not()
        self.view.actualizar_imagen(imagen_not[0], imagen_not[1], imagen_not[2])

    def binarizar_fijo(self):
        if not self.model.checar_existencia_imagen():
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        
        valorUmbral = None
        if self.model.determinar_tipo_imagen() != 'gris':
            self.view.mostrar_mensaje("La imagen debe estar en escala de grises.", "error")
            return

        valorUmbral = self.view.aviso_binarizar_fijo()
        if valorUmbral:
            imagen_binarizada = self.model.binarizar_imagen(valorUmbral)
            self.view.actualizar_imagen(imagen_binarizada[0], imagen_binarizada[1], imagen_binarizada[2])

    def sumar_con_imagen_original(self):
        if not self.model.checar_existencia_imagen():
            self.view.mostrar_mensaje("No se tiene cargada una imagen.", "info")
            return
        
        if self.model.determinar_tipo_imagen() not in ['binaria']:
            self.view.mostrar_mensaje("La operación requiere que la imagen sea binaria", "info")
            return
        
        imagen_sumada = self.model.sumar_con_imagen_original()
        self.view.actualizar_imagen(imagen_sumada[0], imagen_sumada[1], imagen_sumada[2])
        

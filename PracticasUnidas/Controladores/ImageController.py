from Modelos.ImagenModel import ImageModel
from Vistas.mainWindow import MainWindow 

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.conectar_eventos_main()

    def conectar_eventos_main(self):
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

    def cargar_imagen(self, numero_imagen):
        rutaArchivo = self.tabulador_main.pedir_ruta_archivo()
        if rutaArchivo:
            imagen_creada = self.model.crear_imagen(rutaArchivo, numero_imagen)
            if isinstance(imagen_creada, tuple):
                self.tabulador_main.mostrar_imagen_cargada([imagen_creada[0], imagen_creada[0]], imagen_creada[1], numero_imagen)
                self.tabulador_main.activar_botones_frame_img(numero_imagen)
            else:
                self.tabulador_main.mostrar_mensaje(imagen_creada, "error")
        else:
            self.tabulador_main.mostrar_mensaje("No se seleccionó ninguna imagen.", "info")

    def reiniciar_imagen(self, numero_imagen):
        imagen_reiniciada = self.model.reiniciar_imagen(numero_imagen)
        self.tabulador_main.actualizar_imagen(imagen_reiniciada[0], imagen_reiniciada[1], numero_imagen, "rgb")
    
    def convertir_grises(self, numero_imagen):
        imagen_convertida = self.model.convertir_escala_grises(numero_imagen)
        self.tabulador_main.actualizar_imagen(imagen_convertida[0], imagen_convertida[1], numero_imagen, "gris")
    
    def binarizar_fijo(self, numero_imagen):
        valorUmbral = None
        imagen = self.model._determinarImagen(numero_imagen)
        if imagen.tipo != 'gris':
            self.tabulador_main.mostrar_mensaje("La imagen debe estar en escala de grises.", "error")
            return

        valorUmbral = self.tabulador_main.aviso_binarizar_fijo()
        if valorUmbral:
            imagen_binarizada = self.model.binarizar_imagen(numero_imagen, "fijo", valorUmbral)
            self.tabulador_main.actualizar_imagen(imagen_binarizada[0], imagen_binarizada[1], numero_imagen, "binaria")

    def binarizar_otsu(self, numero_imagen):
        imagen = self.model._determinarImagen(numero_imagen)
        if imagen.tipo != 'gris':
            self.tabulador_main.mostrar_mensaje("La imagen debe estar en escala de grises.", "error")
            return
        imagen_binarizada = self.model.binarizar_imagen(numero_imagen, "otsu")
        self.tabulador_main.actualizar_imagen(imagen_binarizada[0], imagen_binarizada[1], numero_imagen, "binaria")
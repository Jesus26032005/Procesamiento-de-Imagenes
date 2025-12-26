from Utilities.ProcesadorImagen import ProcesadorImagen

class ImageModel:
    def __init__(self):
        self.imagen = None

    def checar_existencia_imagen(self):
        if self.imagen is None:
            return False 
        return True
    
    def crear_imagen(self, ruta):
        resultadoCreacion = ProcesadorImagen.cargar_imagen(ruta)
        
        if isinstance(resultadoCreacion, str):
            return resultadoCreacion
            
        self.imagen = resultadoCreacion
            
        return (ProcesadorImagen.convertir_imagen_tk(self.imagen.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(self.imagen.imagen_modified))

    def reiniciar_imagen(self):
        return ProcesadorImagen.reiniciar_imagen(self.imagen)

    def guardar_imagen(self, ruta_archivo):
        ProcesadorImagen.guardar_imagen(self.imagen.imagen_modified, ruta_archivo)

    def determinar_tipo_imagen(self):
        return self.imagen.tipo

    def convertir_escala_grises(self):
        histograma = None
        imagen = self.imagen      
        imagen_tk = ProcesadorImagen.convertir_escala_grises(imagen)
        histograma = ProcesadorImagen.calcular_histograma_gris(imagen.imagen_modified)
        return (imagen_tk, histograma, self.imagen.tipo)

    def aplicar_morfologia(self, tipo_morfologia):
        imagen_modificada = ProcesadorImagen.aplicar_morfologia(tipo_morfologia, self.imagen)    
        histograma = ProcesadorImagen.calcular_histograma_gris(self.imagen.imagen_modified)
        return (imagen_modificada, histograma, self.imagen.tipo)

    def operacion_not(self):
        histograma = None
        resultado_operacion =  ProcesadorImagen.not_logico(self.imagen)
        histograma = ProcesadorImagen.calcular_histograma_gris(self.imagen.imagen_modified)
        return (resultado_operacion, histograma, self.imagen.tipo)

    def binarizar_inversa_fijo(self, umbral: int = None):
        histograma = None
        return (ProcesadorImagen.binarizar_inversa_fijo(self.imagen, umbral), histograma, self.imagen.tipo)

    def sumar_con_imagen_original(self):
        histograma = None
        imagen_sumada = ProcesadorImagen.sumar_imagenes(self.imagen)
        return (imagen_sumada, histograma, self.imagen.tipo)

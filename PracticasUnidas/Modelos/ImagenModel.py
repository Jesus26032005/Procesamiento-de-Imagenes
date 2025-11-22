from Utilidades.ProcesadorImagen import ProcesadorImagen

class ImageModel:
    def __init__(self):
        self.imagen1 = None
        self.imagen2 = None
    
    def crear_imagen(self, ruta, numero_imagen):
        if numero_imagen == 2 and self.imagen1 is None:
            return "La imagen 1 no está cargada."
        resultadoCreacion = ProcesadorImagen.cargar_imagen(ruta)
        if isinstance(resultadoCreacion, str):
            return resultadoCreacion
        if numero_imagen == 1:
            self.imagen1 = resultadoCreacion
        elif numero_imagen == 2:
            self.imagen2 = resultadoCreacion
        return (ProcesadorImagen.convertir_imagen_tk(resultadoCreacion.imagen_modified), 
        ProcesadorImagen.calcular_histograma_color(resultadoCreacion.imagen_modified))

    def _determinarImagen(self, numero_imagen):
        if numero_imagen == 1:
            return self.imagen1
        elif numero_imagen == 2:
            return self.imagen2

    def reiniciar_imagen(self, numero_imagen):
        return ProcesadorImagen.reiniciar_imagen(self._determinarImagen(numero_imagen))

    def convertir_escala_grises(self, numero_imagen):
        imagen = self._determinarImagen(numero_imagen)
        return ProcesadorImagen.convertir_escala_grises(imagen)

    def binarizar_imagen(self, numero_imagen, metodo: str, umbral: int = None):
        imagen = self._determinarImagen(numero_imagen)
        if metodo == 'fijo':
            return [ProcesadorImagen.binarizar_metodo_fijo(imagen, umbral), None]
        if metodo == 'otsu':
            return [ProcesadorImagen.binarizar_metodo_otsu(imagen), None]
        
    def realizar_operacion_aritmetica_escalar(self, numero_imagen, operacion: str, valor: int):
        imagen = self._determinarImagen(numero_imagen)
        if operacion == 'suma':
            resultado_operacion = ProcesadorImagen.sumar_escalar(imagen, valor)
        if operacion == 'resta':
            resultado_operacion = ProcesadorImagen.restar_escalar(imagen, valor)
        if operacion == 'multiplicacion':
            resultado_operacion = ProcesadorImagen.multiplicar_escalar(imagen, valor)
        return resultado_operacion
    
    def realizar_operacion_aritmetica_entre_imagenes(self, numero_imagen_1, numero_imagen_2, operacion: str):
        imagen_1 = self._determinarImagen(numero_imagen_1)
        imagen_2 = self._determinarImagen(numero_imagen_2)
        return ProcesadorImagen.operaciones_aritmeticas_entre_imagenes(imagen_1, imagen_2, operacion)
    
    def realizar_operacion_logica_entre_imagenes(self, numero_imagen_1, numero_imagen_2, operacion: str):
        imagen_1 = self._determinarImagen(numero_imagen_1)
        imagen_2 = self._determinarImagen(numero_imagen_2)
        return ProcesadorImagen.operaciones_logicas_entre_imagenes(imagen_1, imagen_2, operacion)
    
    def operacion_not(self, numero_imagen):
        imagen = self._determinarImagen(numero_imagen)
        return ProcesadorImagen.operacion_not(imagen)

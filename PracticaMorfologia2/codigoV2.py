import cv2
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox

class DetectorFlechaFiltros(ttk.Window):
    def __init__(self):
        # Inicializamos la ventana con un tema oscuro moderno
        super().__init__(themename="cyborg")
        self.title("Detector de señales de tránsito")
        # Colocamos un tamaño para la ventana
        self.geometry("1000x850")
        # Colocamos un zoom para la ventana asi aparece en pantalla completa
        self.state("zoomed")
        
        self.pasos = {} #Almacena las visualizaciones de cada uno de los pasos
        self.imagen_actual_ruta = None #Almacena la ruta de la imagen actual

        # --- Interfaz Principal ---
        # Contenedor principal
        self.frame_principal = ttk.Frame(self, padding=20)
        self.frame_principal.pack(fill=BOTH, expand=YES)

        # Título
        self.label_titulo = ttk.Label( self.frame_principal,  text="DETECTOR DE SEÑALES DE TRÁNSITO", font=("Arial", 40, "bold"), bootstyle="light")
        self.label_titulo.pack(pady=(0, 20))

        # Seccion de botones
        self.frame_botones = ttk.Frame(self.frame_principal)
        self.frame_botones.pack(fill=X, pady=10)
        self.frame_botones.grid_columnconfigure(0, weight=1)
        self.frame_botones.grid_columnconfigure(1, weight=1)

        self.boton_cargar = ttk.Button( self.frame_botones, text="Cargar Imagen y Procesar", command=self._procesar, bootstyle="primary")
        self.boton_cargar.grid(row=0, column=0, padx=5, sticky="nsew")

        self.boton_detalles = ttk.Button( self.frame_botones, text="Ver Desglose de Pasos", command=self._abrir_detalles, bootstyle="success")
        self.boton_detalles.grid(row=0, column=1, padx=5, sticky="nsew")

        # Área de imagen principal
        self.frame_img = ttk.Labelframe(self.frame_principal, text="Resultado Final", padding=10, bootstyle="info")
        self.frame_img.pack(fill=BOTH, expand=YES, pady=10)

        self.label_preview_img = ttk.Label(self.frame_img, text="Esperando imagen...", anchor="center")
        self.label_preview_img.pack(fill=BOTH, expand=YES)

    def _redimensionar_imagen(self, img, ancho_maximo, alto_maximo):
        # Obtenemos el ancho y alto de la imagen originales
        alto_original, ancho_original = img.shape[:2]

        # Calculamos el factor de escala para mantener la proporción original
        ratio = min(ancho_maximo / ancho_original, alto_maximo / alto_original)

        # Calculamos el nuevo ancho y alto
        nuevo_ancho = int(ancho_original * ratio)
        nuevo_alto = int(alto_original * ratio)

        # Redimensionamos la imagen y retornamos
        return cv2.resize(img, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)

    def _procesar(self):
        # Abrimos el explorador de archivos para seleccionar la imagen
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")])
        if not ruta: 
            Messagebox.show_error("No se seleccionó ninguna imagen.", "Error")
            return

        try:
            img = cv2.imread(ruta)
            if img is None: 
                Messagebox.show_error("No se pudo leer la imagen.", "Error")
                return

            # --- 1. PROCESAMIENTO FRECUENCIAL (TF) ---
            # Convertimos la imagen a escala de grises
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Calculamos la Transformada de Fourier
            f = np.fft.fft2(gray)
            fshift = np.fft.fftshift(f) # Trasladamos la componente de frecuencia cero al centro de la imagen
            espectro = 20 * np.log(np.abs(fshift) + 1) # Calculamos el espectro de frecuencia en escala logarítmica
            espectro_vis = cv2.normalize(espectro, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

            # 2. PROCESAMIENTO ESPACIAL Y MORFOLÓGICO
            # Aplicamos un filtro Gaussiano
            blur = cv2.GaussianBlur(img, (7, 7), 0)

            # Aplicamos segmentación por modelo de color HSV (Amarillo)
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            mascara_amarillo = cv2.inRange(hsv, np.array([15, 100, 100]), np.array([35, 255, 255]))

            # Aplicamos morfología: Cierre (Rellenar huecos en el rombo)
            kernel_cierre = np.ones((15, 15), np.uint8)
            rombo_solido = cv2.morphologyEx(mascara_amarillo, cv2.MORPH_CLOSE, kernel_cierre)

            # Aplicamos umbralización Inversa (Detectar símbolos negros)
            _, mascara_inversa = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

            # Aplicamos lógica AND: Lo que es negro Y está dentro del rombo amarillo, quedandonos con la flecha y poco ruido
            flecha_aislada = cv2.bitwise_and(mascara_inversa, mascara_inversa, mask=rombo_solido)

            # Aplicamos morfología: Apertura (Limpiamos ruido pequeño)
            kernel_limpia = np.ones((3, 3), np.uint8)
            flecha_final = cv2.morphologyEx(flecha_aislada, cv2.MORPH_OPEN, kernel_limpia)

            # 3. DETECCION Y DIBUJO
            res_img = img.copy()
            contornos, _ = cv2.findContours(flecha_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Detectamos la flecha y aseguramos si es que se detectó 
            detectado = False
            if contornos:
                c_principal = max(contornos, key=cv2.contourArea)
                if cv2.contourArea(c_principal) > 300:
                    x, y, w, h = cv2.boundingRect(c_principal)
                    # Dibujar rectángulo verde neón
                    cv2.rectangle(res_img, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    # Texto indicativo
                    cv2.putText(res_img, "Flecha", (x, y - 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    detectado = True

            # Guardamos los pasos para la ventana de detalles
            self.pasos = {
                "Original": img,
                "FFT (Espectro)": espectro_vis,
                "Filtro Gaussiano": blur,
                "Mascara amarilla": mascara_amarillo,
                "Morf: Cierre (Máscara)": rombo_solido,
                "Umbral Inverso (Negros)": mascara_inversa,
                "Lógica AND (Intersección)": flecha_aislada,
                "Morf: Apertura (Final)": flecha_final,
                "Detección Final": res_img
            }

            self.mostrar_img(res_img, self.label_preview_img, (1250, 800))
            
            mensaje = "Procesamiento completado con éxito." if detectado else "Procesado, pero no se detectó el objeto."
            if detectado:
                Messagebox.show_info(mensaje, "Exito")
            else:
                Messagebox.show_info(mensaje, "Advertencia")

        except Exception as e:
            Messagebox.show_error(str(e), "Error")

    def _abrir_detalles(self):
        if not self.pasos: 
            Messagebox.show_error("No hay pasos para mostrar ingrese una imagen .", "Error")
            return

        if hasattr(self, 'ventana_detalles') and self.ventana_detalles:
            self.ventana_detalles.destroy()

        # Crear la ventana de detalles
        self.ventana_detalles = ttk.Toplevel(self)
        self.ventana_detalles.title("Pipeline de Procesamiento Digital de Imágenes")
        self.ventana_detalles.geometry("1300x900")
        self.ventana_detalles.state("zoomed")

        # pero para 8 pasos un grid limpio basta.
        frame_principal_detalles = ttk.Frame(self.ventana_detalles, padding=15)
        frame_principal_detalles.pack(fill=BOTH, expand=YES)

        for i in range(3):
            frame_principal_detalles.columnconfigure(i, weight=1)
            frame_principal_detalles.rowconfigure(i, weight=1)

        columnas = 3
        # Iteramos sobre cada paso
        for i, (titulo, img) in enumerate(self.pasos.items()):
            # Frame para cada paso (estilo tarjeta)
            tarjeta_detalle = ttk.Labelframe(frame_principal_detalles, text=titulo, bootstyle="warning", padding=5)
            
            # Calculamos fila y columna de posicionamiento
            fila = i // columnas
            columna = i % columnas
            
            tarjeta_detalle.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")
            
            label_detalle = ttk.Label(tarjeta_detalle)
            label_detalle.pack(fill=BOTH, anchor="center")
            
            # Mostramos imagen un poco más pequeña para que quepan todas
            self.mostrar_img(img, label_detalle, (600, 300))

    def mostrar_img(self, cv_img, label, tamaño):
        # 1. Redimensionar preservando aspecto
        img_resultado = self._redimensionar_imagen(cv_img, tamaño[0], tamaño[1])
        
        # 2. Conversión de Color correcta
        if len(img_resultado.shape) == 3:
            img_resultado = cv2.cvtColor(img_resultado, cv2.COLOR_BGR2RGB)
        else:
            # Si es escala de grises, convertir a RGB para que PIL no falle
            img_resultado = cv2.cvtColor(img_resultado, cv2.COLOR_GRAY2RGB)

        # 3. Pasar a PIL y luego a Tkinter
        img_pillow = Image.fromarray(img_resultado)
        img_tkinter = ImageTk.PhotoImage(img_pillow)
        
        label.configure(image=img_tkinter)
        label.image = img_tkinter

if __name__ == "__main__":
    app = DetectorFlechaFiltros()
    app.mainloop()
import ttkbootstrap as ttk
from tkinter import simpledialog

class TabulatorSegmentation(ttk.Frame):
    """
    Clase que representa la pestaña de segmentación en la interfaz gráfica.
    Permite al usuario aplicar diferentes tipos de segmentación a las imágenes cargadas.
    """
    def __init__(self, parent):
        super().__init__(parent)

        for i in range(1,3): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        self.label_titulo = ttk.Label(self, text="Operaciones de segmentación", font=("Arial", 18, "bold"))
        self.label_titulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self._crear_componentes_segmentacion_img1()
        self._crear_componentes_segmentacion_img2()

    def _crear_componentes_segmentacion_img1(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar segmentación
        a la imagen principal (Imagen 1).
        """
        estiloControlesSegmentacion = "info"
        self.marco_controles_segmentacion_img1 = ttk.Labelframe(self, text="Segmentación para imagen principal", padding=5, bootstyle=estiloControlesSegmentacion)
        self.marco_controles_segmentacion_img1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(5): self.marco_controles_segmentacion_img1.rowconfigure(i, weight=1)
        for i in range(2): self.marco_controles_segmentacion_img1.columnconfigure(i, weight=1)

        self.subtitutulo_controles_segmentacion_img1 = ttk.Label(self.marco_controles_segmentacion_img1, text="Métodos de segmentación para la imagen principal", font=("Arial", 16, "bold"), wraplength= 400)
        self.subtitutulo_controles_segmentacion_img1.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.boton_segmentacion_otsu_img1 = ttk.Button(self.marco_controles_segmentacion_img1, text="Método de Otsu", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_entropia_kapur_img1 = ttk.Button(self.marco_controles_segmentacion_img1, text="Método de entropía de Kapur", bootstyle= estiloControlesSegmentacion)
        self.boton_minimo_histograma_img1 = ttk.Button(self.marco_controles_segmentacion_img1, text="Método de mínimo de histograma", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_media_img1 = ttk.Button(self.marco_controles_segmentacion_img1, text="Método de la media", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_dos_umbrales_img1 = ttk.Button(self.marco_controles_segmentacion_img1, text="Método de dos umbrales", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_umbral_banda_img1 = ttk.Button(self.marco_controles_segmentacion_img1, text="Método de umbral de banda", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_moho_hsv_img1 = ttk.Button(self.marco_controles_segmentacion_img1, text="Método de segmentación de moho", bootstyle= estiloControlesSegmentacion)

    
        self.boton_segmentacion_otsu_img1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_entropia_kapur_img1.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_minimo_histograma_img1.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_media_img1.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_dos_umbrales_img1.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_umbral_banda_img1.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_moho_hsv_img1.grid(row=4, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)

    def _crear_componentes_segmentacion_img2(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar ruido y filtros
        a la imagen secundaria (Imagen 2).
        """
        estiloControlesSegmentacion = "primary"
        self.marco_controles_segmentacion_img2 = ttk.Labelframe(self, text="Segmentación para imagen secundaria", padding=5, bootstyle=estiloControlesSegmentacion)
        self.marco_controles_segmentacion_img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(5): self.marco_controles_segmentacion_img2.rowconfigure(i, weight=1)
        for i in range(2): self.marco_controles_segmentacion_img2.columnconfigure(i, weight=1)

        self.subtitutulo_controles_segmentacion_img2 = ttk.Label(self.marco_controles_segmentacion_img2, text="Métodos de segmentación para la imagen secundaria", font=("Arial", 16, "bold"), wraplength= 400)
        self.subtitutulo_controles_segmentacion_img2.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.boton_segmentacion_otsu_img2 = ttk.Button(self.marco_controles_segmentacion_img2, text="Método de Otsu", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_entropia_kapur_img2 = ttk.Button(self.marco_controles_segmentacion_img2, text="Método de entropía de Kapur", bootstyle= estiloControlesSegmentacion)
        self.boton_minimo_histograma_img2 = ttk.Button(self.marco_controles_segmentacion_img2, text="Método de mínimo de histograma", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_media_img2 = ttk.Button(self.marco_controles_segmentacion_img2, text="Método de la media", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_dos_umbrales_img2 = ttk.Button(self.marco_controles_segmentacion_img2, text="Método de dos umbrales", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_umbral_banda_img2 = ttk.Button(self.marco_controles_segmentacion_img2, text="Método de umbral de banda", bootstyle= estiloControlesSegmentacion)
        self.boton_segmentacion_moho_hsv_img2 = ttk.Button(self.marco_controles_segmentacion_img2, text="Método de segmentación de moho", bootstyle= estiloControlesSegmentacion)

        self.boton_segmentacion_otsu_img2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_entropia_kapur_img2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_minimo_histograma_img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_media_img2.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_dos_umbrales_img2.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_umbral_banda_img2.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_segmentacion_moho_hsv_img2.grid(row=4, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)

    def pedir_valor_umbrales(self, tipo_segmentacion):
        if tipo_segmentacion == "dos umbrales":
            texto = "Seleccione un valor entre 0 y 255 para el umbral 1:"
        else:
            texto = "Seleccione un valor entre 0 y 255 para el inicio de la banda:"

        valor_umbral_1 = simpledialog.askinteger("Valor del umbral", texto, 
        minvalue=0, maxvalue=255,
        parent=self)

        if valor_umbral_1 is None:
            return None, None

        if tipo_segmentacion == "dos umbrales":
            texto_2 = "Seleccione un valor entre " + str(valor_umbral_1) + " y 255 para el umbral 2:"
        else:
            texto_2 = "Seleccione un valor entre " + str(valor_umbral_1) + " y 255 para el fin de la banda:"

        valor_umbral_2 = simpledialog.askinteger("Valor de extremo de la banda", texto_2, 
        minvalue=valor_umbral_1, maxvalue=255,
        parent=self)


        if valor_umbral_2 is None:
            return None, None
        
        return valor_umbral_1, valor_umbral_2
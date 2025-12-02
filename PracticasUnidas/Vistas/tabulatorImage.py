import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import DISABLED, NORMAL
from tkinter import filedialog, messagebox, simpledialog, DISABLED

paddingBotones = {"padx": 10, "pady": 5, "ipady": 3}
paddingTitulos = {"padx": 5, "pady": 1}
paddingFrames = {"padx": 10, "pady": 10, "ipady": 5}

class TabulatorImage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure(0, weight=0)
        for i in range(1,9): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        self._configurarPanelControl()

    def _configurarPanelControl(self):
        # Configuracion de estilos
        estilosCargaReinicio = "primary"
        estilosControlesBasicos = "success"

        # Titulo del panel de control
        titulo = ttk.Label(self, text="Operaciones base", font=("Arial", 18, "bold"), anchor="center")
        titulo.grid(row=0, column=0, sticky="w", **paddingTitulos)

        # Generacion de frame completo para carga y reinicio de imagenes
        self.frame_carga_reinicio= ttk.Labelframe(self, text="Opciones de carga y reinicio de imagenes", bootstyle=estilosCargaReinicio)

        for i in [2,3,5,6]: self.frame_carga_reinicio.rowconfigure(i, weight=1)
        for i in [0,1,4,]: self.frame_carga_reinicio.rowconfigure(i, weight=0)
        for i in range(2): self.frame_carga_reinicio.columnconfigure(i, weight=1)
        self.frame_carga_reinicio.grid(row=1, column=0, sticky="nsew", **paddingFrames, rowspan=2)

        self.label_carga_reinicio_title = ttk.Label(self.frame_carga_reinicio, text="Carga y Reinicio de Imagenes", font=("Arial", 16, "bold"), anchor="center")
        self.label_carga_reinicio_title_img1 = ttk.Label(self.frame_carga_reinicio, text="Imagen 1", font=("Arial ", 15, "bold"), anchor="center")
        self.button_cargar_img1 = ttk.Button(self.frame_carga_reinicio, text="Cargar Imagen 1", bootstyle=estilosCargaReinicio)
        self.button_reiniciar_img1 = ttk.Button(self.frame_carga_reinicio, text="Reiniciar Imagen 1", bootstyle=estilosCargaReinicio)
        self.button_guardar_img1 = ttk.Button(self.frame_carga_reinicio, text="Guardar Imagen 1", bootstyle=estilosCargaReinicio)
        self.label_carga_reinicio_title_img2 = ttk.Label(self.frame_carga_reinicio, text="Imagen 2", font=("Arial", 15, "bold"), anchor="center")
        self.button_cargar_img2 = ttk.Button(self.frame_carga_reinicio, text="Cargar Imagen 2", bootstyle=estilosCargaReinicio)
        self.button_reiniciar_img2 = ttk.Button(self.frame_carga_reinicio, text="Reiniciar Imagen 2", bootstyle=estilosCargaReinicio)
        self.button_guardar_img2 = ttk.Button(self.frame_carga_reinicio, text="Guardar Imagen 2", bootstyle=estilosCargaReinicio)
        
        self.label_carga_reinicio_title.grid(row=0, column=0, columnspan=2, **paddingTitulos)
        self.label_carga_reinicio_title_img1.grid(row=1, column=0, sticky="nsew", **paddingBotones, columnspan=2)
        self.button_cargar_img1.grid(row=2, column=0, sticky="ew", **paddingBotones)
        self.button_reiniciar_img1.grid(row=2, column=1, sticky="ew", **paddingBotones)
        self.button_guardar_img1.grid(row=3, column=0, sticky="ew", **paddingBotones, columnspan=2)
        self.label_carga_reinicio_title_img2.grid(row=4, column=0, sticky="nsew", **paddingBotones, columnspan=2)
        self.button_cargar_img2.grid(row=5, column=0, sticky="ew", **paddingBotones)
        self.button_reiniciar_img2.grid(row=5, column=1, sticky="ew", **paddingBotones)
        self.button_guardar_img2.grid(row=6, column=0, sticky="ew", **paddingBotones, columnspan=2)
        
        # Generacion de frame completo para operaciones generales
        self.frame_operaciones_generales = ttk.Labelframe(self, text="Operaciones Basicas", bootstyle=estilosControlesBasicos)
        for i in [2,3,4,6,7,8]: self.frame_operaciones_generales.rowconfigure(i, weight=1)
        self.frame_operaciones_generales.columnconfigure(0, weight=1)
        self.frame_operaciones_generales.grid(row=3, column=0, sticky="nsew", **paddingFrames, rowspan=6)

        self.label_operaciones_generales_title = ttk.Label(self.frame_operaciones_generales, text="Operaciones Generales", font=("Arial", 16, "bold"), anchor="center")
        self.label_operaciones_generales_title_img1 = ttk.Label(self.frame_operaciones_generales, text="Imagen 1", font=("Arial", 15, "bold"), anchor="center")
        self.button_convertir_grises_img1 = ttk.Button(self.frame_operaciones_generales, text="Convertir a Escala de Grises", bootstyle=estilosControlesBasicos)
        self.button_binarizar_fijo_img1 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con umbral fijo", bootstyle=estilosControlesBasicos)
        self.button_binarizar_otsu_img1 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con Otsu", bootstyle=estilosControlesBasicos)
        self.label_operaciones_generales_title_img2 = ttk.Label(self.frame_operaciones_generales, text="Imagen 2", font=("Arial", 15, "bold"), anchor="center")
        self.button_convertir_grises_img2 = ttk.Button(self.frame_operaciones_generales, text="Convertir a Escala de Grises", bootstyle=estilosControlesBasicos)
        self.button_binarizar_fijo_img2 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con umbral fijo", bootstyle=estilosControlesBasicos)
        self.button_binarizar_otsu_img2 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con Otsu", bootstyle=estilosControlesBasicos)
        
        self.label_operaciones_generales_title.grid(row=0, column=0, columnspan=2, **paddingTitulos)
        self.label_operaciones_generales_title_img1.grid(row=1, column=0, sticky="nsew", **paddingBotones)
        self.button_convertir_grises_img1.grid(row=2, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_fijo_img1.grid(row=3, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_otsu_img1.grid(row=4, column=0, sticky="ew", **paddingBotones)
        self.label_operaciones_generales_title_img2.grid(row=5, column=0, sticky="nsew", **paddingBotones)
        self.button_convertir_grises_img2.grid(row=6, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_fijo_img2.grid(row=7, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_otsu_img2.grid(row=8, column=0, sticky="ew", **paddingBotones)
    
    def pedir_ruta_archivo(self):
        ruta_archivo = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files")])
        if ruta_archivo:
            return ruta_archivo
        else: 
            return None

    def pedir_ruta_archivo_guardar(self):
        ruta_archivo = filedialog.asksaveasfilename(title="Guardar imagen", filetypes=[("Image files", "*.jpg *.JPEJ *.png"), ("All files")])
        if ruta_archivo:
            return ruta_archivo
        else: 
            return None
    
    def aviso_binarizar_fijo(self):
        valorUmbral = simpledialog.askinteger("Binarización", "Ingrese el valor de umbral (0-255):", minvalue=0, maxvalue=255)
        return valorUmbral

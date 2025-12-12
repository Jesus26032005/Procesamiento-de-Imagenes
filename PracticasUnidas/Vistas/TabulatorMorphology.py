import ttkbootstrap as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import cv2
from ttkbootstrap.scrolled import ScrolledFrame

class TabulatorMorphology(ttk.Frame):
    """
    Clase que representa la pestaña de operaciones de morfología.
    Hereda de ttk.Frame.
    """
    def __init__(self, parent):
        """
        Inicializa la pestaña de operaciones.
        
        Args:
            parent: Widget padre (contenedor).
        """
        super().__init__(parent)
        
        # Configuración de la cuadrícula principal
        for i in range(1,3): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        # Título de la sección
        self.label_titulo = ttk.Label(self, text="Operaciones de morfología", font=("Arial", 18, "bold"))
        self.label_titulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Crear componentes para cada imagen
        self._crear_componentes_operaciones_img1()
        self._crear_componentes_operaciones_img2()

    def _crear_componentes_operaciones_img1(self):
        """
        Crea y organiza los controles para las operaciones de la imagen principal (Imagen 1).
        Incluye operaciones de morfología.
        """

        estiloControlesImg = "warning"
        self.marcoControlesImagen1 =ttk.Labelframe(self, text="Controles de imagen principal", padding=5, bootstyle=estiloControlesImg)
        self.marcoControlesImagen1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configuración del grid interno
        for i in range(4):
            self.marcoControlesImagen1.rowconfigure(i, weight=1)
        for j in range(2):
            self.marcoControlesImagen1.columnconfigure(j, weight=1)

        # Subtítulos y etiquetas
        self.subtitulo_operaciones_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones disponibles para la imagen principal", font=("Arial", 16, "bold"), wraplength=400, anchor="center")
        self.subtitulo_operaciones_morfologicas_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones morfológicas", font=("Arial", 14, "bold"), anchor="center")

        # Botones de operaciones morfológicas
        self.boton_erosion_img1 = ttk.Button(self.marcoControlesImagen1, text="Erosión", bootstyle=estiloControlesImg)
        self.boton_dilatacion_img1 = ttk.Button(self.marcoControlesImagen1, text="Dilatación", bootstyle=estiloControlesImg)
        self.boton_apertura_img1 = ttk.Button(self.marcoControlesImagen1, text="Apertura", bootstyle=estiloControlesImg)
        self.boton_cierre_img1 = ttk.Button(self.marcoControlesImagen1, text="Cierre", bootstyle=estiloControlesImg)
        self.boton_frontera_img1 = ttk.Button(self.marcoControlesImagen1, text="Frontera", bootstyle=estiloControlesImg)
        self.boton_hit_or_miss_img1 = ttk.Button(self.marcoControlesImagen1, text="Hit or Miss", bootstyle=estiloControlesImg)
        self.boton_adelgazamiento_img1 = ttk.Button(self.marcoControlesImagen1, text="Adelgazamiento", bootstyle=estiloControlesImg)
        self.boton_suavizado_morfologico_img1 = ttk.Button(self.marcoControlesImagen1, text="Suavizado morfológico", bootstyle=estiloControlesImg)
        self.boton_grad_erosion_img1 = ttk.Button(self.marcoControlesImagen1, text="Gradiente por erosión", bootstyle=estiloControlesImg)
        self.boton_grad_dilatacion_img1 = ttk.Button(self.marcoControlesImagen1, text="Gradiente por dilatación", bootstyle=estiloControlesImg)
        self.boton_grad_simetrico_img1 = ttk.Button(self.marcoControlesImagen1, text="Gradiente simétrico", bootstyle=estiloControlesImg)
        self.boton_tophat_img1 = ttk.Button(self.marcoControlesImagen1, text="Top-hat", bootstyle=estiloControlesImg)
        self.boton_blackhat_img1 = ttk.Button(self.marcoControlesImagen1, text="Black-hat", bootstyle=estiloControlesImg)

        # Posicionamiento en el grid
        self.subtitulo_operaciones_img1.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_morfologicas_img1.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.boton_erosion_img1.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_dilatacion_img1.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_apertura_img1.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_cierre_img1.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_frontera_img1.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_hit_or_miss_img1.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_adelgazamiento_img1.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_suavizado_morfologico_img1.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_grad_erosion_img1.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_grad_dilatacion_img1.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_grad_simetrico_img1.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_tophat_img1.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_blackhat_img1.grid(row=8, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)

        

    def _crear_componentes_operaciones_img2(self):
        """
        Crea y organiza los controles para las operaciones de la imagen secundaria (Imagen 2).
        Sigue la misma estructura que para la imagen 1 pero con diferente estilo visual.
        """
        estiloControlesImg = "danger"
        self.marcoControlesImagen2 =ttk.Labelframe(self, text="Controles de imagen secundaria", padding=5, bootstyle=estiloControlesImg)
        self.marcoControlesImagen2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configuración del grid interno
        for i in range(4):
            self.marcoControlesImagen2.rowconfigure(i, weight=1)
        for j in range(2):
            self.marcoControlesImagen2.columnconfigure(j, weight=1)

        # Subtítulos y etiquetas
        self.subtitulo_operaciones_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones disponibles para la imagen secundaria", font=("Arial", 16, "bold"), wraplength=400, anchor="center")
        self.subtitulo_operaciones_morfologicas_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones morfológicas", font=("Arial", 14, "bold"), anchor="center")
        
        # Botones de operaciones morfológicas
        self.boton_erosion_img2 = ttk.Button(self.marcoControlesImagen2, text="Erosión", bootstyle=estiloControlesImg)
        self.boton_dilatacion_img2 = ttk.Button(self.marcoControlesImagen2, text="Dilatación", bootstyle=estiloControlesImg)
        self.boton_apertura_img2 = ttk.Button(self.marcoControlesImagen2, text="Apertura", bootstyle=estiloControlesImg)
        self.boton_cierre_img2 = ttk.Button(self.marcoControlesImagen2, text="Cierre", bootstyle=estiloControlesImg)
        self.boton_frontera_img2 = ttk.Button(self.marcoControlesImagen2, text="Frontera", bootstyle=estiloControlesImg)
        self.boton_hit_or_miss_img2 = ttk.Button(self.marcoControlesImagen2, text="Hit or Miss", bootstyle=estiloControlesImg)
        self.boton_adelgazamiento_img2 = ttk.Button(self.marcoControlesImagen2, text="Adelgazamiento", bootstyle=estiloControlesImg)
        self.boton_suavizado_morfologico_img2 = ttk.Button(self.marcoControlesImagen2, text="Suavizado morfológico", bootstyle=estiloControlesImg)
        self.boton_grad_erosion_img2 = ttk.Button(self.marcoControlesImagen2, text="Gradiente por erosión", bootstyle=estiloControlesImg)
        self.boton_grad_dilatacion_img2 = ttk.Button(self.marcoControlesImagen2, text="Gradiente por dilatación", bootstyle=estiloControlesImg)
        self.boton_grad_simetrico_img2 = ttk.Button(self.marcoControlesImagen2, text="Gradiente simétrico", bootstyle=estiloControlesImg)
        self.boton_tophat_img2 = ttk.Button(self.marcoControlesImagen2, text="Top-hat", bootstyle=estiloControlesImg)
        self.boton_blackhat_img2 = ttk.Button(self.marcoControlesImagen2, text="Black-hat", bootstyle=estiloControlesImg)
        
        # Posicionamiento en el grid
        self.subtitulo_operaciones_img2.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_morfologicas_img2.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.boton_erosion_img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_dilatacion_img2.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_apertura_img2.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_cierre_img2.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_frontera_img2.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_hit_or_miss_img2.grid(row=4, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_adelgazamiento_img2.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_suavizado_morfologico_img2.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_grad_erosion_img2.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_grad_dilatacion_img2.grid(row=6, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_grad_simetrico_img2.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_tophat_img2.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_blackhat_img2.grid(row=8, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)

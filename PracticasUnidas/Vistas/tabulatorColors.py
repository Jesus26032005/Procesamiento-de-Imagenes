import ttkbootstrap as ttk
from tkinter import simpledialog

class TabulatorColors(ttk.Frame):
    """
    Clase que representa la pestaña de filtros y ruido en la interfaz gráfica.
    Permite al usuario aplicar diferentes tipos de ruido y filtros a las imágenes cargadas.
    """
    def __init__(self, parent):
        """
        Inicializa la pestaña de filtros.
        
        Args:
            parent: Widget padre.
        """
        super().__init__(parent)

        for i in range(1,3): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        self.label_titulo = ttk.Label(self, text="Operaciones de modelos-mapas de color", font=("Arial", 18, "bold"), wraplength=400)
        self.label_titulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self._crear_componentes_modelos_color_mapas_colores_img1()
        self._crear_componentes_modelos_color_mapas_colores_img2()

    def _crear_componentes_modelos_color_mapas_colores_img1(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar modelos de color y mapas de colores
        a la imagen principal (Imagen 1).
        """
        estiloControlesModelosColorMapasColores = "info"
        self.marco_controles_modelos_color_mapas_colores_img1 = ttk.Labelframe(self, text="Modelos de color y mapas de colores para imagen principal", padding=5, bootstyle=estiloControlesModelosColorMapasColores)

        self.marco_controles_modelos_color_mapas_colores_img1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(7): self.marco_controles_modelos_color_mapas_colores_img1.rowconfigure(i, weight=1)
        self.marco_controles_modelos_color_mapas_colores_img1.columnconfigure(0, weight=1)

        # Subtítulos
        self.subtitulo_controles_modelos_color_mapas_colores_Img1 = ttk.Label(self.marco_controles_modelos_color_mapas_colores_img1, text="Operaciones de modelos de color y mapas de colores para la imagen principal", font=("Arial", 16, "bold"), wraplength= 400)
        
        # Sección de Ruido
        self.subtitulo_mostrar_modelos_de_color_Img1 = ttk.Label(self.marco_controles_modelos_color_mapas_colores_img1, text="Mostrar modelos de color", font=("Arial", 14, "bold"), wraplength=400)
        self.boton_mostrar_modelo_de_color_RGB_IMG1 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img1, text="Mostrar modelo de color RGB", bootstyle="primary")
        self.boton_mostrar_modelo_de_color_HSV_IMG1 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img1, text="Mostrar modelo de color HSV", bootstyle="primary")
        self.boton_mostrar_modelo_de_color_CMY_IMG1 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img1, text="Mostrar modelo de color CMY", bootstyle="primary")      
        
        # Seccion de mapas de colores
        self.subtitulo_mostrar_mapas_de_colores_Img1 = ttk.Label(self.marco_controles_modelos_color_mapas_colores_img1, text="Mostrar mapas de colores", font=("Arial", 14, "bold"), wraplength=400)
        self.boton_mostrar_mapa_de_colores_Img1 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img1, text="Mostrar mapa de colores", bootstyle="primary")

        self.subtitulo_controles_modelos_color_mapas_colores_Img1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.subtitulo_mostrar_modelos_de_color_Img1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_modelo_de_color_RGB_IMG1.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_modelo_de_color_HSV_IMG1.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_modelo_de_color_CMY_IMG1.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.subtitulo_mostrar_mapas_de_colores_Img1.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_mapa_de_colores_Img1.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
                

    def _crear_componentes_modelos_color_mapas_colores_img2(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar modelos de color y mapas de colores
        a la imagen secundaria (Imagen 2).
        """
        estiloControlesRuidoFiltro = "primary"
        self.marco_controles_modelos_color_mapas_colores_img2 = ttk.Labelframe(self, text="Modelos de color y mapas de colores para imagen secundaria", padding=5, bootstyle=estiloControlesRuidoFiltro )
        self.marco_controles_modelos_color_mapas_colores_img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(7): self.marco_controles_modelos_color_mapas_colores_img2.rowconfigure(i, weight=1)
        self.marco_controles_modelos_color_mapas_colores_img2.columnconfigure(0, weight=1)
        
        self.subtitulo_controles_modelos_color_mapas_colores_Img2 = ttk.Label(self.marco_controles_modelos_color_mapas_colores_img2, text="Operaciones de modelos de color y mapas de colores para la imagen secundaria", font=("Arial", 16, "bold"), wraplength=400)
        self.subtitulo_mostrar_modelos_de_color_Img2 = ttk.Label(self.marco_controles_modelos_color_mapas_colores_img2, text="Mostrar modelos de color", font=("Arial", 14, "bold"), wraplength=400)
        self.boton_mostrar_modelo_de_color_RGB_IMG2 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img2, text="Mostrar modelo de color RGB", bootstyle="primary")
        self.boton_mostrar_modelo_de_color_HSV_IMG2 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img2, text="Mostrar modelo de color HSV", bootstyle="primary")
        self.boton_mostrar_modelo_de_color_CMY_IMG2 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img2, text="Mostrar modelo de color CMY", bootstyle="primary")      
        
        self.subtitulo_mostrar_mapas_de_colores_Img2 = ttk.Label(self.marco_controles_modelos_color_mapas_colores_img2, text="Mostrar mapas de colores", font=("Arial", 14, "bold"), wraplength=400)
        self.boton_mostrar_mapa_de_colores_Img2 = ttk.Button(self.marco_controles_modelos_color_mapas_colores_img2, text="Mostrar mapa de colores", bootstyle="primary")

        self.subtitulo_controles_modelos_color_mapas_colores_Img2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.subtitulo_mostrar_modelos_de_color_Img2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_modelo_de_color_RGB_IMG2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_modelo_de_color_HSV_IMG2.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_modelo_de_color_CMY_IMG2.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.subtitulo_mostrar_mapas_de_colores_Img2.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_mostrar_mapa_de_colores_Img2.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
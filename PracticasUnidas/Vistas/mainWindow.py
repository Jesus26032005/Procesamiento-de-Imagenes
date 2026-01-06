import ttkbootstrap as ttk  
from ttkbootstrap.constants import *  
from Vistas.tabulatorOperations import TabulatorOperations
from Vistas.tabulatorImage import TabulatorImage
from Vistas.tabulatorFilters import TabulatorFilters
from Vistas.tabulatorSegmentation import TabulatorSegmentation
from Vistas.tabulatorbrightness import TabulatorBrightness
from Vistas.TabulatorMorphology import TabulatorMorphology
from Vistas.tabulatorColors import TabulatorColors
from tkinter import filedialog, messagebox, simpledialog, DISABLED
from ttkbootstrap.scrolled import ScrolledFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
from matplotlib.colors import LinearSegmentedColormap
import cv2
import os
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import matplotlib.gridspec as gridspec


# Configuraciones de padding para consistencia visual
paddingBotones = {"padx": 10, "pady": 5, "ipady": 3}
paddingTitulos = {"padx": 5, "pady": 1}
paddingFrames = {"padx": 10, "pady": 10, "ipady": 5}

class MainWindow(ttk.Window):
    """
    Ventana principal de la aplicación.
    Hereda de ttk.Window y gestiona la disposición general de los paneles y pestañas.
    """
    def __init__(self):
        """
        Inicializa la ventana principal, configura el tema y la disposición de la cuadrícula.
        """
        super().__init__(themename="cyborg")
        self.title("Procesamiento de Imagenes - Practicas minireto")
        self.state('zoomed') # Inicia maximizada

        # Configuración de la cuadrícula principal (8 columnas para imagen, 2 para controles)
        self.rowconfigure(0, weight=1)
        for i in range(8): self.columnconfigure(i, weight=1)

        self.configurar_frames()

    def configurar_frames(self):
        """
        Configura los marcos principales de la interfaz:
        1. Panel de visualización de imágenes (izquierda).
        2. Panel de pestañas de control (derecha).
        """
        # Panel izquierdo para visualizar imágenes (con scroll si es necesario)
        self.panel_imagen_global = ScrolledFrame(self, padding=10)
        self.panel_imagen_global.grid(row=0, column=0, sticky="nsew", columnspan=8)
        self.panel_imagen_global.columnconfigure(0, weight=1)
        for i in range(2): self.panel_imagen_global.rowconfigure(i, weight=1)

        # Panel derecho con pestañas para los controles
        self.panelTabulator = ttk.Notebook(self, padding=10)
        self.panelTabulator.grid(row=0, column=8, sticky="nsew", columnspan=2)
        self.panelTabulator.columnconfigure(0, weight=1)
        self.panelTabulator.rowconfigure(0, weight=1)
        
        self._configurarPanelImagen()
        self._configurarPanelTabulator()

    def _configurarPanelTabulator(self):
        """
        Inicializa y agrega las diferentes pestañas de control al Notebook.
        """
        self.tabulator_main = TabulatorImage(self.panelTabulator)
        self.tabulator_operations = TabulatorOperations(self.panelTabulator)
        self.tabulator_filters = TabulatorFilters(self.panelTabulator)
        self.tabulator_segmentation = TabulatorSegmentation(self.panelTabulator)
        self.tabulator_brightness = TabulatorBrightness(self.panelTabulator)
        self.tabulator_morphology = TabulatorMorphology(self.panelTabulator)
        self.tabulator_colors = TabulatorColors(self.panelTabulator)
        
        self.panelTabulator.add(self.tabulator_main, text="Practica Principal")
        self.panelTabulator.add(self.tabulator_operations, text="Operaciones")
        self.panelTabulator.add(self.tabulator_filters, text="Filtros")
        self.panelTabulator.add(self.tabulator_segmentation, text="Segmentación")
        self.panelTabulator.add(self.tabulator_brightness, text="Brillo")
        self.panelTabulator.add(self.tabulator_morphology, text="Morfológica")  
        self.panelTabulator.add(self.tabulator_colors, text="Colores")

    def _configurarPanelImagen(self):
        """
        Configura los marcos de visualización para la Imagen 1 y la Imagen 2.
        Incluye etiquetas para títulos, imágenes originales, modificadas e histogramas.
        """
        estiloImagen1 = "info"
        estiloImagen2 = "warning"

        # --- Configuración Imagen 1 ---
        self.frame_imagen1 = ttk.Labelframe(self.panel_imagen_global, text="Visualización de la imagen", padding=10, bootstyle=estiloImagen1)
        self.frame_imagen1.grid(row=0, column=0, sticky="nsew", **paddingFrames)
        for i in range(11):  self.frame_imagen1.rowconfigure(i, weight=1)
        self.frame_imagen1.columnconfigure(0, weight=1)

        self.label_visualizacion_title_img1 = ttk.Label(self.frame_imagen1, text="Visualización de la imagen principal", font=("Arial", 16, "bold"))
        self.label_visualizacion_subtitle_img1 = ttk.Label(self.frame_imagen1, text="Imagen Principal", font=("Arial", 12))
        self.label_visualizacion_lab_img1 = ttk.Label(self.frame_imagen1, text="Aquí se mostrará la imagen cargada y resultados", font=("Arial", 12), anchor="center")
        self.label_visualizacion_title_img1Modified = ttk.Label(self.frame_imagen1, text="Imagen Modificada", font=("Arial", 12))
        self.label_visualizacion_lab_img1Modified = ttk.Label(self.frame_imagen1, text="Aquí se mostrará la imagen modificada", font=("Arial", 12), anchor="center")
        
        self.label_visualizacion_title_img1.grid(row=0, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_subtitle_img1.grid(row=1, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_lab_img1.grid(row=2, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_title_img1Modified.grid(row=6, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_lab_img1Modified.grid(row=7, column=0, sticky="nsew", **paddingTitulos)
        
        # --- Configuración Imagen 2 ---
        self.frame_imagen2 = ttk.Labelframe(self.panel_imagen_global, text="Visualización de la imagen adicional", padding=10, bootstyle=estiloImagen2)
        self.frame_imagen2.grid(row=1, column=0, sticky="nsew", **paddingFrames)
        for i in range(11): self.frame_imagen2.rowconfigure(i, weight=1)
        self.frame_imagen2.columnconfigure(0, weight=1)

        self.label_visualizacion_title_img2 = ttk.Label(self.frame_imagen2, text="Visualización de la imagen adicional", font=("Arial", 16, "bold"))
        self.label_visualizacion_subtitle_img2 = ttk.Label(self.frame_imagen2, text="Imagen Adicional", font=("Arial", 12))
        self.label_visualizacion_lab_img2 = ttk.Label(self.frame_imagen2, text="Aquí se mostrará la imagen adicional cargada", font=("Arial", 12), anchor="center")
        self.label_visualizacion_title_img2Modified = ttk.Label(self.frame_imagen2, text="Imagen Adicional Modificada", font=("Arial", 12))
        self.label_visualizacion_lab_img2Modified = ttk.Label(self.frame_imagen2, text="Aquí se mostrará la imagen adicional modificada", font=("Arial", 12), anchor="center")
        
        self.label_visualizacion_title_img2.grid(row=0, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_subtitle_img2.grid(row=1, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_lab_img2.grid(row=2, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_title_img2Modified.grid(row=6, column=0, sticky="nsew", **paddingTitulos)
        self.label_visualizacion_lab_img2Modified.grid(row=7, column=0, sticky="nsew", **paddingTitulos)

    def mostrar_imagen_cargada(self, imagen_tkinter,  histograma ,no_imagen, tipo_imagen="original"):
        """
        Muestra la imagen cargada y su histograma inicial en la interfaz.
        
        Args:
            imagen_tkinter (list): Lista con [imagen_original, imagen_modificada] (al cargar son iguales).
            histograma (list): Datos del histograma.
            no_imagen (int): Identificador de la imagen (1 o 2).
            tipo_imagen (str): Tipo de imagen (por defecto "original").
        """
        imagenOriginal = imagen_tkinter[0]
        imagenModificada = imagen_tkinter[1]
        histograma_imagen = histograma
        
        if no_imagen == 1:
                self.label_visualizacion_lab_img1.config(image=imagenOriginal)
                self.label_visualizacion_lab_img1.image = imagenOriginal
                self.label_visualizacion_lab_img1Modified.config(image=imagenModificada)
                self.label_visualizacion_lab_img1Modified.image = imagenModificada
                self.crear_histograma_rgb(no_imagen, histograma_imagen, modalidad="principal")
                self.crear_histograma_rgb(no_imagen, histograma_imagen, modalidad="modificada")
        elif no_imagen == 2:
                self.label_visualizacion_lab_img2.config(image=imagenOriginal)
                self.label_visualizacion_lab_img2.image = imagenOriginal
                self.label_visualizacion_lab_img2Modified.config(image=imagenModificada)
                self.label_visualizacion_lab_img2Modified.image = imagenModificada
                self.crear_histograma_rgb(no_imagen, histograma_imagen, modalidad="principal")
                self.crear_histograma_rgb(no_imagen, histograma_imagen, modalidad="modificada")

    def crear_histograma_rgb(self, imagen_no, histograma, modalidad= 'principal'):
        """
        Genera y muestra los histogramas RGB usando Matplotlib.
        
        Args:
            imagen_no (int): Identificador de la imagen.
            histograma (list): Datos del histograma (lista de [valores, frecuencias] por canal).
            modalidad (str): 'principal' (imagen original) o 'modificada'.
        """
        datos = self.determinar_ubicacion_grid_img(imagen_no, modalidad)
        ubicacion, no_grid = datos[0], datos[1]
        
        # Limpiar histogramas anteriores
        for i in range(3):
            widgets = ubicacion.grid_slaves(row=no_grid+i, column=0)
            for widget in widgets:
                widget.destroy()

        histogramas_rgb= histograma
        canales = ['Red', 'Green', 'Blue']
        for i, histograma in enumerate(histogramas_rgb):
            ubicacion.rowconfigure(no_grid+i, weight=0)
            # Manejo de caso borde: histograma vacío o con un solo valor
            if len(histograma[0]) == 1:
                x = histograma[0][0]
                y = histograma[1][0]
                histograma = [[254, x], [0, y]]

            fig = Figure(figsize=(16, 6), dpi=100)
            ax = fig.add_subplot(1, 1, 1) 
            ax.bar(histograma[0], histograma[1], color= canales[i], alpha=0.7, width=1)
            ax.set_ylabel("Número de píxeles (Frecuencia)")
            ax.set_xlabel("Intensidad de pixeles")
            ax.set_title("Histograma del canal " + canales[i])
            ax.xaxis.set_major_locator(MultipleLocator(25))
            ax.yaxis.grid(True, linestyle="--", alpha=0.7)
            
            canvas = FigureCanvasTkAgg(fig, master=ubicacion)
            canvas.draw()
            canvas.get_tk_widget().grid(row=no_grid+i, column=0, sticky="nsew")
    
    def crear_histograma_gris(self, imagen_no, histograma):
        """
        Genera y muestra el histograma de escala de grises.
        
        Args:
            imagen_no (int): Identificador de la imagen.
            histograma (tuple): (valores, frecuencias).
        """
        datos = self.determinar_ubicacion_grid_img(imagen_no, 'adicional')
        ubicacion, no_grid = datos[0], datos[1]

        # Limpiar histogramas anteriores
        for i in range(3):
            widgets = ubicacion.grid_slaves(row=no_grid+i, column=0)
            for widget in widgets:
                widget.destroy()
        ubicacion.rowconfigure(no_grid, weight=0)

        fig = Figure(figsize=(16, 5), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        histogramaGris = histograma
        
        if len(histogramaGris[0]) == 1:
                x = histogramaGris[0][0]
                y = histogramaGris[1][0]
                histogramaGris = [[254, x], [0, y]]

        ax.bar(histogramaGris[0], histogramaGris[1], color='black', alpha=0.7, width=1)
        ax.set_xlabel("Intensidad de gris")
        ax.set_ylabel("Número de píxeles (Frecuencia)")
        ax.set_title("Histograma de escala de grises");
        ax.xaxis.set_major_locator(MultipleLocator(25))
        ax.yaxis.grid(True, linestyle="--", alpha=0.7)
        
        canvas = FigureCanvasTkAgg(fig, master=ubicacion)
        canvas.draw()
        canvas.get_tk_widget().grid(row=no_grid, column=0, sticky="nsew")

    def actualizar_imagen(self, imagen_tkinter, histograma, no_imagen, tipo_imagen):
        """
        Actualiza la visualización de la imagen modificada y su histograma.
        
        Args:
            imagen_tkinter (ImageTk.PhotoImage): Imagen modificada.
            histograma (list/tuple): Datos del nuevo histograma.
            no_imagen (int): Identificador de la imagen.
            tipo_imagen (str): Tipo de la imagen ('rgb', 'gris', 'binaria').
        """
        if no_imagen == 1:
            self.label_visualizacion_lab_img1Modified.config(image=imagen_tkinter)
            self.label_visualizacion_lab_img1Modified.image = imagen_tkinter
            if tipo_imagen == 'rgb':
                self.crear_histograma_rgb(no_imagen, histograma, modalidad="modificada")
            elif tipo_imagen == 'gris':
                self.crear_histograma_gris(no_imagen, histograma)
            elif tipo_imagen == 'binaria' or tipo_imagen == 'componentes':
                # Las imágenes binarias no suelen mostrar histograma detallado en esta vista
                ubicacion, noGrid = self.determinar_ubicacion_grid_img(no_imagen, modalidad="modificada")
                for i in range(3):
                    widgets = ubicacion.grid_slaves(row=noGrid+i, column=0)
                    for widget in widgets: widget.destroy()

        elif no_imagen == 2:
            self.label_visualizacion_lab_img2Modified.config(image=imagen_tkinter)
            self.label_visualizacion_lab_img2Modified.image = imagen_tkinter
            if tipo_imagen == 'rgb':
                self.crear_histograma_rgb(no_imagen, histograma, modalidad="modificada")
            elif tipo_imagen == 'gris':
                self.crear_histograma_gris(no_imagen, histograma)
            elif tipo_imagen == 'binaria' or tipo_imagen == 'componentes':
                ubicacion, noGrid = self.determinar_ubicacion_grid_img(no_imagen, modalidad="modificada")
                for i in range(3):
                    widgets = ubicacion.grid_slaves(row=noGrid+i, column=0)
                    for widget in widgets: widget.destroy()

    def determinar_ubicacion_grid_img(self, noImagen, modalidad= 'principal'):
        """
        Helper para determinar en qué frame y fila colocar los elementos visuales.
        """
        ubicacion = None
        no_grid = 0

        if noImagen ==1: ubicacion = self.frame_imagen1
        else: ubicacion = self.frame_imagen2
        
        # Fila 3 para histogramas originales, Fila 8 para modificados
        no_grid = 3 if modalidad == 'principal' else 8
        return ubicacion, no_grid

    def mostrar_mensaje(self, mensaje, tipo_mensaje="info"):
        """
        Muestra un cuadro de diálogo con un mensaje.
        
        Args:
            mensaje (str): Texto del mensaje.
            tipo_mensaje (str): Tipo ('info', 'error', 'warning').
        """
        if tipo_mensaje == "info":
            messagebox.showinfo("Información", mensaje)
        elif tipo_mensaje == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo_mensaje == "warning":
            messagebox.showwarning("Advertencia", mensaje)

    def mostrar_en_ventana_modelo_color(self, canal1, canal2, canal3, modelo_color):
        """
        Muestra 3 canales en una ventana emergente usando Matplotlib.
        
        Args:
            canal1, canal2, canal3: Arrays numpy (imágenes de un solo canal).
            modelo_color (str): Modelo de color de la imagen.
            titulo_ventana (str): Título de la ventana emergente.
        """
        if hasattr(self, 'ventana_modelo_color'):
            self.ventana_modelo_color.destroy()

        self.ventana_modelo_color = ttk.Toplevel(self)
        self.ventana_modelo_color.title(modelo_color)
        self.ventana_modelo_color.geometry("900x400")

        fig = Figure(figsize=(9, 3), dpi=100)
        
        if modelo_color == "RGB":
            mapas = ["Reds", "Greens", "Blues"]
            valores_maximo_minimo = [(0,255), (0,255), (0,255)]
        elif modelo_color == "HSV":
            mapas = ["hsv", "gray", "gray"]
            valores_maximo_minimo = [(0,179), (0,255), (0,255)]
        elif modelo_color == "CMY":
            mapas = ["Blues", "Purples", "Oranges"]
            valores_maximo_minimo = [(0,255), (0,255), (0,255)]

        canales = [canal1, canal2, canal3]
        
        for i in range(3):
            ax = fig.add_subplot(1, 3, i+1)
            ax.imshow(canales[i], cmap=mapas[i], vmin=valores_maximo_minimo[i][0], vmax=valores_maximo_minimo[i][1])
            ax.set_title(modelo_color[i])
            ax.axis('off')

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.ventana_modelo_color)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

    def mostrar_ventana_mapas_colores(self, imagen_gris):
        """
        Genera una ventana emergente con diferentes mapas de colores aplicados a la imagen.
        Args:
            imagen_gris (numpy array): Imagen en escala de grises.
        """
        if hasattr(self, 'ventana_mapas'):
            self.ventana_mapas.destroy()
        
        self.ventana_mapas = ttk.Toplevel(self)
        self.ventana_mapas.title("Visualización de Mapas de Colores y Pseudocolores")
        self.ventana_mapas.geometry("1000x800")
        
        panel_scroll = ScrolledFrame(self.ventana_mapas, autohide=False)
        panel_scroll.pack(fill=BOTH, expand=YES)
 
        colores_pastel = [(1.0, 0.8, 0.9), (0.8, 1.0, 0.8), (0.8, 0.9, 1.0), (1.0, 1.0, 0.8), (0.9, 0.8, 1.0)]
        mapa_pastel = LinearSegmentedColormap.from_list("PastelMap", colores_pastel, N=256)

        coloresTron = [(0/255, 14/255, 82/255), (0/255, 27/255, 145/255), (122/255, 147/255, 255/255)]
        mapa_tron = LinearSegmentedColormap.from_list("TronMap", coloresTron, N=256)

        coloresTronAres = [(64/255, 0/255, 32/255), (130/255, 0/255, 7/255), (255/255, 207/255, 208/255)]
        mapa_tron_ares = LinearSegmentedColormap.from_list("TronAresMap", coloresTronAres, N=256)

        coloresDivisiones = [(176/255, 0/255, 167/255), (0/255, 176/255, 47/255), (176/255, 91/255, 0/255)]
        mapa_divisiones = LinearSegmentedColormap.from_list("DivisionesMap", coloresDivisiones, N=3)

        coloresArcoiris = [
            (148/255, 0/255, 211/255), (75/255, 0/255, 130/255), (0/255, 0/255, 255/255), 
            (0/255, 130/255, 20/255), (240/255, 240/255, 0/255), (240/255, 120/255, 0/255), (255/255, 0/255, 0/255)
        ]
        mapa_arcoiris = LinearSegmentedColormap.from_list("ArcoirisMap", coloresArcoiris, N=7)

        coloresBolilloMoho = [
            (102/255, 51/255, 0/255), (153/255, 102/255, 51/255), (26/255, 128/255, 0/255), 
            (204/255, 153/255, 102/255), (255/255, 204/255, 153/255)
        ]
        mapa_bolillo_moho = LinearSegmentedColormap.from_list("BolilloMohoMap", coloresBolilloMoho, N=5)

        # B. Mapas de OpenCV (Calculados al momento)
        # Nota: OpenCV devuelve BGR, Matplotlib espera RGB
        imagen_jet = cv2.applyColorMap(imagen_gris, cv2.COLORMAP_JET)
        imagen_jet_rgb = cv2.cvtColor(imagen_jet, cv2.COLOR_BGR2RGB)
        
        imagen_hot = cv2.applyColorMap(imagen_gris, cv2.COLORMAP_HOT)
        imagen_hot_rgb = cv2.cvtColor(imagen_hot, cv2.COLOR_BGR2RGB)
        
        imagen_ocean = cv2.applyColorMap(imagen_gris, cv2.COLORMAP_OCEAN)
        imagen_ocean_rgb = cv2.cvtColor(imagen_ocean, cv2.COLOR_BGR2RGB)

        # ---------------------------
        # Creación de la Figura
        # ---------------------------
        # Ajustamos el tamaño vertical (figsize) para que quepan 5 filas cómodamente
        fig = Figure(figsize=(12, 20), dpi=100)
        
        # Lista de configuraciones para iterar y graficar
        # Formato: (Posición, Imagen, Título, Colormap_Matplotlib)
        # Si Colormap_Matplotlib es None, se asume que la imagen ya es RGB
        lista_graficos = [
            (1, imagen_gris, 'Escala de grises (Original)', 'gray'),
            (2, imagen_jet_rgb, 'OpenCV: JET', None),
            (3, imagen_hot_rgb, 'OpenCV: HOT', None),
            (4, imagen_gris, 'Matplotlib: Pastel', mapa_pastel),
            (5, imagen_gris, 'Matplotlib: Tron', mapa_tron),
            (6, imagen_gris, 'Matplotlib: Tron Ares', mapa_tron_ares),
            (7, imagen_gris, 'Matplotlib: Divisiones (N=3)', mapa_divisiones),
            (8, imagen_gris, 'Matplotlib: Arcoiris (N=7)', mapa_arcoiris),
            (9, imagen_gris, 'Matplotlib: Bolillo Moho', mapa_bolillo_moho),
            (10, imagen_ocean_rgb, 'OpenCV: OCEAN', None) 
        ]

        for pos, img, titulo, cmap in lista_graficos:
            ax = fig.add_subplot(5, 2, pos)
            if cmap:
                ax.imshow(img, cmap=cmap)
            else:
                ax.imshow(img) # Ya viene en RGB
            
            ax.set_title(titulo, fontsize=10)
            ax.axis('off')

        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, master=panel_scroll)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES, padx=10, pady=10)

    def mostrar_mensaje_valores_histograma(self, valores):
        """
        Muestra un cuadro de diálogo con los valores del histograma.
        
        Args:
            valores (list): Lista de valores del histograma.
        """
        messagebox.showinfo("Valores del Histograma", "\n\n".join(valores))

    def analisis_frecuencia_completo(self, imagen_gris_cv):
        """
        Realiza el análisis de frecuencia (FFT y DCT) adaptado del script proporcionado.
        Genera una ventana emergente con los resultados visuales usando GridSpec.
        
        Args:
            imagen_gris_cv (numpy array): Imagen en formato OpenCV (Grayscale).
        """

        imagen_gris = imagen_gris_cv
        img_float = imagen_gris.astype(np.float32) / 255.0

        # --- FUNCIONES INTERNAS ---
        def fft2_imagen(img):
            F = np.fft.fft2(img)
            Fshift = np.fft.fftshift(F)
            magnitud = np.log(1 + np.abs(Fshift))
            fase = np.angle(Fshift)
            return F, Fshift, magnitud, fase

        def crear_mascara(img_shape, filtro='butterworth', tipo='lowpass', cutoff=0.15, orden=2):
            rows, cols = img_shape
            crow, ccol = rows//2, cols//2
            Y, X = np.ogrid[:rows, :cols]
            D = np.sqrt((Y - crow)**2 + (X - ccol)**2)
            Dnorm = D / float(min(crow, ccol))
            
            if filtro == 'ideal':
                H = (Dnorm <= cutoff).astype(np.float32)
            elif filtro == 'gaussiano':
                H = np.exp(-(Dnorm**2) / (2 * (cutoff**2)))
            elif filtro == 'butterworth':
                H = 1 / (1 + (Dnorm / (cutoff + 1e-8))**(2*orden))
            
            if tipo == 'highpass': H = 1 - H
            return H.astype(np.float32)

        def dct_matrix(N=8):
            C = np.zeros((N, N), dtype=np.float64)
            for k in range(N):
                alpha = math.sqrt(1/N) if k == 0 else math.sqrt(2/N)
                for n in range(N):
                    C[k, n] = alpha * math.cos(((2*n + 1) * k * math.pi) / (2*N))
            return C

        def dct_compresion_simulada(img, q_factor=0.5):
            C8 = dct_matrix(8)
            Q_JPEG = np.array([
                [16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],
                [14,13,16,24,40,57,69,56],[14,17,22,29,51,87,80,62],
                [18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],
                [49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]
            ], dtype=np.float64) * q_factor

            h_orig, w_orig = img.shape
            nh = ((h_orig + 7)//8)*8
            nw = ((w_orig + 7)//8)*8
            padded = np.zeros((nh, nw), dtype=img.dtype)
            padded[:h_orig, :w_orig] = img

            recon = np.zeros_like(padded, dtype=np.float64)

            for i in range(0, nh, 8):
                for j in range(0, nw, 8):
                    b = padded[i:i+8, j:j+8]
                    b_shift = b - 0.5
                    D = C8 @ b_shift @ C8.T
                    Dq = np.round(D / Q_JPEG)
                    Dr = Dq * Q_JPEG
                    br = C8.T @ Dr @ C8 + 0.5
                    recon[i:i+8, j:j+8] = br
            
            recon = np.clip(recon[:h_orig, :w_orig], 0, 1)
            mse = np.mean((img - recon)**2)
            psnr = 20 * math.log10(1.0) - 10 * math.log10(mse) if mse > 0 else float('inf')
            return recon, psnr

        # --- CÁLCULOS ---
        p_filtro = 'butterworth'
        p_tipo = 'lowpass'
        p_cutoff = 0.15
        p_orden = 2
        p_dct_q = 0.5

        F, Fshift, magnitud, fase = fft2_imagen(img_float)
        mask = crear_mascara(img_float.shape, p_filtro, p_tipo, p_cutoff, p_orden)
        Gshift = Fshift * mask
        g = np.real(np.fft.ifft2(np.fft.ifftshift(Gshift)))
        g = np.clip(g, 0, 1)

        dct_reconstruida, psnr_val = dct_compresion_simulada(img_float, q_factor=p_dct_q)

        ventana_fft = ttk.Toplevel(self)
        ventana_fft.title("Análisis de Frecuencia (FFT y DCT)")
        ventana_fft.geometry("1100x800")
        
        scroll_panel = ScrolledFrame(ventana_fft, autohide=False)
        scroll_panel.pack(fill=BOTH, expand=YES)

        fig = Figure(figsize=(10, 14), dpi=100)
        
        gs = gridspec.GridSpec(3, 6, figure=fig)

        ax_orig = fig.add_subplot(gs[0, 0:2])
        ax_mag = fig.add_subplot(gs[0, 2:4])
        ax_fase = fig.add_subplot(gs[0, 4:6])

        ax_mask = fig.add_subplot(gs[1, 0:3])
        ax_filt = fig.add_subplot(gs[1, 3:6])

        ax_dct_orig = fig.add_subplot(gs[2, 0:3])
        ax_dct_rec = fig.add_subplot(gs[2, 3:6])

        ax_orig.imshow(img_float, cmap='gray')
        ax_orig.set_title('Original')
        ax_orig.axis('off')

        ax_mag.imshow(magnitud, cmap='gray')
        ax_mag.set_title('Espectro Magnitud (log)')
        ax_mag.axis('off')

        ax_fase.imshow(fase, cmap='twilight')
        ax_fase.set_title('Espectro Fase')
        ax_fase.axis('off')

        ax_mask.imshow(mask, cmap='gray')
        ax_mask.set_title(f'Máscara {p_filtro}\n({p_tipo}, cut={p_cutoff})')
        ax_mask.axis('off')

        ax_filt.imshow(g, cmap='gray')
        ax_filt.set_title('Filtrada (IFFT)')
        ax_filt.axis('off')

        ax_dct_orig.imshow(img_float, cmap='gray')
        ax_dct_orig.set_title('Original para DCT')
        ax_dct_orig.axis('off')

        ax_dct_rec.imshow(dct_reconstruida, cmap='gray')
        ax_dct_rec.set_title(f'Reconstruida DCT (q={p_dct_q})\nPSNR: {psnr_val:.2f} dB')
        ax_dct_rec.axis('off')

        fig.suptitle("Resultados de Práctica Frecuencia (FFT & DCT)", fontsize=16)
        
        fig.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, master=scroll_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=YES, padx=10, pady=10)
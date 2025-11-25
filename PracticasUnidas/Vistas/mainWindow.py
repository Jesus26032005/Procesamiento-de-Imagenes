import ttkbootstrap as ttk  
from ttkbootstrap.constants import *  
from Vistas.tabulatorOperations import TabulatorOperations
from Vistas.tabulatorImage import TabulatorImage
from Vistas.tabulatorFilters import TabulatorFilters
from Vistas.tabulatorSegmentation import TabulatorSegmentation
from Vistas.tabulatorbrightness import TabulatorBrightness
from tkinter import filedialog, messagebox, simpledialog, DISABLED
from ttkbootstrap.scrolled import ScrolledFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator

paddingBotones = {"padx": 10, "pady": 5, "ipady": 3}
paddingTitulos = {"padx": 5, "pady": 1}
paddingFrames = {"padx": 10, "pady": 10, "ipady": 5}

class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg")
        self.title("Procesamiento de Imagenes - Practicas minireto")
        self.state('zoomed')

        self.rowconfigure(0, weight=1)
        for i in range(8): self.columnconfigure(i, weight=1)

        self.configurar_frames()

    def configurar_frames(self):
        self.panel_imagen_global = ScrolledFrame(self, padding=10)
        self.panel_imagen_global.grid(row=0, column=0, sticky="nsew", columnspan=8)
        self.panel_imagen_global.columnconfigure(0, weight=1)
        for i in range(2): self.panel_imagen_global.rowconfigure(i, weight=1)

        self.panelTabulator = ttk.Notebook(self, padding=10)
        self.panelTabulator.grid(row=0, column=8, sticky="nsew", columnspan=2)
        self.panelTabulator.columnconfigure(0, weight=1)
        self.panelTabulator.rowconfigure(0, weight=1)
        
        self._configurarPanelImagen()
        self._configurarPanelTabulator()

    def _configurarPanelTabulator(self):
        self.tabulator_main = TabulatorImage(self.panelTabulator)
        self.tabulator_operations = TabulatorOperations(self.panelTabulator)
        self.tabulator_filters = TabulatorFilters(self.panelTabulator)
        self.tabulator_segmentation = TabulatorSegmentation(self.panelTabulator)
        self.tabulator_brightness = TabulatorBrightness(self.panelTabulator)
        self.panelTabulator.add(self.tabulator_main, text="Practica Principal")
        self.panelTabulator.add(self.tabulator_operations, text="Operaciones")
        self.panelTabulator.add(self.tabulator_filters, text="Filtros")
        self.panelTabulator.add(self.tabulator_segmentation, text="Segmentación")
        self.panelTabulator.add(self.tabulator_brightness, text="Brillo")

    def _configurarPanelImagen(self):
        estiloImagen1 = "info"
        estiloImagen2 = "warning"

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

    def crear_histograma_rgb(self, imagen_no, histograma,modalidad= 'principal'):
        datos = self.determinar_ubicacion_grid_img(imagen_no, modalidad)
        ubicacion, no_grid = datos[0], datos[1]
        for i in range(3):
            widgets = ubicacion.grid_slaves(row=no_grid+i, column=0)
            for widget in widgets:
                widget.destroy()

        histogramas_rgb= histograma
        canales = ['Red', 'Green', 'Blue']
        for i, histograma in enumerate(histogramas_rgb):
            ubicacion.rowconfigure(no_grid+i, weight=0)
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
        datos = self.determinar_ubicacion_grid_img(imagen_no, 'adicional')
        ubicacion, no_grid = datos[0], datos[1]

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
        if no_imagen == 1:
            self.label_visualizacion_lab_img1Modified.config(image=imagen_tkinter)
            self.label_visualizacion_lab_img1Modified.image = imagen_tkinter
            if tipo_imagen == 'rgb':
                self.crear_histograma_rgb(no_imagen, histograma, modalidad="modificada")
            elif tipo_imagen == 'gris':
                self.crear_histograma_gris(no_imagen, histograma)
            elif tipo_imagen == 'binaria':
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
            elif tipo_imagen == 'binaria':
                ubicacion, noGrid = self.determinar_ubicacion_grid_img(no_imagen, modalidad="modificada")
                for i in range(3):
                    widgets = ubicacion.grid_slaves(row=noGrid+i, column=0)
                    for widget in widgets: widget.destroy()

    def determinar_ubicacion_grid_img(self, noImagen, modalidad= 'principal'):
        ubicacion = None
        no_grid = 0

        if noImagen ==1: ubicacion = self.frame_imagen1
        else: ubicacion = self.frame_imagen2
        
        no_grid = 3 if modalidad == 'principal' else 8
        return ubicacion, no_grid

    def mostrar_mensaje(self, mensaje, tipo_mensaje="info"):
        if tipo_mensaje == "info":
            messagebox.showinfo("Información", mensaje)
        elif tipo_mensaje == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo_mensaje == "warning":
            messagebox.showwarning("Advertencia", mensaje)

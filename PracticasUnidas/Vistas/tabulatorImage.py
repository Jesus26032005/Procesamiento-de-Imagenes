import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledFrame
from tkinter import filedialog, messagebox, simpledialog, DISABLED, NORMAL
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator

paddingBotones = {"padx": 10, "pady": 5, "ipady": 5}
paddingTitulos = {"padx": 5, "pady": 3}
paddingFrames = {"padx": 10, "pady": 10}

class TabulatorImage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        for i in range(5): self.columnconfigure(i, weight=7)
        self.rowconfigure(0, weight=1)
        self._crear_componentes()

    def _crear_componentes(self):
        # Creacion de panel de imagen donde se mostraran las imagenes cargadas
        self.panelImagen = ScrolledFrame(self, padding=10)
        self.panelImagen.grid(row=0, column=0, sticky="nsew", columnspan=5)
        
        for i in range(1): self.panelImagen.rowconfigure(i, weight=1)
        self.panelImagen.columnconfigure(0, weight=1)

        # Creacion de panel de control donde se mostraran los controles para manipular las imagenes
        self.panelControl = ttk.Frame(self, padding=10)
        self.panelControl.grid(row=0, column=5, sticky="nsew", columnspan=2)

        self.panelControl.rowconfigure(0, weight=0)
        for i in range(1, 9): self.panelControl.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        self._configurarPanelControl()
        self._configurarPanelImagen()

    def _configurarPanelControl(self):
        # Configuracion de estilos
        estilosCargaReinicio = "primary"
        estilosControlesBasicos = "success"

        # Titulo del panel de control
        titulo = ttk.Label(self.panelControl, text="Operaciones base", font=("Arial", 18, "bold"), anchor="center")
        titulo.grid(row=0, column=0, sticky="w", **paddingTitulos)

        # Generacion de frame completo para carga y reinicio de imagenes
        self.frame_carga_reinicio= ttk.Labelframe(self.panelControl, text="Opciones de carga y reinicio de imagenes", bootstyle=estilosCargaReinicio)

        for i in [2,4]: self.frame_carga_reinicio.rowconfigure(i, weight=1)
        for i in [3,5]: self.frame_carga_reinicio.rowconfigure(i, weight=0)
        for i in range(2): self.frame_carga_reinicio.columnconfigure(i, weight=1)
        self.frame_carga_reinicio.grid(row=1, column=0, sticky="nsew", **paddingFrames, rowspan=2)

        self.label_carga_reinicio_title = ttk.Label(self.frame_carga_reinicio, text="Carga y Reinicio de Imagenes", font=("Arial", 16, "bold"), anchor="center")
        self.label_carga_reinicio_title_img1 = ttk.Label(self.frame_carga_reinicio, text="Imagen 1", font=("Arial ", 15, "bold"), anchor="center")
        self.button_cargar_img1 = ttk.Button(self.frame_carga_reinicio, text="Cargar Imagen 1", bootstyle=estilosCargaReinicio)
        self.button_reiniciar_img1 = ttk.Button(self.frame_carga_reinicio, text="Reiniciar Imagen 1", bootstyle=estilosCargaReinicio, state=DISABLED)
        self.label_carga_reinicio_title_img2 = ttk.Label(self.frame_carga_reinicio, text="Imagen 2", font=("Arial", 15, "bold"), anchor="center")
        self.button_cargar_img2 = ttk.Button(self.frame_carga_reinicio, text="Cargar Imagen 2", bootstyle=estilosCargaReinicio)
        self.button_reiniciar_img2 = ttk.Button(self.frame_carga_reinicio, text="Reiniciar Imagen 2", bootstyle=estilosCargaReinicio, state=DISABLED)
        self.label_carga_reinicio_title.grid(row=0, column=0, columnspan=2, **paddingTitulos)
        self.label_carga_reinicio_title_img1.grid(row=1, column=0, sticky="nsew", **paddingBotones, columnspan=2)
        self.button_cargar_img1.grid(row=2, column=0, sticky="ew", **paddingBotones)
        self.button_reiniciar_img1.grid(row=2, column=1, sticky="ew", **paddingBotones)
        self.label_carga_reinicio_title_img2.grid(row=3, column=0, sticky="nsew", **paddingBotones, columnspan=2)
        self.button_cargar_img2.grid(row=4, column=0, sticky="ew", **paddingBotones)
        self.button_reiniciar_img2.grid(row=4, column=1, sticky="ew", **paddingBotones)
        
        # Generacion de frame completo para operaciones generales
        self.frame_operaciones_generales = ttk.Labelframe(self.panelControl, text="Operaciones Basicas", bootstyle=estilosControlesBasicos)
        for i in [2,3,4,6,7,8]: self.frame_operaciones_generales.rowconfigure(i, weight=1)
        self.frame_operaciones_generales.columnconfigure(0, weight=1)
        self.frame_operaciones_generales.grid(row=3, column=0, sticky="nsew", **paddingFrames, rowspan=6)

        self.label_operaciones_generales_title = ttk.Label(self.frame_operaciones_generales, text="Operaciones Generales", font=("Arial", 16, "bold"), anchor="center")
        self.label_operaciones_generales_title_img1 = ttk.Label(self.frame_operaciones_generales, text="Imagen 1", font=("Arial", 15, "bold"), anchor="center")
        self.button_convertir_grises_img1 = ttk.Button(self.frame_operaciones_generales, text="Convertir a Escala de Grises", bootstyle=estilosControlesBasicos, state=DISABLED)
        self.button_binarizar_fijo_img1 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con umbral fijo", bootstyle=estilosControlesBasicos, state=DISABLED)
        self.button_binarizar_otsu_img1 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con Otsu", bootstyle=estilosControlesBasicos, state=DISABLED)
        self.label_operaciones_generales_title_img2 = ttk.Label(self.frame_operaciones_generales, text="Imagen 2", font=("Arial", 15, "bold"), anchor="center")
        self.button_convertir_grises_img2 = ttk.Button(self.frame_operaciones_generales, text="Convertir a Escala de Grises", bootstyle=estilosControlesBasicos, state=DISABLED)
        self.button_binarizar_fijo_img2 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con umbral fijo", bootstyle=estilosControlesBasicos, state=DISABLED)
        self.button_binarizar_otsu_img2 = ttk.Button(self.frame_operaciones_generales, text="Binarizar con Otsu", bootstyle=estilosControlesBasicos, state=DISABLED)
        
        self.label_operaciones_generales_title.grid(row=0, column=0, columnspan=2, **paddingTitulos)
        self.label_operaciones_generales_title_img1.grid(row=1, column=0, sticky="nsew", **paddingBotones)
        self.button_convertir_grises_img1.grid(row=2, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_fijo_img1.grid(row=3, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_otsu_img1.grid(row=4, column=0, sticky="ew", **paddingBotones)
        self.label_operaciones_generales_title_img2.grid(row=5, column=0, sticky="nsew", **paddingBotones)
        self.button_convertir_grises_img2.grid(row=6, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_fijo_img2.grid(row=7, column=0, sticky="ew", **paddingBotones)
        self.button_binarizar_otsu_img2.grid(row=8, column=0, sticky="ew", **paddingBotones)
    
    def _configurarPanelImagen(self):
        estiloImagen1 = "info"
        estiloImagen2 = "warning"

        self.frame_imagen1 = ttk.Labelframe(self.panelImagen, text="Visualización de la imagen", padding=10, bootstyle=estiloImagen1)
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
        
        self.frame_imagen2 = ttk.Labelframe(self.panelImagen, text="Visualización de la imagen adicional", padding=10, bootstyle=estiloImagen2)
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

    def mostrar_mensaje(self, mensaje, tipo_mensaje="info"):
        if tipo_mensaje == "info":
            messagebox.showinfo("Información", mensaje)
        elif tipo_mensaje == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo_mensaje == "warning":
            messagebox.showwarning("Advertencia", mensaje)
 
    def pedir_ruta_archivo(self):
        ruta_archivo = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files")])
        if ruta_archivo:
            return ruta_archivo
        else: 
            return None
        
    def _determinar_ubicacion_grid_img(self, noImagen, modalidad= 'principal'):
        ubicacion = None
        no_grid = 0

        if noImagen ==1: ubicacion = self.frame_imagen1
        else: ubicacion = self.frame_imagen2
        
        no_grid = 3 if modalidad == 'principal' else 8
        return ubicacion, no_grid

    def activar_botones_frame_img(self, noImagen):
        if noImagen == 1:
            self.button_reiniciar_img1.config(state="normal")
            self.button_convertir_grises_img1.config(state="normal")
            self.button_binarizar_fijo_img1.config(state="normal")
            self.button_binarizar_otsu_img1.config(state="normal")
        else:
            self.button_reiniciar_img2.config(state="normal")
            self.button_convertir_grises_img2.config(state="normal")
            self.button_binarizar_fijo_img2.config(state="normal")
            self.button_binarizar_otsu_img2.config(state="normal")

    def crear_histograma_rgb(self, imagen_no, histograma,modalidad= 'principal'):
        datos = self._determinar_ubicacion_grid_img(imagen_no, modalidad)
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
        datos = self._determinar_ubicacion_grid_img(imagen_no, 'adicional')
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
                ubicacion, noGrid = self._determinar_ubicacion_grid_img(no_imagen, modalidad="modificada")
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
                ubicacion, noGrid = self._determinar_ubicacion_grid_img(no_imagen, modalidad="modificada")
                for i in range(3):
                    widgets = ubicacion.grid_slaves(row=noGrid+i, column=0)
                    for widget in widgets: widget.destroy()

    def aviso_binarizar_fijo(self):
        valorUmbral = simpledialog.askinteger("Binarización", "Ingrese el valor de umbral (0-255):", minvalue=0, maxvalue=255)
        return valorUmbral
    
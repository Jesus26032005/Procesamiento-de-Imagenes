import ttkbootstrap as ttk  
from ttkbootstrap.constants import *  
from tkinter import filedialog, messagebox, simpledialog, DISABLED
from ttkbootstrap.scrolled import ScrolledFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator

# Configuraciones de padding para consistencia visual
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
        # Panel izquierdo para visualizar imágenes (con scroll si es necesario)
        self.panel_imagen_global = ScrolledFrame(self, padding=10)
        self.panel_imagen_global.grid(row=0, column=0, sticky="nsew", columnspan=7)
        self.panel_imagen_global.columnconfigure(0, weight=1)
        for i in range(2): self.panel_imagen_global.rowconfigure(i, weight=1)

        # Panel derecho con pestañas para los controles 
        self.panel_de_control = ttk.Frame(self, padding=5)
        self.panel_de_control.grid(row=0, column=7, sticky="nsew")
        self.panel_de_control.columnconfigure(0, weight=1)
        self.panel_de_control.rowconfigure(0, weight=1)

        self._configurar_panel_de_control()
        self._configurar_panel_imagen()

    def _configurar_panel_de_control(self):
        estilo_panel_control = "success"
        estilo_panel_control_botones = "success-outline"
        self.tabla_de_control = ttk.Labelframe(self.panel_de_control, padding=5, bootstyle=estilo_panel_control, text="Panel de control")
        self.tabla_de_control.grid(row=0, column=0, sticky="nsew", **paddingFrames)

        self.tabla_de_control.columnconfigure(0, weight=1)
        for i in [0,4]: self.tabla_de_control.rowconfigure(i, weight=0)
        for i in [1,2,3,5,6,7,8,9]: self.tabla_de_control.rowconfigure(i, weight=1)

        # SECCION DE OPERACIONES BASICAS
        self.label_titulo_operaciones_basicas = ttk.Label(self.tabla_de_control, text="Operaciones basicas", font=("Arial", 16, "bold"))
        self.label_titulo_operaciones_basicas.grid(row=0, column=0, sticky="nsew", **paddingTitulos)

        self.boton_cargar_imagen = ttk.Button(self.tabla_de_control, text="Cargar imagen", bootstyle=estilo_panel_control_botones)
        self.boton_reiniciar_imagen = ttk.Button(self.tabla_de_control, text="Reiniciar imagen", bootstyle=estilo_panel_control_botones)
        self.boton_guardar_imagen = ttk.Button(self.tabla_de_control, text="Guardar imagen", bootstyle=estilo_panel_control_botones)

        self.boton_cargar_imagen.grid(row=1, column=0, sticky="nsew", **paddingBotones)
        self.boton_reiniciar_imagen.grid(row=2, column=0, sticky="nsew", **paddingBotones)
        self.boton_guardar_imagen.grid(row=3, column=0, sticky="nsew", **paddingBotones)

        # SECCION DEL ALGORITMO
        self.label_titulo_algoritmo = ttk.Label(self.tabla_de_control, text="Algoritmo", font=("Arial", 16, "bold"))
        self.label_titulo_algoritmo.grid(row=4, column=0, sticky="nsew", **paddingTitulos)

        self.boton_convertir_grises = ttk.Button(self.tabla_de_control, text="Convertir a grises", bootstyle=estilo_panel_control_botones)
        self.boton_morfologia_cierre = ttk.Button(self.tabla_de_control, text="Morfologia Cierre", bootstyle=estilo_panel_control_botones)
        self.boton_morfologia_dilatacion = ttk.Button(self.tabla_de_control, text="Morfologia Dilatacion", bootstyle=estilo_panel_control_botones)
        self.boton_binarizacion_inversa_fija = ttk.Button(self.tabla_de_control, text="Binarizacion Inversa Fija", bootstyle=estilo_panel_control_botones)
        self.boton_sumar_con_imagen_original = ttk.Button(self.tabla_de_control, text="Sumar con imagen original", bootstyle=estilo_panel_control_botones)
        
        self.boton_convertir_grises.grid(row=5, column=0, sticky="nsew", **paddingBotones)
        self.boton_morfologia_cierre.grid(row=6, column=0, sticky="nsew", **paddingBotones)
        self.boton_morfologia_dilatacion.grid(row=7, column=0, sticky="nsew", **paddingBotones)
        self.boton_binarizacion_inversa_fija.grid(row=8, column=0, sticky="nsew", **paddingBotones)
        self.boton_sumar_con_imagen_original.grid(row=9, column=0, sticky="nsew", **paddingBotones)

    def _configurar_panel_imagen(self):
        estiloImagen1 = "primary"

        self.frame_imagen1 = ttk.Labelframe(self.panel_imagen_global, text="Visualización de la imagen", padding=10, bootstyle=estiloImagen1)
        self.frame_imagen1.grid(row=0, column=0, sticky="nsew", **paddingFrames)
        for i in range(8):  self.frame_imagen1.rowconfigure(i, weight=1)
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

    def mostrar_imagen_cargada(self, imagen_tkinter,  histograma, tipo_imagen="original"):
        imagenOriginal = imagen_tkinter[0]
        imagenModificada = imagen_tkinter[1]
        histograma_imagen = histograma
        
        self.label_visualizacion_lab_img1.config(image=imagenOriginal)
        self.label_visualizacion_lab_img1.image = imagenOriginal
        self.label_visualizacion_lab_img1Modified.config(image=imagenModificada)
        self.label_visualizacion_lab_img1Modified.image = imagenModificada
        self.crear_histograma_rgb(histograma_imagen, modalidad="principal")
        self.crear_histograma_rgb(histograma_imagen, modalidad="modificada")

    def crear_histograma_rgb(self, histograma, modalidad= 'principal'):
        datos = self.determinar_ubicacion_grid_img(modalidad)
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
    
    def crear_histograma_gris(self, histograma):
        datos = self.determinar_ubicacion_grid_img('adicional')
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

    def actualizar_imagen(self, imagen_tkinter, histograma, tipo_imagen):
        self.label_visualizacion_lab_img1Modified.config(image=imagen_tkinter)
        self.label_visualizacion_lab_img1Modified.image = imagen_tkinter
        if tipo_imagen == 'rgb':
            self.crear_histograma_rgb(histograma, modalidad="modificada")
        elif tipo_imagen == 'gris':
            self.crear_histograma_gris(histograma)
        elif tipo_imagen == 'binaria' or tipo_imagen == 'final':
            ubicacion, noGrid = self.determinar_ubicacion_grid_img(modalidad="modificada")
            for i in range(3):
                widgets = ubicacion.grid_slaves(row=noGrid+i, column=0)
                for widget in widgets: widget.destroy()

    def determinar_ubicacion_grid_img(self, modalidad= 'principal'):
        """
        Helper para determinar en qué frame y fila colocar los elementos visuales.
        """
        ubicacion = None
        no_grid = 0

        ubicacion = self.frame_imagen1
        no_grid = 3 if modalidad == 'principal' else 8
        return ubicacion, no_grid

    def mostrar_mensaje(self, mensaje, tipo_mensaje="info"):
        if tipo_mensaje == "info":
            messagebox.showinfo("Información", mensaje)
        elif tipo_mensaje == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo_mensaje == "warning":
            messagebox.showwarning("Advertencia", mensaje)

    def pedir_ruta_archivo(self):
        ruta_archivo = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files")])
        if ruta_archivo:
            return ruta_archivo
        else: 
            return None

    def pedir_ruta_archivo_guardar(self):
        ruta_archivo = filedialog.asksaveasfilename(title="Guardar imagen", defaultextension=".jpg", filetypes=[("Image files", "*.jpg *.JPEJ *.png"), ("All files")])
        if ruta_archivo:
            return ruta_archivo
        else: 
            return None
    
    def aviso_binarizar_fijo(self):
        valorUmbral = simpledialog.askinteger("Binarización", "Ingrese el valor de umbral (0-255):", minvalue=0, maxvalue=255)
        return valorUmbral

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog, messagebox, Canvas
from Imagen import Imagen as Img
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2

class Interfaz(ttk.Window):
    def __init__(self):
        self.imagen = None
        self.configuracionesIniciales()
        self.crearLayout()
        self.mainloop()

    def configuracionesIniciales(self):
        super().__init__(themename="solar")
        self.title("Practica 1")
        self.geometry("1600x900")
        self.resizable(False,False)

        for i in range(10): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def crearLayout(self):
        # Panel izquierdo (controles)
        self.panelControl = ttk.Frame(self, padding=10, bootstyle="DARK", width=400)
        self.panelControl.grid(row=0, column=0, sticky="nsew", rowspan=10)
        for i in range(8): self.panelControl.rowconfigure(i, weight=1)
        self.panelControl.columnconfigure(0, weight=1)

        # Titulo
        self.labelTitulo = ttk.Label(self.panelControl, text="Practica 1: Modelos de color", font=("Arial", 16, "bold"))
        self.labelTitulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Panel derecho (visualización)
        self.panelVisualizacion = ScrolledFrame(self, padding=10, bootstyle="DARK", width=1200, height=900)
        self.panelVisualizacion.grid(row=0, column=1, sticky="nsew", rowspan=10)
        self.panelVisualizacion.columnconfigure(0, weight=1)

        # Crear los controles de cargar imagen y mostrar modelos
        self.crearControlesCargarImagen()
        self.crearControlesMostrarModelos()
        self.crearMuestraResultado()

    def crearControlesCargarImagen(self):
        # Crear el marco para cargar imagen
        self.marcoCargarImagen = ttk.Labelframe(self.panelControl, text="Cargar Imagen", padding=10, bootstyle="primary")
        self.marcoCargarImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5, rowspan=1)
        # Configurar el grid del marco
        for i in range(3):
            self.marcoCargarImagen.rowconfigure(i, weight=1)
        self.marcoCargarImagen.columnconfigure(0, weight=1)
        # Crear los controles para cargar imagen
        self.subTituloCargar = ttk.Label(self.marcoCargarImagen, text="Cargar una imagen desde su dispositivo", font=("Arial", 12, "bold"))
        self.indicacionesCargar = ttk.Label(self.marcoCargarImagen, text="Seleccione una imagen para cargarla en la aplicación", font=("Arial", 10))
        self.botonCargar = ttk.Button(self.marcoCargarImagen, text="Cargar Imagen", bootstyle="PRIMARY", command=self.cargarImagen)
        # Ubicar los controles en el marco
        self.subTituloCargar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.indicacionesCargar.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.botonCargar.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    def crearControlesMostrarModelos(self):
        # Crear el marco para mostrar modelos
        self.marcoModelos = ttk.Labelframe(self.panelControl, text="Elegir Modelo a mostrar", padding=10, bootstyle="secondary")
        self.marcoModelos.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Configurar el grid del marco
        for i in range(3): self.marcoModelos.columnconfigure(i, weight=1)
        for i in range(2):self.marcoModelos.rowconfigure(i, weight=1)
        # Crear los controles para mostrar modelos
        self.subTituloModelos = ttk.Label(self.marcoModelos, text="Modelos de color", font=("Arial", 12, "bold"))
        self.indicacionesModelos = ttk.Label(self.marcoModelos, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        self.botonModeloRGB = ttk.Button(self.marcoModelos, text="Modelo RGB", bootstyle="secondary", command=self.cargarModeloRGB)
        self.botonModeloHSV = ttk.Button(self.marcoModelos, text="Modelo HSV", bootstyle="secondary", command=self.cargarModeloHSV)
        self.botonModeloCMY = ttk.Button(self.marcoModelos, text="Modelo CMY", bootstyle="secondary", command=self.cargarModeloCMY)
        # Ubicar los controles en el marco
        self.subTituloModelos.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.indicacionesModelos.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.botonModeloRGB.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.botonModeloHSV.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.botonModeloCMY.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
        pass
    
    def crearMuestraResultado(self):
        self.marcoMapa = ttk.Labelframe(self.panelVisualizacion, text="Visualización de la imagen", padding=10, bootstyle="info")
        self.marcoMapa.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoMapa.rowconfigure(0, weight=1)
        self.marcoMapa.columnconfigure(0, weight=1)
        self.tituloVisualizacion = ttk.Label(self.marcoMapa, text="Visualización de la imagen", font=("Arial", 16, "bold"))
        self.SubImagen = ttk.Label(self.marcoMapa, text="Aquí se mostrará la imagen cargada y sus modelos de color", font=("Arial", 12), anchor="center")
        self.tituloVisualizacion.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.SubImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def cargarImagen(self):
        rutaArchivo= filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files")])
        if rutaArchivo:
            self.imagen = Img(rutaArchivo)
            imagenTkinter = self.imagen.iniciarImagen()
            if imagenTkinter:
                self.SubImagen.configure(image=imagenTkinter)
                self.SubImagen.image = imagenTkinter
            else: del self.imagen
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")

    def mostrarModelo(self, modelo):
        if hasattr(self, 'imagen'):
            imagenModelo = self.imagen.obtenerModelo(modelo)
            if imagenModelo:
                self.SubImagen.configure(image=imagenModelo)
                self.SubImagen.image = imagenModelo
            else:
                messagebox.showerror("Error", "No se pudo obtener el modelo de color seleccionado.")

    def cargarModeloRGB(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        self.marcoRGB = ttk.Labelframe(self.panelVisualizacion, text="Modelo RGB (Matplotlib)", padding=10, bootstyle="primary")
        self.marcoRGB.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoRGB.columnconfigure(0, weight=1); self.marcoRGB.rowconfigure(1, weight=1)
        ttk.Label(self.marcoRGB, text="Modelo RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        R, G, B = cv2.split(self.imagen.imagenCv)
        fig = Figure(figsize=(12, 3.8), dpi=100)
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        ax1.imshow(R, cmap="Reds", vmin=0, vmax=255); ax1.set_title("Canal R"); ax1.axis("off")
        ax2.imshow(G, cmap="Greens", vmin=0, vmax=255); ax2.set_title("Canal G"); ax2.axis("off")
        ax3.imshow(B, cmap="Blues", vmin=0, vmax=255); ax3.set_title("Canal B"); ax3.axis("off")
        canvas = FigureCanvasTkAgg(fig, master=self.marcoRGB)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

    def cargarModeloHSV(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        self.marcoHSV = ttk.Labelframe(self.panelVisualizacion, text="Modelo HSV (Matplotlib)", padding=10, bootstyle="success")
        self.marcoHSV.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoHSV.columnconfigure(0, weight=1)
        self.marcoHSV.rowconfigure(1, weight=1)

        ttk.Label(self.marcoHSV, text="Modelo HSV", font=("Arial", 16, "bold")).grid( row=0, column=0, sticky="w", padx=5, pady=5)

        rgb = self.imagen.imagenCv
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        H, S, V = cv2.split(hsv)
        fig = Figure(figsize=(12, 3.8), dpi=100) 
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        im1 = ax1.imshow(H, cmap="hsv", vmin=0, vmax=179)
        ax1.set_title("Canal H"); ax1.axis("off")
        im2 = ax2.imshow(S, cmap="gray", vmin=0, vmax=255)
        ax2.set_title("Canal S"); ax2.axis("off")
        im3 = ax3.imshow(V, cmap="gray", vmin=0, vmax=255)
        ax3.set_title("Canal V"); ax3.axis("off")

        fig.suptitle("Modelo HSV")
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHSV)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky="nsew")

    def cargarModeloCMY(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        self.marcoCMY = ttk.Labelframe(self.panelVisualizacion, text="Modelo CMY (Matplotlib)", padding=10, bootstyle="warning")
        self.marcoCMY.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoCMY.columnconfigure(0, weight=1); self.marcoCMY.rowconfigure(1, weight=1)
        ttk.Label(self.marcoCMY, text="Modelo CMY", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        R, G, B = cv2.split(self.imagen.imagenCv)
        C = 255 - R; M = 255 - G; Y = 255 - B
        fig = Figure(figsize=(12, 3.8), dpi=100)
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        ax1.imshow(C, cmap="Blues",   vmin=0, vmax=255); ax1.set_title("Canal C"); ax1.axis("off")
        ax2.imshow(M, cmap="Purples", vmin=0, vmax=255); ax2.set_title("Canal M"); ax2.axis("off")
        ax3.imshow(Y, cmap="Oranges", vmin=0, vmax=255); ax3.set_title("Canal Y"); ax3.axis("off")
        fig.suptitle("Modelo CMY")

        canvas = FigureCanvasTkAgg(fig, master=self.marcoCMY)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")


if __name__ == "__main__":
    Interfaz()
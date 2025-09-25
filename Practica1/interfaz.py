import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog, messagebox, Canvas
from Imagen import Imagen as Img

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
        self.marcoRGB = ttk.Labelframe(self.panelVisualizacion, text="Modelo RGB", padding=10, bootstyle="primary")
        self.marcoRGB.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range (3): self.marcoRGB.columnconfigure(i, weight=1)
        for i in range (2): self.marcoRGB.rowconfigure(i, weight=1)

        self.tituloModeloRGB = ttk.Label(self.marcoRGB, text="Modelo RGB", font=("Arial", 16, "bold"))
        self.tituloModeloRGB.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, columnspan=3)

        imgs = self.imagen.obtenerModeloRGB()   # tupla (R,G,B)
        self._imgs_rgb = imgs
        labelTitleRed= ttk.Label(self.marcoRGB, text="Rojo", font=("Arial", 12, "bold"))
        labelTitleGreen= ttk.Label(self.marcoRGB, text="Verde", font=("Arial", 12, "bold"))
        labelTitleBlue= ttk.Label(self.marcoRGB, text="Azul", font=("Arial", 12, "bold"))
        labelTitleRed.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        labelTitleGreen.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        labelTitleBlue.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        labelR = ttk.Label(self.marcoRGB, image=imgs[0]); labelR.image = imgs[0]
        labelG = ttk.Label(self.marcoRGB, image=imgs[1]); labelG.image = imgs[1]
        labelB = ttk.Label(self.marcoRGB, image=imgs[2]); labelB.image = imgs[2]
        labelR.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        labelG.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        labelB.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    def cargarModeloHSV(self):
        self.marcoHSV = ttk.Labelframe(self.panelVisualizacion, text="Modelo HSV", padding=10, bootstyle="success")
        self.marcoHSV.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        for i in range (3): self.marcoHSV.columnconfigure(i, weight=1)
        for i in range (2): self.marcoHSV.rowconfigure(i, weight=1)

        self.tituloModeloHSV = ttk.Label(self.marcoHSV, text="Modelo HSV", font=("Arial", 16, "bold"))
        self.tituloModeloHSV.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, columnspan=3)

        imgs = self.imagen.obtenerModeloHSV()   # tupla (H,S,V)
        self._imgs_hsv = imgs
        labelTitleHue= ttk.Label(self.marcoHSV, text="Hue", font=("Arial", 12, "bold"))
        labelTitleSaturation = ttk.Label(self.marcoHSV, text="Saturation", font=("Arial", 12, "bold"))
        labelTitleValue = ttk.Label(self.marcoHSV, text="Value", font=("Arial", 12, "bold"))
        labelTitleHue.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        labelTitleSaturation.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        labelTitleValue.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        labelH = ttk.Label(self.marcoHSV, image=imgs[0]); labelH.image = imgs[0]
        labelS = ttk.Label(self.marcoHSV, image=imgs[1]); labelS.image = imgs[1]
        labelV = ttk.Label(self.marcoHSV, image=imgs[2]); labelV.image = imgs[2]
        labelH.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        labelS.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        labelV.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    def cargarModeloCMY(self):
        self.marcoCMY = ttk.Labelframe(self.panelVisualizacion, text="Modelo CMY", padding=10, bootstyle="warning")
        self.marcoCMY.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        for i in range (3): self.marcoCMY.columnconfigure(i, weight=1)
        for i in range (2): self.marcoCMY.rowconfigure(i, weight=1)

        self.tituloModeloCMY = ttk.Label(self.marcoCMY, text="Modelo CMY", font=("Arial", 16, "bold"))
        self.tituloModeloCMY.grid(row=0, column=0, sticky="nsew", padx=5, pady=5    , columnspan=3)

        imgs = self.imagen.obtenerModeloCMY()   # tupla (C,M,Y)
        self._imgs_cmy = imgs
        labelTitleCyan= ttk.Label(self.marcoCMY, text="Cyan", font=("Arial", 12, "bold"))
        labelTitleMagenta = ttk.Label(self.marcoCMY, text="Magenta", font=("Arial", 12, "bold"))
        labelTitleYellow = ttk.Label(self.marcoCMY, text="Yellow", font=("Arial", 12, "bold"))
        labelTitleCyan.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        labelTitleMagenta.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        labelTitleYellow.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        labelC = ttk.Label(self.marcoCMY, image=imgs[0]); labelC.image = imgs[0]
        labelM = ttk.Label(self.marcoCMY, image=imgs[1]); labelM.image = imgs[1]
        labelY = ttk.Label(self.marcoCMY, image=imgs[2]); labelY.image = imgs[2]
        labelC.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        labelM.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        labelY.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)


if __name__ == "__main__":
    Interfaz()
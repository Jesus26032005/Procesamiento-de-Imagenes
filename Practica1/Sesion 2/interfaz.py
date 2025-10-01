import ttkbootstrap as ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog, messagebox, simpledialog
from Imagen import Imagen as Img
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
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

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def crearLayout(self):
        self.panelControl = ttk.Frame(self, padding=10, bootstyle="DARK", width=400)
        self.panelControl.grid(row=0, column=0, sticky="nsew", rowspan=10)
        for i in range(4): self.panelControl.rowconfigure(i, weight=1)
        self.panelControl.columnconfigure(0, weight=1)

        self.labelTitulo = ttk.Label(self.panelControl, text="Practica 1: Modelos de color", font=("Arial", 16, "bold"))
        self.labelTitulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.panelVisualizacion = ScrolledFrame(self, padding=10, bootstyle="DARK", width=1200, height=900)
        self.panelVisualizacion.grid(row=0, column=1, sticky="nsew", rowspan=10)
        self.panelVisualizacion.columnconfigure(0, weight=1)

        self.crearMuestraResultado()
        self.crearControlesCargarImagen()
        self.crearControlesMostrarModelos()
        self.crearControlesGrisBinarizacion()
        self.crearControlesHistograma()

    def crearControlesCargarImagen(self):
        estiloCargarImg = "primary"
        self.marcoCargarImagen = ttk.Labelframe(self.panelControl, text="Cargar Imagen", padding=10, bootstyle=estiloCargarImg)
        self.marcoCargarImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5, rowspan=1)
        for i in range(3):
            self.marcoCargarImagen.rowconfigure(i, weight=1)
        self.marcoCargarImagen.columnconfigure(0, weight=1)
        
        self.subTituloCargar = ttk.Label(self.marcoCargarImagen, text="Cargar una imagen desde su dispositivo", font=("Arial", 12, "bold"))
        self.indicacionesCargar = ttk.Label(self.marcoCargarImagen, text="Seleccione una imagen para cargarla en la aplicación", font=("Arial", 10))
        self.botonCargar = ttk.Button(self.marcoCargarImagen, text="Cargar Imagen", bootstyle=estiloCargarImg, command=self.cargarImagen)
        
        self.subTituloCargar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.indicacionesCargar.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.botonCargar.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    def crearControlesMostrarModelos(self):
        estiloModelos = "secondary"
        self.marcoModelos = ttk.Labelframe(self.panelControl, text="Elegir Modelo a mostrar", padding=10, bootstyle=estiloModelos)
        self.marcoModelos.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(3): self.marcoModelos.columnconfigure(i, weight=1)
        for i in range(3):self.marcoModelos.rowconfigure(i, weight=1)
        
        self.subTituloModelos = ttk.Label(self.marcoModelos, text="Modelos de color", font=("Arial", 12, "bold"))
        self.indicacionesModelos = ttk.Label(self.marcoModelos, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        self.botonModeloRGB = ttk.Button(self.marcoModelos, text="Modelo RGB", bootstyle=estiloModelos, command=self.cargarModeloRGB)
        self.botonModeloHSV = ttk.Button(self.marcoModelos, text="Modelo HSV", bootstyle=estiloModelos, command=self.cargarModeloHSV)
        self.botonModeloCMY = ttk.Button(self.marcoModelos, text="Modelo CMY", bootstyle=estiloModelos, command=self.cargarModeloCMY)

        self.subTituloModelos.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.indicacionesModelos.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.botonModeloRGB.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.botonModeloHSV.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.botonModeloCMY.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
    
    def crearControlesGrisBinarizacion(self):
        estiloConversiones = "success"
        self.marcoConversiones = ttk.Labelframe(self.panelControl, text="Elegir cambio a mostrar", padding=10, bootstyle=estiloConversiones)
        self.marcoConversiones.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(2): self.marcoConversiones.columnconfigure(i, weight=1)
        for i in range(4):self.marcoConversiones.rowconfigure(i, weight=1)

        self.subTituloConversiones = ttk.Label(self.marcoConversiones, text="Conversion de gris-binario", font=("Arial", 12, "bold"))
        self.indicacionesConversiones = ttk.Label(self.marcoConversiones, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        
        self.botonModeloGris = ttk.Button(self.marcoConversiones, text="Convertir a escala de gris", bootstyle=estiloConversiones, command=self.convertirEscalaGris)
        self.botonUmbralFijo = ttk.Button(self.marcoConversiones, text="Binarizar imagen por fijo", bootstyle=estiloConversiones, command=self.binarizarImagenFijo)
        self.botonUmbralAdaptativo = ttk.Button(self.marcoConversiones, text="Binarizar imagen por adaptativo", bootstyle=estiloConversiones, state=DISABLED)

        self.subTituloConversiones.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.indicacionesConversiones.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.botonModeloGris.grid(row=2, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)
        self.botonUmbralFijo.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.botonUmbralAdaptativo.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

    def crearControlesHistograma(self):
        estiloHistograma = "danger"
        self.marcoHistogramas = ttk.Labelframe(self.panelControl, text="Elegir histograma a mostrar", padding=10, bootstyle=estiloHistograma)
        self.marcoHistogramas.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(2): self.marcoHistogramas.columnconfigure(i, weight=1)
        for i in range(3):self.marcoHistogramas.rowconfigure(i, weight=1)

        self.subTituloHistogramas = ttk.Label(self.marcoHistogramas, text="Histogramas", font=("Arial", 12, "bold"))
        self.indicacionesHistogramas = ttk.Label(self.marcoHistogramas, text="Seleccione un histograma para visualizarlo", font=("Arial", 10))
        self.botonHistogramaColor = ttk.Button(self.marcoHistogramas, text="Histograma de color", bootstyle=estiloHistograma, command=self.crearHistogramaRGB)
        self.botonHistogramaGris = ttk.Button(self.marcoHistogramas, text="Histograma de gris", bootstyle=estiloHistograma, command=self.crearHistogramaGris)

        self.subTituloHistogramas.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.indicacionesHistogramas.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.botonHistogramaColor.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.botonHistogramaGris.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

    # FUNCIONES DE CHAMBA
    def crearMuestraResultado(self):
        self.marcoMapa = ttk.Labelframe(self.panelVisualizacion, text="Visualización de la imagen", padding=10, bootstyle="info")
        self.marcoMapa.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoMapa.rowconfigure(0, weight=1)
        self.marcoMapa.rowconfigure(1, weight=1)
        self.marcoMapa.columnconfigure(0, weight=1)
        self.tituloVisualizacion = ttk.Label(self.marcoMapa, text="Visualización de la imagen", font=("Arial", 16, "bold"))
        self.SubImagen = ttk.Label(self.marcoMapa, text="Aquí se mostrará la imagen cargada y sus modelos de color", font=("Arial", 12), anchor="center")
        self.tituloVisualizacion.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.SubImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def convertirEscalaGris(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        
        self.marcoGris = ttk.Labelframe(self.panelVisualizacion, text="Imagen en escala de gris", padding=10, bootstyle="success")
        self.marcoGris.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoGris.columnconfigure(0, weight=1)
        self.marcoGris.rowconfigure(0, weight=1)
        self.subImagenGris = ttk.Label(self.marcoGris, text="Imagen en escala de grises", font=("Arial", 16, "bold"))
        self.subImagenGris.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        imagenGrisPillow = self.imagen.obtenerImagenGris()
        if imagenGrisPillow:
            self.subImagenGris.configure(image=imagenGrisPillow, anchor="center")
            self.subImagenGris.image = imagenGrisPillow
        else:
            messagebox.showerror("Error", "No se pudo convertir la imagen a escala de grises.")

    def binarizarImagenFijo(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        elif not hasattr(self, 'marcoGris'):
            messagebox.showwarning("Atención", "Primero convierte la imagen a escala de grises.")
            return
        elif not hasattr(self, 'marcoHistogramaGrises'):
            messagebox.showwarning("Atención", "Requieres tener el histograma de grises para usar un umbral fijo.")

        valorUmbralFijo = simpledialog.askinteger("Umbral Fijo", "Introduce el valor del umbral (0-255):", minvalue=0, maxvalue=255)
        if valorUmbralFijo is not None:
            imagenBinarizada= self.imagen.umbralizarFijoImagen(valorUmbralFijo)
            self.marcoBinarizadaFijo = ttk.Labelframe(self.panelVisualizacion, text="Imagen binarizada (Umbral Fijo)", padding=10, bootstyle="success")
            self.marcoBinarizadaFijo.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
            self.marcoBinarizadaFijo.columnconfigure(0, weight=1)
            self.marcoBinarizadaFijo.rowconfigure(0, weight=1)
            self.subImagenBinarizadaFijo = ttk.Label(self.marcoBinarizadaFijo, text="Imagen binarizada (Umbral Fijo)", font=("Arial", 16, "bold"))
            self.subImagenBinarizadaFijo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            if imagenBinarizada:
                self.subImagenBinarizadaFijo.configure(image=imagenBinarizada, anchor="center")
                self.subImagenBinarizadaFijo.image = imagenBinarizada
            else:
                messagebox.showerror("Error", "No se pudo convertir la imagen a escala de grises.")

    def binarizarImagenAdaptativo(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        elif not hasattr(self, 'marcoGris'):
            messagebox.showwarning("Atención", "Primero convierte la imagen a escala de grises.")
            return
        elif not hasattr(self, 'marcoHistogramaGrises'):
            messagebox.showwarning("Atención", "Requieres tener el histograma de grises para usar un umbral fijo.")
        valorConstante = simpledialog.askinteger("Constante", "Introduce el valor de la constante (recomendado 0-10, maximo 20):", minvalue=0, maxvalue=20)
        if valorConstante is not None:
            pass

    def cargarImagen(self):
        rutaArchivo= filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files")])
        if rutaArchivo:
            if self.imagen:
                if hasattr(self, 'marcoGris') and self.marcoGris.winfo_exists():
                    self.marcoGris.destroy()
                if hasattr(self, 'marcoRGB') and self.marcoRGB.winfo_exists():
                    self.marcoRGB.destroy()
                if hasattr(self, 'marcoHSV') and self.marcoHSV.winfo_exists():
                    self.marcoHSV.destroy()
                if hasattr(self, 'marcoCMY') and self.marcoCMY.winfo_exists():
                    self.marcoCMY.destroy()
                if hasattr(self, 'marcoHistogramaGrises') and self.marcoHistogramaGrises.winfo_exists():
                    self.marcoHistogramaGrises.destroy()
                if hasattr(self, 'marcoHistograma') and self.marcoHistograma.winfo_exists():
                    self.marcoHistograma.destroy()
                if hasattr(self, 'marcoBinarizadaFijo') and self.marcoBinarizadaFijo.winfo_exists():
                    self.marcoBinarizadaFijo.destroy()
                self.panelVisualizacion.yview_moveto(0)

            self.imagen = Img(rutaArchivo)
            imagenTkinter = self.imagen.iniciarImagen()
            if imagenTkinter:
                self.SubImagen.configure(image=imagenTkinter)
                self.SubImagen.image = imagenTkinter
            else: del self.imagen
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")

    def cargarModeloRGB(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        self.marcoRGB = ttk.Labelframe(self.panelVisualizacion, text="Modelo RGB (Matplotlib)", padding=10, bootstyle="primary")
        self.marcoRGB.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoRGB.columnconfigure(0, weight=1); self.marcoRGB.rowconfigure(1, weight=1)
        ttk.Label(self.marcoRGB, text="Modelo RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        R, G, B = cv2.split(self.imagen.imagenCv)
        fig = Figure(figsize=(16, 3.7), dpi=100)
        ax1 = fig.add_subplot(1, 3, 1)
        ax2 = fig.add_subplot(1, 3, 2)
        ax3 = fig.add_subplot(1, 3, 3)
        ax1.imshow(R, cmap="Reds", vmin=0, vmax=255); ax1.set_title("Canal R"); ax1.axis("off")
        ax2.imshow(G, cmap="Greens", vmin=0, vmax=255); ax2.set_title("Canal G"); ax2.axis("off")
        ax3.imshow(B, cmap="Blues", vmin=0, vmax=255); ax3.set_title("Canal B"); ax3.axis("off")
        fig.suptitle("Modelo RGB")
        canvas = FigureCanvasTkAgg(fig, master=self.marcoRGB)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

    def cargarModeloHSV(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        self.marcoHSV = ttk.Labelframe(self.panelVisualizacion, text="Modelo HSV (Matplotlib)", padding=10, bootstyle="success")
        self.marcoHSV.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoHSV.columnconfigure(0, weight=1)
        self.marcoHSV.rowconfigure(1, weight=1)

        ttk.Label(self.marcoHSV, text="Modelo HSV", font=("Arial", 16, "bold")).grid( row=0, column=0, sticky="w", padx=5, pady=5)

        rgb = self.imagen.imagenCv
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        H, S, V = cv2.split(hsv)
        fig = Figure(figsize=(12, 3.7), dpi=100)
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
        self.marcoCMY.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoCMY.columnconfigure(0, weight=1); self.marcoCMY.rowconfigure(1, weight=1)
        ttk.Label(self.marcoCMY, text="Modelo CMY", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        R, G, B = cv2.split(self.imagen.imagenCv)
        C = 255 - R; M = 255 - G; Y = 255 - B
        fig = Figure(figsize=(12, 3.7), dpi=100)
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

    def crearHistogramaRGB(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        self.marcoHistograma = ttk.Labelframe(self.panelVisualizacion, text="Histograma RGB (Matplotlib)", padding=10, bootstyle="info")
        self.marcoHistograma.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoHistograma.columnconfigure(0, weight=1); self.marcoHistograma.rowconfigure(1, weight=1)
        ttk.Label(self.marcoHistograma, text="Histograma RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)


        fig = Figure(figsize=(16,10), dpi=100)
        fig.subplots_adjust(hspace=0.4)
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        histogramaRojo, histogramaVerde, histogramaAzul = self.imagen.histogramaColor()
        ax1.bar(histogramaRojo[0], histogramaRojo[1], color='red', alpha=0.7, width=1)
        ax1.set_ylabel("Número de píxeles (Frecuencia)")
        ax1.set_xlabel("Intensidad de rojo")
        ax2.bar(histogramaVerde[0], histogramaVerde[1], color='green', alpha=0.7, width=1)
        ax2.set_ylabel("Número de píxeles (Frecuencia)")
        ax2.set_xlabel("Intensidad de verde")
        ax3.bar(histogramaAzul[0], histogramaAzul[1], color='blue', alpha=0.7, width=1)
        ax3.set_ylabel("Número de píxeles (Frecuencia)")
        ax3.set_xlabel("Intensidad de azul")
        ax1.set_title("Histograma del canal R");
        ax2.set_title("Histograma del canal G");
        ax3.set_title("Histograma del canal B");
        ax1.yaxis.set_major_locator(MultipleLocator(4000))
        ax1.yaxis.grid(True, linestyle="--", alpha=0.7)
        ax2.yaxis.set_major_locator(MultipleLocator(4000))
        ax2.yaxis.grid(True, linestyle="--", alpha=0.7)
        ax3.yaxis.set_major_locator(MultipleLocator(4000))
        ax3.yaxis.grid(True, linestyle="--", alpha=0.7)
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHistograma)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        listaValoresRGB= self.imagen.calcularPropiedadesImagenRGB()
        for i in range(3):
            if i == 0:
                canal = "Rojo"
            if i == 1:
                canal = "Verde"
            if i == 2:
                canal = "Azul"
            texto = f"Canal {canal}: Media={listaValoresRGB[i][0]:.2f}, entropia={listaValoresRGB[i][1]:.2f}, Varianza={listaValoresRGB[i][2]}, asimetria={listaValoresRGB[i][3]:.2f}, energia={listaValoresRGB[i][4]:.2f}"
            ttk.Label(self.marcoHistograma, text= texto, font=("Arial", 10)).grid(row=2+i, column=0, sticky="w", padx=5, pady=2)

    def crearHistogramaGris(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        if not hasattr(self, 'marcoGris') or not self.marcoGris.winfo_exists():
            messagebox.showwarning("Atención", "Primero convierte la imagen a escala de grises.")
            return
        self.marcoHistogramaGrises = ttk.Labelframe(self.panelVisualizacion, text="Histograma de escala de gris (Matplotlib)", padding=10, bootstyle="info")
        self.marcoHistogramaGrises.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoHistogramaGrises.columnconfigure(0, weight=1); self.marcoHistogramaGrises.rowconfigure(1, weight=1)
        ttk.Label(self.marcoHistogramaGrises, text="Histograma de escala de gris", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        fig = Figure(figsize=(16, 6), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        histogramaGris = self.imagen.histogramaGris()
        ax.bar(histogramaGris[0], histogramaGris[1], color='gray', alpha=0.7, width=1)
        ax.set_xlabel("Intensidad de gris")
        ax.set_ylabel("Número de píxeles (Frecuencia)")
        ax.set_title("Histograma de escala de grises");
        ax.yaxis.set_major_locator(MultipleLocator(2000))
        ax.yaxis.grid(True, linestyle="--", alpha=0.7)
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHistogramaGrises)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        listaValoresGris = self.imagen.calcularPropiedadesImagenGris()
        texto = f"Canal Gris: Media={listaValoresGris[0]:.2f}, entropia={listaValoresGris[1]:.2f}, Varianza={listaValoresGris[2]}, asimetria={listaValoresGris[3]:.2f}, energia={listaValoresGris[4]:.2f}"
        ttk.Label(self.marcoHistogramaGrises, text= texto, font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=2)


if __name__ == "__main__":
    Interfaz()
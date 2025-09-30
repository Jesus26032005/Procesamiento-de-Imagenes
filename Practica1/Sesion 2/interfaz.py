"""
===============================================================================
                            DERECHOS DE AUTOR
===============================================================================
© 2025 - Práctica 1: Modelos de Color
Autor: Zaddkiel de Jesus Martinez Alor,Herrera Monroy Abraham Andre, Marcelino Lopez Jessica
Materia: Procesamiento De Imagenes
Semestre: Cuarto Semestre
Institución: Escuela Superior de Cómputo, Instituto Politécnico Nacional

Descripción: 
Aplicación de interfaz gráfica para visualización y análisis de diferentes 
modelos de color (RGB, HSV, CMY) usando ttkbootstrap, OpenCV y matplotlib.

Este código es de uso académico y está protegido por derechos de autor.
Prohibida su reproducción parcial o total sin autorización del autor.

Fecha de creación: Septiembre 2025
Versión: 1.0
===============================================================================
"""

# Importación de ttkbootstrap para crear interfaces gráficas modernas con temas
import ttkbootstrap as ttk
# Importación duplicada (error) - se puede eliminar esta línea
import ttkbootstrap as ttk
# Importación de constantes de ttkbootstrap (como DISABLED, etc.)
from ttkbootstrap.constants import *
# Importación de ScrolledFrame para crear paneles con scroll
from ttkbootstrap.scrolled import ScrolledFrame
# Importación de filedialog para abrir archivos y messagebox para mostrar mensajes
from tkinter import filedialog, messagebox
# Importación de la clase Imagen personalizada con alias Img
from Imagen import Imagen as Img
# Importación de Figure de matplotlib para crear gráficas
from matplotlib.figure import Figure
# Importación del backend de tkinter para matplotlib (para mostrar gráficas en la interfaz)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Importación de OpenCV para procesamiento de imágenes
import cv2

# Definición de la clase Interfaz que hereda de ttk.Window (ventana principal)
class Interfaz(ttk.Window):
    # Constructor de la clase que inicializa todos los componentes
    def __init__(self):
        # Atributo para almacenar el objeto imagen cargada
        self.imagen = None
        # Llama al método para configurar las propiedades iniciales de la ventana
        self.configuracionesIniciales()
        # Llama al método para crear todos los elementos de la interfaz
        self.crearLayout()
        # Inicia el bucle principal de la aplicación (mantiene la ventana abierta)
        self.mainloop()

    # CONFIGURACIONES INICIALES DE LA VENTANA
    def configuracionesIniciales(self):
        # Llama al constructor de la clase padre (ttk.Window) con el tema "solar"
        super().__init__(themename="solar")
        # Establece el título de la ventana
        self.title("Practica 1")
        # Define el tamaño de la ventana (ancho x alto en píxeles)
        self.geometry("1600x900")
        # Hace que la ventana no sea redimensionable (ancho, alto)
        self.resizable(False,False)

        # Configura 10 filas de la grilla principal con peso 1 (se expanden uniformemente)
        for i in range(10): self.rowconfigure(i, weight=1)
        # Configura la columna 0 (panel de control) sin expansión (weight=0)
        self.columnconfigure(0, weight=0)
        # Configura la columna 1 (panel de visualización) para que se expanda (weight=1)
        self.columnconfigure(1, weight=1)

    # CREACION DEL LAYOUT Y SUS CONTROLES
    def crearLayout(self):
        # Crea el panel de control izquierdo con estilo oscuro y ancho fijo de 400px
        self.panelControl = ttk.Frame(self, padding=10, bootstyle="DARK", width=400)
        # Coloca el panel de control en la grilla (fila 0, columna 0, ocupa 10 filas)
        self.panelControl.grid(row=0, column=0, sticky="nsew", rowspan=10)
        # Configura 8 filas del panel de control para que se expandan uniformemente
        for i in range(8): self.panelControl.rowconfigure(i, weight=1)
        # Configura la única columna del panel de control para que se expanda
        self.panelControl.columnconfigure(0, weight=1)

        # Crea la etiqueta del título principal con fuente Arial 16 en negrita
        self.labelTitulo = ttk.Label(self.panelControl, text="Practica 1: Modelos de color", font=("Arial", 16, "bold"))
        # Coloca el título en la primera fila del panel de control
        self.labelTitulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Crea el panel de visualización derecho con scroll, estilo oscuro y tamaño 1200x900
        self.panelVisualizacion = ScrolledFrame(self, padding=10, bootstyle="DARK", width=1200, height=900)
        # Coloca el panel de visualización en la grilla (fila 0, columna 1, ocupa 10 filas)
        self.panelVisualizacion.grid(row=0, column=1, sticky="nsew", rowspan=10)
        # Configura la columna del panel de visualización para que se expanda
        self.panelVisualizacion.columnconfigure(0, weight=1)

        # Llama a los métodos para crear cada sección de la interfaz
        self.crearMuestraResultado()        # Crea la sección de visualización inicial
        self.crearControlesCargarImagen()   # Crea los controles para cargar imágenes
        self.crearControlesMostrarModelos() # Crea los controles para mostrar modelos de color
        self.crearControlesGrisBinarizacion() # Crea los controles para escala de grises y binarización
        self.crearControlesHistograma()     # Crea los controles para mostrar histogramas

    # Método para crear la sección de controles para cargar imágenes
    def crearControlesCargarImagen(self):
        # Define el estilo visual "primary" (generalmente azul) para esta sección
        estiloCargarImg = "primary"
        # Crea un marco con etiqueta (Labelframe) para agrupar los controles de carga
        self.marcoCargarImagen = ttk.Labelframe(self.panelControl, text="Cargar Imagen", padding=10, bootstyle=estiloCargarImg)
        # Coloca el marco en la fila 1 del panel de control
        self.marcoCargarImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5, rowspan=1)
        # Configura 3 filas dentro del marco para que se expandan uniformemente
        for i in range(3):
            self.marcoCargarImagen.rowconfigure(i, weight=1)
        # Configura la columna del marco para que se expanda
        self.marcoCargarImagen.columnconfigure(0, weight=1)
        
        # Crea etiqueta con subtítulo para la sección (fuente Arial 12 en negrita)
        self.subTituloCargar = ttk.Label(self.marcoCargarImagen, text="Cargar una imagen desde su dispositivo", font=("Arial", 12, "bold"))
        # Crea etiqueta con indicaciones para el usuario (fuente Arial 10)
        self.indicacionesCargar = ttk.Label(self.marcoCargarImagen, text="Seleccione una imagen para cargarla en la aplicación", font=("Arial", 10))
        # Crea botón para cargar imagen que ejecuta el método cargarImagen al hacer clic
        self.botonCargar = ttk.Button(self.marcoCargarImagen, text="Cargar Imagen", bootstyle=estiloCargarImg, command=self.cargarImagen)
        
        # Coloca el subtítulo en la fila 0 del marco
        self.subTituloCargar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Coloca las indicaciones en la fila 1 del marco
        self.indicacionesCargar.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        # Coloca el botón en la fila 2 del marco
        self.botonCargar.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    # Método para crear la sección de controles para mostrar modelos de color
    def crearControlesMostrarModelos(self):
        # Define el estilo visual "secondary" (generalmente gris) para esta sección
        estiloModelos = "secondary"
        # Crea un marco con etiqueta para agrupar los controles de modelos de color
        self.marcoModelos = ttk.Labelframe(self.panelControl, text="Elegir Modelo a mostrar", padding=10, bootstyle=estiloModelos)
        # Coloca el marco en la fila 2 del panel de control
        self.marcoModelos.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Configura 3 columnas dentro del marco para que se expandan uniformemente (para 3 botones)
        for i in range(3): self.marcoModelos.columnconfigure(i, weight=1)
        # Configura 3 filas dentro del marco para que se expandan uniformemente
        for i in range(3):self.marcoModelos.rowconfigure(i, weight=1)
        
        # Crea etiqueta con subtítulo para la sección (fuente Arial 12 en negrita)
        self.subTituloModelos = ttk.Label(self.marcoModelos, text="Modelos de color", font=("Arial", 12, "bold"))
        # Crea etiqueta con indicaciones para el usuario (fuente Arial 10)
        self.indicacionesModelos = ttk.Label(self.marcoModelos, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        # Crea botón para mostrar modelo RGB que ejecuta cargarModeloRGB al hacer clic
        self.botonModeloRGB = ttk.Button(self.marcoModelos, text="Modelo RGB", bootstyle=estiloModelos, command=self.cargarModeloRGB)
        # Crea botón para mostrar modelo HSV que ejecuta cargarModeloHSV al hacer clic
        self.botonModeloHSV = ttk.Button(self.marcoModelos, text="Modelo HSV", bootstyle=estiloModelos, command=self.cargarModeloHSV)
        # Crea botón para mostrar modelo CMY que ejecuta cargarModeloCMY al hacer clic
        self.botonModeloCMY = ttk.Button(self.marcoModelos, text="Modelo CMY", bootstyle=estiloModelos, command=self.cargarModeloCMY)

        # Coloca el subtítulo en la fila 0, ocupando las 3 columnas
        self.subTituloModelos.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca las indicaciones en la fila 1, ocupando las 3 columnas
        self.indicacionesModelos.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca el botón RGB en la fila 2, columna 0
        self.botonModeloRGB.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Coloca el botón HSV en la fila 2, columna 1
        self.botonModeloHSV.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        # Coloca el botón CMY en la fila 2, columna 2
        self.botonModeloCMY.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
    
    # Método para crear la sección de controles para conversiones de gris y binarización
    def crearControlesGrisBinarizacion(self):
        # Define el estilo visual "success" (generalmente verde) para esta sección
        estiloConversiones = "success"
        # Crea un marco con etiqueta para agrupar los controles de conversiones
        self.marcoConversiones = ttk.Labelframe(self.panelControl, text="Elegir cambio a mostrar", padding=10, bootstyle=estiloConversiones)
        # Coloca el marco en la fila 3 del panel de control
        self.marcoConversiones.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        # Configura 2 columnas dentro del marco para que se expandan uniformemente (para 2 botones)
        for i in range(2): self.marcoConversiones.columnconfigure(i, weight=1)
        # Configura 3 filas dentro del marco para que se expandan uniformemente
        for i in range(3):self.marcoConversiones.rowconfigure(i, weight=1)

        # Crea etiqueta con subtítulo para la sección (fuente Arial 12 en negrita)
        self.subTituloConversiones = ttk.Label(self.marcoConversiones, text="Conversion de gris-binario", font=("Arial", 12, "bold"))
        # Crea etiqueta con indicaciones para el usuario (fuente Arial 10)
        self.indicacionesConversiones = ttk.Label(self.marcoConversiones, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        # Crea botón para convertir a escala de grises que ejecuta convertirEscalaGris al hacer clic
        self.botonModeloGris = ttk.Button(self.marcoConversiones, text="Convertir a escala de gris", bootstyle=estiloConversiones, command=self.convertirEscalaGris)
        # Crea botón para binarizar imagen (inicialmente deshabilitado) que ejecuta binarizarImagen al hacer clic
        self.binarizar = ttk.Button(self.marcoConversiones, text="Binarizar imagen", bootstyle=estiloConversiones, command=self.binarizarImagen, state=DISABLED)

        # Coloca el subtítulo en la fila 0, ocupando las 3 columnas
        self.subTituloConversiones.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca las indicaciones en la fila 1, ocupando las 3 columnas
        self.indicacionesConversiones.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca el botón de escala de grises en la fila 2, columna 0
        self.botonModeloGris.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Coloca el botón de binarización en la fila 2, columna 1
        self.binarizar.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

    # Método para crear la sección de controles para mostrar histogramas
    def crearControlesHistograma(self):
        # Define el estilo visual "danger" (generalmente rojo) para esta sección
        estiloHistograma = "danger"
        # Crea un marco con etiqueta para agrupar los controles de histogramas
        self.marcoHistogramas = ttk.Labelframe(self.panelControl, text="Elegir histograma a mostrar", padding=10, bootstyle=estiloHistograma)
        # Coloca el marco en la fila 4 del panel de control
        self.marcoHistogramas.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        # Configura 2 columnas dentro del marco para que se expandan uniformemente (para 2 botones)
        for i in range(2): self.marcoHistogramas.columnconfigure(i, weight=1)
        # Configura 3 filas dentro del marco para que se expandan uniformemente
        for i in range(3):self.marcoHistogramas.rowconfigure(i, weight=1)

        # Crea etiqueta con subtítulo para la sección (fuente Arial 12 en negrita)
        self.subTituloHistogramas = ttk.Label(self.marcoHistogramas, text="Histogramas", font=("Arial", 12, "bold"))
        # Crea etiqueta con indicaciones para el usuario (fuente Arial 10)
        self.indicacionesHistogramas = ttk.Label(self.marcoHistogramas, text="Seleccione un histograma para visualizarlo", font=("Arial", 10))
        # Crea botón para mostrar histograma de color que ejecuta crearHistogramaRGB al hacer clic
        self.botonHistogramaColor = ttk.Button(self.marcoHistogramas, text="Histograma de color", bootstyle=estiloHistograma, command=self.crearHistogramaRGB)
        # Crea botón para mostrar histograma de grises que ejecuta crearHistogramaGris al hacer clic
        self.botonHistogramaGris = ttk.Button(self.marcoHistogramas, text="Histograma de gris", bootstyle=estiloHistograma, command=self.crearHistogramaGris)

        # Coloca el subtítulo en la fila 0, ocupando las 3 columnas
        self.subTituloHistogramas.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca las indicaciones en la fila 1, ocupando las 3 columnas
        self.indicacionesHistogramas.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca el botón de histograma de color en la fila 2, columna 0
        self.botonHistogramaColor.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Coloca el botón de histograma de grises en la fila 2, columna 1
        self.botonHistogramaGris.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

    # FUNCION PARA LABEL INICIAL DE PANEL DE VISUALIZACION
    def crearMuestraResultado(self):
        # Crea un marco con etiqueta para mostrar la imagen principal (estilo "info" - azul claro)
        self.marcoMapa = ttk.Labelframe(self.panelVisualizacion, text="Visualización de la imagen", padding=10, bootstyle="info")
        # Coloca el marco en la primera fila del panel de visualización
        self.marcoMapa.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Configura la fila 0 del marco para que se expanda (para el título)
        self.marcoMapa.rowconfigure(0, weight=1)
        # Configura la fila 1 del marco para que se expanda (para la imagen/mensaje)
        self.marcoMapa.rowconfigure(1, weight=1)
        # Configura la columna del marco para que se expanda
        self.marcoMapa.columnconfigure(0, weight=1)
        # Crea etiqueta con el título de la sección de visualización (fuente Arial 16 en negrita)
        self.tituloVisualizacion = ttk.Label(self.marcoMapa, text="Visualización de la imagen", font=("Arial", 16, "bold"))
        # Crea etiqueta que mostrará la imagen cargada o mensaje informativo (centrado)
        self.SubImagen = ttk.Label(self.marcoMapa, text="Aquí se mostrará la imagen cargada y sus modelos de color", font=("Arial", 12), anchor="center")
        # Coloca el título en la fila 0 del marco
        self.tituloVisualizacion.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Coloca la etiqueta de imagen en la fila 1 del marco
        self.SubImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    # FUNCION PARA CONVERTIR A ESCALA DE GRIS O BINARY
    def convertirEscalaGris(self):
        # Verifica si hay una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        
        # Crea un marco para mostrar la imagen en escala de grises con estilo "success" (verde)
        self.marcoGris = ttk.Labelframe(self.panelVisualizacion, text="Imagen en escala de gris", padding=10, bootstyle="success")
        # Coloca el marco en la fila 2 del panel de visualización
        self.marcoGris.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Configura la columna del marco para que se expanda
        self.marcoGris.columnconfigure(0, weight=1)
        # Configura la fila del marco para que se expanda
        self.marcoGris.rowconfigure(0, weight=1)
        # Crea etiqueta que mostrará la imagen en escala de grises (fuente Arial 16 en negrita)
        self.subImagenGris = ttk.Label(self.marcoGris, text="Imagen en escala de grises", font=("Arial", 16, "bold"))
        # Coloca la etiqueta en el marco
        self.subImagenGris.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Llama al método del objeto imagen para obtener la versión en escala de grises
        imagenGrisPillow = self.imagen.obtenerImagenGris()
        # Si la conversión fue exitosa
        if imagenGrisPillow:
            # Configura la etiqueta para mostrar la imagen en escala de grises (centrada)
            self.subImagenGris.configure(image=imagenGrisPillow, anchor="center")
            # Mantiene una referencia a la imagen para evitar que sea recolectada por el garbage collector
            self.subImagenGris.image = imagenGrisPillow
        # Si hubo error en la conversión
        else:
            messagebox.showerror("Error", "No se pudo convertir la imagen a escala de grises.")

    # Método para binarizar imagen (aún no implementado)
    def binarizarImagen(self):
        # Función vacía - implementación pendiente
        pass
    
    # FUNCION DE CARGAR IMAGEN
    def cargarImagen(self):
        # Abre diálogo para seleccionar archivo de imagen (jpg, jpeg, png)
        rutaArchivo= filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files")])
        # Verifica si se seleccionó un archivo
        if rutaArchivo:
            # Si ya hay una imagen cargada, limpia los elementos anteriores
            if self.imagen:
                # Verifica si existe el marco de imagen en escala de grises y lo elimina
                if hasattr(self, 'marcoGris') and self.marcoGris.winfo_exists():
                    self.marcoGris.destroy()
                # Verifica si existe el marco del modelo RGB y lo elimina
                if hasattr(self, 'marcoRGB') and self.marcoRGB.winfo_exists():
                    self.marcoRGB.destroy()
                # Verifica si existe el marco del modelo HSV y lo elimina
                if hasattr(self, 'marcoHSV') and self.marcoHSV.winfo_exists():
                    self.marcoHSV.destroy()
                # Verifica si existe el marco del modelo CMY y lo elimina
                if hasattr(self, 'marcoCMY') and self.marcoCMY.winfo_exists():
                    self.marcoCMY.destroy()
                # Verifica si existe el marco del histograma de grises y lo elimina
                if hasattr(self, 'marcoHistogramaGrises') and self.marcoHistogramaGrises.winfo_exists():
                    self.marcoHistogramaGrises.destroy()
                # Verifica si existe el marco del histograma de color y lo elimina
                if hasattr(self, 'marcoHistograma') and self.marcoHistograma.winfo_exists():
                    self.marcoHistograma.destroy()
                # Mueve el scroll del panel de visualización al inicio (parte superior)
                self.panelVisualizacion.yview_moveto(0)

            # Crea un nuevo objeto Imagen con la ruta del archivo seleccionado
            self.imagen = Img(rutaArchivo)
            # Intenta cargar y procesar la imagen
            imagenTkinter = self.imagen.iniciarImagen()
            # Si la imagen se cargó exitosamente
            if imagenTkinter:
                # Configura la etiqueta para mostrar la imagen cargada
                self.SubImagen.configure(image=imagenTkinter)
                # Mantiene una referencia a la imagen para evitar que sea recolectada por el garbage collector
                self.SubImagen.image = imagenTkinter
            # Si hubo error al cargar la imagen, elimina el objeto imagen
            else: del self.imagen
        # Si no se seleccionó ningún archivo, muestra advertencia
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")

    # FUNCIONES PARA CARGAR LOS MODELOS DE COLOR
    def cargarModeloRGB(self):
        # Verifica si hay una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Crea un marco para mostrar el modelo RGB con estilo "primary" (azul)
        self.marcoRGB = ttk.Labelframe(self.panelVisualizacion, text="Modelo RGB (Matplotlib)", padding=10, bootstyle="primary")
        # Coloca el marco en la fila 4 del panel de visualización
        self.marcoRGB.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        # Configura la columna y fila del marco para que se expandan
        self.marcoRGB.columnconfigure(0, weight=1); self.marcoRGB.rowconfigure(1, weight=1)
        # Crea y coloca una etiqueta con el título del modelo RGB
        ttk.Label(self.marcoRGB, text="Modelo RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Separa la imagen en sus canales de color Rojo, Verde y Azul usando OpenCV
        R, G, B = cv2.split(self.imagen.imagenCv)
        # Crea una figura de matplotlib con tamaño 16x3.7 pulgadas y 100 DPI
        fig = Figure(figsize=(16, 3.7), dpi=100)
        # Crea el primer subplot (1 fila, 3 columnas, posición 1) para el canal R
        ax1 = fig.add_subplot(1, 3, 1)
        # Crea el segundo subplot (1 fila, 3 columnas, posición 2) para el canal G
        ax2 = fig.add_subplot(1, 3, 2)
        # Crea el tercer subplot (1 fila, 3 columnas, posición 3) para el canal B
        ax3 = fig.add_subplot(1, 3, 3)
        # Muestra el canal R con mapa de colores rojos; establece título; oculta ejes
        ax1.imshow(R, cmap="Reds", vmin=0, vmax=255); ax1.set_title("Canal R"); ax1.axis("off")
        # Muestra el canal G con mapa de colores verdes; establece título; oculta ejes
        ax2.imshow(G, cmap="Greens", vmin=0, vmax=255); ax2.set_title("Canal G"); ax2.axis("off")
        # Muestra el canal B con mapa de colores azules; establece título; oculta ejes
        ax3.imshow(B, cmap="Blues", vmin=0, vmax=255); ax3.set_title("Canal B"); ax3.axis("off")
        # Establece el título principal de toda la figura
        fig.suptitle("Modelo RGB")
        # Crea un canvas de tkinter para mostrar la figura de matplotlib
        canvas = FigureCanvasTkAgg(fig, master=self.marcoRGB)
        # Renderiza la figura en el canvas
        canvas.draw()
        # Obtiene el widget de tkinter del canvas y lo coloca en la grilla
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

    # Método para cargar y mostrar el modelo de color HSV
    def cargarModeloHSV(self):
        # Verifica si hay una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Crea un marco para mostrar el modelo HSV con estilo "success" (verde)
        self.marcoHSV = ttk.Labelframe(self.panelVisualizacion, text="Modelo HSV (Matplotlib)", padding=10, bootstyle="success")
        # Coloca el marco en la fila 5 del panel de visualización
        self.marcoHSV.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        # Configura la columna del marco para que se expanda
        self.marcoHSV.columnconfigure(0, weight=1)
        # Configura la fila 1 del marco para que se expanda (donde irá la gráfica)
        self.marcoHSV.rowconfigure(1, weight=1)

        # Crea y coloca una etiqueta con el título del modelo HSV
        ttk.Label(self.marcoHSV, text="Modelo HSV", font=("Arial", 16, "bold")).grid( row=0, column=0, sticky="w", padx=5, pady=5)

        # Obtiene la imagen en formato RGB (numpy array)
        rgb = self.imagen.imagenCv
        # Convierte la imagen de RGB a HSV usando OpenCV
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        # Separa la imagen HSV en sus canales: Hue (matiz), Saturation (saturación), Value (valor/brillo)
        H, S, V = cv2.split(hsv)
        # Crea una figura de matplotlib con tamaño 12x3.7 pulgadas y 100 DPI
        fig = Figure(figsize=(12, 3.7), dpi=100)
        # Crea el primer subplot para el canal H (Hue/Matiz)
        ax1 = fig.add_subplot(1, 3, 1)
        # Crea el segundo subplot para el canal S (Saturation/Saturación)
        ax2 = fig.add_subplot(1, 3, 2)
        # Crea el tercer subplot para el canal V (Value/Valor)
        ax3 = fig.add_subplot(1, 3, 3)
        # Muestra el canal H con mapa de colores HSV (rango 0-179 en OpenCV)
        im1 = ax1.imshow(H, cmap="hsv", vmin=0, vmax=179)
        # Establece título y oculta ejes para el canal H
        ax1.set_title("Canal H"); ax1.axis("off")
        # Muestra el canal S con mapa de colores en escala de grises (rango 0-255)
        im2 = ax2.imshow(S, cmap="gray", vmin=0, vmax=255)
        # Establece título y oculta ejes para el canal S
        ax2.set_title("Canal S"); ax2.axis("off")
        # Muestra el canal V con mapa de colores en escala de grises (rango 0-255)
        im3 = ax3.imshow(V, cmap="gray", vmin=0, vmax=255)
        # Establece título y oculta ejes para el canal V
        ax3.set_title("Canal V"); ax3.axis("off")

        # Establece el título principal de toda la figura
        fig.suptitle("Modelo HSV")
        # Crea un canvas de tkinter para mostrar la figura de matplotlib
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHSV)
        # Renderiza la figura en el canvas
        canvas.draw()
        # Obtiene el widget de tkinter del canvas
        canvas_widget = canvas.get_tk_widget()
        # Coloca el widget del canvas en la grilla
        canvas_widget.grid(row=1, column=0, sticky="nsew")

    # Método para cargar y mostrar el modelo de color CMY (Cyan, Magenta, Yellow)
    def cargarModeloCMY(self):
        # Verifica si hay una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Crea un marco para mostrar el modelo CMY con estilo "warning" (amarillo/naranja)
        self.marcoCMY = ttk.Labelframe(self.panelVisualizacion, text="Modelo CMY (Matplotlib)", padding=10, bootstyle="warning")
        # Coloca el marco en la fila 6 del panel de visualización
        self.marcoCMY.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)
        # Configura la columna y fila del marco para que se expandan
        self.marcoCMY.columnconfigure(0, weight=1); self.marcoCMY.rowconfigure(1, weight=1)
        # Crea y coloca una etiqueta con el título del modelo CMY
        ttk.Label(self.marcoCMY, text="Modelo CMY", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Separa la imagen en sus canales RGB
        R, G, B = cv2.split(self.imagen.imagenCv)
        # Calcula los canales CMY invirtiendo los valores RGB (complemento a 255)
        C = 255 - R; M = 255 - G; Y = 255 - B  # Cyan=255-Rojo, Magenta=255-Verde, Yellow=255-Azul
        # Crea una figura de matplotlib con tamaño 12x3.7 pulgadas y 100 DPI
        fig = Figure(figsize=(12, 3.7), dpi=100)
        # Crea el primer subplot para el canal C (Cyan)
        ax1 = fig.add_subplot(1, 3, 1)
        # Crea el segundo subplot para el canal M (Magenta)
        ax2 = fig.add_subplot(1, 3, 2)
        # Crea el tercer subplot para el canal Y (Yellow)
        ax3 = fig.add_subplot(1, 3, 3)
        # Muestra el canal C con mapa de colores azules; establece título; oculta ejes
        ax1.imshow(C, cmap="Blues",   vmin=0, vmax=255); ax1.set_title("Canal C"); ax1.axis("off")
        # Muestra el canal M con mapa de colores púrpuras; establece título; oculta ejes
        ax2.imshow(M, cmap="Purples", vmin=0, vmax=255); ax2.set_title("Canal M"); ax2.axis("off")
        # Muestra el canal Y con mapa de colores naranjas; establece título; oculta ejes
        ax3.imshow(Y, cmap="Oranges", vmin=0, vmax=255); ax3.set_title("Canal Y"); ax3.axis("off")
        # Establece el título principal de toda la figura
        fig.suptitle("Modelo CMY")

        # Crea un canvas de tkinter para mostrar la figura de matplotlib
        canvas = FigureCanvasTkAgg(fig, master=self.marcoCMY)
        # Renderiza la figura en el canvas
        canvas.draw()
        # Obtiene el widget de tkinter del canvas y lo coloca en la grilla
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

    # Método para crear y mostrar histograma RGB (histograma de canales de color)
    def crearHistogramaRGB(self):
        # Verifica si hay una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        # Crea un marco para mostrar el histograma RGB con estilo "info" (azul claro)
        self.marcoHistograma = ttk.Labelframe(self.panelVisualizacion, text="Histograma RGB (Matplotlib)", padding=10, bootstyle="info")
        # Coloca el marco en la fila 1 del panel de visualización
        self.marcoHistograma.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        # Configura la columna y fila del marco para que se expandan
        self.marcoHistograma.columnconfigure(0, weight=1); self.marcoHistograma.rowconfigure(1, weight=1)
        # Crea y coloca una etiqueta con el título del histograma RGB
        ttk.Label(self.marcoHistograma, text="Histograma RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Crea una figura de matplotlib con tamaño 16x10 pulgadas y 100 DPI (vertical para 3 histogramas)
        fig = Figure(figsize=(16, 10), dpi=100)
        # Crea el primer subplot (3 filas, 1 columna, posición 1) para histograma rojo
        ax1 = fig.add_subplot(3, 1, 1)
        # Crea el segundo subplot (3 filas, 1 columna, posición 2) para histograma verde
        ax2 = fig.add_subplot(3, 1, 2)
        # Crea el tercer subplot (3 filas, 1 columna, posición 3) para histograma azul
        ax3 = fig.add_subplot(3, 1, 3)
        # Obtiene los datos de histograma para cada canal de color desde el objeto imagen
        histogramaRojo, histogramaVerde, histogramaAzul = self.imagen.histogramaColor()
        # Crea gráfico de barras para canal rojo con transparencia 70% y ancho 1
        ax1.bar(histogramaRojo[0], histogramaRojo[1], color='red', alpha=0.7, width=1)
        # Crea gráfico de barras para canal verde con transparencia 70% y ancho 1
        ax2.bar(histogramaVerde[0], histogramaVerde[1], color='green', alpha=0.7, width=1)
        # Crea gráfico de barras para canal azul con transparencia 70% y ancho 1
        ax3.bar(histogramaAzul[0], histogramaAzul[1], color='blue', alpha=0.7, width=1)
        # Establece títulos para cada histograma
        ax1.set_title("Histograma del canal R");
        ax2.set_title("Histograma del canal G");
        ax3.set_title("Histograma del canal B");
        # Crea un canvas de tkinter para mostrar la figura de matplotlib
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHistograma)
        # Renderiza la figura en el canvas
        canvas.draw()
        # Obtiene el widget de tkinter del canvas y lo coloca en la grilla
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
    
    # Método para crear y mostrar histograma de escala de grises
    def crearHistogramaGris(self):
        # Verifica si hay una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        # Verifica si existe la conversión a escala de grises antes de mostrar su histograma
        if not hasattr(self, 'marcoGris') or not self.marcoGris.winfo_exists():
            messagebox.showwarning("Atención", "Primero convierte la imagen a escala de grises.")
            return
        # Crea un marco para mostrar el histograma de grises con estilo "info" (azul claro)
        self.marcoHistogramaGrises = ttk.Labelframe(self.panelVisualizacion, text="Histograma de escala de gris (Matplotlib)", padding=10, bootstyle="info")
        # Coloca el marco en la fila 3 del panel de visualización
        self.marcoHistogramaGrises.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        # Configura la columna y fila del marco para que se expandan
        self.marcoHistogramaGrises.columnconfigure(0, weight=1); self.marcoHistogramaGrises.rowconfigure(1, weight=1)
        # Crea y coloca una etiqueta con el título del histograma de grises
        ttk.Label(self.marcoHistogramaGrises, text="Histograma de escala de gris", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Crea una figura de matplotlib con tamaño 16x6 pulgadas y 100 DPI
        fig = Figure(figsize=(16, 6), dpi=100)
        # Crea un único subplot (1 fila, 1 columna, posición 1) para el histograma de grises
        ax = fig.add_subplot(1, 1, 1)
        # Obtiene los datos de histograma de escala de grises desde el objeto imagen
        histogramaGris = self.imagen.histogramaGris()
        # Crea gráfico de barras en color gris con transparencia 70% y ancho 1
        ax.bar(histogramaGris[0], histogramaGris[1], color='gray', alpha=0.7, width=1)
        # Establece el título del histograma
        ax.set_title("Histograma de escala de grises");
        # Crea un canvas de tkinter para mostrar la figura de matplotlib
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHistogramaGrises)
        # Renderiza la figura en el canvas
        canvas.draw()
        # Obtiene el widget de tkinter del canvas y lo coloca en la grilla
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

# Punto de entrada del programa - se ejecuta solo si este archivo se ejecuta directamente
if __name__ == "__main__":
    # Crea una instancia de la clase Interfaz para iniciar la aplicación
    Interfaz()
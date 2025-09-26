
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

# Importación de la librería ttkbootstrap como ttk - framework moderno para interfaces gráficas basado en tkinter
import ttkbootstrap as ttk
# Importación de todas las constantes de ttkbootstrap (colores, estilos, configuraciones predefinidas)
from ttkbootstrap.constants import *
# Importación del widget ScrolledFrame para crear marcos con barras de desplazamiento automáticas
from ttkbootstrap.scrolled import ScrolledFrame
# Importación de módulos específicos de tkinter: filedialog para diálogos de archivos, messagebox para ventanas emergentes
from tkinter import filedialog, messagebox
# Importación de la clase personalizada Imagen desde el módulo local, renombrada como Img para facilitar su uso
from Imagen import Imagen as Img
# Importación de la clase Figure de matplotlib para crear figuras de gráficos
from matplotlib.figure import Figure
# Importación del backend de matplotlib para integración con tkinter - permite embebber gráficos en la GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Importación de OpenCV para procesamiento y manipulación de imágenes
import cv2

# Definición de la clase Interfaz que hereda de ttk.Window (ventana principal de ttkbootstrap)
class Interfaz(ttk.Window):
    # Constructor de la clase
    def __init__(self):
        # Inicialización del atributo imagen como None - almacenará la instancia de imagen cargada
        self.imagen = None
        # Llamada al método para establecer configuraciones iniciales de la ventana
        self.configuracionesIniciales()
        # Llamada al método para crear y organizar todos los elementos de la interfaz
        self.crearLayout()
        # Inicia el bucle principal de eventos de la aplicación - mantiene la ventana activa y responsive
        self.mainloop()

    # Método para establecer las configuraciones iniciales de la ventana principal
    def configuracionesIniciales(self):
        # Llamada al constructor de la clase padre (ttk.Window) con tema "solar" que define el esquema de colores
        super().__init__(themename="solar")
        # Establece el título que aparecerá en la barra superior de la ventana
        self.title("Practica 1")
        # Define las dimensiones de la ventana: 1600px de ancho por 900px de alto
        self.geometry("1600x900")
        # Deshabilita la capacidad de redimensionar la ventana (ancho=False, alto=False)
        self.resizable(False,False)

        # Configuración del sistema de grid: configura 10 filas con peso igual (weight=1) para distribución proporcional
        for i in range(10): self.rowconfigure(i, weight=1)
        # Configura la columna 0 sin expansión (weight=0) - panel de controles con ancho fijo
        self.columnconfigure(0, weight=0)
        # Configura la columna 1 para expandirse (weight=1) - panel de visualización ocupa espacio restante
        self.columnconfigure(1, weight=1)

    # Método principal para crear y organizar el layout de la interfaz gráfica
    def crearLayout(self):
        # Creación del panel izquierdo - Frame con padding interno de 10px, estilo oscuro, ancho fijo de 400px
        self.panelControl = ttk.Frame(self, padding=10, bootstyle="DARK", width=400)
        # Posicionamiento del panel: fila 0, columna 0, se expande en todas direcciones, ocupa 10 filas
        self.panelControl.grid(row=0, column=0, sticky="nsew", rowspan=10)
        # Configuración de grid interno: 8 filas con distribución proporcional para elementos de control
        for i in range(8): self.panelControl.rowconfigure(i, weight=1)
        # Configuración de la única columna del panel de control para que se expanda
        self.panelControl.columnconfigure(0, weight=1)

        # Creación del título principal, etiqueta con texto, fuente Arial 16px en negrita
        self.labelTitulo = ttk.Label(self.panelControl, text="Practica 1: Modelos de color", font=("Arial", 16, "bold"))
        # Posicionamiento del título en la primera fila del panel de control con márgenes de 5px
        self.labelTitulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Creación del panel derecho usando ScrolledFrame, que permite desplazamiento automático cuando el contenido excede el tamaño
        self.panelVisualizacion = ScrolledFrame(self, padding=10, bootstyle="DARK", width=1200, height=900)
        # Posicionamiento del panel de visualización: columna 1, se expande completamente, ocupa 10 filas
        self.panelVisualizacion.grid(row=0, column=1, sticky="nsew", rowspan=10)
        # Configuración para que la columna interna del panel de visualización se expanda
        self.panelVisualizacion.columnconfigure(0, weight=1)

        # Llamadas a métodos específicos para crear secciones de la interfaz
        # Crea los controles para cargar imágenes desde el disco
        self.crearControlesCargarImagen()
        # Crea los botones para seleccionar y mostrar diferentes modelos de color
        self.crearControlesMostrarModelos()
        # Crea el área donde se mostrarán los resultados y visualizaciones
        self.crearMuestraResultado()
        self.crearControlesGrisUmbralizacion()

    # Método para crear la sección de controles de carga de imágenes
    def crearControlesCargarImagen(self):
        # Creación de un Labelframe con título "Cargar Imagen", padding interno y estilo primario (azul)
        self.marcoCargarImagen = ttk.Labelframe(self.panelControl, text="Cargar Imagen", padding=10, bootstyle="primary")
        # Posicionamiento en fila 1 del panel de control, expandiéndose en todas direcciones con márgenes
        self.marcoCargarImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5, rowspan=1)
        # Configuración del sistema de grid interno: 3 filas con distribución equitativa
        for i in range(3):
            self.marcoCargarImagen.rowconfigure(i, weight=1)
        # Configuración de la columna para que se expanda horizontalmente
        self.marcoCargarImagen.columnconfigure(0, weight=1)
        
        # Creación del subtítulo descriptivo con fuente Arial 12px en negrita
        self.subTituloCargar = ttk.Label(self.marcoCargarImagen, text="Cargar una imagen desde su dispositivo", font=("Arial", 12, "bold"))
        # Creación de etiqueta con instrucciones para el usuario, fuente Arial 10px normal
        self.indicacionesCargar = ttk.Label(self.marcoCargarImagen, text="Seleccione una imagen para cargarla en la aplicación", font=("Arial", 10))
        # Creación del botón de carga con estilo primario, vinculado al método cargarImagen mediante command
        self.botonCargar = ttk.Button(self.marcoCargarImagen, text="Cargar Imagen", bootstyle="PRIMARY", command=self.cargarImagen)
        
        # Posicionamiento del subtítulo en la primera fila con expansión completa y márgenes
        self.subTituloCargar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de las indicaciones en la segunda fila con las mismas características
        self.indicacionesCargar.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        # Posicionamiento del botón en la tercera fila con expansión y márgenes
        self.botonCargar.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    # Método para crear la sección de controles de selección de modelos de color
    def crearControlesMostrarModelos(self):
        # Creación de Labelframe para agrupar controles de modelos con estilo secundario (gris/verde)
        self.marcoModelos = ttk.Labelframe(self.panelControl, text="Elegir Modelo a mostrar", padding=10, bootstyle="secondary")
        # Posicionamiento en fila 2 del panel de control con expansión y márgenes
        self.marcoModelos.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Configuración de grid: 3 columnas con distribución equitativa para los botones horizontales
        for i in range(3): self.marcoModelos.columnconfigure(i, weight=1)
        # Configuración de 3 filas (0: título, 1: instrucciones, 2: botones) con distribución proporcional
        for i in range(3):self.marcoModelos.rowconfigure(i, weight=1)
        
        # Creación de subtítulo descriptivo de la sección con fuente Arial 12px negrita
        self.subTituloModelos = ttk.Label(self.marcoModelos, text="Modelos de color", font=("Arial", 12, "bold"))
        # Creación de etiqueta con instrucciones para el usuario, fuente Arial 10px normal
        self.indicacionesModelos = ttk.Label(self.marcoModelos, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        # Creación de botón para modelo RGB , vinculado al método cargarModeloRGB
        self.botonModeloRGB = ttk.Button(self.marcoModelos, text="Modelo RGB", bootstyle="secondary", command=self.cargarModeloRGB)
        # Creación de botón para modelo HSV , vinculado al método cargarModeloHSV
        self.botonModeloHSV = ttk.Button(self.marcoModelos, text="Modelo HSV", bootstyle="secondary", command=self.cargarModeloHSV)
        # Creación de botón para modelo CMY , vinculado al método cargarModeloCMY
        self.botonModeloCMY = ttk.Button(self.marcoModelos, text="Modelo CMY", bootstyle="secondary", command=self.cargarModeloCMY)
        
        # Posicionamiento del subtítulo abarcando las 3 columnas (columnspan=3) en la fila 0
        self.subTituloModelos.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de instrucciones abarcando las 3 columnas en la fila 1
        self.indicacionesModelos.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de botón RGB en fila 2, columna 0 con expansión y márgenes
        self.botonModeloRGB.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de botón HSV en fila 2, columna 1 con las mismas características
        self.botonModeloHSV.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de botón CMY en fila 2, columna 2 completando la fila horizontal
        self.botonModeloCMY.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
    
    def crearControlesGrisUmbralizacion(self):
        # Creación de Labelframe para agrupar controles de modelos con estilo secundario (gris/verde)
        self.marcoConversiones = ttk.Labelframe(self.panelControl, text="Elegir cambio a mostrar", padding=10, bootstyle="success")
        # Posicionamiento en fila 2 del panel de control con expansión y márgenes
        self.marcoConversiones.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        # Configuración de grid: 3 columnas con distribución equitativa para los botones horizontales
        for i in range(3): self.marcoConversiones.columnconfigure(i, weight=1)
        # Configuración de 3 filas (0: título, 1: instrucciones, 2: botones) con distribución proporcional
        for i in range(3):self.marcoConversiones.rowconfigure(i, weight=1)

        # Creación de subtítulo descriptivo de la sección con fuente Arial 12px negrita
        self.subTituloConversiones = ttk.Label(self.marcoConversiones, text="Modelos de color", font=("Arial", 12, "bold"))
        # Creación de etiqueta con instrucciones para el usuario, fuente Arial 10px normal
        self.indicacionesConversiones = ttk.Label(self.marcoConversiones, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        # Creación de botón para modelo RGB , vinculado al método cargarModeloRGB
        self.botonModeloGris = ttk.Button(self.marcoConversiones, text="Convertir a escala de gris", bootstyle="success", command=self.convertirGris)
        # Creación de botón para modelo HSV , vinculado al método cargarModeloHSV
        self.botonModeloUmbralizarFijo = ttk.Button(self.marcoConversiones, text="Umbralizar con fijo", bootstyle="success", command=self.convertirUmbralizarFijo)
        # Creación de botón para modelo CMY , vinculado al método cargarModeloCMY
        self.botonModeloUmbralizarAdaptativo = ttk.Button(self.marcoConversiones, text="Umbralizar con adaptativo", bootstyle="success", command=self.convertirUmbralizarAdaptativo)

        # Posicionamiento del subtítulo abarcando las 3 columnas (columnspan=3) en la fila 0
        self.subTituloConversiones.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de instrucciones abarcando las 3 columnas en la fila 1
        self.indicacionesConversiones.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de botón RGB en fila 2, columna 0 con expansión y márgenes
        self.botonModeloGris.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de botón HSV en fila 2, columna 1 con las mismas características
        self.botonModeloUmbralizarFijo.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        # Posicionamiento de botón CMY en fila 2, columna 2 completando la fila horizontal
        self.botonModeloUmbralizarAdaptativo.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    def convertirGris(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        
        self.marcoGris = ttk.Labelframe(self.panelVisualizacion, text="Imagen en escala de gris", padding=10, bootstyle="success")
        self.marcoGris.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoGris.columnconfigure(0, weight=1)
        self.marcoGris.rowconfigure(0, weight=1)
        self.subImagenGris = ttk.Label(self.marcoGris, text="Imagen en escala de grises", font=("Arial", 16, "bold"))
        self.subImagenGris.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        imagenGrisPillow = self.imagen.obtenerImagenGris()
        if imagenGrisPillow:
            self.subImagenGris.configure(image=imagenGrisPillow)
            self.subImagenGris.image = imagenGrisPillow
        else:
            messagebox.showerror("Error", "No se pudo convertir la imagen a escala de grises.")

    def convertirUmbralizarFijo(self):
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        self.marcoUmbralizacionFijo = ttk.Labelframe(self.panelVisualizacion, text="Imagen umbralizada con fijo", padding=10, bootstyle="success")
        self.marcoUmbralizacionFijo.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.marcoUmbralizacionFijo.columnconfigure(0, weight=1)
        self.marcoUmbralizacionFijo.rowconfigure(0, weight=1)
        self.SubImagenUmbralFijo = ttk.Label(self.marcoUmbralizacionFijo, text="Imagen umbralizada con fijo", font=("Arial", 16, "bold"))
        self.SubImagenUmbralFijo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        imagenUmbralizadaFijo = self.imagen.obtenerUmbralizacionFija()
        if imagenUmbralizadaFijo:
            self.SubImagenUmbralFijo.configure(image=imagenUmbralizadaFijo)
            self.SubImagenUmbralFijo.image = imagenUmbralizadaFijo
        else:
            messagebox.showerror("Error", "No se pudo aplicar la umbralización fija.")

    def convertirUmbralizarAdaptativo(self):
        pass

    # Método para crear el área de visualización de resultados en el panel derecho
    def crearMuestraResultado(self):
        # Creación de Labelframe con estilo "info" (azul claro) para contener la visualización principal
        self.marcoMapa = ttk.Labelframe(self.panelVisualizacion, text="Visualización de la imagen", padding=10, bootstyle="info")
        # Posicionamiento en la primera fila del panel de visualización con expansión total
        self.marcoMapa.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Configuración de 2 filas: primera para título, segunda para contenido de imagen
        self.marcoMapa.rowconfigure(0, weight=1)
        self.marcoMapa.rowconfigure(1, weight=1)
        # Configuración de columna única que se expande horizontalmente
        self.marcoMapa.columnconfigure(0, weight=1)
        # Creación del título de la sección de visualización con fuente Arial 16px negrita
        self.tituloVisualizacion = ttk.Label(self.marcoMapa, text="Visualización de la imagen", font=("Arial", 16, "bold"))
        # Creación de etiqueta placeholder que será reemplazada por la imagen, centrada con anchor="center"
        self.SubImagen = ttk.Label(self.marcoMapa, text="Aquí se mostrará la imagen cargada y sus modelos de color", font=("Arial", 12), anchor="center")
        # Posicionamiento del título en la primera fila con expansión y márgenes
        self.tituloVisualizacion.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Posicionamiento del área de imagen en la segunda fila donde se mostrará el contenido visual
        self.SubImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    # Método callback para manejar la carga de imágenes desde el sistema de archivos
    def cargarImagen(self):
        # Apertura de diálogo de archivos con filtros específicos para imágenes (jpg, jpeg, png)
        rutaArchivo= filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files")])
        # Verificación de que el usuario seleccionó un archivo (rutaArchivo no está vacío)
        if rutaArchivo:
            # Creación de instancia de la clase Imagen personalizada pasando la ruta del archivo
            self.imagen = Img(rutaArchivo)
            # Llamada al método de la clase Imagen para convertir la imagen a formato compatible con tkinter
            imagenTkinter = self.imagen.iniciarImagen()
            # Verificación de que la conversión fue exitosa
            if imagenTkinter:
                # Actualización de la etiqueta SubImagen para mostrar la imagen cargada
                self.SubImagen.configure(image=imagenTkinter)
                # Mantiene una referencia a la imagen para evitar que sea recolectada por el garbage collector
                self.SubImagen.image = imagenTkinter
            # Si la conversión falló, elimina la instancia de imagen creada
            else: del self.imagen
        # Si no se seleccionó archivo, muestra ventana de advertencia al usuario
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")

    # Método genérico para mostrar un modelo de color específico (actualmente no utilizado)
    def mostrarModelo(self, modelo):
        # Verificación de que existe una imagen cargada mediante hasattr (verifica si el atributo existe)
        if hasattr(self, 'imagen'):
            # Llamada al método obtenerModelo de la clase Imagen para obtener el modelo especificado
            imagenModelo = self.imagen.obtenerModelo(modelo)
            # Verificación de que se obtuvo el modelo correctamente
            if imagenModelo:
                # Actualización de la etiqueta de visualización con el modelo obtenido
                self.SubImagen.configure(image=imagenModelo)
                # Mantenimiento de referencia para prevenir recolección de basura
                self.SubImagen.image = imagenModelo
            # Si no se pudo obtener el modelo, muestra mensaje de error
            else:
                messagebox.showerror("Error", "No se pudo obtener el modelo de color seleccionado.")

    # Método callback para generar y mostrar la visualización del modelo RGB
    def cargarModeloRGB(self):
        # Validación de que existe una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Creación de Labelframe específico para el modelo RGB con estilo primario
        self.marcoRGB = ttk.Labelframe(self.panelVisualizacion, text="Modelo RGB (Matplotlib)", padding=10, bootstyle="primary")
        # Posicionamiento en fila 1 del panel de visualización (debajo del marco principal)
        self.marcoRGB.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        # Configuración de grid: columna expandible y fila 1 expandible para el contenido gráfico
        self.marcoRGB.columnconfigure(0, weight=1); self.marcoRGB.rowconfigure(1, weight=1)
        # Creación y posicionamiento directo de etiqueta de título con alineación izquierda
        ttk.Label(self.marcoRGB, text="Modelo RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Separación de la imagen en sus canales RGB usando OpenCV split
        R, G, B = cv2.split(self.imagen.imagenCv)
        # Creación de figura matplotlib con dimensiones específicas ampliadas (16x7 pulgadas, 100 DPI)
        fig = Figure(figsize=(16, 7), dpi=100)
        # Creación de 3 subplots horizontales (1 fila, 3 columnas) para cada canal
        ax1 = fig.add_subplot(1, 3, 1)  # Subplot para canal rojo
        ax2 = fig.add_subplot(1, 3, 2)  # Subplot para canal verde
        ax3 = fig.add_subplot(1, 3, 3)  # Subplot para canal azul
        # Visualización del canal R con colormap rojo, rango 0-255, título y sin ejes
        ax1.imshow(R, cmap="Reds", vmin=0, vmax=255); ax1.set_title("Canal R"); ax1.axis("off")
        # Visualización del canal G con colormap verde, mismas características
        ax2.imshow(G, cmap="Greens", vmin=0, vmax=255); ax2.set_title("Canal G"); ax2.axis("off")
        # Visualización del canal B con colormap azul, mismas características
        ax3.imshow(B, cmap="Blues", vmin=0, vmax=255); ax3.set_title("Canal B"); ax3.axis("off")
        # Creación del canvas de matplotlib para integración con tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marcoRGB)
        # Renderizado de la figura en el canvas
        canvas.draw()
        # Obtención del widget tkinter del canvas y posicionamiento en el grid
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

    # Método callback para generar y mostrar la visualización del modelo HSV
    def cargarModeloHSV(self):
        # Validación de existencia de imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Creación de Labelframe específico para HSV con estilo "success" (verde)
        self.marcoHSV = ttk.Labelframe(self.panelVisualizacion, text="Modelo HSV (Matplotlib)", padding=10, bootstyle="success")
        # Posicionamiento en fila 2 (tercera sección) del panel de visualización
        self.marcoHSV.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Configuración de grid: columna expandible y fila 1 para contenido gráfico
        self.marcoHSV.columnconfigure(0, weight=1)
        self.marcoHSV.rowconfigure(1, weight=1)

        # Creación y posicionamiento de etiqueta de título con alineación izquierda
        ttk.Label(self.marcoHSV, text="Modelo HSV", font=("Arial", 16, "bold")).grid( row=0, column=0, sticky="w", padx=5, pady=5)

        # Obtención de la imagen RGB desde el objeto imagen
        rgb = self.imagen.imagenCv
        # Conversión del espacio de color RGB a HSV usando OpenCV
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        # Separación de los canales HSV (Hue, Saturation, Value)
        H, S, V = cv2.split(hsv)
        # Creación de figura matplotlib con dimensiones específicas
        fig = Figure(figsize=(12, 3.8), dpi=100) 
        # Creación de 3 subplots horizontales para cada canal HSV
        ax1 = fig.add_subplot(1, 3, 1)  # Subplot para Hue
        ax2 = fig.add_subplot(1, 3, 2)  # Subplot para Saturation
        ax3 = fig.add_subplot(1, 3, 3)  # Subplot para Value
        # Visualización del canal H con colormap HSV, rango 0-179 (OpenCV usa este rango para Hue)
        im1 = ax1.imshow(H, cmap="hsv", vmin=0, vmax=179)
        ax1.set_title("Canal H"); ax1.axis("off")  # Título y ocultación de ejes
        # Visualización del canal S con escala de grises, rango 0-255
        im2 = ax2.imshow(S, cmap="gray", vmin=0, vmax=255)
        ax2.set_title("Canal S"); ax2.axis("off")  # Título y ocultación de ejes
        # Visualización del canal V con escala de grises, rango 0-255
        im3 = ax3.imshow(V, cmap="gray", vmin=0, vmax=255)
        ax3.set_title("Canal V"); ax3.axis("off")  # Título y ocultación de ejes

        # Establecimiento de título general para toda la figura
        fig.suptitle("Modelo HSV")
        # Creación del canvas matplotlib para integración con tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHSV)
        # Renderizado de la figura
        canvas.draw()
        # Obtención del widget tkinter y almacenamiento en variable
        canvas_widget = canvas.get_tk_widget()
        # Posicionamiento del widget en el grid con expansión completa
        canvas_widget.grid(row=1, column=0, sticky="nsew")

    # Método callback para generar y mostrar la visualización del modelo CMY
    def cargarModeloCMY(self):
        # Validación de existencia de imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Creación de Labelframe específico para CMY con estilo "warning" (amarillo/naranja)
        self.marcoCMY = ttk.Labelframe(self.panelVisualizacion, text="Modelo CMY (Matplotlib)", padding=10, bootstyle="warning")
        # Posicionamiento en fila 3 (cuarta sección) del panel de visualización
        self.marcoCMY.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        # Configuración de grid: columna y fila expandibles para el contenido gráfico
        self.marcoCMY.columnconfigure(0, weight=1); self.marcoCMY.rowconfigure(1, weight=1)
        # Creación y posicionamiento directo de etiqueta de título
        ttk.Label(self.marcoCMY, text="Modelo CMY", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Separación de la imagen RGB en sus canales individuales
        R, G, B = cv2.split(self.imagen.imagenCv)
        # Cálculo de los canales CMY mediante inversión: CMY = 255 - RGB (conversión sustractiva)
        C = 255 - R; M = 255 - G; Y = 255 - B  # Cyan = 255-Red, Magenta = 255-Green, Yellow = 255-Blue
        # Creación de figura matplotlib con dimensiones específicas
        fig = Figure(figsize=(12, 3.8), dpi=100)
        # Creación de 3 subplots horizontales para cada canal CMY
        ax1 = fig.add_subplot(1, 3, 1)  # Subplot para canal Cyan
        ax2 = fig.add_subplot(1, 3, 2)  # Subplot para canal Magenta
        ax3 = fig.add_subplot(1, 3, 3)  # Subplot para canal Yellow
        # Visualización del canal C con colormap azul, rango 0-255, título y sin ejes
        ax1.imshow(C, cmap="Blues",   vmin=0, vmax=255); ax1.set_title("Canal C"); ax1.axis("off")
        # Visualización del canal M con colormap púrpura, mismas características
        ax2.imshow(M, cmap="Purples", vmin=0, vmax=255); ax2.set_title("Canal M"); ax2.axis("off")
        # Visualización del canal Y con colormap naranja, mismas características
        ax3.imshow(Y, cmap="Oranges", vmin=0, vmax=255); ax3.set_title("Canal Y"); ax3.axis("off")
        # Establecimiento de título general para toda la figura
        fig.suptitle("Modelo CMY")

        # Creación del canvas matplotlib para integración con tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marcoCMY)
        # Renderizado de la figura en el canvas
        canvas.draw()
        # Obtención del widget tkinter del canvas y posicionamiento directo en el grid
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

# Punto de entrada principal del programa - se ejecuta solo si el archivo se ejecuta directamente
if __name__ == "__main__":
    # Creación e inicialización de la instancia de la clase Interfaz, lo que inicia toda la aplicación
    Interfaz()
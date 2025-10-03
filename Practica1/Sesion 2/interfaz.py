import ttkbootstrap as ttk  
from ttkbootstrap.constants import *  
from ttkbootstrap.scrolled import ScrolledFrame  
from tkinter import filedialog, messagebox, simpledialog  
from Imagen import Imagen as Img 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
from matplotlib.ticker import MultipleLocator 
import cv2  

# Define la clase principal de la interfaz que hereda de ttk.Window
class Interfaz(ttk.Window):
    # METODOS DE CONFIGURACION DE LA VENTANA - Aquí van los métodos que configuran la ventana y layout
    def __init__(self):
        self.imagen = None  # Variable para almacenar la imagen cargada
        self.configuracionesIniciales()  # Configura la ventana principal
        self.crearLayout()  # Crea todos los elementos de la interfaz
        self.mainloop()  # Inicia el bucle principal de la aplicación

    def configuracionesIniciales(self):
        super().__init__(themename="superhero")  # Llama al constructor padre con tema "solar"
        self.title("Practica 1")  # Establece el título de la ventana
        self.geometry("1600x900")  # Define el tamaño de la ventana
        self.resizable(True,True)  # Hace que la ventana no sea redimensionable

        # Configura el comportamiento de las columnas para el layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)  # Columna 0 (panel de control) tamaño fijo
        self.columnconfigure(1, weight=1)  # Columna 1 (panel de visualización) se expande

    def crearLayout(self):
        # Crea el panel de control izquierdo con botones y opciones
        self.panelControl = ttk.Frame(self, padding=10, bootstyle="DARK", width=400)
        self.panelControl.grid(row=0, column=0, sticky="nsew", rowspan=10)  # Se coloca en la primera columna
        # Configura las filas del panel de control para que se distribuyan uniformemente
        for i in range(4): self.panelControl.rowconfigure(i, weight=1)
        self.panelControl.columnconfigure(0, weight=1)  # La columna se expande

        # Crea el título principal del panel de control
        self.labelTitulo = ttk.Label(self.panelControl, text="Practica 1: Modelos de color", font=("Arial", 16, "bold"))
        self.labelTitulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Crea el panel de visualización derecho con scroll para mostrar las imágenes
        self.panelVisualizacion = ScrolledFrame(self, padding=10, bootstyle="DARK", width=1200, height=900)
        self.panelVisualizacion.grid(row=0, column=1, sticky="nsew", rowspan=10)  # Se coloca en la segunda columna
        self.panelVisualizacion.columnconfigure(0, weight=1)  # La columna se expande

        # Llama a los métodos que crean cada sección de la interfaz
        self.crearMuestraResultado()  # Área para mostrar las imágenes
        self.crearControlesCargarImagen()  # Botón para cargar imágenes
        self.crearControlesMostrarModelos()  # Botones para mostrar modelos de color
        self.crearControlesGrisBinarizacion()  # Botones para conversiones de gris y binarización
        self.crearControlesHistograma()  # Botones para mostrar histogramas

    def crearControlesCargarImagen(self):
        estiloCargarImg = "primary"  # Define el estilo azul para esta sección
        # Crea un marco con borde y título para la sección de cargar imagen
        self.marcoCargarImagen = ttk.Labelframe(self.panelControl, text="Cargar Imagen", padding=10, bootstyle=estiloCargarImg)
        self.marcoCargarImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5, rowspan=1)
        # Configura las filas para que se distribuyan uniformemente
        for i in range(3):
            self.marcoCargarImagen.rowconfigure(i, weight=1)
        self.marcoCargarImagen.columnconfigure(0, weight=1)  # La columna se expande
        
        # Crea las etiquetas informativas y el botón
        self.subTituloCargar = ttk.Label(self.marcoCargarImagen, text="Cargar una imagen desde su dispositivo", font=("Arial", 12, "bold"))
        self.indicacionesCargar = ttk.Label(self.marcoCargarImagen, text="Seleccione una imagen para cargarla en la aplicación", font=("Arial", 10))
        self.botonCargar = ttk.Button(self.marcoCargarImagen, text="Cargar Imagen", bootstyle=estiloCargarImg, command=self.cargarImagen)
        
        # Coloca todos los elementos en su posición dentro del marco
        self.subTituloCargar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.indicacionesCargar.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.botonCargar.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

    def crearControlesMostrarModelos(self):
        estiloModelos = "secondary"  # Define el estilo gris para esta sección
        # Crea un marco para los botones de modelos de color
        self.marcoModelos = ttk.Labelframe(self.panelControl, text="Elegir Modelo a mostrar", padding=10, bootstyle=estiloModelos)
        self.marcoModelos.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # Configura 3 columnas para los 3 botones de modelos
        for i in range(3): self.marcoModelos.columnconfigure(i, weight=1)
        for i in range(3):self.marcoModelos.rowconfigure(i, weight=1)
        
        # Crea las etiquetas informativas
        self.subTituloModelos = ttk.Label(self.marcoModelos, text="Modelos de color", font=("Arial", 12, "bold"))
        self.indicacionesModelos = ttk.Label(self.marcoModelos, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        # Crea los tres botones para cada modelo de color
        self.botonModeloRGB = ttk.Button(self.marcoModelos, text="Modelo RGB", bootstyle=estiloModelos, command=self.cargarModeloRGB)
        self.botonModeloHSV = ttk.Button(self.marcoModelos, text="Modelo HSV", bootstyle=estiloModelos, command=self.cargarModeloHSV)
        self.botonModeloCMY = ttk.Button(self.marcoModelos, text="Modelo CMY", bootstyle=estiloModelos, command=self.cargarModeloCMY)

        # Coloca las etiquetas ocupando las 3 columnas
        self.subTituloModelos.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.indicacionesModelos.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca cada botón en una columna diferente
        self.botonModeloRGB.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.botonModeloHSV.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.botonModeloCMY.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
    
    def crearControlesGrisBinarizacion(self):
        estiloConversiones = "success"  # Define el estilo verde para esta sección
        # Crea un marco para los controles de conversión a gris y binarización
        self.marcoConversiones = ttk.Labelframe(self.panelControl, text="Elegir cambio a mostrar", padding=10, bootstyle=estiloConversiones)
        self.marcoConversiones.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        # Configura 2 columnas para distribuir los botones
        for i in range(2): self.marcoConversiones.columnconfigure(i, weight=1)
        for i in range(4):self.marcoConversiones.rowconfigure(i, weight=1)

        # Crea las etiquetas informativas
        self.subTituloConversiones = ttk.Label(self.marcoConversiones, text="Conversion de gris-binario", font=("Arial", 12, "bold"))
        self.indicacionesConversiones = ttk.Label(self.marcoConversiones, text="Seleccione un modelo de color para visualizarlo", font=("Arial", 10))
        
        # Crea los botones para las diferentes conversiones
        self.botonModeloGris = ttk.Button(self.marcoConversiones, text="Convertir a escala de gris", bootstyle=estiloConversiones, command=self.convertirEscalaGris)
        self.botonUmbralFijo = ttk.Button(self.marcoConversiones, text="Binarizar imagen por fijo", bootstyle=estiloConversiones, command=self.binarizarImagenFijo)
        self.botonUmbralAdaptativo = ttk.Button(self.marcoConversiones, text="Binarizar imagen por adaptativo", bootstyle=estiloConversiones, command=self.binarizarImagenAdaptativo)

        # Coloca las etiquetas ocupando ambas columnas
        self.subTituloConversiones.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.indicacionesConversiones.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # El botón de gris ocupa ambas columnas, los de binarización una cada uno
        self.botonModeloGris.grid(row=2, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)
        self.botonUmbralFijo.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.botonUmbralAdaptativo.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)

    def crearControlesHistograma(self):
        estiloHistograma = "danger"  # Define el estilo rojo para esta sección
        # Crea un marco para los controles de histogramas
        self.marcoHistogramas = ttk.Labelframe(self.panelControl, text="Elegir histograma a mostrar", padding=10, bootstyle=estiloHistograma)
        self.marcoHistogramas.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        # Configura 2 columnas para los 2 botones de histogramas
        for i in range(2): self.marcoHistogramas.columnconfigure(i, weight=1)
        for i in range(3):self.marcoHistogramas.rowconfigure(i, weight=1)

        # Crea las etiquetas informativas
        self.subTituloHistogramas = ttk.Label(self.marcoHistogramas, text="Histogramas", font=("Arial", 12, "bold"))
        self.indicacionesHistogramas = ttk.Label(self.marcoHistogramas, text="Seleccione un histograma para visualizarlo", font=("Arial", 10))
        # Crea los botones para los dos tipos de histogramas
        self.botonHistogramaColor = ttk.Button(self.marcoHistogramas, text="Histograma de color", bootstyle=estiloHistograma, command=self.crearHistogramaRGB)
        self.botonHistogramaGris = ttk.Button(self.marcoHistogramas, text="Histograma de gris", bootstyle=estiloHistograma, command=self.crearHistogramaGris)

        # Coloca las etiquetas ocupando ambas columnas
        self.subTituloHistogramas.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.indicacionesHistogramas.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        # Coloca cada botón en una columna diferente
        self.botonHistogramaColor.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.botonHistogramaGris.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

    def crearMuestraResultado(self):
        # Crea un marco en el panel de visualización para mostrar las imágenes
        self.marcoMapa = ttk.Labelframe(self.panelVisualizacion, text="Visualización de la imagen", padding=10, bootstyle="info")
        self.marcoMapa.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Configura las filas para que se distribuyan uniformemente
        self.marcoMapa.rowconfigure(0, weight=1)
        self.marcoMapa.rowconfigure(1, weight=1)
        self.marcoMapa.columnconfigure(0, weight=1)
        # Crea las etiquetas de título y subtítulo
        self.tituloVisualizacion = ttk.Label(self.marcoMapa, text="Visualización de la imagen", font=("Arial", 16, "bold"))
        self.SubImagen = ttk.Label(self.marcoMapa, text="Aquí se mostrará la imagen cargada y sus modelos de color", font=("Arial", 12), anchor="center")
        # Coloca las etiquetas en su posición
        self.tituloVisualizacion.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.SubImagen.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    # MÉTODOS DE FUNCIONALIDADES - Aquí comienzan las funciones que hacen el trabajo real
    def cargarImagen(self):
        # Abre un diálogo para que el usuario seleccione una imagen desde su computadora
        rutaArchivo= filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files")])
        if rutaArchivo:  # Si el usuario seleccionó un archivo
            if self.imagen:  # Si ya había una imagen cargada antes
                # Limpia todos los marcos anteriores para evitar duplicados
                # Verifica si cada marco existe antes de destruirlo
                if hasattr(self, 'marcoGris') and self.marcoGris.winfo_exists():
                    self.marcoGris.destroy()  # Elimina el marco de imagen en gris
                if hasattr(self, 'marcoRGB') and self.marcoRGB.winfo_exists():
                    self.marcoRGB.destroy()  # Elimina el marco del modelo RGB
                if hasattr(self, 'marcoHSV') and self.marcoHSV.winfo_exists():
                    self.marcoHSV.destroy()  # Elimina el marco del modelo HSV
                if hasattr(self, 'marcoCMY') and self.marcoCMY.winfo_exists():
                    self.marcoCMY.destroy()  # Elimina el marco del modelo CMY
                if hasattr(self, 'marcoHistogramaGrises') and self.marcoHistogramaGrises.winfo_exists():
                    self.marcoHistogramaGrises.destroy()  # Elimina el marco del histograma de grises
                if hasattr(self, 'marcoHistograma') and self.marcoHistograma.winfo_exists():
                    self.marcoHistograma.destroy()  # Elimina el marco del histograma RGB
                if hasattr(self, 'marcoBinarizadaFijo') and self.marcoBinarizadaFijo.winfo_exists():
                    self.marcoBinarizadaFijo.destroy()  # Elimina el marco de binarización fija
                if hasattr(self, 'marcoBinarizadaAdaptativo') and self.marcoBinarizadaAdaptativo.winfo_exists():
                    self.marcoBinarizadaAdaptativo.destroy()  # Elimina el marco de binarización adaptativa
                self.panelVisualizacion.yview_moveto(0)  # Mueve el scroll al inicio

            self.imagen = Img(rutaArchivo)  # Crea un objeto Imagen con el archivo seleccionado
            imagenTkinter = self.imagen.iniciarImagen()  # Convierte la imagen para mostrarla en tkinter
            if imagenTkinter:  # Si la conversión fue exitosa
                self.SubImagen.configure(image=imagenTkinter)  # Muestra la imagen en la etiqueta
                self.SubImagen.image = imagenTkinter  # Mantiene una referencia para evitar que se borre
            else: del self.imagen  # Si falló, elimina el objeto imagen
        else:
            # Si el usuario canceló la selección, muestra una advertencia
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")

    def convertirEscalaGris(self):
        # Verifica que haya una imagen cargada antes de proceder
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return  # Sale de la función si no hay imagen
        
        # Crea un nuevo marco para mostrar la imagen en escala de grises
        self.marcoGris = ttk.Labelframe(self.panelVisualizacion, text="Imagen en escala de gris", padding=10, bootstyle="success")
        self.marcoGris.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)  # Lo coloca en la fila 1
        self.marcoGris.columnconfigure(0, weight=1)  # Configura la columna para expandirse
        self.marcoGris.rowconfigure(0, weight=1)  # Configura la fila para expandirse
        # Crea una etiqueta para mostrar la imagen en gris
        self.subImagenGris = ttk.Label(self.marcoGris, text="Imagen en escala de grises", font=("Arial", 16, "bold"))
        self.subImagenGris.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Llama al método de la clase Imagen para convertir a gris
        imagenGrisPillow = self.imagen.obtenerImagenGris()
        if imagenGrisPillow:  # Si la conversión fue exitosa
            self.subImagenGris.configure(image=imagenGrisPillow, anchor="center")  # Muestra la imagen
            self.subImagenGris.image = imagenGrisPillow  # Mantiene la referencia
        else:
            # Si hubo error en la conversión, muestra mensaje de error
            messagebox.showerror("Error", "No se pudo convertir la imagen a escala de grises.")

    def binarizarImagenFijo(self):
        # Verifica que haya una imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        # Verifica que la imagen ya esté convertida a gris (requisito para binarizar)
        elif not hasattr(self, 'marcoGris'):
            messagebox.showwarning("Atención", "Primero convierte la imagen a escala de grises.")
            return
        # Verifica que ya se haya generado el histograma de grises (para elegir buen umbral)
        elif not hasattr(self, 'marcoHistogramaGrises'):
            messagebox.showwarning("Atención", "Requieres tener el histograma de grises para usar un umbral fijo.")
            return

        # Pide al usuario que ingrese el valor del umbral (0-255)
        valorUmbralFijo = simpledialog.askinteger("Umbral Fijo", "Introduce el valor del umbral (0-255):", minvalue=0, maxvalue=255)
        if valorUmbralFijo is not None:  # Si el usuario ingresó un valor
            # Llama al método de binarización con umbral fijo
            imagenBinarizada= self.imagen.umbralizarFijoImagen(valorUmbralFijo)
            # Crea un marco para mostrar la imagen binarizada
            self.marcoBinarizadaFijo = ttk.Labelframe(self.panelVisualizacion, text="Imagen binarizada (Umbral Fijo)", padding=10, bootstyle="success")
            self.marcoBinarizadaFijo.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)  # Fila 2
            self.marcoBinarizadaFijo.columnconfigure(0, weight=1)
            self.marcoBinarizadaFijo.rowconfigure(0, weight=1)
            # Crea etiqueta para mostrar la imagen binarizada
            self.subImagenBinarizadaFijo = ttk.Label(self.marcoBinarizadaFijo, text="Imagen binarizada (Umbral Fijo)", font=("Arial", 16, "bold"))
            self.subImagenBinarizadaFijo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            if imagenBinarizada:  # Si la binarización fue exitosa
                self.subImagenBinarizadaFijo.configure(image=imagenBinarizada, anchor="center")
                self.subImagenBinarizadaFijo.image = imagenBinarizada
            else:
                messagebox.showerror("Error", "No se pudo convertir la imagen a escala de grises.")

    def binarizarImagenAdaptativo(self):
        # Verifica que haya una imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        # Verifica que la imagen ya esté convertida a gris
        elif not hasattr(self, 'marcoGris'):
            messagebox.showwarning("Atención", "Primero convierte la imagen a escala de grises.")
            return
        # Verifica que ya se haya generado el histograma de grises
        elif not hasattr(self, 'marcoHistogramaGrises'):
            messagebox.showwarning("Atención", "Requieres tener el histograma de grises para usar un umbral fijo.")
            return
        # Pide al usuario el valor de la constante para el umbral adaptativo
        valorConstante = simpledialog.askinteger("Constante", "Introduce el valor de la constante (recomendado 2-10, minimo: -15 y maximo 20), si hay mucho ruido pruebe con valores altos:", minvalue=-20, maxvalue=20)
        if valorConstante is not None:  # Si el usuario ingresó un valor
            # Llama al método de binarización con umbral adaptativo
            imagenBinarizada= self.imagen.umbralizarAdaptativoImagen(valorConstante)
            # Crea un marco para mostrar la imagen binarizada con umbral adaptativo
            self.marcoBinarizadaAdaptativo = ttk.Labelframe(self.panelVisualizacion, text="Imagen binarizada (Umbral Adaptativo)", padding=10, bootstyle="success")
            self.marcoBinarizadaAdaptativo.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)  # Fila 3
            self.marcoBinarizadaAdaptativo.columnconfigure(0, weight=1)
            self.marcoBinarizadaAdaptativo.rowconfigure(0, weight=1)
            # Crea etiqueta para mostrar la imagen binarizada
            self.subImagenBinarizadaAdaptativo = ttk.Label(self.marcoBinarizadaAdaptativo, text="Imagen binarizada (Umbral Adaptativo)", font=("Arial", 16, "bold"))
            self.subImagenBinarizadaAdaptativo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            if imagenBinarizada:  # Si la binarización fue exitosa
                self.subImagenBinarizadaAdaptativo.configure(image=imagenBinarizada, anchor="center")
                self.subImagenBinarizadaAdaptativo.image = imagenBinarizada
            else:
                messagebox.showerror("Error", "No se pudo convertir la imagen a escala de grises.")

    def crearHistogramaRGB(self):
        # Verifica que haya una imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        # Crea un marco para mostrar los histogramas RGB
        self.marcoHistograma = ttk.Labelframe(self.panelVisualizacion, text="Histograma RGB (Matplotlib)", padding=10, bootstyle="info")
        self.marcoHistograma.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)  # Fila 4
        # Configura el marco para que se expanda correctamente
        self.marcoHistograma.columnconfigure(0, weight=1); self.marcoHistograma.rowconfigure(1, weight=1)
        # Crea el título del histograma
        ttk.Label(self.marcoHistograma, text="Histograma RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Obtiene los datos del histograma de cada canal de color
        histogramasRGB= self.imagen.histogramaColor()
        # Obtiene las propiedades estadísticas de cada canal (media, entropía, etc.)
        listaValoresRGB= self.imagen.calcularPropiedadesImagenRGB()
        # Define los nombres de los canales de color
        canales = ['Red', 'Green', 'Blue']
        # Crea un histograma separado para cada canal (R, G, B)
        for i, histograma in enumerate(histogramasRGB):
            fig = Figure(figsize=(16,6.5), dpi=100)  # Crea una figura de matplotlib
            ax = fig.add_subplot(1, 1, 1)  # Añade un subplot
            # Crea el gráfico de barras con el color correspondiente al canal
            ax.bar(histograma[0], histograma[1], color= canales[i], alpha=0.7, width=1)
            # Configura las etiquetas y título del gráfico
            ax.set_ylabel("Número de píxeles (Frecuencia)")
            ax.set_xlabel("Intensidad de pixeles")
            ax.set_title("Histograma del canal " + canales[i])
            # Configura la cuadrícula del eje Y
            ax.yaxis.set_major_locator(MultipleLocator(1000))
            ax.xaxis.set_major_locator(MultipleLocator(25))
            ax.yaxis.grid(True, linestyle="--", alpha=0.7)
            # Integra el gráfico en la interfaz de tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.marcoHistograma)
            canvas.draw()  # Dibuja el gráfico
            canvas.get_tk_widget().grid(row=i*2, column=0, sticky="nsew")  # Lo coloca en la interfaz

            # Crea un texto con las propiedades estadísticas del canal
            texto = f"Canal {canales[i]}: Media={listaValoresRGB[i][0]:.2f}, entropia={listaValoresRGB[i][1]:.2f}, Varianza={listaValoresRGB[i][2]:.2f}, asimetria={listaValoresRGB[i][3]:.2f}, energia={listaValoresRGB[i][4]:.2f}"
            # Muestra el texto debajo de cada histograma
            ttk.Label(self.marcoHistograma, text=texto, font=("Arial", 10)).grid(row=i*2+1, column=0, sticky="w", padx=5, pady=2)

    def crearHistogramaGris(self):
        # Verifica que haya una imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return
        # Verifica que la imagen ya esté convertida a escala de grises
        if not hasattr(self, 'marcoGris') or not self.marcoGris.winfo_exists():
            messagebox.showwarning("Atención", "Primero convierte la imagen a escala de grises.")
            return
        # Crea un marco para mostrar el histograma de escala de grises
        self.marcoHistogramaGrises = ttk.Labelframe(self.panelVisualizacion, text="Histograma de escala de gris (Matplotlib)", padding=10, bootstyle="info")
        self.marcoHistogramaGrises.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)  # Fila 5
        # Configura el marco para que se expanda correctamente
        self.marcoHistogramaGrises.columnconfigure(0, weight=1); self.marcoHistogramaGrises.rowconfigure(1, weight=1)
        # Crea el título del histograma
        ttk.Label(self.marcoHistogramaGrises, text="Histograma de escala de gris", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Crea una figura de matplotlib para el histograma
        fig = Figure(figsize=(16, 6), dpi=100)
        ax = fig.add_subplot(1, 1, 1)  # Añade un subplot
        # Obtiene los datos del histograma de la imagen en gris
        histogramaGris = self.imagen.histogramaGris()
        # Crea el gráfico de barras en color gris
        ax.bar(histogramaGris[0], histogramaGris[1], color='gray', alpha=0.7, width=1)
        # Configura las etiquetas y título del gráfico
        ax.set_xlabel("Intensidad de gris")
        ax.set_ylabel("Número de píxeles (Frecuencia)")
        ax.set_title("Histograma de escala de grises");
        # Configura la cuadrícula del eje Y
        ax.yaxis.set_major_locator(MultipleLocator(1000))
        ax.xaxis.set_major_locator(MultipleLocator(25))
        ax.yaxis.grid(True, linestyle="--", alpha=0.7)
        # Integra el gráfico en la interfaz de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHistogramaGrises)
        canvas.draw()  # Dibuja el gráfico
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")  # Lo coloca en la interfaz
        # Obtiene las propiedades estadísticas de la imagen en gris
        listaValoresGris = self.imagen.calcularPropiedadesImagenGris()
        # Crea un texto con las propiedades estadísticas
        texto = f"Canal Gris: Media={listaValoresGris[0]:.2f}, entropia={listaValoresGris[1]:.2f}, Varianza={listaValoresGris[2]}, asimetria={listaValoresGris[3]:.2f}, energia={listaValoresGris[4]:.2f}"
        # Muestra el texto debajo del histograma
        ttk.Label(self.marcoHistogramaGrises, text= texto, font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=2)

    def cargarModeloRGB(self):
        # Verifica que haya una imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Crea un marco para mostrar el modelo RGB
        self.marcoRGB = ttk.Labelframe(self.panelVisualizacion, text="Modelo RGB (Matplotlib)", padding=10, bootstyle="primary")
        self.marcoRGB.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)  # Fila 6
        # Configura el marco para que se expanda correctamente
        self.marcoRGB.columnconfigure(0, weight=1); self.marcoRGB.rowconfigure(1, weight=1)
        # Crea el título del modelo RGB
        ttk.Label(self.marcoRGB, text="Modelo RGB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Separa la imagen en sus tres canales de color (Rojo, Verde, Azul)
        R, G, B = cv2.split(self.imagen.imagenCv)
        # Crea una figura de matplotlib con 3 subplots horizontales
        fig = Figure(figsize=(16, 3.7), dpi=100)
        ax1 = fig.add_subplot(1, 3, 1)  # Subplot para canal R
        ax2 = fig.add_subplot(1, 3, 2)  # Subplot para canal G
        ax3 = fig.add_subplot(1, 3, 3)  # Subplot para canal B
        # Muestra cada canal con su respectivo mapa de color
        ax1.imshow(R, cmap="Reds", vmin=0, vmax=255); ax1.set_title("Canal R"); ax1.axis("off")  # Canal rojo
        ax2.imshow(G, cmap="Greens", vmin=0, vmax=255); ax2.set_title("Canal G"); ax2.axis("off")  # Canal verde
        ax3.imshow(B, cmap="Blues", vmin=0, vmax=255); ax3.set_title("Canal B"); ax3.axis("off")  # Canal azul
        fig.suptitle("Modelo RGB")  # Título general de la figura
        # Integra el gráfico en la interfaz de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marcoRGB)
        canvas.draw()  # Dibuja el gráfico
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")  # Lo coloca en la interfaz

    def cargarModeloHSV(self):
        # Verifica que haya una imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Crea un marco para mostrar el modelo HSV
        self.marcoHSV = ttk.Labelframe(self.panelVisualizacion, text="Modelo HSV (Matplotlib)", padding=10, bootstyle="success")
        self.marcoHSV.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)  # Fila 7
        # Configura el marco para que se expanda correctamente
        self.marcoHSV.columnconfigure(0, weight=1)
        self.marcoHSV.rowconfigure(1, weight=1)

        # Crea el título del modelo HSV
        ttk.Label(self.marcoHSV, text="Modelo HSV", font=("Arial", 16, "bold")).grid( row=0, column=0, sticky="w", padx=5, pady=5)

        # Obtiene la imagen RGB original
        rgb = self.imagen.imagenCv
        # Convierte la imagen de RGB a HSV (Hue, Saturation, Value)
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        # Separa la imagen HSV en sus tres canales
        H, S, V = cv2.split(hsv)
        # Crea una figura de matplotlib con 3 subplots horizontales
        fig = Figure(figsize=(12, 3.7), dpi=100)
        ax1 = fig.add_subplot(1, 3, 1)  # Subplot para canal H (Matiz)
        ax2 = fig.add_subplot(1, 3, 2)  # Subplot para canal S (Saturación)
        ax3 = fig.add_subplot(1, 3, 3)  # Subplot para canal V (Valor/Brillo)
        # Muestra cada canal con su respectivo mapa de color
        im1 = ax1.imshow(H, cmap="hsv", vmin=0, vmax=179)  # Canal H con mapa hsv
        ax1.set_title("Canal H"); ax1.axis("off")
        im2 = ax2.imshow(S, cmap="gray", vmin=0, vmax=255)  # Canal S en escala de grises
        ax2.set_title("Canal S"); ax2.axis("off")
        im3 = ax3.imshow(V, cmap="gray", vmin=0, vmax=255)  # Canal V en escala de grises
        ax3.set_title("Canal V"); ax3.axis("off")

        fig.suptitle("Modelo HSV")  # Título general de la figura
        # Integra el gráfico en la interfaz de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marcoHSV)
        canvas.draw()  # Dibuja el gráfico
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, sticky="nsew")  # Lo coloca en la interfaz

    def cargarModeloCMY(self):
        # Verifica que haya una imagen cargada
        if not self.imagen:
            messagebox.showwarning("Atención", "Primero carga una imagen.")
            return

        # Crea un marco para mostrar el modelo CMY
        self.marcoCMY = ttk.Labelframe(self.panelVisualizacion, text="Modelo CMY (Matplotlib)", padding=10, bootstyle="warning")
        self.marcoCMY.grid(row=8, column=0, sticky="nsew", padx=5, pady=5)  # Fila 8
        # Configura el marco para que se expanda correctamente
        self.marcoCMY.columnconfigure(0, weight=1); self.marcoCMY.rowconfigure(1, weight=1)
        # Crea el título del modelo CMY
        ttk.Label(self.marcoCMY, text="Modelo CMY", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Separa la imagen en sus tres canales RGB
        R, G, B = cv2.split(self.imagen.imagenCv)
        # Convierte RGB a CMY (Cyan, Magenta, Yellow) usando la fórmula: CMY = 255 - RGB
        C = 255 - R; M = 255 - G; Y = 255 - B  # Calcula cada canal CMY
        # Crea una figura de matplotlib con 3 subplots horizontales
        fig = Figure(figsize=(12, 3.7), dpi=100)
        ax1 = fig.add_subplot(1, 3, 1)  # Subplot para canal C (Cian)
        ax2 = fig.add_subplot(1, 3, 2)  # Subplot para canal M (Magenta)
        ax3 = fig.add_subplot(1, 3, 3)  # Subplot para canal Y (Amarillo)
        # Muestra cada canal con su respectivo mapa de color
        ax1.imshow(C, cmap="Blues",   vmin=0, vmax=255); ax1.set_title("Canal C"); ax1.axis("off")  # Canal cian
        ax2.imshow(M, cmap="Purples", vmin=0, vmax=255); ax2.set_title("Canal M"); ax2.axis("off")  # Canal magenta
        ax3.imshow(Y, cmap="Oranges", vmin=0, vmax=255); ax3.set_title("Canal Y"); ax3.axis("off")  # Canal amarillo
        fig.suptitle("Modelo CMY")  # Título general de la figura

        # Integra el gráfico en la interfaz de tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.marcoCMY)
        canvas.draw()  # Dibuja el gráfico
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")  # Lo coloca en la interfaz


# PUNTO DE ENTRADA DEL PROGRAMA
if __name__ == "__main__":
    Interfaz()  # Crea una instancia de la clase Interfaz, lo que inicia la aplicación
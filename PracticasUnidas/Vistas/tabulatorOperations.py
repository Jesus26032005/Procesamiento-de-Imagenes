import ttkbootstrap as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import cv2
from ttkbootstrap.scrolled import ScrolledFrame

class TabulatorOperations(ttk.Frame):
    """
    Clase que representa la pestaña de operaciones aritméticas y lógicas en la interfaz gráfica.
    Hereda de ttk.Frame.
    """
    def __init__(self, parent):
        """
        Inicializa la pestaña de operaciones.
        
        Args:
            parent: Widget padre (contenedor).
        """
        super().__init__(parent)
        
        # Configuración de la cuadrícula principal
        for i in range(1,3): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        # Título de la sección
        self.label_titulo = ttk.Label(self, text="Operaciones aritmeticas y logicas", font=("Arial", 18, "bold"))
        self.label_titulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Crear componentes para cada imagen
        self._crear_componentes_operaciones_img1()
        self._crear_componentes_operaciones_img2()

    def _crear_componentes_operaciones_img1(self):
        """
        Crea y organiza los controles para las operaciones de la imagen principal (Imagen 1).
        Incluye operaciones aritméticas escalares, entre imágenes y lógicas.
        """
        estiloControlesImg = "warning"
        self.marcoControlesImagen1 =ttk.Labelframe(self, text="Controles de imagen principal", padding=5, bootstyle=estiloControlesImg)
        self.marcoControlesImagen1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configuración del grid interno
        for i in range(10):
            self.marcoControlesImagen1.rowconfigure(i, weight=1)
        for j in range(3):
            self.marcoControlesImagen1.columnconfigure(j, weight=1)

        # Subtítulos y etiquetas
        self.subtitulo_controles_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones disponibles para la imagen principal", font=("Arial", 16, "bold"), wraplength=400)
        self.subtitulo_operaciones_aritmeticas_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        
        # Controles aritméticos escalares
        self.campo_entrada_valor_img1 = ttk.Entry(self.marcoControlesImagen1)
        self.boton_sumar_escalar_img1 = ttk.Button(self.marcoControlesImagen1, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_escalar_img1 = ttk.Button(self.marcoControlesImagen1, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_escalar_img1 = ttk.Button(self.marcoControlesImagen1, text="Multiplicar", bootstyle=estiloControlesImg)

        # Controles aritméticos entre imágenes
        self.subtitulo_operaciones_aritmeticas_entre_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_sumar_entre_img1 = ttk.Button(self.marcoControlesImagen1, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_entre_img1 = ttk.Button(self.marcoControlesImagen1, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_entre_img1 = ttk.Button(self.marcoControlesImagen1, text="Multiplicar", bootstyle=estiloControlesImg)

        # Controles lógicos
        self.subtitulo_operaciones_logicas_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones Lógicas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_or_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="OR", bootstyle=estiloControlesImg)
        self.boton_and_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="AND", bootstyle=estiloControlesImg)
        self.boton_not_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="NOT", bootstyle=estiloControlesImg)
        self.boton_xor_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="XOR", bootstyle=estiloControlesImg)

        # Botón extra
        self.boton_extra_img1 = ttk.Button(self.marcoControlesImagen1, text="Extraccion conexas", bootstyle=estiloControlesImg)

        # Posicionamiento en el grid
        self.subtitulo_controles_img1.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_aritmeticas_img1.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.campo_entrada_valor_img1.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.boton_sumar_escalar_img1.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_restar_escalar_img1.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_multiplicar_escalar_img1.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_aritmeticas_entre_img1.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.boton_sumar_entre_img1.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_restar_entre_img1.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_multiplicar_entre_img1.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_logicas_img1.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.boton_or_logico_img1.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_and_logico_img1.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_not_logico_img1.grid(row=7, column=2, sticky="nsew", padx=5, pady=5)
        self.boton_xor_logico_img1.grid(row=8, column=0, sticky="nsew", padx=5, pady=5, columnspan=3)
        self.boton_extra_img1.grid(row=9, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def _crear_componentes_operaciones_img2(self):
        """
        Crea y organiza los controles para las operaciones de la imagen secundaria (Imagen 2).
        Sigue la misma estructura que para la imagen 1 pero con diferente estilo visual.
        """
        estiloControlesImg = "danger"
        self.marcoControlesImagen2 =ttk.Labelframe(self, text="Controles de imagen secundaria", padding=5, bootstyle=estiloControlesImg)
        self.marcoControlesImagen2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configuración del grid interno
        for i in range(10):
            self.marcoControlesImagen2.rowconfigure(i, weight=1)
        for j in range(3):
            self.marcoControlesImagen2.columnconfigure(j, weight=1)

        # Subtítulos y etiquetas
        self.subtitulo_controles_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones disponibles para la imagen secundaria", font=("Arial", 16, "bold"), wraplength=400)
        self.subtitulo_operaciones_aritmeticas_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        
        # Controles aritméticos escalares
        self.campo_entrada_valor_img2 = ttk.Entry(self.marcoControlesImagen2)
        self.boton_sumar_escalar_img2 = ttk.Button(self.marcoControlesImagen2, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_escalar_img2 = ttk.Button(self.marcoControlesImagen2, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_escalar_img2 = ttk.Button(self.marcoControlesImagen2, text="Multiplicar", bootstyle=estiloControlesImg)

        # Controles aritméticos entre imágenes
        self.subtitulo_operaciones_aritmeticas_entre_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_sumar_entre_img2 = ttk.Button(self.marcoControlesImagen2, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_entre_img2 = ttk.Button(self.marcoControlesImagen2, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_entre_img2 = ttk.Button(self.marcoControlesImagen2, text="Multiplicar", bootstyle=estiloControlesImg)

        # Controles lógicos
        self.subtitulo_operaciones_logicas_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones Lógicas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_or_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="OR", bootstyle=estiloControlesImg)
        self.boton_and_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="AND", bootstyle=estiloControlesImg)
        self.boton_not_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="NOT", bootstyle=estiloControlesImg)
        self.boton_xor_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="XOR", bootstyle=estiloControlesImg)

        # Botón extra
        self.boton_extra_img2 = ttk.Button(self.marcoControlesImagen2, text="Extraccion conexas", bootstyle=estiloControlesImg)

        # Posicionamiento en el grid
        self.subtitulo_controles_img2.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_aritmeticas_img2.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.campo_entrada_valor_img2.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.boton_sumar_escalar_img2.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_restar_escalar_img2.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_multiplicar_escalar_img2.grid(row=3, column=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_aritmeticas_entre_img2.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.boton_sumar_entre_img2.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_restar_entre_img2.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_multiplicar_entre_img2.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_operaciones_logicas_img2.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.boton_or_logico_img2.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_and_logico_img2.grid(row=7, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_not_logico_img2.grid(row=7, column=2, sticky="nsew", padx=5, pady=5)
        self.boton_xor_logico_img2.grid(row=8, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.boton_extra_img2.grid(row=9, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def mostrar_resultados_etiquetado_y_contornos(self, imagenNo, num_objetos_4, num_objetos_8, diferencia, labels_4, labels_8, image_color):
        """
        Muestra una ventana emergente con los resultados del análisis de objetos (etiquetado y contornos).
        
        Args:
            imagenNo (int): Número de la imagen (1 o 2).
            num_objetos_4 (int): Cantidad de objetos detectados con vecindad-4.
            num_objetos_8 (int): Cantidad de objetos detectados con vecindad-8.
            diferencia (int): Diferencia entre ambos conteos.
            labels_4 (numpy.ndarray): Imagen etiquetada con vecindad-4.
            labels_8 (numpy.ndarray): Imagen etiquetada con vecindad-8.
            image_color (numpy.ndarray): Imagen original con contornos dibujados.
        """
        ventana_resultados = ttk.Toplevel(self)
        ventana_resultados.title(f"Resultados de Análisis de Objetos - Imagen {'Principal' if imagenNo == 1 else 'Adicional'}")
        ventana_resultados.geometry("1000x800")
            
        # Marco para texto informativo
        marco_texto = ttk.Frame(ventana_resultados, padding=10)
        marco_texto.pack(fill='x', padx=10, pady=5)

        ttk.Label(marco_texto, text="Resultados de Conteo y Comparación", font=("Arial", 18, "bold")).pack(anchor='w')
        ttk.Label(marco_texto, text=f"Número de objetos detectados con vecindad-4: {num_objetos_4}", font=("Arial", 16)).pack(anchor='w')
        ttk.Label(marco_texto, text=f"Número de objetos detectados con vecindad-8: {num_objetos_8}", font=("Arial", 16)).pack(anchor='w')
        ttk.Label(marco_texto, text=f"Diferencia entre vecindad-4 y vecindad-8: {diferencia}", font=("Arial", 16)).pack(anchor='w')

        # Marco para visualizaciones gráficas
        marco_visualizaciones = ttk.Frame(ventana_resultados, padding=10)
        marco_visualizaciones.pack(fill='both', expand=True, padx=10, pady=10)
        marco_visualizaciones.columnconfigure(0, weight=1)
        marco_visualizaciones.columnconfigure(1, weight=1)
        marco_visualizaciones.columnconfigure(2, weight=1)

        def mostrar_figure(marcoPadre, figura, titulo, fila, columna):
            """Helper para mostrar una figura de matplotlib en un marco de tkinter."""
            sub_marco = ttk.Labelframe(marcoPadre, text=titulo, padding=5)
            sub_marco.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

            canvas = FigureCanvasTkAgg(figura, master=sub_marco)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

        # Figura 1: Vecindad-4
        fig1 = Figure(figsize=(4, 4), dpi=100)
        ax1 = fig1.add_subplot(1, 1, 1)
        ax1.imshow(labels_4, cmap='jet')
        ax1.set_title('Etiquetado con Vecindad-4')
        ax1.axis('off')
        fig1.colorbar(ax1.get_images()[0], ax=ax1, shrink=0.8)

        # Figura 2: Vecindad-8
        fig2 = Figure(figsize=(4, 4), dpi=100)
        ax2 = fig2.add_subplot(1, 1, 1)
        ax2.imshow(labels_8, cmap='jet')
        ax2.set_title('Etiquetado con Vecindad-8')
        ax2.axis('off')
        fig2.colorbar(ax2.get_images()[0], ax=ax2, shrink=0.8) 
            
        # Figura 3: Contornos
        fig3 = Figure(figsize=(4, 4), dpi=100)
        ax3 = fig3.add_subplot(1, 1, 1)
        ax3.imshow(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB)) 
        ax3.set_title('Objetos Detectados y Numerados')
        ax3.axis('off')

        mostrar_figure(marco_visualizaciones, fig1, "Visualización Vecindad-4", 0, 0)
        mostrar_figure(marco_visualizaciones, fig2, "Visualización Vecindad-8", 0, 1)
        mostrar_figure(marco_visualizaciones, fig3, "Contornos y Numeración", 0, 2)

    def mostrar_datos_objetos(self, matriz_objetos):
        ventana_resultados = ttk.Toplevel(self)
        ventana_resultados.title("Datos de los Objetos")
        ventana_resultados.geometry("400x300")

        marco_texto = ScrolledFrame(ventana_resultados)
        marco_texto.pack(fill='both', expand=True, padx=10, pady=5)

        ttk.Label(marco_texto, text="Resultados de Conteo y Comparación", font=("Arial", 18, "bold")).pack(anchor='w')

        for i in range(len(matriz_objetos)):
            ttk.Label(marco_texto, text=f"Objeto {matriz_objetos[i][0]}").pack(anchor='w')
            ttk.Label(marco_texto, text=f"Área: {matriz_objetos[i][1]} pixeles").pack(anchor='w')
            ttk.Label(marco_texto, text=f"Perímetro: {matriz_objetos[i][2]} pixeles").pack(anchor='w')
            ttk.Label(marco_texto, text="----------------").pack(anchor='w')

        
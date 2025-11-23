import ttkbootstrap as ttk
from tkinter import simpledialog

class TabulatorFilters(ttk.Frame):
    """
    Clase que representa la pestaña de filtros y ruido en la interfaz gráfica.
    Permite al usuario aplicar diferentes tipos de ruido y filtros a las imágenes cargadas.
    """
    def __init__(self, parent):
        super().__init__(parent)

        for i in range(1,2): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        self.label_titulo = ttk.Label(self, text="Operaciones de ruido y filtros", font=("Arial", 18, "bold"))
        self.label_titulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self._crear_componentes_ruido_filtros_img1()
        self._crear_componentes_ruido_filtros_img2()

    def _crear_componentes_ruido_filtros_img1(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar ruido y filtros
        a la imagen principal (Imagen 1).
        """
        estiloControlesRuidoFiltro = "info"
        self.marco_controles_ruido_filtros_img1 =ttk.Labelframe(self, text="Ruido y Filtros para imagen principal", padding=5, bootstyle=estiloControlesRuidoFiltro)

        self.marco_controles_ruido_filtros_img1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(8): self.marco_controles_ruido_filtros_img1.rowconfigure(i, weight=1)
        self.marco_controles_ruido_filtros_img1.columnconfigure(0, weight=1)

        self.subtitulo_controles_ruido_filtro_Img1 = ttk.Label(self.marco_controles_ruido_filtros_img1, text="Operaciones de ruido y filtros para la imagen principal", font=("Arial", 16, "bold"), wraplength= 400)
        self.subtitulo_agregar_ruido_Img1 = ttk.Label(self.marco_controles_ruido_filtros_img1, text="Agregar ruido a la imagen principal", font=("Arial", 14, "bold"), wraplength=400)
        self.boton_agregar_ruido_sal_y_pimienta_Img1 = ttk.Button(self.marco_controles_ruido_filtros_img1, text="Ruido Sal y Pimienta", bootstyle=estiloControlesRuidoFiltro)
        self.boton_agregar_ruido_gaussiano_Img1 = ttk.Button(self.marco_controles_ruido_filtros_img1, text="Ruido Gaussiano", bootstyle=estiloControlesRuidoFiltro)
        self.subtitulo_aplicar_filtros_Img1 = ttk.Label(self.marco_controles_ruido_filtros_img1, text="Aplicar filtros a la imagen principal", font=("Arial", 14, "bold"), wraplength=400)
        self.lista_tipo_filtros_Img1 = ttk.Combobox(self.marco_controles_ruido_filtros_img1, values=["Lineales", "No lineales", "Avanzados", "Pasa-altas"], state="readonly")
        self.lista_opciones_filtros_Img1 = ttk.Combobox(self.marco_controles_ruido_filtros_img1, values=[])
        self.lista_tipo_filtros_Img1.bind("<<ComboboxSelected>>", self._actualizar_opciones_filtro_img1)

        self.lista_tipo_filtros_Img1.current(0)
        self.lista_opciones_filtros_Img1['values'] = ["Filtro Promediador", "Filtro Promediador Pesado", "Filtro Gaussiano"]
        self.lista_opciones_filtros_Img1['state'] = "readonly"

        self.boton_aplicar_filtro_Img1 = ttk.Button(self.marco_controles_ruido_filtros_img1, text="Aplicar Filtro", bootstyle=estiloControlesRuidoFiltro)
        self.subtitulo_controles_ruido_filtro_Img1.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_agregar_ruido_Img1.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.boton_agregar_ruido_sal_y_pimienta_Img1.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_agregar_ruido_gaussiano_Img1.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.subtitulo_aplicar_filtros_Img1.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.lista_tipo_filtros_Img1.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.lista_opciones_filtros_Img1.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.boton_aplicar_filtro_Img1.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
    def _actualizar_opciones_filtro_img1(self, event):
        """
        Actualiza las opciones del combobox de filtros para la imagen 1
        basado en la categoría de filtro seleccionada.
        
        Args:
            event: Evento de selección del combobox.
        """
        opcionSeleccionada = self.lista_tipo_filtros_Img1.get()
        if opcionSeleccionada == "Lineales":
            opcionesFiltros = ["Filtro Promediador", "Filtro Promediador Pesado", "Filtro Gaussiano"]
        elif opcionSeleccionada == "No lineales":
            opcionesFiltros = ["Filtro de Mediana", "Filtro de Moda", "Filtro de Máximo", "Filtro de Mínimo"]
        elif opcionSeleccionada == "Avanzados":
            opcionesFiltros = ["Filtro Bilateral", "Filtro de Mediana Adaptativa", "Filtro de Media Contraharmonica", "Filtro de Mediana Ponderada"]
        elif opcionSeleccionada == "Pasa-altas":
            opcionesFiltros = ["Filtro de Sobel", "Filtro de Prewitt", "Filtro de Roberts", "Filtro de Canny", "Filtro Kirsch", "Filtro Laplaciano"]

        self.lista_opciones_filtros_Img1.set("")
        self.lista_opciones_filtros_Img1['values'] = opcionesFiltros
        self.lista_opciones_filtros_Img1['state'] = "readonly"

    def _crear_componentes_ruido_filtros_img2(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar ruido y filtros
        a la imagen secundaria (Imagen 2).
        """
        estiloControlesRuidoFiltro = "primary"
        self.marco_controles_ruido_filtros_img2 =ttk.Labelframe(self, text="Ruido y Filtros para imagen secundaria", padding=5, bootstyle=estiloControlesRuidoFiltro )
        self.marco_controles_ruido_filtros_img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(8): self.marco_controles_ruido_filtros_img2.rowconfigure(i, weight=1)
        self.marco_controles_ruido_filtros_img2.columnconfigure(0, weight=1)
        
        self.subtitulo_controles_ruido_filtro_Img2 = ttk.Label(self.marco_controles_ruido_filtros_img2, text="Operaciones de ruido y filtros para la imagen secundaria", font=("Arial", 16, "bold"), wraplength=400)
        self.subtitulo_agregar_ruido_Img2 = ttk.Label(self.marco_controles_ruido_filtros_img2, text="Agregar ruido a la imagen secundaria", font=("Arial", 14, "bold"), wraplength=400)
        self.boton_agregar_ruido_sal_y_pimienta_Img2 = ttk.Button(self.marco_controles_ruido_filtros_img2, text="Ruido Sal y Pimienta", bootstyle="primary")
        self.boton_agregar_ruido_gaussiano_Img2 = ttk.Button(self.marco_controles_ruido_filtros_img2, text="Ruido Gaussiano", bootstyle="primary")
        self.subtitulo_aplicar_filtros_Img2 = ttk.Label(self.marco_controles_ruido_filtros_img2, text="Aplicar filtros a la imagen secundaria", font=("Arial", 14, "bold"), wraplength=400)
        self.lista_tipo_filtros_Img2 = ttk.Combobox(self.marco_controles_ruido_filtros_img2, values=["Lineales", "No lineales", "Avanzados", "Pasa-altas"], state="readonly")
        self.lista_opciones_filtros_Img2 = ttk.Combobox(self.marco_controles_ruido_filtros_img2, values=[])
        self.lista_tipo_filtros_Img2.bind("<<ComboboxSelected>>", self._actualizar_opciones_filtros_Img2)
        self.boton_aplicar_filtro_Img2 = ttk.Button(self.marco_controles_ruido_filtros_img2, text="Aplicar Filtro", bootstyle=estiloControlesRuidoFiltro)
        
        self.lista_tipo_filtros_Img2.current(0)
        self.lista_opciones_filtros_Img2['values'] = ["Filtro Promediador", "Filtro Promediador Pesado", "Filtro Gaussiano"]
        self.lista_opciones_filtros_Img2['state'] = "readonly"
        
        self.subtitulo_controles_ruido_filtro_Img2.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.subtitulo_agregar_ruido_Img2.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.boton_agregar_ruido_sal_y_pimienta_Img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_agregar_ruido_gaussiano_Img2.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.subtitulo_aplicar_filtros_Img2.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.lista_tipo_filtros_Img2.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.lista_opciones_filtros_Img2.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.boton_aplicar_filtro_Img2.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    
    def _actualizar_opciones_filtros_Img2(self, event):
        """
        Actualiza las opciones del combobox de filtros para la imagen 2
        basado en la categoría de filtro seleccionada.
        
        Args:
            event: Evento de selección del combobox.
        """
        opcionSeleccionada = self.lista_tipo_filtros_Img2.get()
        if opcionSeleccionada == "Lineales":
            opcionesFiltros = ["Filtro Promediador", "Filtro Promediador Pesado", "Filtro Gaussiano"]
        elif opcionSeleccionada == "No lineales":
            opcionesFiltros = ["Filtro de Mediana", "Filtro de Moda", "Filtro de Máximo", "Filtro de Mínimo"]
        elif opcionSeleccionada == "Avanzados":
            opcionesFiltros = ["Filtro Bilateral", "Filtro de Mediana Adaptativa", "Filtro de Media Contraharmonica"]
        elif opcionSeleccionada == "Pasa-altas":
            opcionesFiltros = ["Filtro de Sobel", "Filtro de Prewitt", "Filtro de Roberts", "Filtro de Canny", "Filtro Kirsch", "Filtro Laplaciano"]

        self.lista_opciones_filtros_Img2.set("")
        self.lista_opciones_filtros_Img2['values'] = opcionesFiltros
        self.lista_opciones_filtros_Img2['state'] = "readonly"

    def pedir_valor_canny(self):
        """
        Solicita al usuario los valores de umbral mínimo y máximo para el filtro Canny.
        
        Returns:
            tuple: (valor_umbral_minimo, valor_umbral_maximo) ingresados por el usuario.
        """
        valor_umbral_minimo = simpledialog.askinteger("Canny", "Ingrese el valor minimo del umbral (0-255):", minvalue=0, maxvalue=255)
        valor_umbral_maximo = simpledialog.askinteger("Canny", "Ingrese el valor maximo del umbral (0-255):", minvalue=0, maxvalue=255)
        return valor_umbral_minimo, valor_umbral_maximo
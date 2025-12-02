import ttkbootstrap as ttk
from tkinter import simpledialog

class TabulatorBrightness(ttk.Frame):
    """
    Clase que representa la pestaña de ajuste de brillo en la interfaz gráfica.
    Permite al usuario aplicar diferentes tipos de ajuste de brillo a las imágenes cargadas.
    """
    def __init__(self, parent):
        """
        Inicializa la pestaña de brillo.
        
        Args:
            parent: Widget padre.
        """
        super().__init__(parent)

        for i in range(1,3): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        self.label_titulo = ttk.Label(self, text="Operaciones de ajuste de brillo", font=("Arial", 18, "bold"))
        self.label_titulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self._crear_componentes_ajuste_brillo_img1()
        self._crear_componentes_ajuste_brillo_img2()

    def _crear_componentes_ajuste_brillo_img1(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar ajuste de brillo
        a la imagen principal (Imagen 1).
        """
        estiloControlesAjusteBrillo = "info"
        self.marco_controles_ajuste_brillo_img1 = ttk.Labelframe(self, text="Ajuste de brillo para imagen principal", padding=5, bootstyle=estiloControlesAjusteBrillo)
        self.marco_controles_ajuste_brillo_img1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(5): self.marco_controles_ajuste_brillo_img1.rowconfigure(i, weight=1)
        for i in range(2): self.marco_controles_ajuste_brillo_img1.columnconfigure(i, weight=1)

        self.subtitutulo_controles_ajuste_brillo_img1 = ttk.Label(self.marco_controles_ajuste_brillo_img1, text="Métodos de ajuste de brillo para la imagen principal", font=("Arial", 16, "bold"), wraplength= 400)
        self.subtitutulo_controles_ajuste_brillo_img1.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Botones de ajuste de brillo
        self.boton_ecualizacion_uniforme_img1 = ttk.Button(self.marco_controles_ajuste_brillo_img1, text="Ecualización uniforme", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_exponencial_img1 = ttk.Button(self.marco_controles_ajuste_brillo_img1, text="Ecualización exponencial", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_Rayleigh_img1 = ttk.Button(self.marco_controles_ajuste_brillo_img1, text="Ecualización Rayleigh", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_hipercubica_img1 = ttk.Button(self.marco_controles_ajuste_brillo_img1, text="Ecualización hipercúbica", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_logaritmica_hiperbolica_img1 = ttk.Button(self.marco_controles_ajuste_brillo_img1, text="Ecualización logarítmica hiperbólica", bootstyle= estiloControlesAjusteBrillo)
        self.boton_funcion_exponencial_img1 = ttk.Button(self.marco_controles_ajuste_brillo_img1, text="Función exponencial", bootstyle= estiloControlesAjusteBrillo)
        self.boton_correccion_gamma_img1 = ttk.Button(self.marco_controles_ajuste_brillo_img1, text="Corrección gamma", bootstyle= estiloControlesAjusteBrillo)

        # Layout
        self.boton_ecualizacion_uniforme_img1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_exponencial_img1.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_Rayleigh_img1.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_hipercubica_img1.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_logaritmica_hiperbolica_img1.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_funcion_exponencial_img1.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_correccion_gamma_img1.grid(row=4, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)

    def _crear_componentes_ajuste_brillo_img2(self):
        """
        Crea e inicializa los componentes de la interfaz para aplicar ajuste de brillo
        a la imagen secundaria (Imagen 2).
        """
        estiloControlesAjusteBrillo = "primary"
        self.marco_controles_ajuste_brillo_img2 = ttk.Labelframe(self, text="Ajuste de brillo para imagen secundaria", padding=5, bootstyle=estiloControlesAjusteBrillo)
        self.marco_controles_ajuste_brillo_img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(5): self.marco_controles_ajuste_brillo_img2.rowconfigure(i, weight=1)
        for i in range(2): self.marco_controles_ajuste_brillo_img2.columnconfigure(i, weight=1)

        self.subtitutulo_controles_ajuste_brillo_img2 = ttk.Label(self.marco_controles_ajuste_brillo_img2, text="Métodos de ajuste de brillo para la imagen secundaria", font=("Arial", 16, "bold"), wraplength= 400)
        self.subtitutulo_controles_ajuste_brillo_img2.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Botones de ajuste de brillo
        self.boton_ecualizacion_uniforme_img2 = ttk.Button(self.marco_controles_ajuste_brillo_img2, text="Ecualización uniforme", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_exponencial_img2 = ttk.Button(self.marco_controles_ajuste_brillo_img2, text="Ecualización exponencial", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_Rayleigh_img2 = ttk.Button(self.marco_controles_ajuste_brillo_img2, text="Ecualización Rayleigh", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_hipercubica_img2 = ttk.Button(self.marco_controles_ajuste_brillo_img2, text="Ecualización hipercúbica", bootstyle= estiloControlesAjusteBrillo)
        self.boton_ecualizacion_logaritmica_hiperbolica_img2 = ttk.Button(self.marco_controles_ajuste_brillo_img2, text="Ecualización logarítmica hiperbólica", bootstyle= estiloControlesAjusteBrillo)
        self.boton_funcion_exponencial_img2 = ttk.Button(self.marco_controles_ajuste_brillo_img2, text="Función exponencial", bootstyle= estiloControlesAjusteBrillo)
        self.boton_correccion_gamma_img2 = ttk.Button(self.marco_controles_ajuste_brillo_img2, text="Corrección gamma", bootstyle= estiloControlesAjusteBrillo)

        # Layout
        self.boton_ecualizacion_uniforme_img2.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_exponencial_img2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_Rayleigh_img2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_hipercubica_img2.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_ecualizacion_logaritmica_hiperbolica_img2.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.boton_funcion_exponencial_img2.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        self.boton_correccion_gamma_img2.grid(row=4, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)

    def pedir_valor_operacion(self, tipo_ajuste):
        """
        Solicita al usuario un valor numérico necesario para ciertos ajustes de brillo.
        
        Args:
            tipo_ajuste (str): Nombre del ajuste seleccionado.
            
        Returns:
            float: Valor ingresado por el usuario.
        """
        texto = ""
        minimo = 0
        maximo = 0

        if tipo_ajuste == "Ecualización hipercúbica":
            texto = "Ingrese el valor potencia para la ecualización hipercúbica (max:5 min:1): "
            minimo = 1
            maximo = 5
        elif tipo_ajuste == "Función exponencial":
            texto = "Ingrese el valor potencia para la funcion exponencial (max:20 min:1): "
            minimo =1
            maximo = 20
        elif tipo_ajuste == "Corrección gamma":
            texto = "Ingrese el valor gamma para la corrección gamma (max:5 min:0.1): "
            minimo = 0.1
            maximo = 5
        
        valor = simpledialog.askfloat("Valor", texto, parent=self, minvalue=minimo, maxvalue=maximo)
        return valor
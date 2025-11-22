import ttkbootstrap as ttk

class TabulatorOperations(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        for i in range(1,2): self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        self.label_titulo = ttk.Label(self, text="Operaciones aritmeticas y logicas", font=("Arial", 18, "bold"))
        self.label_titulo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self._crear_componentes_operaciones_img1()
        self._crear_componentes_operaciones_img2()

    def _crear_componentes_operaciones_img1(self):
        estiloControlesImg = "warning"
        self.marcoControlesImagen1 =ttk.Labelframe(self, text="Controles de imagen principal", padding=5, bootstyle=estiloControlesImg)
        self.marcoControlesImagen1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(10):
            self.marcoControlesImagen1.rowconfigure(i, weight=1)
        for j in range(3):
            self.marcoControlesImagen1.columnconfigure(j, weight=1)

        self.subtitulo_controles_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones disponibles para la imagen principal", font=("Arial", 16, "bold"), wraplength=400)
        self.subtitulo_operaciones_aritmeticas_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        self.campo_entrada_valor_img1 = ttk.Entry(self.marcoControlesImagen1)
        self.boton_sumar_escalar_img1 = ttk.Button(self.marcoControlesImagen1, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_escalar_img1 = ttk.Button(self.marcoControlesImagen1, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_escalar_img1 = ttk.Button(self.marcoControlesImagen1, text="Multiplicar", bootstyle=estiloControlesImg)

        self.subtitulo_operaciones_aritmeticas_entre_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_sumar_entre_img1 = ttk.Button(self.marcoControlesImagen1, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_entre_img1 = ttk.Button(self.marcoControlesImagen1, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_entre_img1 = ttk.Button(self.marcoControlesImagen1, text="Multiplicar", bootstyle=estiloControlesImg)

        self.subtitulo_operaciones_logicas_img1 = ttk.Label(self.marcoControlesImagen1, text="Operaciones Lógicas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_or_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="OR", bootstyle=estiloControlesImg)
        self.boton_and_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="AND", bootstyle=estiloControlesImg)
        self.boton_not_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="NOT", bootstyle=estiloControlesImg)
        self.boton_xor_logico_img1 = ttk.Button(self.marcoControlesImagen1, text="XOR", bootstyle=estiloControlesImg)

        self.boton_extra_img1 = ttk.Button(self.marcoControlesImagen1, text="Extraccion conexas0", bootstyle=estiloControlesImg)

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
        estiloControlesImg = "danger"
        self.marcoControlesImagen2 =ttk.Labelframe(self, text="Controles de imagen secundaria", padding=5, bootstyle=estiloControlesImg)
        self.marcoControlesImagen2.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(10):
            self.marcoControlesImagen2.rowconfigure(i, weight=1)
        for j in range(3):
            self.marcoControlesImagen2.columnconfigure(j, weight=1)

        self.subtitulo_controles_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones disponibles para la imagen secundaria", font=("Arial", 16, "bold"), wraplength=400)
        self.subtitulo_operaciones_aritmeticas_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        self.campo_entrada_valor_img2 = ttk.Entry(self.marcoControlesImagen2)
        self.boton_sumar_escalar_img2 = ttk.Button(self.marcoControlesImagen2, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_escalar_img2 = ttk.Button(self.marcoControlesImagen2, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_escalar_img2 = ttk.Button(self.marcoControlesImagen2, text="Multiplicar", bootstyle=estiloControlesImg)

        self.subtitulo_operaciones_aritmeticas_entre_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones Aritméticas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_sumar_entre_img2 = ttk.Button(self.marcoControlesImagen2, text="Sumar", bootstyle=estiloControlesImg)
        self.boton_restar_entre_img2 = ttk.Button(self.marcoControlesImagen2, text="Restar", bootstyle=estiloControlesImg)
        self.boton_multiplicar_entre_img2 = ttk.Button(self.marcoControlesImagen2, text="Multiplicar", bootstyle=estiloControlesImg)

        self.subtitulo_operaciones_logicas_img2 = ttk.Label(self.marcoControlesImagen2, text="Operaciones Lógicas entre imágenes", font=("Arial", 14, "bold"))
        self.boton_or_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="OR", bootstyle=estiloControlesImg)
        self.boton_and_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="AND", bootstyle=estiloControlesImg)
        self.boton_not_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="NOT", bootstyle=estiloControlesImg)
        self.boton_xor_logico_img2 = ttk.Button(self.marcoControlesImagen2, text="XOR", bootstyle=estiloControlesImg)

        self.boton_extra_img2 = ttk.Button(self.marcoControlesImagen2, text="Extraccion conexas", bootstyle=estiloControlesImg)

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
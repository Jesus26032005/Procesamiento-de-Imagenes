"""
===============================================================================
                            DERECHOS DE AUTOR
===============================================================================
© 2025 - Práctica 2 Minireto- "Mejoramiento de una imagen"

Autores:
Dominguez Jimenez Ana Andrea
Miranda Ferreyra Uriel
Salas Velazquez Orlando
Martinez Alor Zaddkiel de Jesus
Urbina Garcidueñas Luis Jesus

Materia: Procesamiento De Imagenes
Semestre: Cuarto Semestre
Institución: Escuela Superior de Cómputo, Instituto Politécnico Nacional

Este código es de uso académico y está protegido por derechos de autor.
Prohibida su reproducción parcial o total sin autorización del autor.

Fecha de creación: Noviembre 2025
Versión: 1.0
===============================================================================
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Procesamiento Digital de Imagenes - Mejoraramiento de Imagenes")
        self.root.geometry("1080x720")
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=BOTH, expand=True)
        
        control_frame = ttk.Labelframe(main_frame, text="Controles", padding="10")
        control_frame.pack(fill=X, pady=(0, 10))
        
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=True)
        
        image_frame = ttk.Labelframe(content_frame, text="Imagen", padding="10")
        image_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        histogram_frame = ttk.Labelframe(content_frame, text="Histograma", padding="10")
        histogram_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill=X, pady=5)
        
        ttk.Button(file_frame, text="Cargar Imagen", 
                  command=self.controller.load_image, 
                  bootstyle=PRIMARY).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(file_frame, text="Resetear", 
                  command=self.controller.reset_image, 
                  bootstyle=WARNING).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(file_frame, text="Escala de Grises", 
                  command=self.controller.convert_to_grayscale, 
                  bootstyle=INFO).pack(side=LEFT, padx=(0, 10))
        
        noise_frame = ttk.Frame(control_frame)
        noise_frame.pack(fill=X, pady=5)
        
        ttk.Label(noise_frame, text="Ruido:").pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(noise_frame, text="Sal y Pimienta", 
                  command= lambda: self.controller.add_noise("salt_pepper"), 
                  bootstyle=WARNING).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(noise_frame, text="Gaussiano", 
                  command= lambda: self.controller.add_noise("gaussian"), 
                  bootstyle=WARNING).pack(side=LEFT, padx=(0, 10))
        
        linear_frame = ttk.Frame(control_frame)
        linear_frame.pack(fill=X, pady=5)
        
        ttk.Label(linear_frame, text="Filtros Lineales:").pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(linear_frame, text="Promediador", 
                  command= lambda: self.controller.apply_linear_filter("average"), 
                  bootstyle=SUCCESS).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(linear_frame, text="Promediador Pesado", 
                  command=lambda: self.controller.apply_linear_filter("weighted_average"), 
                  bootstyle=SUCCESS).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(linear_frame, text="Gaussiano", 
                  command=lambda: self.controller.apply_linear_filter("gaussian"), 
                  bootstyle=SUCCESS).pack(side=LEFT, padx=(0, 10))
        
        nonlinear_frame = ttk.Frame(control_frame)
        nonlinear_frame.pack(fill=X, pady=5)
        
        ttk.Label(nonlinear_frame, text="Filtros No Lineales:").pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(nonlinear_frame, text="Mediana", 
                  command= lambda: self.controller.apply_nonlinear_filter("median"), 
                  bootstyle=DANGER).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(nonlinear_frame, text="Moda", 
                  command=lambda: self.controller.apply_nonlinear_filter("mode"), 
                  bootstyle=DANGER).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(nonlinear_frame, text="Maximo", 
                  command= lambda: self.controller.apply_nonlinear_filter("max"), 
                  bootstyle=DANGER).pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(nonlinear_frame, text="Minimo", 
                  command=lambda: self.controller.apply_nonlinear_filter("min"), 
                  bootstyle=DANGER).pack(side=LEFT, padx=(0, 10))
        
        advanced_frame = ttk.Frame(control_frame)
        advanced_frame.pack(fill=X, pady=5)
        
        ttk.Label(advanced_frame, text="Filtros Avanzados:").pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(advanced_frame, text="Bilateral", 
                  command= lambda: self.controller.apply_linear_filter("bilateral"), 
                  bootstyle="light").pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(advanced_frame, text="Mediana Adaptativa", 
                  command= lambda: self.controller.apply_nonlinear_filter("adaptive_median"), 
                  bootstyle="light").pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(advanced_frame, text="Media Contraharmónica", 
                  command=lambda: self.controller.apply_nonlinear_filter("contraharmonic_mean"), 
                  bootstyle="light").pack(side=LEFT, padx=(0, 10))
        
        ttk.Button(advanced_frame, text="Mediana Ponderada", 
                  command=lambda: self.controller.apply_nonlinear_filter("weighted_median"), 
                  bootstyle="light").pack(side=LEFT, padx=(0, 10))
        
        self.image_label = ttk.Label(image_frame, text="Cargue una imagen para comenzar", 
                                   font=("Arial", 12))
        self.image_label.pack(expand=True)
        
        self.histogram_frame = histogram_frame
        self.histogram_canvas = None
    
    def update_image_display(self, photo_image):
        if photo_image:
            self.image_label.configure(image=photo_image)
            self.image_label.image = photo_image
        else:
            self.image_label.configure(image='')
            self.image_label.text = "Error al cargar imagen"
    
    def update_histogram(self, histograms):
        if self.histogram_canvas:
            self.histogram_canvas.get_tk_widget().destroy()
        
        if histograms:
            from Utilidades.Histograma import HistogramUtils
            fig = HistogramUtils.plot_histogram(histograms)
            self.histogram_canvas = FigureCanvasTkAgg(fig, self.histogram_frame)
            self.histogram_canvas.draw()
            self.histogram_canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
    
    def get_file_path(self):
        return filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
import ttkbootstrap as ttk  
from ttkbootstrap.constants import *  
from .tabulatorOperations import TabulatorOperations
from .tabulatorImage import TabulatorImage

import cv2  
class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg")
        self.title("Procesamiento de Imagenes - Practicas minireto")
        self.state('zoomed')
        self.control_tabulator = None
        self.crear_componentes()

    def crear_componentes(self):
        self.control_tabulator = ttk.Notebook(self)
        self.tabulator_main = TabulatorImage(self.control_tabulator)
        self.tabulator_operations = TabulatorOperations(self.control_tabulator)
        
        self.control_tabulator.add(self.tabulator_main, text="Practica Principal")
        self.control_tabulator.add(self.tabulator_operations, text="Operaciones con Imagenes")
        
        self.control_tabulator.pack(fill=BOTH, expand=True)




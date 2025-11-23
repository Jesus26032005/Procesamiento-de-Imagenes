from Controladores.ImageController import ImageController
from Vistas.mainWindow import MainWindow
from Modelos.ImagenModel import ImageModel

"""
Módulo principal de la aplicación.
Inicializa los componentes MVC (Modelo, Vista, Controlador) y arranca la aplicación.
"""

def main():
    """
    Función principal que inicia la aplicación.
    Crea las instancias de la vista, el modelo y el controlador, y comienza el bucle principal.
    """
    root = MainWindow()
    modelo = ImageModel()
    controlador = ImageController(model=modelo, view=root) 
    root.mainloop()

if __name__ == "__main__":
    main()
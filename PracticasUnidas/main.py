"""
Módulo principal de la aplicación de Procesamiento de Imágenes.

Este módulo inicializa la aplicación configurando la vista principal (MainWindow),
el modelo de datos (ImageModel) y el controlador (ImageController).
"""

from Controladores.ImageController import ImageController
from Vistas.mainWindow import MainWindow
from Modelos.ImagenModel import ImageModel

def main():
    """
    Función principal que arranca la aplicación.
        
    Pasos:
    1. Instancia la vista principal (MainWindow).
    2. Instancia el modelo de datos (ImageModel).
    3. Instancia el controlador (ImageController) conectando la vista y el modelo.
    4. Inicia el bucle principal de la interfaz gráfica (mainloop).
    """
    # Crear la instancia de la ventana principal (Vista)
    root = MainWindow()
    
    # Crear la instancia del modelo de datos (Modelo)
    modelo = ImageModel()
    
    # Crear la instancia del controlador, inyectando dependencias de modelo y vista
    controlador = ImageController(model=modelo, view=root) 
    
    # Iniciar el bucle de eventos de la interfaz gráficaz
    root.mainloop()

if __name__ == "__main__":
    main()
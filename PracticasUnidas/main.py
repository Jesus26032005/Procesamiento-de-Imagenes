from Controladores.ImageController import ImageController
from Vistas.mainWindow import MainWindow
from Modelos.ImagenModel import ImageModel

def main():
    root = MainWindow()
    modelo = ImageModel()
    controlador = ImageController(model=modelo, view=root) 
    root.mainloop()

if __name__ == "__main__":
    main()
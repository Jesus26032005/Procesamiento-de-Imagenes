from Controller.ImageController import ImageController
from View.mainWindow import MainWindow
from Model.ImagenModel import ImageModel

def main():
    root = MainWindow()
    modelo = ImageModel()
    controlador = ImageController(model=modelo, view=root) 
    root.mainloop()

if __name__ == "__main__":
    main()
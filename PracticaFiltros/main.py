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


from Controladores.Control_Imagen import ImageController

def main():
    root = ttk.Window(
        title="Procesamiento de Imagenes",
        themename="darkly",
        size=(1920, 1080),
        resizable=(True, True)
    )
    
    app = ImageController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
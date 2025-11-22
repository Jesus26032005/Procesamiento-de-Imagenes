import ttkbootstrap as ttk

class TabulatorOperations(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._crear_componentes()

    def _crear_componentes(self):
        label = ttk.Label(self, text="Contenido del Tabulador de Operaciones", font=("Helvetica", 16))
        label.pack(pady=20)
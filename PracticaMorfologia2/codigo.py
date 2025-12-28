import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk

class DetectorFlechaFiltros:
    def __init__(self, root):
        self.root = root
        self.root.title("Ejemplo de aplicación de MM, TF y diversas técnicas de PDI")
        self.root.geometry("900x800")
        self.root.configure(bg="#1a1a1a")

        self.pasos = {}

        # --- Interfaz ---
        tk.Label(root, text="DETECTOR DE FLECHA PELIGROSA EN TRANSITO", font=("Arial", 16, "bold"),
                 bg="#1a1a1a", fg="#2ecc71").pack(pady=20)

        self.btn_cargar = tk.Button(root, text="Cargar Imagen y Ejecutar", command=self.procesar,
                                    bg="#2ecc71", fg="black", font=("Arial", 12, "bold"), width=30)
        self.btn_cargar.pack(pady=10)

        self.lbl_final = tk.Label(root, bg="#2c3e50", relief="sunken")
        self.lbl_final.pack(pady=20, padx=20, expand=True, fill="both")

        self.btn_detalles = tk.Button(root, text="Ver detalles", command=self.abrir_detalles,
                                      state="disabled", bg="#f1c40f", fg="black", font=("Arial", 12, "bold"), width=30)
        self.btn_detalles.pack(pady=20)

    def procesar(self):
        ruta = filedialog.askopenfilename()
        if not ruta: return

        img = cv2.imread(ruta)
        if img is None: return

        # --- 1. PROCESAMIENTO FRECUENCIAL (TF) ---
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Calcular la FFT
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f) # Centrar bajas frecuencias
        # Espectro de magnitud (log para visualización)
        espectro = 20 * np.log(np.abs(fshift) + 1)
        espectro_vis = cv2.normalize(espectro, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # --- 2. PROCESAMIENTO ESPACIAL Y MORFOLÓGICO ---
        # Filtro Espacial: Suavizado
        blur = cv2.GaussianBlur(img, (7, 7), 0)

        # Segmentación de Color: Máscara Amarilla
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask_yellow = cv2.inRange(hsv, np.array([15, 100, 100]), np.array([35, 255, 255]))

        # MM: CIERREpara el Rombo
        kernel_cierre = np.ones((15, 15), np.uint8)
        rombo_solido = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel_cierre)

        # Umbralización Inversa: Detección de Negros
        _, mask_dark = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

        # Operación Lógica AND: Aislamiento
        flecha_aislada = cv2.bitwise_and(mask_dark, mask_dark, mask=rombo_solido)

        # MM: APERTURA para limpieza
        kernel_limpia = np.ones((3, 3), np.uint8)
        flecha_final = cv2.morphologyEx(flecha_aislada, cv2.MORPH_OPEN, kernel_limpia)

        # --- 3. DETECCIÓN ---
        res_img = img.copy()
        contornos, _ = cv2.findContours(flecha_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contornos:
            # Seleccionar solo el contorno más grande (me detectaba otras cosas)
            c_principal = max(contornos, key=cv2.contourArea)
            if cv2.contourArea(c_principal) > 300:
                x, y, w, h = cv2.boundingRect(c_principal)
                cv2.rectangle(res_img, (x, y), (x + w, y + h), (0, 255, 0), 4)

        # Guardamos los pasos
        self.pasos = {
            "A. Imagen Original": img,
            "B. Transformada de Fourier (Espectro)": espectro_vis,
            "C. Filtro Gaussiano (Espacial)": blur,
            "D. Morfología: Cierre (Rombo)": rombo_solido,
            "E. Umbral Inverso (Negros)": mask_dark,
            "F. Filtro Lógico: Intersección AND": flecha_aislada,
            "G. Morfología: Apertura (Limpieza)": flecha_final,
            "H. Resultado Final": res_img
        }

        self.mostrar_img(res_img, self.lbl_final, (700, 450))
        self.btn_detalles.config(state="normal")

    def abrir_detalles(self):
        v = Toplevel(self.root)
        v.title("Detalles del Procesamiento")
        v.geometry("1200x900")
        v.configure(bg="#222")

        for i, (titulo, img) in enumerate(self.pasos.items()):
            frame = tk.Frame(v, bd=1, relief="solid", bg="#333")
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            lbl = tk.Label(frame, bg="#222")
            lbl.pack()
            self.mostrar_img(img, lbl, (350, 250))
            tk.Label(frame, text=titulo, font=("Arial", 10, "bold"), bg="#333", fg="white").pack(pady=5)

    def mostrar_img(self, cv_img, label, size):
        img_res = cv2.resize(cv_img, size)
        color = cv2.COLOR_BGR2RGB if len(img_res.shape) == 3 else cv2.COLOR_GRAY2RGB
        img_tk = ImageTk.PhotoImage(
            Image.fromarray(cv2.cvtColor(img_res, color) if len(img_res.shape) == 3 else img_res))
        label.configure(image=img_tk)
        label.image = img_tk

if __name__ == "__main__":
    app = DetectorFlechaFiltros(tk.Tk())
    app.root.mainloop()
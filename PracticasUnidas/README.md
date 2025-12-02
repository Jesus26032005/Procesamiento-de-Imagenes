# Procesamiento de Imágenes - Prácticas Unidas

Este proyecto es una aplicación de escritorio completa para el procesamiento de imágenes, desarrollada en Python utilizando `tkinter` (con `ttkbootstrap` para el diseño) y `OpenCV`. Integra múltiples prácticas y funcionalidades en una sola interfaz unificada, siguiendo el patrón de diseño Modelo-Vista-Controlador (MVC).

## Descripción

La aplicación permite cargar imágenes, visualizarlas y aplicar una amplia gama de operaciones de procesamiento digital de imágenes. Desde operaciones básicas como conversión a escala de grises y binarización, hasta técnicas avanzadas de filtrado, segmentación y ajuste de brillo/contraste.

## Características Principales

*   **Interfaz Gráfica Moderna:** Utiliza `ttkbootstrap` para una apariencia limpia y profesional (tema "cyborg").
*   **Visualización en Tiempo Real:** Muestra la imagen original y la modificada lado a lado.
*   **Histogramas:** Generación automática de histogramas (RGB y Gris) para analizar la distribución de intensidades.
*   **Operaciones Básicas:**
    *   Carga y guardado de imágenes.
    *   Conversión a escala de grises.
    *   Binarización (Umbral fijo y Otsu).
*   **Operaciones Aritméticas y Lógicas:**
    *   Suma, resta, multiplicación (escalar y entre imágenes).
    *   Operaciones lógicas AND, OR, XOR, NOT.
*   **Filtros y Ruido:**
    *   Agregar ruido (Sal y Pimienta, Gaussiano).
    *   Filtros Lineales (Promediador, Gaussiano).
    *   Filtros No Lineales (Mediana, Moda, Máximo, Mínimo).
    *   Filtros Avanzados (Bilateral, Mediana Adaptativa, etc.).
    *   Detección de Bordes (Sobel, Prewitt, Roberts, Canny, Laplaciano, Kirsch).
*   **Segmentación:**
    *   Métodos de umbralización (Otsu, Entropía de Kapur, Mínimo del histograma, Media, Dos umbrales, Umbral de banda).
    *   Segmentación específica para detección de moho.
*   **Ajuste de Brillo y Contraste:**
    *   Ecualización de histograma (Uniforme, Exponencial, Rayleigh, Hipercúbica, Logarítmica).
    *   Corrección Gamma.
*   **Análisis de Objetos:**
    *   Etiquetado de componentes conexos (Vecindad-4 vs Vecindad-8).
    *   Conteo de objetos y visualización de contornos.

## Estructura del Proyecto (MVC)

El código está organizado para facilitar la mantenibilidad y escalabilidad:

*   **`main.py`**: Punto de entrada de la aplicación. Inicializa los componentes principales.
*   **`Controladores/`**:
    *   `ImageController.py`: Gestiona la lógica de la aplicación, comunicando la Vista con el Modelo.
*   **`Modelos/`**:
    *   `ImagenModel.py`: Gestiona los datos de las imágenes y el estado de la aplicación.
*   **`Vistas/`**:
    *   `mainWindow.py`: Ventana principal y disposición general.
    *   `tabulatorImage.py`: Pestaña de operaciones básicas y carga.
    *   `tabulatorOperations.py`: Pestaña de operaciones aritméticas y lógicas.
    *   `tabulatorFilters.py`: Pestaña de filtros y ruido.
    *   `tabulatorSegmentation.py`: Pestaña de segmentación.
    *   `tabulatorbrightness.py`: Pestaña de brillo y contraste.
*   **`Utilidades/`**:
    *   `ProcesadorImagen.py`: Clase estática con la implementación de todos los algoritmos de procesamiento (OpenCV, NumPy).
    *   `ImagenData.py`: Estructura de datos para manejar la información de la imagen.

## Requisitos

Para ejecutar este proyecto, necesitas tener instalado Python y las siguientes librerías:

```bash
pip install opencv-python numpy pillow ttkbootstrap matplotlib scipy
```

## Uso

1.  Ejecuta el archivo principal:
    ```bash
    python main.py
    ```
2.  Usa la pestaña "Práctica Principal" para cargar una imagen (Imagen 1 o Imagen 2).
3.  Navega por las pestañas ("Operaciones", "Filtros", "Segmentación", "Brillo") para aplicar las diferentes transformaciones.
4.  Los resultados se mostrarán inmediatamente en el panel de visualización.
5.  Puedes guardar la imagen resultante usando los botones de guardar en la pestaña principal.

## Autor

Desarrollado como parte de las prácticas de la asignatura de Procesamiento de Imágenes.
Autor: Martinez Alor Zaddkiel de Jesus
Semestre: Cuarto semestre
Institucion: Instituto Politecnico Nacional-ESCOM
Version: 1.0

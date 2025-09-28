import matplotlib.pyplot as plt
import numpy as np

# Generar datos aleatorios de una distribución normal
datos = np.random.randn(1000)

# Crear el histograma
plt.hist(datos)

# Mostrar el gráfico
plt.show()

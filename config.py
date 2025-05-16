# config.py

import os

# Carpeta donde se guardarán los archivos de datos
CARPETA_DATOS = "data"

# Asegurarse de que la carpeta exista
if not os.path.exists(CARPETA_DATOS):
    os.makedirs(CARPETA_DATOS)

# Ruta completa al archivo Excel
RUTA_DATOS_EXCEL = os.path.join(CARPETA_DATOS, "registros.xlsx")

# Puedes agregar más configuraciones globales aquí más adelante (colores, estilos, etc.)

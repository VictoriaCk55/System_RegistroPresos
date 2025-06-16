import os

CARPETA_DATOS = "data"

if not os.path.exists(CARPETA_DATOS):
    os.makedirs(CARPETA_DATOS)

RUTA_DATOS_EXCEL = os.path.join(CARPETA_DATOS, "registros.xlsx")


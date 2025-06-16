import pandas as pd
import os

ARCHIVO_DATOS = "data/registros.xlsx"

def leer_datos():
    """Lee los datos de los arrestados desde el archivo de Excel."""
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_excel(ARCHIVO_DATOS)
    else:
        return pd.DataFrame()

def guardar_datos(df):
    """Guarda los datos de los arrestados en el archivo de Excel."""
    if not os.path.exists("data"):
        os.makedirs("data") 
    df.to_excel(ARCHIVO_DATOS, index=False)

def agregar_registro(datos):
    """Agrega un nuevo registro de arrestado al archivo de datos."""
    df = leer_datos()
    df_nuevo = pd.DataFrame([datos])
    df = pd.concat([df, df_nuevo], ignore_index=True)
    guardar_datos(df)

def obtener_registros():
    """Obtiene todos los registros de arrestados."""
    return leer_datos()

def eliminar_registro(index):
    """Elimina un registro por su índice."""
    df = leer_datos()
    df = df.drop(index)
    guardar_datos(df)

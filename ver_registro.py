from tkinter import filedialog
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

from config import RUTA_DATOS_EXCEL

def crear_ventana_ver_registros():
    if not os.path.exists(RUTA_DATOS_EXCEL):
        messagebox.showinfo("Información", "Aún no hay registros guardados.")
        return

    ventana = tk.Toplevel()
    ventana.title("Ver Registro de Detenidos")
    ventana.geometry("1200x600")
    ventana.configure(bg="#f0f0f0")

    frame_busqueda = tk.Frame(ventana, bg="#f0f0f0")
    frame_busqueda.pack(pady=10)
    tk.Label(frame_busqueda, text="Buscar por nombre o CI:", bg="#f0f0f0", font=("Segoe UI", 10)).pack(side="left", padx=5)
    entrada_busqueda = tk.Entry(frame_busqueda, width=40, font=("Segoe UI", 10))
    entrada_busqueda.pack(side="left", padx=5)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = [
        "Fecha y Hora de Ingreso", "Fecha y Hora de Salida", "Motivo de la Detención",
        "Nombre del Arrestado", "Edad", "Ocupación", "CI", "Nombre del Funcionario Policial",
        "Unidad", "Estado Físico del Arrestado", "Descripción de Objetos del Arrestado",
        "Lugar donde fue Arrestado", "Nombre del Denunciante", "Imagen"
    ]

    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white", foreground="black", fieldbackground="white")
    estilo.map("Treeview", background=[('selected', '#0078D7')])

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

    ancho_columnas = {
        "Fecha y Hora de Ingreso": 150, "Fecha y Hora de Salida": 150, "Motivo de la Detención": 200,
        "Nombre del Arrestado": 150, "Edad": 50, "Ocupación": 120, "CI": 100,
        "Nombre del Funcionario Policial": 150, "Unidad": 100, "Estado Físico del Arrestado": 150,
        "Descripción de Objetos del Arrestado": 200, "Lugar donde fue Arrestado": 150,
        "Nombre del Denunciante": 150, "Imagen": 100
    }

    for col in columnas:
        tabla.heading(col, text=col, anchor="center")
        tabla.column(col, width=ancho_columnas.get(col, 120), anchor="center")

    tabla.pack(fill="both", expand=True)
    scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scrollbar_y.pack(side="right", fill="y")
    tabla.configure(yscrollcommand=scrollbar_y.set)

    def cargar_datos(df):
        tabla.delete(*tabla.get_children())
        for _, fila in df.iterrows():
            tabla.insert("", "end", values=list(fila))

    def actualizar_tabla():
        try:
            df = pd.read_excel(RUTA_DATOS_EXCEL)
            cargar_datos(df)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")

    def buscar():
        texto = entrada_busqueda.get().lower()
        try:
            df = pd.read_excel(RUTA_DATOS_EXCEL)
            df_filtrado = df[df["Nombre del Arrestado"].str.lower().str.contains(texto) | df["CI"].astype(str).str.contains(texto)]
            cargar_datos(df_filtrado)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {str(e)}")

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar", "Por favor selecciona un registro para eliminar.")
            return
        index = tabla.index(seleccion[0])
        try:
            df = pd.read_excel(RUTA_DATOS_EXCEL)
            df.drop(index, inplace=True)
            df.to_excel(RUTA_DATOS_EXCEL, index=False)
            actualizar_tabla()
            messagebox.showinfo("Eliminado", "Registro eliminado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {str(e)}")

    def modificar_registro():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Modificar", "Por favor selecciona un registro.")
            return

        valores = tabla.item(seleccion[0], "values")
        ventana_modificar = tk.Toplevel(ventana)
        ventana_modificar.title("Modificar Registro")
        ventana_modificar.geometry("800x600")
        ventana_modificar.configure(bg="#f0f0f0")

        entradas = []
        for i, campo in enumerate(columnas):
            tk.Label(ventana_modificar, text=campo, bg="#f0f0f0", font=("Segoe UI", 10)).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            if campo in ["Motivo de la Detención", "Descripción de Objetos del Arrestado", "Lugar donde fue Arrestado"]:
                entrada = tk.Text(ventana_modificar, width=50, height=3, font=("Segoe UI", 10))
                entrada.insert("1.0", valores[i])
            else:
                entrada = tk.Entry(ventana_modificar, width=60, font=("Segoe UI", 10))
                entrada.insert(0, valores[i])
            entrada.grid(row=i, column=1, padx=5, pady=5)
            entradas.append(entrada)

        def guardar_cambios_modificados():
            nuevos_valores = []
            for entrada, campo in zip(entradas, columnas):
                if campo in ["Motivo de la Detención", "Descripción de Objetos del Arrestado", "Lugar donde fue Arrestado"]:
                    nuevos_valores.append(entrada.get("1.0", "end").strip())
                else:
                    nuevos_valores.append(entrada.get().strip())
            tabla.item(seleccion[0], values=nuevos_valores)

            filas = tabla.get_children()
            nuevos_datos = [tabla.item(fila)["values"] for fila in filas]
            df_modificado = pd.DataFrame(nuevos_datos, columns=columnas)
            df_modificado.to_excel(RUTA_DATOS_EXCEL, index=False)

            messagebox.showinfo("Guardado", "Cambios guardados exitosamente.")
            ventana_modificar.destroy()

        tk.Button(ventana_modificar, text="💾 Guardar Cambios", command=guardar_cambios_modificados,
                  bg="#4CAF50", fg="white", width=20, font=("Segoe UI", 10, "bold")).grid(row=len(columnas), column=1, pady=10)

    def mostrar_reporte():
        try:
            df = pd.read_excel(RUTA_DATOS_EXCEL)
            if df.empty:
                messagebox.showinfo("Reporte", "No hay datos disponibles para el reporte.")
                return

            df["Fecha y Hora de Ingreso"] = pd.to_datetime(df["Fecha y Hora de Ingreso"])
            df["Fecha"] = df["Fecha y Hora de Ingreso"].dt.date
            resumen = df.groupby(["Fecha", "Motivo de la Detención"]).size().reset_index(name="Número de Arrestos")

            ventana_reporte = tk.Toplevel(ventana)
            ventana_reporte.title("Reporte de Arrestos")
            ventana_reporte.geometry("1000x700")
            ventana_reporte.configure(bg="#f0f0f0")

            frame_tabla_reporte = tk.Frame(ventana_reporte)
            frame_tabla_reporte.pack(fill="both", expand=True, padx=10, pady=10)

            tabla_reporte = ttk.Treeview(frame_tabla_reporte, columns=["Fecha", "Motivo", "Número de Arrestos"], show="headings")
            tabla_reporte.heading("Fecha", text="Fecha")
            tabla_reporte.heading("Motivo", text="Motivo de la Detención")
            tabla_reporte.heading("Número de Arrestos", text="Cantidad")
            for _, fila in resumen.iterrows():
                tabla_reporte.insert("", "end", values=list(fila))
            tabla_reporte.pack(fill="both", expand=True)

            frame_grafico = tk.Frame(ventana_reporte)
            frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

            totales = df["Motivo de la Detención"].value_counts()
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(totales.values, labels=totales.index, autopct="%1.1f%%", colors=plt.get_cmap("tab20").colors)
            ax.set_title("Distribución Total de Arrestos por Motivo")
            canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {str(e)}")

    tabla.bind("<Double-1>", lambda e: modificar_registro())

    frame_botones = tk.Frame(ventana, bg="#f0f0f0")
    frame_botones.pack(pady=10)
    tk.Button(frame_botones, text="📊 Ver Reporte", command=mostrar_reporte, width=15, bg="#673AB7", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botones, text="🖨 Exportar PDF", command=lambda: messagebox.showinfo("Función no implementada", "Exportar PDF está pendiente."),
              width=18, bg="#009688", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botones, text="🔍 Buscar", command=buscar, width=15, bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botones, text="⟳ Actualizar", command=actualizar_tabla, width=15, font=("Segoe UI", 10)).pack(side="left", padx=5)
    tk.Button(frame_botones, text="✏️ Modificar", command=modificar_registro, width=15, bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botones, text="🚩 Eliminar", command=eliminar, width=15, bg="#F44336", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botones, text="❌ Salir", command=ventana.destroy, width=15, bg="#9E9E9E", fg="white", font=("Segoe UI", 10)).pack(side="left", padx=5)

    actualizar_tabla()

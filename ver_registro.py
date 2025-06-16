import os
import sys
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import platform
import subprocess
from datetime import datetime
from tkinter import filedialog, messagebox, ttk 
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from config import RUTA_DATOS_EXCEL

def rutas(ruta_relativa):
        try:
            rutabase=sys._MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase, ruta_relativa)

def obtener_hoja_actual():
    return seleccion_anio.get()

def crear_ventana_ver_registros():
    if not os.path.exists(RUTA_DATOS_EXCEL):
        messagebox.showinfo("Información", "Aún no hay registros guardados.")
        return

    ventana = tk.Toplevel()
    ventana.title("Ver Registro de Arrestados y Aprehendidos")
    ventana.state("zoomed")
    ventana.configure(bg="#e6edd8")
    ruta = rutas(r"logo.ico")
    ventana.iconbitmap(ruta)

    frame_busqueda = tk.Frame(ventana, bg="#e6edd8")
    frame_busqueda.pack(pady=10)

    tk.Label(frame_busqueda, text="Buscar por nombre o CI:", bg="#e6edd8", font=("Segoe UI", 12)).pack(side="left", padx=5)

    entrada_busqueda = tk.Entry(frame_busqueda, width=40, font=("Segoe UI", 12))
    entrada_busqueda.pack(side="left", padx=5)

    tk.Label(frame_busqueda, text="Año:", bg="#e6edd8", font=("Segoe UI", 12)).pack(side="left", padx=5)
    global seleccion_anio
    seleccion_anio = ttk.Combobox(frame_busqueda, state="readonly", font=("Segoe UI", 12), width=6)
    seleccion_anio.pack(side="left", padx=5)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = [
        "Nombre del Arrestado", "CI", "Edad", "Ocupación", "Fecha y Hora de Ingreso", "Motivo de la Detención", "Estado Físico del Arrestado",
        "Nombre del Funcionario Policial", "Unidad", "Descripción de Objetos del Arrestado", "Lugar donde fue Arrestado", "Nombre del Denunciante", "Fecha y Hora de Salida", "Imagen"
    ]

    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white", foreground="black", fieldbackground="white")
    estilo.map("Treeview", background=[('selected', "#7DB21C")])

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")
    ancho_columnas = {
        "Nombre del Arrestado": 150, "CI": 100, "Edad": 50, "Ocupación": 120, "Fecha y Hora de Ingreso": 150, "Motivo de la Detención": 200, "Estado Físico del Arrestado": 150, "Nombre del Funcionario Policial": 150, "Unidad": 100, "Descripción de Objetos del Arrestado": 200, "Lugar donde fue Arrestado": 150, "Nombre del Denunciante": 150, "Fecha y Hora de Salida": 150, "Imagen": 100
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
        hoja = obtener_hoja_actual()
        try:
            df = pd.read_excel(RUTA_DATOS_EXCEL, sheet_name=hoja)
            columnas_existentes = [col for col in columnas if col in df.columns]
            df = df[columnas_existentes]
            cargar_datos(df)
        except ValueError:
            messagebox.showinfo("Información", f"No hay registros para el año {hoja}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")

    def buscar():
        texto = entrada_busqueda.get().lower()
        try:
            hoja = obtener_hoja_actual()
            try:
                df = pd.read_excel(RUTA_DATOS_EXCEL, sheet_name=hoja)
                columnas_existentes = [col for col in columnas if col in df.columns]
                df = df[columnas_existentes]
                df_filtrado = df[df["Nombre del Arrestado"].str.lower().str.contains(texto) | df["CI"].astype(str).str.contains(texto)]
                cargar_datos(df_filtrado)
            except ValueError:
                messagebox.showinfo("Información", f"No hay registros para el año {hoja}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {str(e)}")
    
    btn_buscar = tk.Button(frame_busqueda, text="🔍 Buscar", command=buscar, bg="#4CB6EB", fg="white", font=("Segoe UI", 10, "bold"))
    btn_buscar.pack(side="left", padx=5)

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar", "Por favor selecciona un registro para eliminar.", parent=ventana)
            return
        if not messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar el registro seleccionado?", parent=ventana):
            return
    
        index = tabla.index(seleccion[0])
        hoja = obtener_hoja_actual()
        try:
            excel = pd.read_excel(RUTA_DATOS_EXCEL, sheet_name=None)
            df = excel.get(hoja, pd.DataFrame())

            if index >= len(df):
                messagebox.showerror("Error", "Índice inválido. No se pudo eliminar.", parent=ventana)
                return
            df = df.drop(index).reset_index(drop=True)  

            excel[hoja] = df  
                 
            with pd.ExcelWriter(RUTA_DATOS_EXCEL, engine='openpyxl') as writer:
                for hoja_nombre, df_hoja in excel.items():
                    df_hoja.to_excel(writer, sheet_name=hoja_nombre, index=False)

            actualizar_tabla()
            messagebox.showinfo("Eliminado", "Registro eliminado exitosamente.", parent=ventana)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {str(e)}")
    def salir():
        ventana.destroy()
    try:
        hojas = pd.ExcelFile(RUTA_DATOS_EXCEL).sheet_names
        seleccion_anio['values'] = hojas
        anio_actual = datetime.now().strftime("%Y")
        if anio_actual in hojas:
            seleccion_anio.set(anio_actual)
        else:
            seleccion_anio.set(hojas[-1])
        actualizar_tabla()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los años disponibles: {str(e)}")

    def ver_detalle():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Ver Detalle", "Por favor selecciona un registro para ver.", parent=ventana)
            return
        
        valores = tabla.item(seleccion[0], "values")
        ruta_imagen = valores[-1]
        ventana_detalle = tk.Toplevel(ventana)
        ventana_detalle.title("Detalle de Arrestados y Aprehendidos")
        ventana_detalle.state("zoomed")
        ventana_detalle.configure(bg="#e6edd8")
        ruta = rutas(r"logo.ico")
        ventana_detalle.iconbitmap(ruta)

        titulo = tk.Label(ventana_detalle, text="DETALLE DEL ARRESTADO Y APREHENDIDO", font=("Segoe UI", 22, "bold"), bg="#e6edd8", fg="#204e4a")
        titulo.pack(pady=20)

        contenedor = tk.Frame(ventana_detalle, bg="#e6edd8")
        contenedor.pack(fill="both", expand=True, padx=50, pady=10)

        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)

        frame_izq = tk.Frame(contenedor, bg="#e6edd8")
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=30, pady=10)

        frame_izq = tk.Frame(contenedor, bg="#e6edd8")
        frame_der = tk.Frame(contenedor, bg="#e6edd8")
        frame_izq.grid(row=0, column=0, padx=60, pady=10, sticky="n")
        frame_der.grid(row=0, column=1, padx=60, pady=10, sticky="n")

        for i, campo in enumerate(columnas[:-1]):
            tk.Label(frame_izq, text=f"{campo}:", font=("Segoe UI", 11, "bold"), bg="#e6edd8").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if campo == "Descripción de Objetos del Arrestado":
                txt = tk.Text(frame_izq, width=80, height=5, font=("Segoe UI", 11))
                txt.insert("1.0", valores[i])
                txt.config(state="disabled")
                txt.grid(row=i, column=1, padx=35, pady=5)
            else:
                entry = tk.Entry(frame_izq, width=80, font=("Segoe UI", 11))
                entry.insert(0, valores[i])
                entry.config(state="readonly")
                entry.grid(row=i, column=1, padx=35, pady=5)

        frame_der = tk.Frame(contenedor, bg="#e6edd8")
        frame_der.grid(row=0, column=1, sticky="n", padx=30, pady=10)

        if ruta_imagen and os.path.exists(ruta_imagen):
            from PIL import Image, ImageTk
            img = Image.open(ruta_imagen).resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(frame_der, image=img_tk, bg="#e6edd8")
            lbl_img.image = img_tk
            lbl_img.pack()
        else:
            tk.Label(frame_der, text="No hay imagen disponible", bg="#e6edd8", fg="red", font=("Segoe UI", 15, "italic")).pack()
  
        def abrir_ventana_modificar():
            valores = tabla.item(tabla.selection()[0], "values")
            ventana_modificar = tk.Toplevel(ventana_detalle)
            ventana_modificar.title("MODIFICACION DE DATOS _ REGISTRO DE ARRESTADOS Y APREHENDIDOS")
            ventana_modificar.state("zoomed")
            ventana_modificar.configure(bg="#e6edd8")
            ruta = rutas(r"logo.ico")
            ventana_modificar.iconbitmap(ruta)

            titulo = tk.Label(ventana_modificar, text="COMANDO DEPARTAMENTAL DE POTOSÍ\nCONCILIACIÓN CIUDADANA", font=("Segoe UI", 16, "bold"), bg="#e6edd8", fg="#204e4a")
            titulo.pack(pady=5)

            frame_mod = tk.Frame(ventana_modificar, bg="#e6edd8")
            frame_mod.pack(pady=2)
            anchura_label = 40

            entradas, textos = [], []
            ruta_nueva_imagen = [valores[-1]]
            
            for i, campo in enumerate(columnas[:-1]):
                tk.Label(frame_mod, text=campo + ":", bg="#e6edd8", font=("Segoe UI", 11, "bold"), anchor="w", justify="left", width=anchura_label).grid(row=i, column=0, sticky="e", padx=2, pady=2)

                if campo == "Fecha y Hora de Salida":
                    entrada = DateEntry(frame_mod, width=25, font=("Segoe UI", 10))
                    entrada.grid(row=i, column=1, padx=10, pady=6, sticky="w")
                    entradas.append(entrada)
                elif campo in ["Motivo de la Detención", "Lugar donde fue Arrestado", "Descripción de Objetos del Arrestado"]:
                    texto = tk.Text(frame_mod, width=80, height=3, font=("Segoe UI", 10))
                    texto.insert("1.0", valores[i])
                    texto.grid(row=i, column=1, padx=10, pady=6, sticky="w")
                    textos.append(texto)
                else:
                    entrada = tk.Entry(frame_mod, width=80, font=("Segoe UI", 10))
                    entrada.insert(0, valores[i])
                    entrada.grid(row=i, column=1, padx=10, pady=6, sticky="w")
                    entradas.append(entrada)
            def seleccionar_imagen():
                ruta = filedialog.askopenfilename(parent=ventana_modificar,filetypes=[("Imagenes", "*.jpg;*.png")])
                if ruta:
                    ruta_nueva_imagen[0] = ruta
                    
            tk.Button(frame_mod, text="📷 Seleccionar Nueva Imagen",  command=seleccionar_imagen, bg="#4CB6EB", fg="white").grid(row=len(columnas), column=1, pady=10, sticky="w")

            def guardar():
                nuevos = []
                idx_e, idx_t = 0, 0
                for campo in columnas[:-1]:
                    if campo in ["Motivo de la Detención", "Lugar donde fue Arrestado", "Descripción de Objetos del Arrestado"]:
                        nuevos.append(textos[idx_t].get("1.0", "end").strip())
                        idx_t += 1
                    elif campo == "Fecha y Hora de Salida":
                        nuevos.append(entradas[idx_e].get())
                        idx_e += 1
                    else:
                        nuevos.append(entradas[idx_e].get().strip())
                        idx_e += 1
                nuevos.append(ruta_nueva_imagen[0])

                año_actual = obtener_hoja_actual()
                try:
                    excel = pd.read_excel(RUTA_DATOS_EXCEL, sheet_name=None) 
                    df_año = excel.get(año_actual, pd.DataFrame())
                    
                    index = tabla.index(tabla.selection()[0])
                    if df_año.empty or index >= len(df_año):
                        messagebox.showerror("Error", "No se pudo localizar el registro a modificar.", parent=ventana_modificar)
                        return
                    columnas_archivo = list(df_año.columns)

                    if "ID" in columnas_archivo:
                        columnas_modificables = [col for col in columnas_archivo if col != "ID"]
                    else:
                        columnas_modificables = columnas_archivo
                    
                    if len(nuevos) != len(columnas_modificables):
                        messagebox.showerror(
                            "Error",
                            f"No se pudo guardar: el número de campos ({len(nuevos)}) no coincide con las columnas modificables ({len(columnas_modificables)}).",
                            parent=ventana_modificar
                        )
                        return
                    for i, col in enumerate(columnas_modificables):
                        valor = nuevos[i]
                        if pd.api.types.is_numeric_dtype(df_año[col]):
                            try:
                                df_año.at[index, col] = pd.to_numeric(valor, errors="coerce")
                            except:
                                df_año.at[index, col] = valor
                        else:
                            df_año.at[index, col] = valor
                    excel[año_actual] = df_año

                    with pd.ExcelWriter(RUTA_DATOS_EXCEL, engine="openpyxl") as writer:
                        for hoja, df in excel.items():
                            df.to_excel(writer, sheet_name=hoja, index=False)

                    messagebox.showinfo("Guardado", "Cambios guardados correctamente.", parent=ventana_modificar)
                    ventana_modificar.destroy()
                    actualizar_tabla() 
                    ventana_detalle.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=ventana_modificar)

            frame_botones = tk.Frame(ventana_modificar, bg="#f0f0f0")
            frame_botones.pack(pady=30)

            btn_guardar = tk.Button(frame_botones, text="💾 Guardar", command=guardar, bg="#4CAF50", fg="white", width=25, font=("Segoe UI", 10, "bold"))
            btn_guardar.grid(row=0, column=0, padx=10)
            btn_cancelar = tk.Button(frame_botones, text="❌ Cancelar", command=ventana_modificar.destroy, bg="#D32F2F", fg="white", width=25, font=("Segoe UI", 10, "bold"))
            btn_cancelar.grid(row=0, column=1, padx=10)

        def Descargar():
            ci = ""
            nombre_arrestado = ""
            for campo, valor in zip(columnas, valores):
                if campo.lower() in ["ci", "c.i.", "c.i"]:
                    ci = str(valor).replace(" ", "")
                elif "nombre del arrestado" in campo.lower():
                    nombre_arrestado = str(valor).strip().replace(" ", "_")

            if not ci or not nombre_arrestado:
                messagebox.showerror("Error", "No se pudo generar el nombre del archivo PDF automáticamente.\nFaltan CI o Nombre.")
                return
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            nombre_sugerido = f"{ci}_{nombre_arrestado}_{fecha_actual}.pdf"

            ruta_pdf = filedialog.asksaveasfilename(parent=ventana_detalle, defaultextension=".pdf", initialfile=nombre_sugerido, filetypes=[("PDF files", "*.pdf")])
            if not ruta_pdf:
                return

            c = pdf_canvas.Canvas(ruta_pdf, pagesize=letter)
            ancho, alto = letter
            margen_izquierdo = 3 * cm
            margen_derecho = ancho - 3 * cm
            ancho_contenido = margen_derecho - margen_izquierdo
            y = alto - 4 * cm
            espacio_linea = 14
            
            ruta=rutas(r"images/CARCANCHO CON LETRAS.png")
            logo_path = ruta
            if os.path.exists(logo_path):
                try:
                    c.drawImage(logo_path, ancho - 130.4, alto - 70.05, width=92, height=46)
                except:
                    pass

            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(ancho / 2, y, "INFORME DEL ARRESTADO / APREHENDIDO")
            y -= 30

            if ruta_imagen and os.path.exists(ruta_imagen):
                try:
                    img_width = 150
                    img_height = 150
                    img_x = (ancho - img_width) / 2
                    c.drawImage(ruta_imagen, img_x, y - img_height, width=img_width, height=img_height)
                    y -= img_height + 10
                except:
                    c.setFont("Helvetica-Oblique", 10)
                    c.drawCentredString(ancho / 2, y, "(No se pudo insertar la imagen)")
                    y -= 20

            campos_saltados = ["Imagen"]
            for campo, valor in zip(columnas, valores):
                if campo in campos_saltados:
                    continue
                if y < 5 * cm:
                    c.showPage()
                    y = alto - 3 * cm
                    c.setFont("Helvetica-Bold", 16)
                    c.drawCentredString(ancho / 2, y, "INFORME DEL ARRESTADO (Continuación)")
                    y -= 30

                c.setFont("Helvetica-Bold", 11)
                c.drawString(margen_izquierdo + 5, y, f"{campo}:")
                y -= 15

                c.setFont("Helvetica", 11)
                lineas = simpleSplit(str(valor), "Helvetica", 11, ancho_contenido - 10)
                altura_celda = (len(lineas) * espacio_linea) + 10
                c.rect(margen_izquierdo, y - altura_celda + 5, ancho_contenido, altura_celda, stroke=1, fill=0)

                texto_y = y - 6
                centro_recuadro = margen_izquierdo + (ancho_contenido / 2)
                for linea in lineas:
                    c.drawCentredString(centro_recuadro, texto_y, linea)
                    texto_y -= espacio_linea

                y -= altura_celda + 10
            c.save()
            messagebox.showinfo("Descargar", "PDF generado correctamente.", parent=ventana_detalle)
            try:
                if platform.system() == "Windows":
                    os.startfile(ruta_pdf)
                elif platform.system() == "Darwin":
                    subprocess.call(["open", ruta_pdf])
                else: 
                    subprocess.call(["xdg-open", ruta_pdf])
            except Exception as e:
                messagebox.showwarning("Advertencia", f"PDF guardado, pero no se pudo abrir automáticamente:\n{e}", parent=ventana_detalle)

        frame_botones = tk.Frame(contenedor, bg="#e6edd8")
        frame_botones.grid(row=20, column=0, columnspan=2, pady=50)
        
        estilo_btn = {"font": ("Segoe UI", 12, "bold"), "width": 15, "padx": 15, "pady": 5}

        tk.Button(frame_botones, text="📝 Modificar Detalle", bg="#FFC107", fg="white", command=abrir_ventana_modificar, **estilo_btn).pack(side="left", padx=10)

        tk.Button(frame_botones, text="🖨️ Descargar PDF", bg="#4CAF50", fg="white", command=Descargar, **estilo_btn).pack(side="left", padx=10)

        tk.Button(frame_botones, text="❌ Salir", bg="#D32F2F", fg="white", command=ventana_detalle.destroy, **estilo_btn).pack(side="left", padx=10)

    def mostrar_reporte():
        def generar_resumen_por_fechas(df, desde, hasta, tipo):
            df_filtrado = df[
                (df["Fecha y Hora de Ingreso"] >= pd.to_datetime(desde)) & 
                (df["Fecha y Hora de Ingreso"] <= pd.to_datetime(hasta))
                ].copy()
            df_filtrado["Fecha"] = df_filtrado["Fecha y Hora de Ingreso"].dt.date
            if tipo == "Diario":
                resumen = df_filtrado.groupby(["Fecha", "Motivo de la Detención"]).size().reset_index(name="Número de Arrestos")
            else:
                df_filtrado["Semana"] = df_filtrado["Fecha y Hora de Ingreso"].dt.to_period("W").apply(lambda r: r.start_time.date())
                resumen = df_filtrado.groupby(["Semana", "Motivo de la Detención"]).size().reset_index(name="Número de Arrestos")
                resumen.rename(columns={"Semana": "Fecha"}, inplace=True)
            return resumen, df_filtrado
        try:
            df = pd.read_excel(RUTA_DATOS_EXCEL)
            if df.empty:
                messagebox.showinfo("Reporte", "No hay datos disponibles para el reporte.")
                return

            df["Fecha y Hora de Ingreso"] = pd.to_datetime(df["Fecha y Hora de Ingreso"])

            ventana_reporte = tk.Toplevel(ventana)
            ventana_reporte.title("Reporte de Arrestos y Aprehendidos")
            ventana_reporte.state("zoomed")
            ventana_reporte.configure(bg="#e6edd8")
            ruta = rutas(r"logo.ico")
            ventana_reporte.iconbitmap(ruta)
 
            titulo = tk.Label(ventana_reporte, text="REPORTE DE ARRESTADOS Y APREHENDIDOS", font=("Segoe UI", 16, "bold"), bg="#e6edd8", fg="black")
            titulo.pack(pady=10)

            frame_filtros = tk.Frame(ventana_reporte, bg="#e6edd8")
            frame_filtros.pack(pady=10)

            tk.Label(frame_filtros, text="Fecha desde:", font=("Segoe UI", 11, "bold"), bg="#e6edd8").grid(row=0, column=0)
            entry_desde = DateEntry(frame_filtros, date_pattern='yyyy-mm-dd')
            entry_desde.grid(row=0, column=1, padx=5)

            tk.Label(frame_filtros, text="Fecha hasta:", font=("Segoe UI", 11, "bold"), bg="#e6edd8").grid(row=0, column=2)
            entry_hasta = DateEntry(frame_filtros, date_pattern='yyyy-mm-dd')
            entry_hasta.grid(row=0, column=3, padx=5)

            tk.Label(frame_filtros, text="Tipo de reporte:", font=("Segoe UI", 11, "bold"), bg="#e6edd8").grid(row=0, column=4)
            tipo_reporte = ttk.Combobox(frame_filtros, values=["Diario", "Semanal"], state="readonly")
            tipo_reporte.current(0)
            tipo_reporte.grid(row=0, column=5, padx=5)

            def aplicar_filtro():
                desde = entry_desde.get_date()
                hasta = entry_hasta.get_date()
                tipo = tipo_reporte.get()
                resumen, df_filtrado = generar_resumen_por_fechas(df, desde, hasta, tipo)

                for item in tabla_reporte.get_children():
                    tabla_reporte.delete(item)
                for _, fila in resumen.iterrows():
                    tabla_reporte.insert("", "end", values=list(fila))

                totales = df_filtrado["Motivo de la Detención"].value_counts()
                fig, ax = plt.subplots(figsize=(7, 7))
                ax.pie(totales.values, labels=totales.index, autopct="%1.1f%%", colors=plt.get_cmap("tab20").colors)
                ax.set_title("Cuadro Estadistico")

                for widget in frame_grafico.winfo_children():
                    widget.destroy()

                canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
                canvas.draw()
                canvas.get_tk_widget().pack()

                btn_exportar.configure(command=lambda: exportar_reporte_pdf(resumen, tipo, desde, hasta, fig))

            btn_filtrar = tk.Button(frame_filtros, text="Aplicar Filtro", command=aplicar_filtro, bg="#83b71c")
            btn_filtrar.grid(row=0, column=6, padx=10)

            frame_tabla = tk.Frame(ventana_reporte, bg="#e6edd8")
            frame_tabla.pack(fill="x", padx=10, pady=5)

            tabla_reporte = ttk.Treeview(frame_tabla, columns=["Fecha", "Motivo", "Número de Arrestos"], show="headings")
            for col in ["Fecha", "Motivo", "Número de Arrestos"]:
                tabla_reporte.heading(col, text=col)
                tabla_reporte.column(col, anchor="center", width=200)
            tabla_reporte.pack(fill="x")

            frame_contenedor = tk.Frame(ventana_reporte, bg="#e6edd8")
            frame_contenedor.pack(fill="both", expand=True, padx=10, pady=10)

            frame_grafico = tk.Frame(frame_contenedor, bg="#e6edd8")
            frame_grafico.pack(side="left", fill="both", expand=True)

            frame_boton = tk.Frame(frame_contenedor, bg="#e6edd8", width=150)
            frame_boton.pack(side="right", fill="y", padx=20)

            btn_exportar = tk.Button(
                frame_boton,
                text="Exportar a PDF",
                bg="green",
                fg="white",
                font=("Segoe UI", 12, "bold"),
                height=2,
                width=20
            )
            btn_exportar.pack(padx=30, pady=130)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {str(e)}")
        
        def exportar_reporte_pdf(resumen, tipo_reporte, desde, hasta, fig):
            try:
                nombre_fecha = f"{desde.strftime('%Y%m%d')}_a_{hasta.strftime('%Y%m%d')}"
                ruta_pdf = filedialog.asksaveasfilename(parent=ventana_reporte,
                    defaultextension=".pdf",
                    filetypes=[("Archivos PDF", "*.pdf")],
                    title="Guardar Reporte como PDF",
                    initialfile=f"reporte_{tipo_reporte.lower()}_{nombre_fecha}.pdf"
                )
                if not ruta_pdf:
                    return

                c = pdf_canvas.Canvas(ruta_pdf, pagesize=A4)
                width, height = A4
                
                ruta=rutas(r"images/CARCANCHO CON LETRAS.png")
                logo_path = ruta
                if os.path.exists(logo_path):
                    try:
                        c.drawImage(logo_path, width - 130.4, height - 70.05, width=92, height=46)
                    except:
                        pass
 
                y = height - 3.5 * cm
                c.setFont("Helvetica-Bold", 16)
                c.drawCentredString(width / 2, y, "REPORTE DE ARRESTADOS Y APREHENDIDOS")
                
                y -= 2 * cm
                tabla_data = [["Fecha", "Motivo", "Cantidad"]]
                for _, row in resumen.iterrows():
                    tabla_data.append([str(row["Fecha"]), row["Motivo de la Detención"], row["Número de Arrestos"]])

                col_widths = [140, 250, 100]
                tabla = Table(tabla_data, colWidths=col_widths)
                tabla.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]))

                tabla.wrapOn(c, width, height)
                tabla_height = tabla._height
                tabla.drawOn(c, 2 * cm, y - tabla._height)

                y -= tabla_height + 2 * cm 

                ruta_img = "grafico_arrestos.png"
                fig.savefig(ruta_img, bbox_inches="tight")
                plt.close(fig)

                img_width = width - 8 * cm
                x_img = 4 * cm 
                img_height = 200
                c.drawImage(ruta_img, x_img, y - img_height, width=img_width, height=img_height)

                c.showPage()
                c.save()
                os.remove(ruta_img)

                messagebox.showinfo("PDF Generado", f"Reporte guardado como: {ruta_pdf}", parent=ventana_reporte)
                try:
                    if platform.system() == "Windows":
                        os.startfile(ruta_pdf)
                    elif platform.system() == "Darwin":
                        subprocess.call(["open", ruta_pdf])
                    else: 
                        subprocess.call(["xdg-open", ruta_pdf])
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"PDF guardado, pero no se pudo abrir automáticamente:\n{e}", parent=ventana_reporte)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el PDF: {str(e)}")

    frame_botones = tk.Frame(ventana, bg="#f0f0f0")
    frame_botones.pack(pady=30)

    btn_ver = tk.Button(frame_botones, text="👁️Ver Detalle", command=ver_detalle, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), width=20)
    btn_ver.grid(row=0, column=1, padx=10)

    btn_grafico = tk.Button(frame_botones, text="📊 Ver Reporte", command=mostrar_reporte, bg="#00796B", fg="white", font=("Segoe UI", 10, "bold"), width=20)
    btn_grafico.grid(row=0, column=2, padx=10)

    btn_actualizar = tk.Button(frame_botones, text="🔄 Actualizar", command=actualizar_tabla, bg="#544CAF", fg="white", font=("Segoe UI", 10, "bold"), width=20) 
    btn_actualizar.grid(row=0, column=3, padx=10)

    btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar", command=eliminar, bg="#0E1041", fg="white", font=("Segoe UI", 10, "bold"), width=20)
    btn_eliminar.grid(row=0, column=4, padx=10)

    btn_salir = tk.Button(frame_botones, text="❌ Salir", command=salir, bg="#D32F2F", fg="white", font=("Segoe UI", 10, "bold"), width=20)
    btn_salir.grid(row=0, column=5, padx=10)

    actualizar_tabla()
    ventana.mainloop()
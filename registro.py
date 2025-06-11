import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
import os
from datetime import datetime
from uuid import uuid4
from config import RUTA_DATOS_EXCEL

def crear_formulario_registro(root):
    if hasattr(root, 'registro_window') and tk.Toplevel.winfo_exists(root.registro_window):
        root.registro_window.focus()
        return

    root.registro_window = tk.Toplevel(root)
    root.registro_window.title("Registrar Arrestados y Aprehendidos")
    root.registro_window.state('zoomed')
    root.registro_window.configure(bg="#e6edd8")

    global barra_original, carcancho_original
    barra_original = Image.open("images/barra.png")
    carcancho_original = Image.open("images/CARCANCHO CON LETRAS.png").resize((230, 80))

    main_frame = tk.Frame(root.registro_window, bg="#e6edd8")
    main_frame.pack(expand=True)

    titulo = tk.Label(main_frame, text="COMANDO DEPARTAMENTAL DE POTOSÍ\nCONCILIACIÓN CIUDADANA", font=("Segoe UI", 25, "bold"), bg="#e6edd8", fg="#204e4a")
    titulo.pack(pady=5)

    formulario_frame = tk.Frame(main_frame, bg="#ffffff", padx=30, pady=30, relief="groove", bd=2)
    formulario_frame.pack(expand=True, pady=(40, 100))

    campos = [
        "Motivo de la Detención",
        "Nombre del Arrestado",
        "Edad",
        "Ocupación",
        "CI",
        "Nombre del Funcionario Policial",
        "Unidad",
        "Estado Físico del Arrestado",
        "Descripción de Objetos del Arrestado",
        "Lugar donde fue Arrestado",
        "Nombre del Denunciante"
    ]

    campos_texto_amplio = [
        "Motivo de la Detención",
        "Estado Físico del Arrestado",
        "Descripción de Objetos del Arrestado",
        "Lugar donde fue Arrestado"
    ]

    opciones_unidad = [
        "Inspectoria Departamental", 'Dpto. "II" Inteligencia', 'Dpto. "III" PP.OO',
        'Sof. Plana Mayor', 'Tribunal Disciplinario Dptal.', 'Fiscalia Dptal. Policial',
        'DI.DI.PI', 'Dir. Dptal Bomberos', 'Dir. Dptal. DIPROVE', 'Dir. Dptal. F.E.L.C-C',
        'Dir. Dptal. F.E.L.C-V', 'Dir. Dptal. Gestion Estrategica', 'Dir. Dptal. Interpol',
        'Dir. Dptal. Recaudaciones', 'Dir. Dptal. Transito', 'Dir. Dptal. Telematica',
        'FATESCIPOL', 'EPI Distrito N°7', 'EPI Distrito N°8', 'EPI Distrito N°9',
        'EPI Distrito N°10', 'EPI Distrito N°20', 'Radio Patrullas - 110',
        'CMDO. POL. RURAL y Fronteriza', 'U.T.O.P', 'Patrulla Caminera', 'C.A.C',
        'P.A.C', 'Bat. Seg. Fis. Estatal', 'Bat. Seg. Fis. Privada', 'DELTA',
        'Banda de Musica', 'CADI', 'Centro de Readaptacion Cantumarca', 'CIC-VIAL',
        'Conciliacion Ciudadana', 'IITCUP', 'JEDECEV', 'REAFUC', 'SINARAP', 'Otros'
    ]

    entradas = {}
    unidad_combobox = None
    unidad_personalizada_entry = None

    def seleccionar_imagen():
        filepath = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if filepath:
            entradas["Imagen"] = filepath
            img = Image.open(filepath)
            img.thumbnail((120, 120))
            img = ImageTk.PhotoImage(img)
            panel_imagen.config(image=img)
            panel_imagen.image = img

    entradas["Imagen"] = ""

    def actualizar_entrada_unidad_personalizada(event=None):
        seleccion = unidad_combobox.get()
        if seleccion == "Otros":
            unidad_combobox.grid_remove()
            unidad_personalizada_entry.grid()
            unidad_personalizada_entry.delete(0, "end")
            unidad_personalizada_entry.after(100, lambda: unidad_personalizada_entry.focus_set())
            
        else:
            unidad_personalizada_entry.grid_remove()
            unidad_combobox.grid()


    for idx, campo in enumerate(campos):
        col = 0 if idx < len(campos) // 2 else 2
        fila = idx if idx < len(campos) // 2 else idx - len(campos) // 2

        label = tk.Label(formulario_frame, text=campo + ":", bg="#ffffff", anchor="w", font=("Arial", 12))
        label.grid(row=fila, column=col, sticky="w", padx=20, pady=20)

        if campo == "Unidad":
            unidad_combobox = ttk.Combobox(formulario_frame, values=opciones_unidad, state="normal", width=47)
            unidad_combobox.set("Seleccione unidad")
            unidad_combobox.grid(row=fila, column=col + 1, sticky="w", pady=5)
            unidad_combobox.bind("<<ComboboxSelected>>", actualizar_entrada_unidad_personalizada) 
            entradas[campo] = unidad_combobox
            
            unidad_personalizada_entry = tk.Entry(formulario_frame, width=50)
            unidad_personalizada_entry.grid(row=fila, column=col + 1, sticky="w", pady=5)
            unidad_personalizada_entry.grid_remove()

        elif campo in campos_texto_amplio:
            text_widget = tk.Text(formulario_frame, height=3, width=48, wrap="word", font=("Arial", 10))
            text_widget.grid(row=fila, column=col + 1, sticky="w", pady=5)
            entradas[campo] = text_widget
        else:
            entry = tk.Entry(formulario_frame, width=50, font=("Arial", 10))
            entry.grid(row=fila, column=col + 1, sticky="w", pady=5)
            entradas[campo] = entry

    btn_imagen = tk.Button(formulario_frame, text="Seleccionar Imagen", command=seleccionar_imagen, bg="#71AA2C", fg="white", width=20)
    btn_imagen.grid(row=0, column=4, padx=10, pady=10)

    panel_imagen = tk.Label(formulario_frame, bg="#ffffff")
    panel_imagen.grid(row=1, column=4, padx=10, pady=10)

    def guardar_datos():
        datos = {}
        for campo in campos:
            if campo == "Unidad":
                seleccion = unidad_combobox.get()
                if not seleccion or seleccion == "Seleccione unidad":
                     messagebox.showwarning("Campo vacío", "Por favor ingresa o selecciona una unidad.")
                     return
                datos[campo] = seleccion.strip()
            elif campo in campos_texto_amplio:
                texto = entradas[campo].get("1.0", "end").strip()
                if not texto:
                    messagebox.showwarning("Campo vacío", f"Llena el campo '{campo}'")
                    return
                datos[campo] = texto
            else:
                valor = entradas[campo].get().strip()
                if not valor:
                    messagebox.showwarning("Campo vacío", f"Llena el campo '{campo}'")
                    return
                datos[campo] = valor

        datos["Fecha y Hora de Ingreso"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos["ID"] = str(uuid4())[:8]
        datos["Imagen"] = entradas.get("Imagen", "")
        datos["Fecha y Hora de Salida"] = ""

        df_nuevo = pd.DataFrame([datos])
        if os.path.exists(RUTA_DATOS_EXCEL):
            df_existente = pd.read_excel(RUTA_DATOS_EXCEL)
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo

        df_final.to_excel(RUTA_DATOS_EXCEL, index=False)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        limpiar_formulario()

    def limpiar_formulario():
        for campo in campos:
            if campo == "Unidad":
                unidad_combobox.set("Seleccione unidad")
                unidad_personalizada_entry.delete(0, tk.END)
                unidad_personalizada_entry.grid_remove()
            elif campo in campos_texto_amplio:
                entradas[campo].delete("1.0", tk.END)
            else:
                entradas[campo].delete(0, tk.END)
        entradas["Imagen"] = ""
        panel_imagen.config(image="")
        panel_imagen.image = None

    def volver_atras():
        if messagebox.askyesno("Volver", "¿Deseas volver? Se perderán los datos no guardados."):
            root.registro_window.destroy()

    boton_frame = tk.Frame(main_frame, bg="#f0f0f0")
    boton_frame.pack(pady=15)

    btn_guardar = tk.Button(boton_frame, text="Guardar", command=guardar_datos, width=18, height=2, bg="#4CAF50", fg="white")
    btn_guardar.grid(row=0, column=0, padx=10)

    btn_limpiar = tk.Button(boton_frame, text="Limpiar", command=limpiar_formulario, width=18, height=2, bg="#4CAFAC", fg="white")
    btn_limpiar.grid(row=0, column=1, padx=10)

    btn_volver = tk.Button(boton_frame, text="Volver Atrás", command=volver_atras, width=18, height=2, bg="#f44336", fg="white")
    btn_volver.grid(row=0, column=2, padx=10)

    carcancho = ImageTk.PhotoImage(carcancho_original)
    label_carcancho = tk.Label(root.registro_window, image=carcancho, bg="#e6edd8")
    label_carcancho.image = carcancho
    label_carcancho.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-70)  

    barra_resized = barra_original.resize((root.registro_window.winfo_width(), 50))
    barra_resized = ImageTk.PhotoImage(barra_resized)
    label_barra = tk.Label(root.registro_window, image=barra_resized, bg="#e6edd8")
    label_barra.image = barra_resized
    label_barra.pack(side="bottom", fill="x")

    def ajustar_barra(event):
        if root.registro_window.state() == 'normal':
            return
        nueva_ancho = root.registro_window.winfo_width()
        if nueva_ancho <= 1: 
            return
        nueva_barra = barra_original.resize((nueva_ancho, 50))
        nueva_barra = ImageTk.PhotoImage(nueva_barra)
        label_barra.config(image=nueva_barra)
        label_barra.image = nueva_barra

    root.registro_window.bind("<Configure>", ajustar_barra)

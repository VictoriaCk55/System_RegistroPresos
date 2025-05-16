import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
#from registro import crear_formulario_registro 
from registro import crear_formulario_registro
#from ver_registro import mostrar_registros
from ver_registro import crear_ventana_ver_registros


def iniciar_registro():
    def abrir_registro():
        crear_formulario_registro(ventana)

    def ver_registro():
        #mostrar_registros(ventana)
        crear_ventana_ver_registros()

    def salir():
        respuesta = messagebox.askyesno("Salir", "¿Seguro que quieres salir?")
        if respuesta:
            ventana.destroy()

    def ajustar_barra(event):
        nueva_ancho = ventana.winfo_width()
        barra_resized = barra_original.resize((nueva_ancho, 50))
        barra_resized = ImageTk.PhotoImage(barra_resized)
        label_barra.config(image=barra_resized)
        label_barra.image = barra_resized

    ventana = tk.Tk()
    ventana.title("Sistema de Registro de Arrestados y Aprehendidos")
    ventana.state('zoomed')
    ventana.configure(bg="#f0f0f0")

    titulo = tk.Label(ventana, text="COMANDO DEPARTAMENTAL DE POTOSÍ\nCONCILIACIÓN CIUDADANA",
                      font=("Arial", 20, "bold"), bg="#f0f0f0")
    titulo.pack(pady=15)

    carcancho = Image.open("images/CARCANCHO CON LETRAS.png").resize((230, 80))
    carcancho = ImageTk.PhotoImage(carcancho)
    label_carcancho = tk.Label(ventana, image=carcancho, bg="#f0f0f0")
    label_carcancho.image = carcancho
    label_carcancho.place(x=1200, y=640)

    logo = Image.open("images/logo.png").resize((220, 220))
    logo = ImageTk.PhotoImage(logo)
    label_logo = tk.Label(ventana, image=logo, bg="#f0f0f0")
    label_logo.image = logo
    label_logo.pack(pady=20)

    btn_registro = tk.Button(ventana, text="📋 Registrar Detenidos", command=abrir_registro,
                             font=("Arial", 14, "bold"), bg="#2196F3", fg="white", width=30, height=2)
    btn_registro.pack(pady=10)

    btn_ver_registro = tk.Button(ventana, text="📂 Ver Registro de Detenidos", command=ver_registro,
                                 font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=30, height=2)
    btn_ver_registro.pack(pady=10)

    btn_salir = tk.Button(ventana, text="❌ Salir", command=salir,
                          font=("Arial", 14, "bold"), bg="#F44336", fg="white", width=30, height=2)
    btn_salir.pack(pady=10)

    # Barra inferior
    global barra_original
    barra_original = Image.open("images/barra.png")
    barra_resized = barra_original.resize((1000, 50))
    barra_resized = ImageTk.PhotoImage(barra_resized)
    label_barra = tk.Label(ventana, image=barra_resized, bg="#f0f0f0")
    label_barra.image = barra_resized
    label_barra.pack(side="bottom", fill="x")

    ventana.bind("<Configure>", ajustar_barra)
    ventana.mainloop()

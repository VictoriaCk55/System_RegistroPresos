import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
import main_window 

USUARIO_GENERAL = "admin"
CONTRASEÑA_GENERAL = "admin"

ventana_login = None

def rutas(ruta_relativa):
        try:
            rutabase=sys._MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase, ruta_relativa)

def crear_login(on_login_success):
    global ventana_login
    ventana_login = tk.Tk()
    ventana_login.title("Login - Sistema de Registro de Arrestados y Aprehendidos")
    ventana_login.state("zoomed")
    ventana_login.resizable(True, True)
    ventana_login.configure(bg="#e6edd8")
    ruta = rutas(r"logo.ico")
    ventana_login.iconbitmap(ruta)

    def verificar_usuario():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()

        if usuario == USUARIO_GENERAL and contraseña == CONTRASEÑA_GENERAL:
            mensaje_label.config(text="✅ Inicio de sesión exitoso.", fg="green")
            ventana_login.after(1000, cerrar_login_y_abrir_registro)
        else:
            mensaje_label.config(text="❌ Usuario o contraseña incorrectos.", fg="red")

    def cerrar_login_y_abrir_registro():
        ventana_login.destroy() 
        main_window.iniciar_registro() 

    ruta = rutas("images/barra.png")
    barra_original = Image.open(ruta).resize((ventana_login.winfo_screenwidth(), 50))
    barra_img = ImageTk.PhotoImage(barra_original)  
    barra_label = tk.Label(ventana_login, image=barra_img, bg="#e6edd8")
    barra_label.image = barra_img
    barra_label.place(x=0, y=ventana_login.winfo_screenheight() - 110)

    ruta = rutas("images/CARCANCHO CON LETRAS.png")
    carcancho = Image.open(ruta).resize((230, 80))
    carcancho = ImageTk.PhotoImage(carcancho)
    label_carcancho = tk.Label(ventana_login, image=carcancho, bg="#e6edd8")
    label_carcancho.image = carcancho
    label_carcancho.place(x=1200, y=640)

    label_titulo = tk.Label(ventana_login, text="COMANDO DEPARTAMENTAL DE POTOSÍ\nCONCILIACIÓN CIUDADANA", font=("Segoe UI", 25, "bold"), justify="center", bg="#e6edd8", fg="#204e4a")
    label_titulo.pack(pady=(50, 20))
    
    ruta = rutas("images/logo.png")
    img = Image.open(ruta)
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)

    label_img = tk.Label(ventana_login, image=img)
    label_img.image = img
    label_img.pack(pady=10)

    tk.Label(ventana_login, text="USUARIO:", font=("Arial", 15, "bold"), bg="#e6edd8").pack()
    entry_usuario = tk.Entry(ventana_login, font=("Arial", 15), width=30, justify="center")
    entry_usuario.pack()

    tk.Label(ventana_login, text="CONTRASEÑA:", font=("Arial", 15, "bold"), bg="#e6edd8").pack()
    entry_contraseña = tk.Entry(ventana_login, show="*", font=("Arial", 15), width=30, justify="center")
    entry_contraseña.pack()

    btn_login = tk.Button(ventana_login, text="Iniciar sesión", command=verificar_usuario, font=("Arial", 14, "bold"), bg="#48B14B", fg="white", width=25, height=2)
    btn_login.pack(pady=20)

    mensaje_label = tk.Label(ventana_login, text="", font=("Arial", 14, "bold"), bg="#e6edd8")
    mensaje_label.pack()

    ventana_login.mainloop()

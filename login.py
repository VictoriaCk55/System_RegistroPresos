import tkinter as tk
from PIL import Image, ImageTk
import main_window  # Asegúrate de que 'ventana_principal' esté correctamente importado

# Credenciales generales
USUARIO_GENERAL = "admin"
CONTRASEÑA_GENERAL = "admin"

# Declaramos la ventana como global
ventana_login = None

def crear_login(on_login_success):
    global ventana_login
    ventana_login = tk.Tk()
    ventana_login.title("Login - Sistema de Registro de Arrestados y Aprehendidos")
    ventana_login.geometry("800x700")
    ventana_login.resizable(True, True)
    ventana_login.configure(bg="#f0f0f0")

    # Función para verificar el usuario
    def verificar_usuario():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()

        if usuario == USUARIO_GENERAL and contraseña == CONTRASEÑA_GENERAL:
            mensaje_label.config(text="✅ Inicio de sesión exitoso.", fg="green")
            ventana_login.after(1000, cerrar_login_y_abrir_registro)  # Esperar 1 segundo para cerrar login y abrir ventana principal
        else:
            mensaje_label.config(text="❌ Usuario o contraseña incorrectos.", fg="red")

    def cerrar_login_y_abrir_registro():
        ventana_login.destroy()  # Cierra la ventana de login
        main_window.iniciar_registro()  # Abre la ventana principal (aquí llamas a la función de tu ventana principal)

    # UI (Interfaz)
    label_titulo = tk.Label(ventana_login, text="COMANDO DEPARTAMENTAL DE POTOSÍ\nCONCILIACIÓN CIUDADANA",
                             font=("Arial", 20, "bold"), justify="center", bg="#f0f0f0")
    label_titulo.pack(pady=20)

    # Imagen
    img = Image.open("images/logo.png")
    img = img.resize((250, 250))
    img = ImageTk.PhotoImage(img)

    label_img = tk.Label(ventana_login, image=img, bg="#f0f0f0")
    label_img.image = img  # Muy importante para evitar que se elimine la imagen de memoria
    label_img.pack(pady=10)

    # Usuario
    tk.Label(ventana_login, text="Usuario:", font=("Arial", 14), bg="#f0f0f0").pack()
    entry_usuario = tk.Entry(ventana_login, font=("Arial", 14), width=20)
    entry_usuario.pack()

    # Contraseña
    tk.Label(ventana_login, text="Contraseña:", font=("Arial", 14), bg="#f0f0f0").pack()
    entry_contraseña = tk.Entry(ventana_login, show="*", font=("Arial", 14), width=20)
    entry_contraseña.pack()

    # Botón
    btn_login = tk.Button(ventana_login, text="Iniciar sesión", command=verificar_usuario, font=("Arial", 14, "bold"),
                          bg="#4CAF50", fg="white", width=15, height=2)
    btn_login.pack(pady=20)

    # Mensajes
    mensaje_label = tk.Label(ventana_login, text="", font=("Arial", 14, "bold"), bg="#f0f0f0")
    mensaje_label.pack()

    # Mostrar ventana
    ventana_login.mainloop()

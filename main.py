import login
import main_window

def iniciar():
    login.crear_login(on_login_success=main_window.iniciar_registro)

if __name__ == "__main__":
    iniciar()

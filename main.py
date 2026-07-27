#MODULO 3:
import tkinter as tk
from models import TicketManager
from views import HelpdeskUI

def main():
    """Configuramos la ventana raiz e iniciamos el bucle de eventos (mainloop)."""
    root = tk.Tk()

    # Inicializacion del gestor de persistencia de datos
    manager = TicketManager("tickets.json")
    
    # Inyeccion de dependencias (hacia la interfaz)
    app = HelpdeskUI(root, manager)

    # Iniciamos el bucle de eventos
    root.mainloop()

if __name__ == "__main__":
    main()
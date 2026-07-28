import tkinter as tk
from models import TicketManager
from views import HelpdeskUI

def main() -> None:
    """Orquesta el arranque de la aplicación inicializando datos y la interfaz."""
    manager = TicketManager()
    root = tk.Tk()
    app = HelpdeskUI(parent=root, manager=manager)
    root.mainloop()

if __name__ == "__main__":
    main()

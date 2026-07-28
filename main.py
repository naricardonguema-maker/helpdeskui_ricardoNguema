# ================================== #
# Punto de Entrada de la Aplicación  #
# ================================== #
"""
Este archivo es el núcleo que inicia la app mediante la carga del gestor de datos(models.py), 
genera la ventana principal creada con Tkinter(views.py) y e inicia el bucle del sistema; respondiendo
así a las acciones del usuario.
"""
import tkinter as tk
from models import TicketManager
from views import HelpdeskUI

def main() -> None:

    ''' Arranque de la aplicación inicializando datos y la interfaz. '''

    #1. Carga y administra la información de los tickets (crear, borrar, modificar) #
    manager = TicketManager() 

    #2. Elemento visual(ventana que veremos en pantalla) #
    root = tk.Tk() 

    #3. Conecta la ventana (root) con los datos (manager). Eso nos permite mostrar y actualiar los datos #
    app = HelpdeskUI(root, manager)

    #4. Inicia el bucle de eventos y escucha las acciones del usuario #
    root.mainloop() 

'''--- Punto de inicio de la aplicación (ejecutador) ---'''

if __name__ == "__main__":
    main()

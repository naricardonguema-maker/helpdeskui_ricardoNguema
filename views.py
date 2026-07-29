# ======================================= #
# Creación de Interfaz visual con Tkinter #
# ======================================= #
"""
Aquí nos encargamos exclusivamente de lo que el usuario ve en la ventana y de escuchar sus interacciones con la interfaz.
Las líneas de código siguientes sirven para importar herramientas externas al archivo de Python. Al importarlas, 
podemos usarlas para construir la interfaz gráfica de la aplicación y gestionar los datos sin tener que escribir 
todo el código desde cero.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models import TicketManager

class HelpdeskUI:
    def __init__(self, root: tk.Tk, manager: TicketManager):
        self.root = root
        self.manager = manager

        self.root.title(" Helpdesk System - Gestión de tickets")
        self.root.geometry("950x650")
        self.root.minsize(850, 550)
        
        # 1. COLOR DE FONDO GENERAL DE LA VENTANA (Beige)
        self.root.configure(background="#f5f5dc")

        # Aplicamos estilos
        self.style = ttk.Style()
        self.style.theme_use("alt")

        # Configuración global para que los Frames de ttk hereden el fondo beige
        self.style.configure(".", background="#f5f5dc")
        self.style.configure("TLabelframe", background="#f5f5dc")
        self.style.configure("TLabelframe.Label", background="#f5f5dc", font=("Segoe UI", 10, "bold"))

        # 2. CONFIGURACIÓN DEL ENCABEZADO DE LA TABLA (Azul Marino)
        self.style.configure(
            "Treeview.Heading", 
            background="#001F3F",       # Azul marino oscuro
            foreground="white",         # Letras blancas para contraste
            font=("Segoe UI", 10, "bold")
        )
        # Evita que el color cambie bruscamente de manera extraña al pasar el cursor (hover)
        self.style.map("Treeview.Heading", background=[("active", "#002a54")])

        # 3. DEFINICIÓN DE ESTILOS PARA LOS BOTONES (Madera de roble y otros tonos)
        self.style.configure("Oak.TButton", background="#cd853f", foreground="white", font=("Segoe UI", 9, "bold"))
        self.style.map("Oak.TButton", background=[("active", "#8b5a2b")])

        self.style.configure("Action.TButton", background="#3498db", foreground="white", font=("Segoe UI", 9, "bold"))
        self.style.map("Action.TButton", background=[("active", "#2980b9")])

        self.style.configure("Danger.TButton", background="#e74c3c", foreground="white", font=("Segoe UI", 9, "bold"))
        self.style.map("Danger.TButton", background=[("active", "#c0392b")])

        self._crear_interfaz()
        self.actualizar_tabla()

    def _crear_interfaz(self):
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill=tk.X)
        
        # TÍTULO MODIFICADO CON ICONOS UNICODE (Llave inglesa y pulgar arriba)
        ttk.Label(
            header,
            text="🔧 DASHBOARD DE SOPORTE TÉCNICO 👍",
            font=("Segoe UI", 16, "bold")
        ).pack(side=tk.LEFT)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._crear_formulario(main_frame)
        self._crear_panel_derecho(main_frame)

    def _crear_formulario(self, parent):
        frame = ttk.LabelFrame(parent, text="Nuevo ticket", padding=15)
        frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Campos
        ttk.Label(frame, text="Usuario / Solicitante").pack(anchor=tk.W, pady=(0, 5))
        self.ent_usuario = ttk.Entry(frame, width=25)
        self.ent_usuario.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text="Descripción").pack(anchor=tk.W, pady=(0, 5))
        self.ent_descripcion = ttk.Entry(frame, width=25)
        self.ent_descripcion.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text="Categoría").pack(anchor=tk.W, pady=(0, 5))
        self.cmb_categoria = ttk.Combobox(
            frame,
            values=["Hardware", "Software", "Redes/Conectividad", "Accesos/Permisos"],
            state="readonly"
        )
        self.cmb_categoria.set("Hardware")
        self.cmb_categoria.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame, text="Prioridad").pack(anchor=tk.W, pady=(0, 5))
        self.cmb_prioridad = ttk.Combobox(
            frame,
            values=["Baja", "Media", "Alta", "Crítica"],
            state="readonly"
        )
        self.cmb_prioridad.set("Baja")
        self.cmb_prioridad.pack(fill=tk.X, pady=(0, 10))

        # Botones con estilo madera de roble
        ttk.Button(frame, text="Crear Ticket", style="Oak.TButton", command=self._on_crear).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(frame, text="Limpiar Campos", command=self._limpiar_formulario).pack(fill=tk.X)

    def _crear_panel_derecho(self, parent):
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Buscador
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame, text="Filtrar: ").pack(side=tk.LEFT, padx=(0, 5))
        self.ent_buscar = ttk.Entry(search_frame)
        self.ent_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ent_buscar.bind("<KeyRelease>", lambda e: self.actualizar_tabla())

        # Tabla Treeview
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "usuario", "descripcion", "categoria", "prioridad", "estado")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        # Asignación de nombres a las cabeceras (ahora serán Azul Marino automáticamente)
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("prioridad", text="Prioridad")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("usuario", width=120)
        self.tree.column("descripcion", width=200)
        self.tree.column("categoria", width=120)
        self.tree.column("prioridad", width=80, anchor=tk.CENTER)
        self.tree.column("estado", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones de acción
        actions = ttk.Frame(right_frame, padding=(0, 10, 0, 0))
        actions.pack(fill=tk.X)

        ttk.Button(actions, text="Cambiar estado", style="Action.TButton", command=self._on_cambiar_estado).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions, text="Eliminar Ticket", style="Danger.TButton", command=self._on_eliminar).pack(side=tk.LEFT)

        # Métricas
        self.lbl_stats = ttk.Label(right_frame, text="", font=("Segoe UI", 9, "italic"))
        self.lbl_stats.pack(anchor=tk.E, pady=(10, 0))

    def _on_crear(self):
        usuario = self.ent_usuario.get().strip()
        descripcion = self.ent_descripcion.get().strip()

        if not usuario or not descripcion:
            messagebox.showwarning("Campos Requeridos", "Por favor completa el Usuario y la Descripción")
            return

        ticket = self.manager.crear_ticket(
            usuario=usuario,
            descripcion=descripcion,
            categoria=self.cmb_categoria.get(),
            prioridad=self.cmb_prioridad.get()
        )

        messagebox.showinfo("Éxito", f"Ticket #{ticket.id} creado correctamente.")
        self._limpiar_formulario()
        self.actualizar_tabla()

    def _limpiar_formulario(self):
        self.ent_usuario.delete(0, tk.END)
        self.ent_descripcion.delete(0, tk.END)
        self.cmb_categoria.set("Hardware")
        self.cmb_prioridad.set("Baja")

    def _on_cambiar_estado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un ticket primero.")
            return

        ticket_id = int(self.tree.item(selected[0], "values")[0])
        self.manager.cambiar_estado(ticket_id)
        self.actualizar_tabla()

    def _on_eliminar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un ticket para eliminar.")
            return
        ticket_id = int(self.tree.item(selected[0], "values")[0])
        if messagebox.askyesno("Confirmar", f"¿Deseas borrar el ticket #{ticket_id}?"):
            self.manager.eliminar_ticket(ticket_id)
            self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if hasattr(self, 'ent_buscar'):
            criterio = self.ent_buscar.get().strip()
        else:
            criterio = ""

        tickets = self.manager.actualizar_tabla(criterio)

        for t in tickets:
            self.tree.insert("", tk.END, values=(
                t.id, t.usuario, t.descripcion, t.categoria, t.prioridad, t.estado
            ))

        stats = self.manager.obtener_metricas()
        self.lbl_stats.config(
            text=f"Total: {stats.get('total', 0)} | Pendientes: {stats.get('pendientes', 0)} | Resueltos: {stats.get('resueltos', 0)}"
        )
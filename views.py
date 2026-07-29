# ======================================= #
# Creación de Interfaz visual con Tkinter #
# ======================================= #
"""
Aquí nos encargamos exclusivamente de lo que el usuario ve y de escuchar sus interacciones con la interfaz.
Las líneas de código siguientes sirven para importar herramientas externas al archivo de Python. Al importarlas, 
podemos usarlas para construir la interfaz gráfica de la aplicación y gestionar los datos sin tener que escribir 
todo el código desde cero.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List
from models import TicketManager, Ticket

class HelpdeskUI(ttk.Frame):

    def __init__(self, parent: tk.Tk, manager: TicketManager) -> None:
        super().__init__(parent)
        self.manager = manager
        
        parent.title("DataDesk Helpdesk System")
        parent.geometry("980x600")
        parent.configure(bg="#F3F4F6") # Fondo de la ventana principal
        
        self.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self) -> None:
        """Define y aplica la paleta de colores y tipografía mediante TTK Styles."""
        style = ttk.Style()
        style.theme_use("clam") # Base flexible para sobreescribir estilos

        # Configuración global de frames y etiquetas de sección
        style.configure("TFrame", background="#F3F4F6")
        style.configure("TLabelframe", background="#FFFFFF", bordercolor="#E5E7EB", borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background="#FFFFFF", foreground="#374151", font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background="#FFFFFF", foreground="#4B5563", font=("Segoe UI", 9))

        # Configuración del Buscador Dinámico e Inputs
        style.configure("TEntry", fieldbackground="#F9FAFB", bordercolor="#D1D5DB", lightcolor="#D1D5DB", darkcolor="#D1D5DB")
        style.configure("TCombobox", fieldbackground="#F9FAFB", bordercolor="#D1D5DB", arrowcolor="#4B5563")

        # Botones Personalizados por Estados de Acción
        style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), background="#2563EB", foreground="#FFFFFF", borderwidth=0, padding=6)
        style.map("Primary.TButton", background=[("active", "#1D4ED8")])

        style.configure("Success.TButton", font=("Segoe UI", 9, "bold"), background="#10B981", foreground="#FFFFFF", borderwidth=0, padding=6)
        style.map("Success.TButton", background=[("active", "#059669")])

        style.configure("Warning.TButton", font=("Segoe UI", 9, "bold"), background="#F59E0B", foreground="#FFFFFF", borderwidth=0, padding=6)
        style.map("Warning.TButton", background=[("active", "#D97706")])

        style.configure("Danger.TButton", font=("Segoe UI", 9, "bold"), background="#EF4444", foreground="#FFFFFF", borderwidth=0, padding=6)
        style.map("Danger.TButton", background=[("active", "#DC2626")])

        # Diseño de la Tabla Avanzada (Treeview)
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26, background="#FFFFFF", fieldbackground="#FFFFFF", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#F3F4F6", foreground="#374151", borderwidth=1, relief="flat")
        style.map("Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", "#1E40AF")])

    def _build_ui(self) -> None:
        # --- 1. PANEL SUPERIOR (KPIs y Buscador Predictivo) ---
        top_frame = ttk.LabelFrame(self, text=" Métricas de Rendimiento ", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # Sub-contenedor interno para alinear métricas
        metrics_box = ttk.Frame(top_frame)
        metrics_box.pack(side=tk.LEFT)

        self.lbl_met = ttk.Label(metrics_box, text="Cargando métricas...", font=("Segoe UI", 10, "bold"), background="#FFFFFF")
        self.lbl_met.pack(side=tk.LEFT, padx=5)

        # Buscador Predictivo alineado a la derecha
        search_box = ttk.Frame(top_frame)
        search_box.pack(side=tk.RIGHT)
        
        ttk.Label(search_box, text="Filtrar incidencias:").pack(side=tk.LEFT, padx=(0, 5))
        self.sv_buscar = tk.StringVar()
        self.sv_buscar.trace_add("write", lambda *a: self.refresh_table())
        
        entry_search = ttk.Entry(search_box, textvariable=self.sv_buscar, width=28)
        entry_search.pack(side=tk.LEFT)

        # --- 2. PANEL CENTRAL (Formulario y Grid de Datos) ---
        main_body = ttk.Frame(self)
        main_body.pack(fill=tk.BOTH, expand=True)

        # Formulario de Alta
        form_frame = ttk.LabelFrame(main_body, text=" Registrar Incidencia ", padding=12)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        ttk.Label(form_frame, text="Usuario Afectado:").pack(anchor=tk.W, pady=(0, 2))
        self.ent_user = ttk.Entry(form_frame, width=25)
        self.ent_user.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Categoría Técnica:").pack(anchor=tk.W, pady=(0, 2))
        self.cb_cat = ttk.Combobox(form_frame, values=["Hardware", "Software", "Redes"], state="readonly")
        self.cb_cat.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Prioridad SLA:").pack(anchor=tk.W, pady=(0, 2))
        self.cb_prio = ttk.Combobox(form_frame, values=["Baja", "Media", "Alta"], state="readonly")
        self.cb_prio.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Descripción del Problema:").pack(anchor=tk.W, pady=(0, 2))
        self.txt_desc = tk.Text(form_frame, width=24, height=7, font=("Segoe UI", 9), bg="#F9FAFB", fg="#374151", bd=1, relief="solid", highlightthickness=0)
        self.txt_desc.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        ttk.Button(form_frame, text="Guardar Registro", style="Primary.TButton", command=self._add_ticket).pack(fill=tk.X)

        # Tabla Interactiva (Treeview)
        table_frame = ttk.LabelFrame(main_body, text=" Registro General de Tickets ", padding=5)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        cols = ("id", "user", "cat", "prio", "status", "desc")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        
        headers = {"id": "ID", "user": "Usuario", "cat": "Categoría", "prio": "Prioridad", "status": "Estado", "desc": "Descripción"}
        for k, v in headers.items():
            self.tree.heading(k, text=v)
            self.tree.column(k, width=50 if k == "id" else 100 if k != "desc" else 220, anchor=tk.CENTER if k in ["id", "prio", "status"] else tk.W)

        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --- 3. PANEL INFERIOR (Barra de Acciones Avanzadas) ---
        bottom_frame = ttk.Frame(self, padding=5)
        bottom_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(bottom_frame, text="Marcar Resuelto", style="Success.TButton", command=lambda: self._change_status("Resuelto")).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Reabrir Ticket", style="Warning.TButton", command=lambda: self._change_status("Pendiente")).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Eliminar Registro", style="Danger.TButton", command=self._delete_ticket).pack(side=tk.RIGHT, padx=5)

        self.refresh_table()

    def refresh_table(self) -> None:
        self.tree.delete(*self.tree.get_children())
        query = self.sv_buscar.get().lower()

        for t in self.manager.tickets:
            if any(query in str(val).lower() for val in [t.usuario, t.categoria, t.prioridad, t.estado, t.descripcion]):
                self.tree.insert("", tk.END, iid=str(t.id), values=(t.id, t.usuario, t.categoria, t.prioridad, t.estado, t.descripcion))

        m = self.manager.metrics()
        self.lbl_met.config(text=f"📊  Total: {m['total']}   |   🟠  Pendientes: {m['pendientes']}   |   🟢  Resueltos: {m['resueltos']}")

    def _add_ticket(self) -> None:
        user, cat, prio = self.ent_user.get().strip(), self.cb_cat.get(), self.cb_prio.get()
        desc = self.txt_desc.get("1.0", tk.END).strip()

        if not (user and cat and prio and desc):
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos requeridos.")
            return

        self.manager.create(user, desc, cat, prio)
        self.ent_user.delete(0, tk.END)
        self.cb_cat.set(''); self.cb_prio.set('')
        self.txt_desc.delete("1.0", tk.END)
        self.refresh_table()

    def _get_selected(self) -> Optional[int]:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selección Obligatoria", "Seleccione un ticket del listado para operar.")
            return None
        return int(sel[0])

    def _change_status(self, n_status: str) -> None:
        tid = self._get_selected()
        if tid is not None:
            self.manager.update_status(tid, n_status)
            self.refresh_table()

    def _delete_ticket(self) -> None:
        tid = self._get_selected()
        if tid is not None and messagebox.askyesno("Confirmar Acción", f"¿Está seguro de eliminar permanentemente el ticket ID #{tid}?"):
            self.manager.delete(tid)
            self.refresh_table()
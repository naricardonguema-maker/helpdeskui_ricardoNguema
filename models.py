# ======================================= #
# ----------- Manejo de Datos ----------- #
# ======================================= #
""" 
Estas herramientas nos permiten trabajar con el sistema operativo, 
manejar archivos de datos.
"""
import os
import json
from typing import List, Dict, Any

class Ticket:
    """Entidad que representa una incidencia técnica."""
    def __init__(self, id_t: int, user: str, desc: str, cat: str, prio: str, status: str = "Pendiente") -> None:
        self.id = id_t
        self.usuario = user
        self.descripcion = desc
        self.categoria = cat
        self.prioridad = prio
        self.estado = status

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Ticket":
        return cls(d["id"], d["usuario"], d["descripcion"], d["categoria"], d["prioridad"], d["estado"])


class TicketManager:
    """Gestiona operaciones CRUD y persistencia en un archivo JSON."""
    def __init__(self, path: str = "tickets.json") -> None:
        self.path = path
        self.tickets: List[Ticket] = []
        self.load()

    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.tickets = [Ticket.from_dict(t) for t in json.load(f)]
            except (json.JSONDecodeError, IOError):
                self.tickets = []

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tickets], f, indent=4, ensure_ascii=False)

    # (Retorna el ticket creado para el cuadro de éxito)
    def crear_ticket(self, usuario: str, descripcion: str, categoria: str, prioridad: str) -> Ticket:
        nid = max([t.id for t in self.tickets], default=0) + 1
        nuevo_ticket = Ticket(nid, usuario, descripcion, categoria, prioridad)
        self.tickets.append(nuevo_ticket)
        self.save()
        return nuevo_ticket

    # Implementa el ciclo de estados automáticamente
    def cambiar_estado(self, id_t: int) -> bool:
        for t in self.tickets:
            if t.id == id_t:
                # Si está Pendiente pasa a Resuelto, si está Resuelto vuelve a Pendiente
                t.estado = "Resuelto" if t.estado == "Pendiente" else "Pendiente"
                self.save()
                return True
        return False

    def eliminar_ticket(self, id_t: int) -> bool:
        self.tickets = [t for t in self.tickets if t.id != id_t]
        self.save()
        return True

    def obtener_metricas(self) -> Dict[str, int]:
        return {
            "total": len(self.tickets),
            "pendientes": sum(1 for t in self.tickets if t.estado == "Pendiente"),
            "resueltos": sum(1 for t in self.tickets if t.estado == "Resuelto")
        }

    # MÉTODO requerido por views.py para listar y filtrar en tiempo real
    def actualizar_tabla(self, criterio: str = "") -> List[Ticket]:
        """Filtra y retorna los tickets según el cuadro de búsqueda."""
        if not criterio:
            return self.tickets
            
        criterio = criterio.lower()
        return [
            t for t in self.tickets 
            if criterio in t.usuario.lower() 
            or criterio in t.descripcion.lower() 
            or criterio in t.categoria.lower()
            or criterio in t.prioridad.lower()
            or criterio in t.estado.lower()
        ]
import json
import os
from typing import List, Dict, Any, Optional

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

    def create(self, user: str, desc: str, cat: str, prio: str) -> None:
        nid = max([t.id for t in self.tickets], default=0) + 1
        self.tickets.append(Ticket(nid, user, desc, cat, prio))
        self.save()

    def update_status(self, id_t: int, status: str) -> bool:
        for t in self.tickets:
            if t.id == id_t:
                t.estado = status
                self.save()
                return True
        return False

    def delete(self, id_t: int) -> bool:
        self.tickets = [t for t in self.tickets if t.id != id_t]
        self.save()
        return True

    def metrics(self) -> Dict[str, int]:
        return {
            "total": len(self.tickets),
            "pendientes": sum(1 for t in self.tickets if t.estado == "Pendiente"),
            "resueltos": sum(1 for t in self.tickets if t.estado == "Resuelto")
        }
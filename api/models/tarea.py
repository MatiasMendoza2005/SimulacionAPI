from pydantic import BaseModel
from datetime import datetime

class Tarea(BaseModel):
    TareaID: int
    Descripcion: str
    FechaAsignacion: datetime
    FechaLimite: datetime
    Estado: str
    VoluntarioID: int
    AdministradorID: int
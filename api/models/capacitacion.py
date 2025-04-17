from pydantic import BaseModel
from datetime import datetime

class Capacitacion(BaseModel):
    CursoID: int
    Nombre: str
    FechaInicio: datetime
    FechaFin: datetime
    Categoria: str
    Dificultad: str

class HistorialCapacitacion(BaseModel):
    HistorialID: int
    VoluntarioID: int
    CursoID: int
    FechaInicio: datetime
    FechaFin: datetime
    Estado: str
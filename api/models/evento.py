from pydantic import BaseModel
from typing import List
from datetime import datetime

class Evento(BaseModel):
    EventoID: int
    NombreEvento: str
    Fecha: datetime
    Ubicacion: str
    Descripcion: str
    OrganizadorID: int

class VoluntarioEvento(BaseModel):
    VoluntarioID: int
    EventoID: int
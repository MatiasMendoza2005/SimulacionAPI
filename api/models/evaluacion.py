from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class Evaluacion(BaseModel):
    fecha: date
    resultado_psicologico: str  # Ejemplo: "Estable", "En observación"
    nivel_estrés: int  # Escala de 1 a 5
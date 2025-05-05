from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class Evaluacion(BaseModel):
    fecha: date
    resultado_psicologico: str  
    nivel_estrés: int 
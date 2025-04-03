# api/models/voluntario.py
from pydantic import BaseModel, conint
from typing import Dict
from datetime import date

class Voluntario(BaseModel):
    id: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    genero: str
    tipo_sangre: str  # Tipo de sangre, por ejemplo: 'A+', 'O-', etc.
    
    # Respuestas del test psicológico
    respuestas_test_psicologico: Dict[str, int]  # Respuestas del test psicológico
    
    # Respuestas del test físico
    respuestas_test_fisico: Dict[str, int]  # Respuestas del test físico
    
    fecha_ultimo_test: date  # Fecha de la última evaluación
    fecha_proximo_test: date  # Fecha de la próxima evaluación

from pydantic import BaseModel, conint
from typing import Dict
from datetime import date

class Voluntario(BaseModel):
    id: int
    usuario_id: int
    email: str
    rol_id: int  # Relación con Roles
    fecha_registro: date
    nombre: str
    apellido: str
    fecha_nacimiento: date
    genero: str
    tipo_sangre: str
    telefono: str
    ubicacion: str 
    ci: str  
    estado: str 
    
    respuestas_test_psicologico: Dict[str, int]  
    
    respuestas_test_fisico: Dict[str, int] 
    
    fecha_ultimo_test: date 
    fecha_proximo_test: date


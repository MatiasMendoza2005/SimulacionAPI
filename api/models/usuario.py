from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    contrasena: str
    rolId: int
    fechaRegistro: str
    ci: int

class Rol(BaseModel):
    RolID: int
    NombreRol: str

class Privilegio(BaseModel):
    PrivilegioID: int
    NombrePrivilegio: str
    Descripcion: str
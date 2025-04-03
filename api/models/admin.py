# app/models/admin.py
from pydantic import BaseModel

class Admin(BaseModel):
    username: str
    password: str  # La contraseña debe ser almacenada de manera segura

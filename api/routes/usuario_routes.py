from fastapi import APIRouter, HTTPException, Depends, Header
from api.models.usuario import Usuario, Rol
from typing import List
from api.auth import verify_token

router = APIRouter()

fake_usuarios_db = {
    1: {"id": 1, "nombre": "Juan Pérez", "apellido": "Pérez", "email": "juan.perez@example.com", "rolId": 2, "contrasena": "admin123", "fechaRegistro": "2025-01-01"},
    2: {"id": 2, "nombre": "Ana Gómez", "apellido": "Gómez", "email": "ana.gomez@example.com", "rolId": 1, "contrasena": "admin456", "fechaRegistro": "2025-02-01"}
}

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split("Bearer ")[-1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no válido")
    
    return verify_token(token)

# Ruta para obtener todos los usuarios
@router.get("/usuarios", response_model=List[Usuario])
def get_usuarios(token: str = Depends(get_current_user)):
    return list(fake_usuarios_db.values())

# Ruta para obtener un usuario específico
@router.get("/usuarios/{usuario_id}", response_model=Usuario)
def get_usuario(usuario_id: int, token: str = Depends(get_current_user)):
    usuario = fake_usuarios_db.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

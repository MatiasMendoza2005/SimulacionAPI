# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from api.models.usuario import Usuario, Rol, Privilegio
from typing import List
from pydantic import BaseModel
from datetime import timedelta
from api.auth import create_access_token, verify_token

router = APIRouter()

fake_usuarios_db = {
    1: {"id": 1, "nombre": "Juan", "apellido": "Pérez", "email": "admin@gmail.com", "contrasena": "admin123", "rolId": 1, "fechaRegistro": "2023-01-01"},
    2: {"id": 2, "nombre": "Ana", "apellido": "Gómez", "email": "ana@gmail.com", "contrasena": "usuario", "rolId": 2, "fechaRegistro": "2023-02-01"},
    3: {"id": 3, "nombre": "María", "apellido": "López", "email": "maria@gmail.com", "contrasena": "maria123", "rolId": 2, "fechaRegistro": "2023-03-01"},
    4: {"id": 4, "nombre": "Carlos", "apellido": "García", "email": "carlos@gmail.com", "contrasena": "carlos456", "rolId": 2, "fechaRegistro": "2023-04-15"},
    5: {"id": 5, "nombre": "Laura", "apellido": "Martínez", "email": "laura@gmail.com", "contrasena": "laura789", "rolId": 2, "fechaRegistro": "2023-05-20"},
    6: {"id": 6, "nombre": "Pedro", "apellido": "Sánchez", "email": "pedro@gmail.com", "contrasena": "pedro012", "rolId": 2, "fechaRegistro": "2023-06-10"},
    7: {"id": 7, "nombre": "Sofía", "apellido": "Díaz", "email": "sofia@gmail.com", "contrasena": "sofia345", "rolId": 2, "fechaRegistro": "2023-07-05"}
}

fake_roles_db = {
    1: {"RolID": 1, "NombreRol": "Admin"},
    2: {"RolID": 2, "NombreRol": "Voluntario"}
}

fake_privilegios_db = {
    1: {"PrivilegioID": 1, "NombrePrivilegio": "Acceso completo", "Descripcion": "Acceso total a la plataforma"},
    2: {"PrivilegioID": 2, "NombrePrivilegio": "Acceso limitado", "Descripcion": "Acceso limitado para voluntarios"}
}

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split("Bearer ")[-1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no válido")
    
    return verify_token(token)

# Ruta para obtener todos los usuarios
@router.get("/usuarios")
def get_usuarios(token: str = Depends(get_current_user)):
    return JSONResponse(content=list(fake_usuarios_db.values()), media_type="application/json; charset=utf-8")

# Ruta para obtener un usuario específico
@router.get("/usuarios/{usuario_id}")
def get_usuario(usuario_id: int, token: str = Depends(get_current_user)):
    usuario = fake_usuarios_db.get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return JSONResponse(content=usuario, media_type="application/json; charset=utf-8")

# Ruta para obtener todos los roles
@router.get("/roles")
def get_roles():
    return JSONResponse(content=list(fake_roles_db.values()), media_type="application/json; charset=utf-8")

# Ruta para obtener un rol específico
@router.get("/roles/{rol_id}")
def get_rol(rol_id: int):
    rol = fake_roles_db.get(rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return JSONResponse(content=rol, media_type="application/json; charset=utf-8")

# Ruta para obtener todos los privilegios
@router.get("/privilegios")
def get_privilegios():
    return JSONResponse(content=list(fake_privilegios_db.values()), media_type="application/json; charset=utf-8")

# Ruta para obtener un privilegio específico
@router.get("/privilegios/{privilegio_id}")
def get_privilegio(privilegio_id: int):
    privilegio = fake_privilegios_db.get(privilegio_id)
    if not privilegio:
        raise HTTPException(status_code=404, detail="Privilegio no encontrado")
    return JSONResponse(content=privilegio, media_type="application/json; charset=utf-8")

# Función para verificar la contraseña
def verify_password(plain_password, stored_password):
    return plain_password == stored_password    

# Pydantic modelo para el login
class LoginRequest(BaseModel):
    email: str
    contrasena: str

# Ruta para iniciar sesión (Generar JWT)
@router.post("/login")
def login(credentials: LoginRequest):
    user = None
    for u in fake_usuarios_db.values():
        if u["email"] == credentials.email:
            user = u
            break
    
    if user is None or not verify_password(credentials.contrasena, user["contrasena"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": credentials.email}, expires_delta=access_token_expires)
    
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, media_type="application/json; charset=utf-8")

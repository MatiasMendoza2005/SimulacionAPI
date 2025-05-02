from fastapi import APIRouter, HTTPException, Depends, Header
from api.models.usuario import Usuario, Rol, Privilegio
from typing import List
from pydantic import BaseModel
from datetime import timedelta
from api.auth import create_access_token, verify_token

router = APIRouter()

fake_usuarios_db = {
    1: {"id": 1, "nombre": "Juan", "apellido": "Pérez", "email": "admin@gmail.com", "contrasena": "admin123", "rolId": 1, "fechaRegistro": "2025-01-01"},
    2: {"id": 2, "nombre": "Ana", "apellido": "Gómez", "email": "usuario@gmail.com", "contrasena": "usuario", "rolId": 2, "fechaRegistro": "2025-02-01"}
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

# Ruta para obtener todos los roles
@router.get("/roles", response_model=List[Rol])
def get_roles():
    return list(fake_roles_db.values())

# Ruta para obtener un rol específico
@router.get("/roles/{rol_id}", response_model=Rol)
def get_rol(rol_id: int):
    rol = fake_roles_db.get(rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

# Ruta para obtener todos los privilegios
@router.get("/privilegios", response_model=List[Privilegio])
def get_privilegios():
    return list(fake_privilegios_db.values())

# Ruta para obtener un privilegio específico
@router.get("/privilegios/{privilegio_id}", response_model=Privilegio)
def get_privilegio(privilegio_id: int):
    privilegio = fake_privilegios_db.get(privilegio_id)
    if not privilegio:
        raise HTTPException(status_code=404, detail="Privilegio no encontrado")
    return privilegio

# Función para verificar la contraseña
def verify_password(plain_password, stored_password):
    return plain_password == stored_password    

# Pydantic modelo para el login
class LoginRequest(BaseModel):
    email: str  # Cambié username por email
    password: str

# Ruta para iniciar sesión (Generar JWT)
@router.post("/login")
def login(credentials: LoginRequest):
    # Buscar al usuario por su email en lugar de username
    user = None
    for u in fake_usuarios_db.values():
        if u["email"] == credentials.email:
            user = u
            break
    
    if user is None or not verify_password(credentials.password, user["contrasena"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Crear el token de acceso
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": credentials.email}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

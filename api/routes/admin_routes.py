from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.auth import create_access_token, verify_token
from datetime import timedelta

router = APIRouter()

# Base de datos simulada de administradores (sin MongoDB)
fake_admin_db = {
    "admin": {
        "username": "admin",
        "password": "admin",
    }
}

# Función para verificar si la contraseña es correcta
def verify_password(plain_password, stored_password):
    return plain_password == stored_password    

# Pydantic modelo para el login
class LoginRequest(BaseModel):
    username: str
    password: str

# Ruta para iniciar sesión (Generar JWT)
@router.post("/login")
def login(credentials: LoginRequest):
    user = fake_admin_db.get(credentials.username)
    if user is None or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Crear el token de acceso
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": credentials.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para verificar el token JWT (ejemplo de ruta protegida)
#@router.get("/protected")
#def protected_route(token: str):
#    user = verify_token(token)
#    if user is None:
#        raise HTTPException(status_code=401, detail="Token no válido")
#    
#    return {"message": "Acceso autorizado", "user": user}

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from typing import Optional
from api.models.usuario import Usuario

SECRET_KEY = "mi_super_clave_secreta_de_32_caracteres_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duración del token (en minutos)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para generar el token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar el token JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # El token puede incluir información del usuario, como ID o nombre
        return payload  # Devolver los datos decodificados del token
    except jwt.PyJWTError:
        return None  # Si el token no es válido

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token no válido o expirado")
    return payload
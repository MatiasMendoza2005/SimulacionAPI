from fastapi import APIRouter, HTTPException, Depends, Header
from api.models.evaluacion import Evaluacion, EvaluacionCreate
from typing import List
from api.auth import verify_token

router = APIRouter()

# Fake DB de Evaluaciones
fake_evaluaciones_db = {
    1: {"id": 1, "voluntario_id": 1, "test_id": 1, "fecha": "2025-01-15"},
    2: {"id": 2, "voluntario_id": 2, "test_id": 2, "fecha": "2025-02-01"}
}

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split("Bearer ")[-1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no válido")
    
    return verify_token(token)

# Ruta para obtener todas las evaluaciones
@router.get("/evaluaciones", response_model=List[Evaluacion])
def get_evaluaciones(token: str = Depends(get_current_user)):
    return list(fake_evaluaciones_db.values())

# Ruta para obtener una evaluación específica
@router.get("/evaluaciones/{evaluacion_id}", response_model=Evaluacion)
def get_evaluacion(evaluacion_id: int, token: str = Depends(get_current_user)):
    evaluacion = fake_evaluaciones_db.get(evaluacion_id)
    if not evaluacion:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluacion

# Ruta para crear una evaluación
@router.post("/evaluaciones", response_model=Evaluacion)
def create_evaluacion(evaluacion: EvaluacionCreate, token: str = Depends(get_current_user)):
    new_id = max(fake_evaluaciones_db.keys()) + 1  # Generamos un nuevo ID de forma sencilla
    fake_evaluaciones_db[new_id] = evaluacion.dict()  # Guardamos la nueva evaluación
    return fake_evaluaciones_db[new_id]

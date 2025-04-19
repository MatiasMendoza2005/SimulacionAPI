from fastapi import APIRouter, HTTPException, Depends, Header
from api.models.reporte import Reporte, ReporteCreate
from typing import List
from api.auth import verify_token

router = APIRouter()

# Fake DB de Reportes
fake_reportes_db = {
    1: {"id": 1, "voluntario_id": 1, "fecha_generado": "2025-01-15", "estado_general": "Activo", "resumen_emocional": "Estrés moderado", "resumen_fisico": "Fatiga leve"},
    2: {"id": 2, "voluntario_id": 2, "fecha_generado": "2025-02-01", "estado_general": "Inactivo", "resumen_emocional": "Estrés alto", "resumen_fisico": "Cansancio extremo"}
}

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split("Bearer ")[-1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no válido")
    
    return verify_token(token)

# Ruta para obtener todos los reportes
@router.get("/reportes", response_model=List[Reporte])
def get_reportes(token: str = Depends(get_current_user)):
    return list(fake_reportes_db.values())

# Ruta para obtener un reporte específico
@router.get("/reportes/{reporte_id}", response_model=Reporte)
def get_reporte(reporte_id: int, token: str = Depends(get_current_user)):
    reporte = fake_reportes_db.get(reporte_id)
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte

# Ruta para crear un reporte
@router.post("/reportes", response_model=Reporte)
def create_reporte(reporte: ReporteCreate, token: str = Depends(get_current_user)):
    new_id = max(fake_reportes_db.keys()) + 1  # Generamos un nuevo ID de forma sencilla
    fake_reportes_db[new_id] = reporte.dict()  # Guardamos el nuevo reporte
    return fake_reportes_db[new_id]

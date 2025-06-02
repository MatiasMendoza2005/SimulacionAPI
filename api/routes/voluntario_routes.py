# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from api.auth import verify_token
from typing import List
from api.models.voluntario import Voluntario
from fastapi import Request
from datetime import date
from fastapi.responses import JSONResponse
import json
from fastapi.encoders import jsonable_encoder

router = APIRouter()

fake_voluntarios_db = {
    1: {
        "id": 1,
        "usuario_id": 1,
        "email": "admin@gmail.com",
        "rol_id": 1,
        "fecha_registro": "2023-01-01",
        "nombre": "Franco",
        "apellido": "Torrez",
        "fecha_nacimiento": "2005-05-31",
        "genero": "Masculino",
        "tipo_sangre": "O+",
        "telefono": "+591 78281321",
        "ubicacion": "Av. Banzer, 8vo Anillo",
        "ci": "9782951",
        "estado": "Activo",
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 2,
            "hacer_algo_diferente": 3,
            "disminucion_apetito": 1,
            "dificultad_relajarse": 4,
            "dificultad_concentrarse": 2,
            "insomnio": 3,
            "inestabilidad_emocional": 2,
            "preocupacion_constante": 3
        },
        "respuestas_test_fisico": {
            "cansancio": 2,
            "irritacion_piel": 1,
            "dificultad_respirar": 2,
            "dolor_pecho": 1,
            "palpitaciones": 2,
            "irritacion_ojos": 3,
            "dificultad_respiracion": 2,
            "congestion_nasal": 1
        },
        "fecha_ultimo_test": "2024-01-15",
        "fecha_proximo_test": "2024-04-15"
    },
    2: {
        "id": 2,
        "usuario_id": 2,
        "email": "aoc@gmail.com",
        "rol_id": 2,
        "fecha_registro": "2023-02-01",
        "nombre": "Alejandro",
        "apellido": "Ormachea",
        "fecha_nacimiento": "1992-08-22",
        "genero": "Masculino",
        "tipo_sangre": "A+",
        "telefono": "+591 68371234",
        "ubicacion": "Calle Libertad, 4to Anillo",
        "ci": "8774732",
        "estado": "Activo",
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 4,
            "hacer_algo_diferente": 2,
            "disminucion_apetito": 3,
            "dificultad_relajarse": 1,
            "dificultad_concentrarse": 4,
            "insomnio": 2,
            "inestabilidad_emocional": 3,
            "preocupacion_constante": 4
        },
        "respuestas_test_fisico": {
            "cansancio": 3,
            "irritacion_piel": 2,
            "dificultad_respirar": 4,
            "dolor_pecho": 2,
            "palpitaciones": 3,
            "irritacion_ojos": 1,
            "dificultad_respiracion": 3,
            "congestion_nasal": 2
        },
        "fecha_ultimo_test": "2024-02-01",
        "fecha_proximo_test": "2024-05-01"
    },
    3: {
        "id": 3,
        "usuario_id": 3,
        "email": "mrmp@gmail.com",
        "rol_id": 2,
        "fecha_registro": "2023-03-01",
        "nombre": "Matías",
        "apellido": "Mendoza",
        "fecha_nacimiento": "1995-04-18",
        "genero": "Masculino",
        "tipo_sangre": "B+",
        "telefono": "+591 79887713",
        "ubicacion": "Av. Piraí, 3er Anillo",
        "ci": "9604708",
        "estado": "Activo",
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 1,
            "hacer_algo_diferente": 4,
            "disminucion_apetito": 2,
            "dificultad_relajarse": 3,
            "dificultad_concentrarse": 1,
            "insomnio": 4,
            "inestabilidad_emocional": 1,
            "preocupacion_constante": 2
        },
        "respuestas_test_fisico": {
            "cansancio": 4,
            "irritacion_piel": 3,
            "dificultad_respirar": 1,
            "dolor_pecho": 1,
            "palpitaciones": 4,
            "irritacion_ojos": 2,
            "dificultad_respiracion": 1,
            "congestion_nasal": 3
        },
        "fecha_ultimo_test": "2024-03-10",
        "fecha_proximo_test": "2024-06-10"
    },
    4: {
        "id": 4,
        "usuario_id": 4,
        "email": "carlos@gmail.com",
        "rol_id": 2,
        "fecha_registro": "2023-04-15",
        "nombre": "Carlos",
        "apellido": "García",
        "fecha_nacimiento": "1988-11-30",
        "genero": "Masculino",
        "tipo_sangre": "AB-",
        "telefono": "+591 78487654",
        "ubicacion": "Calle Sucre, 6to Anillo",
        "ci": "9641467",
        "estado": "Inactivo",
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 3,
            "hacer_algo_diferente": 1,
            "disminucion_apetito": 4,
            "dificultad_relajarse": 2,
            "dificultad_concentrarse": 3,
            "insomnio": 1,
            "inestabilidad_emocional": 4,
            "preocupacion_constante": 1
        },
        "respuestas_test_fisico": {
            "cansancio": 1,
            "irritacion_piel": 4,
            "dificultad_respirar": 3,
            "dolor_pecho": 2,
            "palpitaciones": 1,
            "irritacion_ojos": 4,
            "dificultad_respiracion": 2,
            "congestion_nasal": 1
        },
        "fecha_ultimo_test": "2023-12-01",
        "fecha_proximo_test": "2024-03-01"
    },
    5: {
        "id": 5,
        "usuario_id": 5,
        "email": "laura@gmail.com",
        "rol_id": 2,
        "fecha_registro": "2023-05-20",
        "nombre": "Laura",
        "apellido": "Martínez",
        "fecha_nacimiento": "1993-07-12",
        "genero": "Femenino",
        "tipo_sangre": "O-",
        "telefono": "+591 76548271",
        "ubicacion": "Av. Busch, 7mo Anillo",
        "ci": "9746451",
        "estado": "Activo",
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 5,
            "hacer_algo_diferente": 3,
            "disminucion_apetito": 2,
            "dificultad_relajarse": 4,
            "dificultad_concentrarse": 3,
            "insomnio": 2,
            "inestabilidad_emocional": 3,
            "preocupacion_constante": 4
        },
        "respuestas_test_fisico": {
            "cansancio": 3,
            "irritacion_piel": 2,
            "dificultad_respirar": 3,
            "dolor_pecho": 1,
            "palpitaciones": 2,
            "irritacion_ojos": 3,
            "dificultad_respiracion": 4,
            "congestion_nasal": 2
        },
        "fecha_ultimo_test": "2024-05-01",
        "fecha_proximo_test": "2024-08-01"
    },
    6: {
        "id": 6,
        "usuario_id": 6,
        "email": "pedro@gmail.com",
        "rol_id": 2,
        "fecha_registro": "2023-06-10",
        "nombre": "Pedro",
        "apellido": "Sánchez",
        "fecha_nacimiento": "1990-09-25",
        "genero": "Masculino",
        "tipo_sangre": "A-",
        "telefono": "+591 68271644",
        "ubicacion": "Av. Las Américas, 2do Anillo",
        "ci": "98373613",
        "estado": "Activo",
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 2,
            "hacer_algo_diferente": 4,
            "disminucion_apetito": 1,
            "dificultad_relajarse": 3,
            "dificultad_concentrarse": 2,
            "insomnio": 3,
            "inestabilidad_emocional": 2,
            "preocupacion_constante": 3
        },
        "respuestas_test_fisico": {
            "cansancio": 2,
            "irritacion_piel": 1,
            "dificultad_respirar": 2,
            "dolor_pecho": 1,
            "palpitaciones": 2,
            "irritacion_ojos": 3,
            "dificultad_respiracion": 2,
            "congestion_nasal": 1
        },
        "fecha_ultimo_test": "2024-06-15",
        "fecha_proximo_test": "2024-09-15"
    },
    7: {
        "id": 7,
        "usuario_id": 7,
        "email": "sofia@gmail.com",
        "rol_id": 2,
        "fecha_registro": "2023-07-05",
        "nombre": "Sofía",
        "apellido": "Díaz",
        "fecha_nacimiento": "1996-12-05",
        "genero": "Femenino",
        "tipo_sangre": "B+",
        "telefono": "+591 78217344",
        "ubicacion": "Calle Monseñor Rivero, 1er Anillo",
        "ci": "98731234",
        "estado": "Activo",
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 4,
            "hacer_algo_diferente": 2,
            "disminucion_apetito": 3,
            "dificultad_relajarse": 1,
            "dificultad_concentrarse": 4,
            "insomnio": 2,
            "inestabilidad_emocional": 3,
            "preocupacion_constante": 4
        },
        "respuestas_test_fisico": {
            "cansancio": 3,
            "irritacion_piel": 2,
            "dificultad_respirar": 4,
            "dolor_pecho": 2,
            "palpitaciones": 3,
            "irritacion_ojos": 1,
            "dificultad_respiracion": 3,
            "congestion_nasal": 2
        },
        "fecha_ultimo_test": "2024-07-01",
        "fecha_proximo_test": "2024-10-01"
    }
}

def get_current_user(authorization: str = Header(...)):
    # La función de autenticación se mantiene igual
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split("Bearer ")[-1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no válido")
    
    return verify_token(token)

@router.get("/voluntarios", response_model=List[Voluntario])
def get_voluntarios(token: str = Depends(get_current_user)):
    formatted_voluntarios = []
    for vol in fake_voluntarios_db.values():
        formatted = vol.copy()
        for date_field in ['fecha_registro', 'fecha_nacimiento', 'fecha_ultimo_test', 'fecha_proximo_test']:
            if formatted.get(date_field):
                formatted[date_field] = date.fromisoformat(formatted[date_field])
        formatted_voluntarios.append(formatted)

    # Convertir a JSON serializable + devolver con UTF-8
    return JSONResponse(
        content=json.loads(json.dumps(jsonable_encoder(formatted_voluntarios), ensure_ascii=False)),
        media_type="application/json; charset=utf-8"
    )


@router.get("/voluntarios/{voluntario_id}", response_model=Voluntario)
def get_voluntario(voluntario_id: int, token: str = Depends(get_current_user)):
    voluntario = fake_voluntarios_db.get(voluntario_id)
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")

    formatted = voluntario.copy()
    for date_field in ['fecha_registro', 'fecha_nacimiento', 'fecha_ultimo_test', 'fecha_proximo_test']:
        if formatted.get(date_field):
            formatted[date_field] = date.fromisoformat(formatted[date_field])

    return JSONResponse(
        content=json.loads(json.dumps(jsonable_encoder(formatted), ensure_ascii=False)),
        media_type="application/json; charset=utf-8"
    )


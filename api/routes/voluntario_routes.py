from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from api.auth import verify_token
from typing import List
from api.models.voluntario import Voluntario
from fastapi import Request
from datetime import date

router = APIRouter()

fake_voluntarios_db = {
    1: {
        "id": 1, 
        "nombre": "Juan Pérez", 
        "apellido": "Pérez", 
        "fecha_nacimiento": "1990-01-05", 
        "telefono": "+591 76291234", 
        "ubicacion": "Av. Banzer, 8vo Anillo", 
        "ci": "97841123", 
        "estado": "Activo",
        "genero": "Masculino",  
        "tipo_sangre": "O+",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 3,
            "hacer_algo_diferente": 2,
            "disminucion_apetito": 1,
            "dificultad_relajarse": 3,
            "dificultad_concentrarse": 4,
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
        "fecha_ultimo_test": "2025-03-15",
        "fecha_proximo_test": "2025-06-15"
    },
    2: {
        "id": 2, 
        "nombre": "Ana Gómez", 
        "apellido": "Gómez", 
        "fecha_nacimiento": "1985-04-23", 
        "telefono": "+591 65498127", 
        "ubicacion": "Av. Irala, Santa Cruz", 
        "ci": "65498127", 
        "estado": "Inactivo",
        "genero": "Femenino",  
        "tipo_sangre": "A-",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 4,
            "hacer_algo_diferente": 3,
            "disminucion_apetito": 2,
            "dificultad_relajarse": 3,
            "dificultad_concentrarse": 4,
            "insomnio": 3,
            "inestabilidad_emocional": 2,
            "preocupacion_constante": 5
        },
        "respuestas_test_fisico": {
            "cansancio": 4,
            "irritacion_piel": 2,
            "dificultad_respirar": 3,
            "dolor_pecho": 1,
            "palpitaciones": 3,
            "irritacion_ojos": 4,
            "dificultad_respiracion": 3,
            "congestion_nasal": 2
        },
        "fecha_ultimo_test": "2025-02-10",
        "fecha_proximo_test": "2025-05-10"
    },
    3: {
        "id": 3, 
        "nombre": "Carlos López", 
        "apellido": "López", 
        "fecha_nacimiento": "1992-08-12", 
        "telefono": "+591 81329764", 
        "ubicacion": "Av. Piraí, Santa Cruz", 
        "ci": "81329764", 
        "estado": "Activo",
        "genero": "Masculino",  
        "tipo_sangre": "B+",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 2,
            "hacer_algo_diferente": 1,
            "disminucion_apetito": 3,
            "dificultad_relajarse": 3,
            "dificultad_concentrarse": 2,
            "insomnio": 1,
            "inestabilidad_emocional": 2,
            "preocupacion_constante": 3
        },
        "respuestas_test_fisico": {
            "cansancio": 2,
            "irritacion_piel": 1,
            "dificultad_respirar": 2,
            "dolor_pecho": 1,
            "palpitaciones": 2,
            "irritacion_ojos": 1,
            "dificultad_respiracion": 2,
            "congestion_nasal": 1
        },
        "fecha_ultimo_test": "2025-01-05",
        "fecha_proximo_test": "2025-04-05"
    },
    4: {
        "id": 4, 
        "nombre": "María Rodríguez", 
        "apellido": "Rodríguez", 
        "fecha_nacimiento": "1988-07-30", 
        "telefono": "+591 98765432", 
        "ubicacion": "Calle 10, Santa Cruz", 
        "ci": "98765432", 
        "estado": "Inactivo",
        "genero": "Femenino",  
        "tipo_sangre": "AB+",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 5,
            "hacer_algo_diferente": 4,
            "disminucion_apetito": 2,
            "dificultad_relajarse": 3,
            "dificultad_concentrarse": 4,
            "insomnio": 3,
            "inestabilidad_emocional": 4,
            "preocupacion_constante": 5
        },
        "respuestas_test_fisico": {
            "cansancio": 5,
            "irritacion_piel": 4,
            "dificultad_respirar": 3,
            "dolor_pecho": 1,
            "palpitaciones": 4,
            "irritacion_ojos": 4,
            "dificultad_respiracion": 4,
            "congestion_nasal": 3
        },
        "fecha_ultimo_test": "2025-03-20",
        "fecha_proximo_test": "2025-06-20"
    },
    5: {
        "id": 5, 
        "nombre": "Pedro Martínez", 
        "apellido": "Martínez", 
        "fecha_nacimiento": "1994-05-18", 
        "telefono": "+591 98712345", 
        "ubicacion": "Av. Busch, Santa Cruz", 
        "ci": "98712345", 
        "estado": "Activo",
        "genero": "Masculino",  
        "tipo_sangre": "O-",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 3,
            "hacer_algo_diferente": 2,
            "disminucion_apetito": 5,
            "dificultad_relajarse": 4,
            "dificultad_concentrarse": 3,
            "insomnio": 2,
            "inestabilidad_emocional": 3,
            "preocupacion_constante": 4
        },
        "respuestas_test_fisico": {
            "cansancio": 4,
            "irritacion_piel": 3,
            "dificultad_respirar": 3,
            "dolor_pecho": 2,
            "palpitaciones": 2,
            "irritacion_ojos": 3,
            "dificultad_respiracion": 4,
            "congestion_nasal": 3
        },
        "fecha_ultimo_test": "2025-02-25",
        "fecha_proximo_test": "2025-05-25"
    },
    6: {
        "id": 6, 
        "nombre": "Lucía Méndez", 
        "apellido": "Méndez", 
        "fecha_nacimiento": "1995-03-11", 
        "telefono": "+591 76543210", 
        "ubicacion": "Av. Las Américas, Santa Cruz", 
        "ci": "76543210", 
        "estado": "Activo",
        "genero": "Femenino",  
        "tipo_sangre": "A+",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 4,
            "hacer_algo_diferente": 3,
            "disminucion_apetito": 1,
            "dificultad_relajarse": 2,
            "dificultad_concentrarse": 5,
            "insomnio": 3,
            "inestabilidad_emocional": 2,
            "preocupacion_constante": 4
        },
        "respuestas_test_fisico": {
            "cansancio": 2,
            "irritacion_piel": 1,
            "dificultad_respirar": 1,
            "dolor_pecho": 1,
            "palpitaciones": 2,
            "irritacion_ojos": 3,
            "dificultad_respiracion": 4,
            "congestion_nasal": 1
        },
        "fecha_ultimo_test": "2025-02-05",
        "fecha_proximo_test": "2025-05-05"
    },
    7: {
        "id": 7, 
        "nombre": "Ricardo Ramírez", 
        "apellido": "Ramírez", 
        "fecha_nacimiento": "1993-12-05", 
        "telefono": "+591 78451236", 
        "ubicacion": "Calle Libertad, Santa Cruz", 
        "ci": "78451236", 
        "estado": "Inactivo",
        "genero": "Masculino",  
        "tipo_sangre": "B+",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 1,
            "hacer_algo_diferente": 2,
            "disminucion_apetito": 2,
            "dificultad_relajarse": 4,
            "dificultad_concentrarse": 3,
            "insomnio": 2,
            "inestabilidad_emocional": 1,
            "preocupacion_constante": 2
        },
        "respuestas_test_fisico": {
            "cansancio": 3,
            "irritacion_piel": 2,
            "dificultad_respirar": 4,
            "dolor_pecho": 1,
            "palpitaciones": 3,
            "irritacion_ojos": 2,
            "dificultad_respiracion": 1,
            "congestion_nasal": 4
        },
        "fecha_ultimo_test": "2025-01-20",
        "fecha_proximo_test": "2025-04-20"
    },
    8: {
        "id": 8, 
        "nombre": "Claudia Díaz", 
        "apellido": "Díaz", 
        "fecha_nacimiento": "1990-09-22", 
        "telefono": "+591 79123456", 
        "ubicacion": "Av. Litoral, Santa Cruz", 
        "ci": "79123456", 
        "estado": "Activo",
        "genero": "Femenino",  
        "tipo_sangre": "O+",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 4,
            "hacer_algo_diferente": 3,
            "disminucion_apetito": 1,
            "dificultad_relajarse": 2,
            "dificultad_concentrarse": 4,
            "insomnio": 3,
            "inestabilidad_emocional": 3,
            "preocupacion_constante": 4
        },
        "respuestas_test_fisico": {
            "cansancio": 3,
            "irritacion_piel": 1,
            "dificultad_respirar": 3,
            "dolor_pecho": 2,
            "palpitaciones": 2,
            "irritacion_ojos": 3,
            "dificultad_respiracion": 4,
            "congestion_nasal": 3
        },
        "fecha_ultimo_test": "2025-02-10",
        "fecha_proximo_test": "2025-05-10"
    },
    9: {
        "id": 9, 
        "nombre": "Luis Gómez", 
        "apellido": "Gómez", 
        "fecha_nacimiento": "1988-02-14", 
        "telefono": "+591 76587654", 
        "ubicacion": "Calle El Parque, Santa Cruz", 
        "ci": "76587654", 
        "estado": "Activo",
        "genero": "Masculino",  
        "tipo_sangre": "A+",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 5,
            "hacer_algo_diferente": 4,
            "disminucion_apetito": 2,
            "dificultad_relajarse": 3,
            "dificultad_concentrarse": 4,
            "insomnio": 4,
            "inestabilidad_emocional": 3,
            "preocupacion_constante": 4
        },
        "respuestas_test_fisico": {
            "cansancio": 3,
            "irritacion_piel": 2,
            "dificultad_respirar": 4,
            "dolor_pecho": 1,
            "palpitaciones": 4,
            "irritacion_ojos": 3,
            "dificultad_respiracion": 3,
            "congestion_nasal": 2
        },
        "fecha_ultimo_test": "2025-01-25",
        "fecha_proximo_test": "2025-04-25"
    },
    10: {
        "id": 10, 
        "nombre": "Javier Martínez", 
        "apellido": "Martínez", 
        "fecha_nacimiento": "1989-07-01", 
        "telefono": "+591 77665544", 
        "ubicacion": "Av. San Martín, Santa Cruz", 
        "ci": "77665544", 
        "estado": "Inactivo",
        "genero": "Masculino",  
        "tipo_sangre": "O-",  
        "respuestas_test_psicologico": {
            "pensamientos_no_deseados": 2,
            "hacer_algo_diferente": 3,
            "disminucion_apetito": 4,
            "dificultad_relajarse": 2,
            "dificultad_concentrarse": 3,
            "insomnio": 2,
            "inestabilidad_emocional": 2,
            "preocupacion_constante": 3
        },
        "respuestas_test_fisico": {
            "cansancio": 4,
            "irritacion_piel": 2,
            "dificultad_respirar": 3,
            "dolor_pecho": 1,
            "palpitaciones": 3,
            "irritacion_ojos": 4,
            "dificultad_respiracion": 2,
            "congestion_nasal": 3
        },
        "fecha_ultimo_test": "2025-02-15",
        "fecha_proximo_test": "2025-05-15"
    }
}

# Función para verificar el token
def get_current_user(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = authorization.split("Bearer ")[-1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Token no válido")
    
    return verify_token(token)

# Ruta para obtener la lista de voluntarios
@router.get("/voluntarios", response_model=List[Voluntario])
def get_voluntarios(token: str = Depends(get_current_user)):
    return list(fake_voluntarios_db.values())

# Ruta para obtener un voluntario específico
@router.get("/voluntarios/{voluntario_id}", response_model=Voluntario)
def get_voluntario(voluntario_id: int, token: str = Depends(get_current_user)):
    voluntario = fake_voluntarios_db.get(voluntario_id)
    if not voluntario:
        raise HTTPException(status_code=404, detail="Voluntario no encontrado")
    return voluntario

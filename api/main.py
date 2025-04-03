from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.voluntario_routes import router as voluntario_router
from api.routes.admin_routes import router as admin_router

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen (puedes restringir esto a un dominio específico)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP: GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir las rutas de los administradores y voluntarios
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(voluntario_router, prefix="/admin", tags=["Voluntarios"])

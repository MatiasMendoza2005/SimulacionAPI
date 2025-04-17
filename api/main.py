from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.voluntario_routes import router as voluntario_router
from api.routes.admin_routes import router as admin_router
from api.routes.usuario_routes import router as usuario_router

app = FastAPI()

#Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Rutas
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(voluntario_router, prefix="/voluntario", tags=["Voluntarios"])

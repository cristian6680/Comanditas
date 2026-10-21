from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db
from app.api.v1.categorias import router as categorias_router
from app.api.v1.productos import router as productos_router
from app.api.v1.auth import router as auth_router
from app.api.deps import get_current_user
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API para el sistema de gestión de comandas y pedidos de Comanditas"
)

# Registrar enrutadores modulares V1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(categorias_router, prefix="/api/v1")
app.include_router(productos_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def read_root():
    return {
        "sistema": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "estado": "Online 🚀"
    }

@app.get("/health/db", tags=["Health"])
def health_check_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        return {
            "database": "postgresql",
            "conexion": "exitosa",
            "resultado": result.scalar()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando a la BD: {str(e)}")

@app.get("/api/v1/auth/me", response_model=UsuarioResponse, tags=["Autenticación"])
def leer_usuario_autenticado(usuario_actual: Usuario = Depends(get_current_user)):
    """
    Endpoint privado protegido: Requiere Token Bearer JWT en las cabeceras HTTP.
    """
    return usuario_actual


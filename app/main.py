from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db, engine, Base
import app.models  # Registra los modelos ORM para SQLAlchemy

# Crea automáticamente en PostgreSQL las tablas que no existan (mesas, pedidos, etc.)
Base.metadata.create_all(bind=engine)

from app.api.v1.auth import router as auth_router
from app.api.v1.categorias import router as categorias_router
from app.api.v1.productos import router as productos_router
from app.api.v1.pedidos import router as pedidos_router
from app.api.v1.kds import router as kds_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API para el sistema de gestión de comandas y pedidos de Comanditas"
)

# Registrar enrutadores modulares V1 (una sola vez por router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(categorias_router, prefix="/api/v1")
app.include_router(productos_router, prefix="/api/v1")
app.include_router(pedidos_router, prefix="/api/v1")
app.include_router(kds_router, prefix="/api/v1")

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
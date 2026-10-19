from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.core.database import get_db
from app.api.v1.categorias import router as categorias_router
from app.api.v1.productos import router as productos_router

app = FastAPI(
    title=settings.PROYECT_NAME,
    version=settings.VERSION,
    description="Backend API para el sistema de gestión de comandas y pedidos"
)

# Registrar los enrutadores con prefijo /api/v1
app.include_router(categorias_router,prefix="/api/v1")
app.include_router(productos_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
def read_root():
    return {
        "sistema": settings.PROYECT_NAME,
        "version": settings.VERSION,
        "estado": "Online"
    }

@app.get("/health/db", tags=["Health"])
def health_check_db(db: Session = Depends(get_db)):
    try:
        # Ejecutar una consulta simple para verificar la conexión activa
        result = db.execute(text("SELECT 1"))
        return {
            "database": "postgresql",
            "conexion": "exitosa",
            "resultado": result.scalar()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando a la BD: {str(e)}")

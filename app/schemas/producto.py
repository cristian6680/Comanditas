from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime 
from typing import Optional 
from app.schemas.categoria import CategoriaResponse

class ProductoBase(BaseModel):
    categoria_id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal = Field(gt=0, description="El precio debe ser mayor a 0")
    disponible: Optional[bool] = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    categoria_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(default=None, gt=0)
    disponible: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id: int
    creado_en: datetime
    categoria: Optional[CategoriaResponse] = None 

    model_config = ConfigDict(from_attribute=True)


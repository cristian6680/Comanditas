from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from app.schemas.producto import ProductoResponse

# DTO para los items al crear un pedido
class DetallePedidoCreate(BaseModel):
	producto_id: int
	cantidad: int = Field(gt=0, description="La cantidad debe ser al menos 1")
	observaciones: Optional[str] = None

class PedidoCreate(BaseModel):
	mesa_id: int
	notas: Optional[str] = None
	detalles: List[DetallePedidoCreate] = Field(min_items=1, description="El pedido debe tener al menos un item")

# DTOs de respuesta
class DetallePedidoResponse(BaseModel):
	id: int
	producto_id: int
	precio_unitario: Decimal
	subtotal: Decimal
	observaciones: Optional[str] = None
	producto: Optional[ProductoResponse] = None

	model_config = ConfigDict(from_attributes=True)

class PedidoResponse(BaseModel):
	id: int
	mesa_id: int
	usuario_id: int
	estado: str 
	total: Decimal
	notas: Optional[str] = None
	creado_en: datetime
	detalles: List[DetallePedidoResponse] = []

	model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from typing import Optional

class MesaBase(BaseModel):
	numero: int
	capacidad: Optional[int] = 4

class MesaCreate(MesaBase):
	pass

class MesaResponse(MesaBase):
	id: int
	estado: str 

	model_config = ConfigDict(from_attributes=True)

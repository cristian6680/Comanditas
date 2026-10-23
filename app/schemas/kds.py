
# Esquema DTO Pydantic: Definimos la validación para cuando el cocinero cambia el estado de un renglón/item de comanda   

# app/schemas/kds.py
from pydantic import BaseModel
from enum import Enum

# Para que no haya errores y los datos sean strings
class EstadoItemKDS(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"

class ActualizarEstadoItem(BaseModel):
    estado: EstadoItemKDS
# Endpoint y Rutas REST/WebSocket
# Integramos el controlador que consulta los pedidos pendientes e informa los cambios en tiempo real


# app/api/v1/kds.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.pedido import Pedido, DetallePedido
from app.schemas.kds import ActualizarEstadoItem
from app.services.ws_manager import manager

router = APIRouter(prefix="/kds", tags=["KDS - Pantalla de Cocina"])

# WebSocket para la pantalla KDS
@router.websocket("/ws")
async def websocket_kds_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Obtener comandas activas para la cocina
@router.get("/comandas")
def obtener_comandas_cocina(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    pedidos_activos = db.query(Pedido).filter(
        Pedido.estado.in_(["PENDIENTE", "EN_PREPARACION"])
    ).all()
    return pedidos_activos

# Cambiar el estado de un renglón de pedido desde la pantalla táctil
@router.patch("/items/{item_id}/estado")
async def cambiar_estado_item(
    item_id: int,
    payload: ActualizarEstadoItem,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    item = db.query(DetallePedido).filter(DetallePedido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item de comanda no encontrado")

    item.estado = payload.estado
    db.commit()

    # 🔔 Transmitir el evento en tiempo real por WebSocket a todas las pantallas
    await manager.broadcast({
        "evento": "CAMBIO_ESTADO_ITEM",
        "data": {
            "item_id": item.id,
            "pedido_id": item.pedido_id,
            "nuevo_estado": item.estado
        }
    })

    return {"mensaje": "Estado actualizado correctamente", "nuevo_estado": item.estado}
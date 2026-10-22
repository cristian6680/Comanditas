from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.usuario import Usuario
from app.models.mesa import Mesa
from app.models.producto import Producto
from app.models.pedido import Pedido, DetallePedido
from app.schemas.pedido import PedidoCreate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos / Comandas"])

@router.get("/", response_model=List[PedidoResponse])
def listar_pedidos(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user)
):
    """Obtiene la lista de comandas registradas (Requiere Autenticación)"""
    return db.query(Pedido).order_by(Pedido.creado_en.desc()).all()

@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    pedido_in: PedidoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user)
):
    """
    Crea un pedido transaccional:
    1. Verifica existencia de mesa y productos.
    2. Calcula subprecio y total.
    3. Cambia estado de la mesa a 'ocupada'.
    4. Confirma todo en un único commit (ACID).
    """
    # 1. Verificar mesa
    mesa = db.query(Mesa).filter(Mesa.id == pedido_in.mesa_id).first()
    if not mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La mesa ID {pedido_in.mesa_id} no existe"
        )

    # 2. Inicializar cabecera del pedido
    nuevo_pedido = Pedido(
        mesa_id=pedido_in.mesa_id,
        usuario_id=usuario_actual.id,
        notas=pedido_in.notas,
        estado="pendiente",
        total=0.0
    )
    db.add(nuevo_pedido)
    db.flush()  # Asigna ID al pedido dentro de la transacción activa

    monto_total = 0.0

    # 3. Procesar renglones de la comanda
    for item in pedido_in.detalles:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not producto:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto ID {item.producto_id} no existe"
            )
        if not producto.disponible:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto '{producto.nombre}' no se encuentra disponible"
            )

        subtotal = float(producto.precio) * item.cantidad
        monto_total += subtotal

        detalle = DetallePedido(
            pedido_id=nuevo_pedido.id,
            producto_id=producto.id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio,
            subtotal=subtotal,
            observaciones=item.observaciones
        )
        db.add(detalle)

    # 4. Actualizar total y estado de la mesa
    nuevo_pedido.total = monto_total
    mesa.estado = "ocupada"

    # 5. Confirmar transacción atómica
    db.commit()
    db.refresh(nuevo_pedido)

    return nuevo_pedido
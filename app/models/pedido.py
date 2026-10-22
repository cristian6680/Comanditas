from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base 

class Pedido(Base):
	__tablename__ = "pedidos"

	id = Column(Integer, primary_key=True, index=True)
	mesa_id = Column(Integer, ForeignKey("mesas.id", ondelete="RESTRICT"), nullable=False)
	usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False)
	estado = Column(String(20), nullable=False, default="pendiente") # 'pendiente', 'en_preparacion', 'listo', 'entregado', 'pagado', 'cancelado'
	total = Column(Numeric(10, 2), nullable=False, default=0.0)
	notas = Column(Text, nullable=True)
	creado_en = Column(DateTime(timezone=True), server_default=func.now())

	# Relaciones
	mesa = relationship("Mesa", back_populates="pedidos")
	usuario = relationship("Usuario")
	detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")

class DetallePedido(Base):
	__tablename__ = "detalle_pedidos"

	id = Column(Integer, primary_key=True, index=True)
	pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"), nullable=False)
	producto_id = Column(Integer, ForeignKey("productos.id", ondelete="RESTRICT"), nullable=False)
	cantidad = Column(Integer, nullable=False, default=1)
	precio_unitario = Column(Numeric(10, 2), nullable=False)
	subtotal = Column(Numeric(10, 2), nullable=False)
	observaciones = Column(String(150), nullable=True) # ej, "sin cebolla"

	pedido = relationship("Pedido", back_populates="detalles")
	producto = relationship("Producto")
	
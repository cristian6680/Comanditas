from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base 

class Mesa(Base):
	__tablename__ = "mesas"

	id = Column(Integer, primary_key=True, index=True)
	numero = Column(Integer, unique=True, nullable=False, index=True)
	capacidad = Column(Integer, nullable=False, default=4)
	estado = Column(String(20), nullable=False, default="Libre") # 'Libre', 'ocupada', 'pidiendo_cuenta'

	pedidos = relationship("Pedido", back_populates="mesa")
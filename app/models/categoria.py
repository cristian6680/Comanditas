from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Categoria(Base):
    __tablename__="categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    # Relación uno-a-muchos (una categoría tiene muchos productos)
    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")

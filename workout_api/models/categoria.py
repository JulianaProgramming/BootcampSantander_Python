from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class CategoriaModel(Base):
    """Modelo que representa uma categoria de atleta."""
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    atletas = relationship("AtletaModel", back_populates="categoria")  # Relacionamento com atletas
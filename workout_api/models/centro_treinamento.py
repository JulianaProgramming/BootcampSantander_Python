from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class CentroTreinamentoModel(Base):
    """Modelo que representa um centro de treinamento."""
    __tablename__ = "centros_treinamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(200), nullable=False)
    proprietario = Column(String(100), nullable=False)

    atletas = relationship("AtletaModel", back_populates="centro_treinamento")  # Relacionamento com atletas
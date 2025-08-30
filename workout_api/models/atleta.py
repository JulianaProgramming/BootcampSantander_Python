from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class AtletaModel(Base):
    """Modelo que representa um atleta, com relacionamentos para centro de treinamento e categoria."""
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    idade = Column(Integer, nullable=False)
    peso = Column(Integer, nullable=False)
    altura = Column(Integer, nullable=False)
    sexo = Column(String(1), nullable=False)
    centro_treinamento_id = Column(Integer, ForeignKey("centros_treinamento.id"))  # FK para centro de treinamento
    categoria_id = Column(Integer, ForeignKey("categorias.id"))  # FK para categoria

    # Relacionamentos ORM
    centro_treinamento = relationship("CentroTreinamentoModel", back_populates="atletas")
    categoria = relationship("CategoriaModel", back_populates="atletas")
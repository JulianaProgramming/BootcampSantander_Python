
# Rotas para manipulação de centros de treinamento
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.centro_treinamento import CentroTreinamentoModel
from schemas.centro_treinamento import CentroTreinamentoCreate, CentroTreinamentoResponse

router = APIRouter()

# Endpoint para criar um novo centro de treinamento
@router.post("/centros_treinamento", response_model=CentroTreinamentoResponse, status_code=201)
async def create_centro_treinamento(centro: CentroTreinamentoCreate, db: Session = Depends(get_db)):
    db_centro = CentroTreinamentoModel(**centro.dict())
    db.add(db_centro)
    db.commit()
    db.refresh(db_centro)
    return db_centro

# Endpoint para listar todos os centros de treinamento
@router.get("/centros_treinamento", response_model=list[CentroTreinamentoResponse])
async def get_centros_treinamento(db: Session = Depends(get_db)):
    return db.query(CentroTreinamentoModel).all()

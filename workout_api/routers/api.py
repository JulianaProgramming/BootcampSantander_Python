from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate
from typing import Optional

from database.database import get_db
from models.atleta import AtletaModel
from models.centro_treinamento import CentroTreinamentoModel
from models.categoria import CategoriaModel
from schemas.atleta import AtletaCreate, AtletaResponse, AtletaResponseCustom

router = APIRouter()

@router.get("/atletas", response_model=Page[AtletaResponseCustom])
async def get_atletas(
    db: Session = Depends(get_db),
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    query = db.query(AtletaModel)
    
    if nome:
        query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
    
    atletas = query.offset(offset).limit(limit).all()
    
    # Custom response com tratamento para campos nulos
    response_data = []
    for atleta in atletas:
        response_data.append(
            AtletaResponseCustom(
                nome=atleta.nome,
                centro_treinamento=atleta.centro_treinamento.nome if atleta.centro_treinamento else "Não informado",
                categoria=atleta.categoria.nome if atleta.categoria else "Não informado"
            )
        )
    return paginate(response_data)

@router.get("/atletas/{atleta_id}", response_model=AtletaResponse)
async def get_atleta(atleta_id: int, db: Session = Depends(get_db)):
    atleta = db.query(AtletaModel).filter(AtletaModel.id == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    return atleta

@router.post("/atletas", response_model=AtletaResponse, status_code=201)
async def create_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    try:
        db_atleta = AtletaModel(**atleta.dict())
        db.add(db_atleta)
        db.commit()
        db.refresh(db_atleta)
        return db_atleta
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303, 
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )

@router.put("/atletas/{atleta_id}", response_model=AtletaResponse)
async def update_atleta(atleta_id: int, atleta: AtletaCreate, db: Session = Depends(get_db)):
    db_atleta = db.query(AtletaModel).filter(AtletaModel.id == atleta_id).first()
    if not db_atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    
    try:
        for key, value in atleta.dict().items():
            setattr(db_atleta, key, value)
        
        db.commit()
        db.refresh(db_atleta)
        return db_atleta
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303, 
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}"
        )

@router.delete("/atletas/{atleta_id}", status_code=204)
async def delete_atleta(atleta_id: int, db: Session = Depends(get_db)):
    atleta = db.query(AtletaModel).filter(AtletaModel.id == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    
    db.delete(atleta)
    db.commit()
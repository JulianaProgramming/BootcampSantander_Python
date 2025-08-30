
# Rotas para manipulação de categorias
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.categoria import CategoriaModel
from schemas.categoria import CategoriaCreate, CategoriaResponse

router = APIRouter()

# Endpoint para criar uma nova categoria
@router.post("/categorias", response_model=CategoriaResponse, status_code=201)
async def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = CategoriaModel(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Endpoint para listar todas as categorias
@router.get("/categorias", response_model=list[CategoriaResponse])
async def get_categorias(db: Session = Depends(get_db)):
    return db.query(CategoriaModel).all()

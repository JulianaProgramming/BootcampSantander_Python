from fastapi import APIRouter, HTTPException, status, Depends, Query
from src.schemas.fitness_schemas import ProdutoCriar, ProdutoResponse
from src.database.mongo_connection import get_database
from bson import ObjectId
from typing import List, Optional

router = APIRouter(prefix="/produtos", tags=["produtos-fitness"])

@router.get("/", response_model=List[ProdutoResponse])
async def listar_produtos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    categoria: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    preco_min: Optional[float] = Query(None, ge=0),
    preco_max: Optional[float] = Query(None, ge=0),
    marca: Optional[str] = Query(None),
    db=Depends(get_database)
):
    filtro = {}
    
    if categoria:
        filtro["categoria"] = categoria
    if tipo:
        filtro["tipo"] = tipo
    if marca:
        filtro["marca"] = marca
    if preco_min is not None or preco_max is not None:
        filtro_preco = {}
        if preco_min is not None:
            filtro_preco["$gte"] = preco_min
        if preco_max is not None:
            filtro_preco["$lte"] = preco_max
        filtro["preco"] = filtro_preco

    cursor = db.produtos_fitness.find(filtro).skip(skip).limit(limit)
    produtos = await cursor.to_list(length=limit)
    
    produtos_formatados = []
    for produto in produtos:
        produto["id"] = str(produto["_id"])
        produtos_formatados.append(produto)
    
    return produtos_formatados

@router.get("/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(produto_id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(produto_id):
        raise HTTPException(status_code=400, detail="ID do produto inválido")
    
    produto = await db.produtos_fitness.find_one({"_id": ObjectId(produto_id)})
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    produto["id"] = str(produto["_id"])
    return produto

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(produto: ProdutoCriar, db=Depends(get_database)):
    produto_dict = produto.model_dump()
    
    produto_existente = await db.produtos_fitness.find_one({"nome": produto_dict["nome"]})
    if produto_existente:
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um produto com o nome '{produto_dict['nome']}'"
        )
    
    resultado = await db.produtos_fitness.insert_one(produto_dict)
    novo_produto = await db.produtos_fitness.find_one({"_id": resultado.inserted_id})
    
    novo_produto["id"] = str(novo_produto["_id"])
    return novo_produto

@router.put("/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(produto_id: str, produto: ProdutoCriar, db=Depends(get_database)):
    if not ObjectId.is_valid(produto_id):
        raise HTTPException(status_code=400, detail="ID do produto inválido")
    
    produto_dict = produto.model_dump()
    
    produto_existente = await db.produtos_fitness.find_one({"_id": ObjectId(produto_id)})
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    produto_mesmo_nome = await db.produtos_fitness.find_one({
        "nome": produto_dict["nome"],
        "_id": {"$ne": ObjectId(produto_id)}
    })
    if produto_mesmo_nome:
        raise HTTPException(
            status_code=400,
            detail=f"Outro produto com nome '{produto_dict['nome']}' já existe"
        )
    
    await db.produtos_fitness.update_one(
        {"_id": ObjectId(produto_id)},
        {"$set": produto_dict}
    )
    
    produto_atualizado = await db.produtos_fitness.find_one({"_id": ObjectId(produto_id)})
    produto_atualizado["id"] = str(produto_atualizado["_id"])
    return produto_atualizado

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_produto(produto_id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(produto_id):
        raise HTTPException(status_code=400, detail="ID do produto inválido")
    
    resultado = await db.produtos_fitness.delete_one({"_id": ObjectId(produto_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
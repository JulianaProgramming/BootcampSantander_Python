from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

class FitnessProduct(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    nome: str = Field(..., min_length=3, max_length=100)
    preco: float = Field(..., gt=0)
    descricao: str = Field(..., max_length=500)
    categoria: str = Field(..., min_length=2, max_length=50)
    estoque: int = Field(..., ge=0)
    marca: str = Field(..., min_length=2, max_length=50)
    peso: Optional[float] = Field(None, ge=0)
    tipo: str = Field(..., pattern="^(suplemento|equipamento|vestuario|acessorio)$")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Nome deve ter pelo menos 3 caracteres')
        return v.strip()

    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Categoria deve ter pelo menos 2 caracteres')
        return v.strip()

    @field_validator('id', mode='before')
    @classmethod
    def validar_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "nome": "Whey Protein",
                "preco": 89.90,
                "descricao": "Proteína isolada de alta qualidade",
                "categoria": "proteina",
                "estoque": 50,
                "marca": "Growth",
                "peso": 900.0,
                "tipo": "suplemento"
            }
        }
    }
# Schemas Pydantic para validação e serialização de dados de atleta
from pydantic import BaseModel, validator
from typing import Optional

class AtletaBase(BaseModel):
    nome: str
    cpf: str
    idade: int
    peso: int
    altura: int
    sexo: str
    centro_treinamento_id: int
    categoria_id: int

    @validator('cpf')
    def validate_cpf(cls, v):
        if len(v) != 11 or not v.isdigit():
            raise ValueError('CPF deve ter 11 dígitos numéricos')
        return v

    @validator('sexo')
    def validate_sexo(cls, v):
        if v.upper() not in ['M', 'F']:
            raise ValueError('Sexo deve ser M ou F')
        return v.upper()

class AtletaCreate(AtletaBase):
    pass

class AtletaResponse(AtletaBase):
    id: int

    class Config:
        from_attributes = True

class AtletaResponseCustom(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        from_attributes = True
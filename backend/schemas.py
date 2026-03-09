from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str
    slug: str
    estoque_minimo: Optional[int] = 50
    unidade: Optional[str] = "cx"

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    estoque_atual: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class LoteBase(BaseModel):
    codigo: str
    produto_id: int
    quantidade: int
    validade: Optional[str] = None
    observacoes: Optional[str] = None

class LoteCreate(LoteBase):
    pass

class LoteResponse(LoteBase):
    id: int
    data_producao: datetime
    created_at: datetime
    produto: Optional[str] = None
    class Config:
        from_attributes = True

class MovimentacaoBase(BaseModel):
    produto_id: int
    tipo: str
    quantidade: int
    motivo: Optional[str] = None
    lote_id: Optional[int] = None
    origem: Optional[str] = "manual"

class MovimentacaoCreate(MovimentacaoBase):
    pass

class MovimentacaoResponse(MovimentacaoBase):
    id: int
    created_at: datetime
    produto: Optional[str] = None
    class Config:
        from_attributes = True

class AlertaResponse(BaseModel):
    id: int
    produto_id: int
    tipo: str
    mensagem: Optional[str] = None
    resolvido: int
    created_at: datetime
    class Config:
        from_attributes = True

class EstoqueMinimoUpdate(BaseModel):
    estoque_minimo: int

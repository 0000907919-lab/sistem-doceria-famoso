from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Produto, Movimentacao
from schemas import MovimentacaoCreate, MovimentacaoResponse
from services.alerta import verificar_alertas
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[MovimentacaoResponse])
def listar_movimentacoes(
    produto_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Movimentacao)
    if produto_id:
        query = query.filter(Movimentacao.produto_id == produto_id)
    movimentacoes = query.order_by(Movimentacao.created_at.desc()).limit(limit).all()
    for m in movimentacoes:
        if m.produto:
            m.produto = m.produto.nome
    return movimentacoes

@router.post("/", status_code=201)
def registrar_movimentacao(
    payload: MovimentacaoCreate,
    db: Session = Depends(get_db)
):
    if payload.tipo not in ["entrada", "saida"]:
        raise HTTPException(status_code=400, detail="tipo deve ser entrada ou saida")
    produto = db.query(Produto).filter(Produto.id == payload.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if payload.tipo == "saida" and produto.estoque_atual < payload.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")
    delta = payload.quantidade if payload.tipo == "entrada" else -payload.quantidade
    movimentacao = Movimentacao(**payload.model_dump())
    db.add(movimentacao)
    produto.estoque_atual += delta
    db.commit()
    db.refresh(produto)
    verificar_alertas(produto, db)
    return {"ok": True, "estoque_atual": produto.estoque_atual}

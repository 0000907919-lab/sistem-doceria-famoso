from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Lote
from schemas import LoteCreate, LoteResponse
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[LoteResponse])
def listar_lotes(
    produto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lote)
    if produto_id:
        query = query.filter(Lote.produto_id == produto_id)
    lotes = query.order_by(Lote.created_at.desc()).all()
    for l in lotes:
        if l.produto:
            l.produto = l.produto.nome
    return lotes

@router.post("/", response_model=LoteResponse, status_code=201)
def criar_lote(payload: LoteCreate, db: Session = Depends(get_db)):
    lote = Lote(**payload.model_dump())
    db.add(lote)
    db.commit()
    db.refresh(lote)
    return lote

@router.get("/{codigo}", response_model=LoteResponse)
def buscar_lote(codigo: str, db: Session = Depends(get_db)):
    lote = db.query(Lote).filter(Lote.codigo == codigo).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    if lote.produto:
        lote.produto = lote.produto.nome
    return lote

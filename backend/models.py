from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=50)
    unidade = Column(String, default="cx")
    created_at = Column(DateTime, server_default=func.now())
    movimentacoes = relationship("Movimentacao", back_populates="produto")
    lotes = relationship("Lote", back_populates="produto")
    alertas = relationship("Alerta", back_populates="produto")

    @property
    def status(self):
        if self.estoque_atual == 0:
            return "zerado"
        elif self.estoque_atual <= self.estoque_minimo:
            return "critico"
        elif self.estoque_atual <= self.estoque_minimo * 1.5:
            return "baixo"
        return "ok"

class Lote(Base):
    __tablename__ = "lotes"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_producao = Column(DateTime, server_default=func.now())
    validade = Column(String, nullable=True)
    observacoes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    produto = relationship("Produto", back_populates="lotes")

class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=True)
    tipo = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String, nullable=True)
    origem = Column(String, default="manual")
    created_at = Column(DateTime, server_default=func.now())
    produto = relationship("Produto", back_populates="movimentacoes")

class Alerta(Base):
    __tablename__ = "alertas"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(String, nullable=False)
    mensagem = Column(Text, nullable=True)
    resolvido = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    produto = relationship("Produto", back_populates="alertas")

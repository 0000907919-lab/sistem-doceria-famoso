import os
import aiosmtplib
from email.message import EmailMessage
from sqlalchemy.orm import Session
from models import Alerta
from dotenv import load_dotenv

load_dotenv()

async def enviar_email(assunto: str, corpo: str):
    if not os.getenv("SMTP_USER"):
        return
    msg = EmailMessage()
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = os.getenv("EMAIL_ALERTA")
    msg["Subject"] = assunto
    msg.set_content(corpo, subtype="html")
    await aiosmtplib.send(
        msg,
        hostname=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        port=int(os.getenv("SMTP_PORT", 587)),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True
    )

def verificar_alertas(produto, db: Session):
    if produto.status in ["critico", "zerado"]:
        ja_existe = db.query(Alerta).filter(
            Alerta.produto_id == produto.id,
            Alerta.tipo == "estoque_minimo",
            Alerta.resolvido == 0
        ).first()
        if not ja_existe:
            alerta = Alerta(
                produto_id=produto.id,
                tipo="estoque_minimo",
                mensagem=f"{produto.nome} com estoque {produto.status}: {produto.estoque_atual} {produto.unidade}"
            )
            db.add(alerta)
            db.commit()
    else:
        db.query(Alerta).filter(
            Alerta.produto_id == produto.id,
            Alerta.tipo == "estoque_minimo",
            Alerta.resolvido == 0
        ).update({"resolvido": 1})
        db.commit()

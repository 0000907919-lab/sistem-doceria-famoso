from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import engine, SessionLocal
from models import Base
from routes import produtos, movimentacoes, lotes
from services.mqtt import iniciar_mqtt, configurar_db
import os

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doceria Famoso API",
    description="Sistema Inteligente de Estoque",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produtos.router, prefix="/api/produtos", tags=["Produtos"])
app.include_router(movimentacoes.router, prefix="/api/movimentacoes", tags=["Movimentações"])
app.include_router(lotes.router, prefix="/api/lotes", tags=["Lotes"])

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    configurar_db(SessionLocal)
    try:
        iniciar_mqtt()
    except Exception as e:
        print(f"⚠️ MQTT indisponível: {e}")

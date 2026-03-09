import os, json, threading
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASS = os.getenv("MQTT_PASS", "")
_db_session_factory = None

def configurar_db(session_factory):
    global _db_session_factory
    _db_session_factory = session_factory

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("📡 MQTT conectado!")
        client.subscribe("doceria/contador/#")
        client.subscribe("doceria/lote/#")

def on_message(client, userdata, msg):
    try:
        topico = msg.topic
        payload = json.loads(msg.payload.decode())
        if _db_session_factory is None:
            return
        db = _db_session_factory()
        try:
            from models import Produto, Movimentacao, Lote
            from services.alerta import verificar_alertas
            if topico.startswith("doceria/contador/"):
                slug = topico.split("/")[2]
                produto = db.query(Produto).filter(Produto.slug == slug).first()
                if not produto:
                    return
                quantidade = payload.get("quantidade", 1)
                produto.estoque_atual += quantidade
                mov = Movimentacao(
                    produto_id=produto.id,
                    tipo="entrada",
                    quantidade=quantidade,
                    motivo="Sensor automático",
                    origem="mqtt"
                )
                db.add(mov)
                db.commit()
                db.refresh(produto)
                verificar_alertas(produto, db)
            elif topico.startswith("doceria/lote/"):
                codigo = topico.split("/")[2]
                if not db.query(Lote).filter(Lote.codigo == codigo).first():
                    lote = Lote(
                        codigo=codigo,
                        produto_id=payload.get("produto_id"),
                        quantidade=payload.get("quantidade", 1),
                        validade=payload.get("validade")
                    )
                    db.add(lote)
                    db.commit()
        finally:
            db.close()
    except Exception as e:
        print(f"❌ Erro MQTT: {e}")

def iniciar_mqtt():
    client = mqtt.Client()
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message
    def loop():
        while True:
            try:
                client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
                client.loop_forever()
            except Exception as e:
                import time
                print(f"❌ Erro MQTT: {e}")
                time.sleep(5)
    threading.Thread(target=loop, daemon=True).start()

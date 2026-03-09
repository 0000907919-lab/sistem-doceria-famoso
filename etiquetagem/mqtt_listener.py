import os, json, time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from gerar_qrcode import gerar_qrcode

load_dotenv()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("📡 MQTT conectado!")
        client.subscribe("doceria/lote/#")
        print("👂 Escutando: doceria/lote/#")
    else:
        print(f"❌ Falha MQTT. Código: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        codigo  = msg.topic.split("/")[-1]
        print(f"\n📨 Lote recebido: {codigo}")
        gerar_qrcode(
            codigo=codigo,
            produto=payload.get("produto", "Desconhecido"),
            quantidade=payload.get("quantidade", 1),
            validade=payload.get("validade", "N/A")
        )
    except Exception as e:
        print(f"❌ Erro: {e}")

def iniciar():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(
                os.getenv("MQTT_BROKER", "localhost"),
                int(os.getenv("MQTT_PORT", 1883))
            )
            client.loop_forever()
        except Exception as e:
            print(f"❌ {e} — reconectando em 5s...")
            time.sleep(5)

if __name__ == "__main__":
    iniciar()

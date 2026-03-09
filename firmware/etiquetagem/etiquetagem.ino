#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "config.h"

WiFiClient espClient;
PubSubClient mqtt(espClient);
int sequencia = 1;
bool botaoAnterior = HIGH;
unsigned long ultimoPressionamento = 0;

void conectarWiFi() {
  Serial.print("📶 Conectando WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado!");
  configTime(-3 * 3600, 0, "pool.ntp.org");
}

void conectarMQTT() {
  while (!mqtt.connected()) {
    Serial.print("📡 Conectando MQTT...");
    if (mqtt.connect(MQTT_CLIENT)) {
      Serial.println(" conectado!");
      digitalWrite(LED_OK_PIN, HIGH);
      delay(200);
      digitalWrite(LED_OK_PIN, LOW);
    } else {
      digitalWrite(LED_ERR_PIN, HIGH);
      delay(3000);
      digitalWrite(LED_ERR_PIN, LOW);
    }
  }
}

void publicarLote() {
  char codigo[32];
  sprintf(codigo, "LOT-%03d", sequencia++);
  String topico = String(MQTT_TOPIC_LOTE) + "/" + codigo;
  StaticJsonDocument<128> doc;
  doc["produto_id"] = PRODUTO_ID;
  doc["quantidade"] = 1;
  char payload[128];
  serializeJson(doc, payload);
  if (mqtt.publish(topico.c_str(), payload)) {
    Serial.printf("✅ Lote publicado: %s\n", codigo);
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_OK_PIN, HIGH);
      delay(100);
      digitalWrite(LED_OK_PIN, LOW);
      delay(100);
    }
  } else {
    Serial.println("❌ Erro ao publicar lote");
    digitalWrite(LED_ERR_PIN, HIGH);
    delay(500);
    digitalWrite(LED_ERR_PIN, LOW);
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(BOTAO_PIN, INPUT_PULLUP);
  pinMode(LED_OK_PIN, OUTPUT);
  pinMode(LED_ERR_PIN, OUTPUT);
  conectarWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (!mqtt.connected()) conectarMQTT();
  mqtt.loop();
  bool botaoAtual = digitalRead(BOTAO_PIN);
  if (botaoAnterior == HIGH && botaoAtual == LOW) {
    if (millis() - ultimoPressionamento >= 500) {
      ultimoPressionamento = millis();
      publicarLote();
    }
  }
  botaoAnterior = botaoAtual;
}

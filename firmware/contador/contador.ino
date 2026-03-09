#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "config.h"

WiFiClient espClient;
PubSubClient mqtt(espClient);
bool sensorAnterior = HIGH;
unsigned long ultimaContagem = 0;

void conectarWiFi() {
  Serial.print("📶 Conectando WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado!");
}

void conectarMQTT() {
  while (!mqtt.connected()) {
    Serial.print("📡 Conectando MQTT...");
    if (mqtt.connect(MQTT_CLIENT)) {
      Serial.println(" conectado!");
      digitalWrite(LED_PIN, HIGH);
    } else {
      Serial.println(" falhou. Tentando em 3s...");
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  conectarWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (!mqtt.connected()) conectarMQTT();
  mqtt.loop();

  bool sensorAtual = digitalRead(SENSOR_PIN);
  unsigned long agora = millis();

  if (sensorAnterior == HIGH && sensorAtual == LOW) {
    if (agora - ultimaContagem >= DEBOUNCE_MS) {
      ultimaContagem = agora;
      StaticJsonDocument<64> doc;
      doc["quantidade"] = BATCH_SIZE;
      doc["dispositivo"] = MQTT_CLIENT;
      char payload[64];
      serializeJson(doc, payload);
      mqtt.publish(MQTT_TOPIC, payload);
      Serial.printf("📦 Caixa detectada! Publicado: %s\n", payload);
      digitalWrite(LED_PIN, LOW);
      delay(80);
      digitalWrite(LED_PIN, HIGH);
    }
  }
  sensorAnterior = sensorAtual;
}

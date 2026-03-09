# 🔢 Firmware — Doceria Famoso

Firmware para os módulos físicos baseados em **ESP32**.

## Módulos

| Pasta | Função | Hardware |
|-------|--------|----------|
| `contador/` | Conta caixas na esteira via sensor IR | ESP32 + Sensor IR FC-51 |
| `etiquetagem/` | Gera e envia dados do lote via MQTT | ESP32 + Botão |

## Dependências (Arduino IDE)

Instale via **Gerenciador de Bibliotecas**:
- `PubSubClient` — MQTT
- `ArduinoJson` — JSON
- `WiFi` — já incluso no ESP32

## Como usar

1. Abra o Arduino IDE
2. Instale o suporte ao ESP32 em **Preferências → URLs adicionais**:
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
3. Edite o `config.h` com suas credenciais de WiFi e MQTT
4. Faça o upload para o ESP32

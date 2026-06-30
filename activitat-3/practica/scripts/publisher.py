#!/usr/bin/env python3
"""
Simulador de sensors de temperatura i humitat.
Publica a MQTT cada 3 segons com a números simples (sense JSON).
"""

import paho.mqtt.client as mqtt
import time
import random

BROKER = "localhost"
PORT = 1883
TOPIC_TEMP = "NomAlumne/aula_1/temperatura"
TOPIC_HUM = "NomAlumne/aula_1/humitat"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connectat al broker {BROKER}:{PORT}")
    else:
        print(f"❌ Error de connexió. Codi: {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

print("🌡️💧 Simulador de sensors en marxa...")
print("Prem Ctrl+C per aturar")

try:
    while True:
        temperatura = round(random.uniform(18.0, 35.0), 1)
        humitat = round(random.uniform(40.0, 90.0), 1)

        client.publish(TOPIC_TEMP, str(temperatura))
        client.publish(TOPIC_HUM, str(humitat))

        print(f"📤 {TOPIC_TEMP} → {temperatura}")
        print(f"📤 {TOPIC_HUM}      → {humitat}%")

        time.sleep(3)

except KeyboardInterrupt:
    print("\n⏹️  Aturat per l'usuari")
finally:
    client.loop_stop()
    client.disconnect()
    print("🔌 Desconnectat del broker")

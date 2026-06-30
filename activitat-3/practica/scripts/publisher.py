import paho.mqtt.client as mqtt
import random
import time
BROKER = "localhost"
PORT = 1883
TOPIC = "NomAlumne/aula_1/temperatura"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    valor = round(random.uniform(20.0, 30.0), 1)
    client.publish(TOPIC, str(valor))
    print(f"Publicat {TOPIC} → {valor}")
    time.sleep(3)

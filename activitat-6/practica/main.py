# ============================================================
# ESP32 + DS18B20 + MQTT — Enviar temperatura a broker
# Llibreries oficials MicroPython (Espressif)
# ============================================================

import machine
import onewire
import ds18x20
import network
import time
from umqtt.simple import MQTTClient

# ============ CONFIGURACIÓ ============

WIFI_SSID = "el_teu_wifi"
WIFI_PASSWORD = "la_teva_contrasenya"

MQTT_BROKER = "192.168.0.57"  # IP de la VM
MQTT_PORT = 1883
MQTT_TOPIC = "alumne/aula/temperatura"
MQTT_CLIENT_ID = "esp32_ds18b20"

PIN_SENSOR = 4  # GPIO4 (D2 a la majoria de plaques)
INTERVAL = 5    # Segons entre lectures

# ============ FUNCIONS ============

def connectar_wifi():
    """Connecta l'ESP32 a la xarxa WiFi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("🔄 Connectant a WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print(f"✅ WiFi connectat! IP: {wlan.ifconfig()[0]}")
        return wlan
    else:
        print("❌ No s'ha pogut connectar WiFi")
        return None


def inicialitzar_sensor(pin):
    """Inicialitza el sensor DS18B20 al pin indicat."""
    ow = onewire.OneWire(machine.Pin(pin))
    sensor = ds18x20.DS18X20(ow)
    roms = sensor.scan()
    if len(roms) == 0:
        print("❌ No s'ha trobat cap sensor DS18B20!")
        print("  Comprova les connexions i el pull-up de 4.7kΩ")
        return None, None
    print(f"✅ Sensor trobat! Adreça: {roms[0].hex()}")
    return sensor, roms[0]


def connectar_mqtt():
    """Connecta al broker MQTT."""
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print(f"✅ Connectat a MQTT broker {MQTT_BROKER}:{MQTT_PORT}")
        return client
    except Exception as e:
        print(f"❌ Error connectant MQTT: {e}")
        return None


def llegir_temperatura(sensor, rom):
    """Llegeix la temperatura del DS18B20."""
    sensor.convert_temp()        # Inicia la conversió
    time.sleep_ms(750)           # Espera 750ms (temps màxim de conversió)
    temp = sensor.read_temp(rom) # Llegeix el resultat
    return temp


# ============ PROGRAMA PRINCIPAL ============

def main():
    print("=" * 45)
    print("🌡️  ESP32 + DS18B20 → MQTT")
    print("=" * 45)

    # 1. Connectar WiFi
    wlan = connectar_wifi()
    if not wlan:
        return

    # 2. Inicialitzar sensor
    sensor, rom = inicialitzar_sensor(PIN_SENSOR)
    if not sensor:
        return

    # 3. Connectar MQTT
    client = connectar_mqtt()
    if not client:
        return

    # 4. Bucle principal
    print(f"\n📤 Enviant temperatura cada {INTERVAL} segons al topic '{MQTT_TOPIC}'...")
    print("   Prem Ctrl+C per aturar\n")

    while True:
        try:
            temp = llegir_temperatura(sensor, rom)
            missatge = f"{temp:.2f}"
            client.publish(MQTT_TOPIC, missatge)
            print(f"🌡️  {temp:.2f}°C → {MQTT_TOPIC}")

            time.sleep(INTERVAL)

        except KeyboardInterrupt:
            print("\n⏹️  Programa aturat per l'usuari")
            break
        except OSError as e:
            print(f"⚠️  Error de connexió: {e}")
            print("   Reconnectant...")
            time.sleep(2)
            client = connectar_mqtt()
        except Exception as e:
            print(f"⚠️  Error inesperat: {e}")
            time.sleep(2)

    # 5. Neteja
    client.disconnect()
    wlan.disconnect()
    print("👋 Fet!")


# ============ ARRENCADA ============

if __name__ == "__main__":
    main()

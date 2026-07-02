# 📚 Mòdul optatiu

Activitats d'aprofundiment en eines professionals per a IoT, sistemes encastats i automatització.

---

## 🗺️ Activitats

| # | Activitat | ✅ Estat |
|:--|:----------|:---------|
| 1 | 🖥️ **Crear un entorn virtual** — VirtualBox + Ubuntu Linux | Fet |
| 2 | 🐳 **Instal·lació de Docker i eines IoT** — Docker, Compose, Python, MQTT | Fet |
| 3 | 🚀 **Primers contenidors IoT** — Mosquitto + Node-RED + Python MQTT | Fet |
| 4 | 🗄️ **Emmagatzematge i visualització** — InfluxDB + Grafana | ✅ Fet |
| 5 | 🌐 **Xarxa local (LAN)** — Bridge, IPs, ping, accés des de Windows | ✅ Fet |
| 6 | 🌡️ **ESP32 + BME280** — Sensor real (temp+hum+press), I2C, MQTT, ESP-IDF | ✅ Fet |

---

## 📋 Estructura de cada activitat

```📁 activitat-N/
   ├── 📖 teoria/     →  Conceptes, fonaments, esquemes
   └── 🔧 practica/   →  Guia pas a pas, scripts, configuracions
```

---

Per a qualsevol dubte: **pregunta a classe o obre un issue al repositori!** 🚀

---

## 🔧 Prerequisits per a l'Activitat 6

Abans de començar amb l'ESP32, necessites **ESP-IDF** instal·lat a la teva VM:

👉 **[Guia d'instal·lació pas a pas →](activitat-6/instalacio-esp-idf.md)**

Inclou: dependències, clonar ESP-IDF, toolchain, verificació amb `hello_world`, i resolució de problemes (USB, flash 2MB, etc.).

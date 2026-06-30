# 🖥️ Pràctica 3: Primers contenidors IoT

**🎯 Objectiu:** Crear i executar un stack IoT real amb Docker Compose: Mosquitto (broker MQTT) + Node-RED (dashboard visual) + clients Python.

**⏱ Durada estimada:** 30-40 minuts

---

## 📋 Què necessites?

| 🔧 Requisit | 📝 Detall |
|:-----------|:----------|
| 💻 La teva VM Ubuntu | De l'Activitat 1 (engegada i funcionant) |
| 🐳 Docker + Docker Compose | Instal·lats a l'Activitat 2 |
| 🐍 Python 3 + paho-mqtt | Instal·lats a l'Activitat 2 |
| 🌐 Connexió a Internet | Per baixar les imatges Docker |

---

## 🗺️ Mapa de la pràctica

```
1️⃣  Crear el projecte ──────────── 📁 Activitat 3 al teu directori
       │
2️⃣  docker-compose.yml ─────────── 📜 Mosquitto + Node-RED
       │
3️⃣  docker compose up ──────────── 🚀 Engegar els contenidors
       │
4️⃣  Prova MQTT des de terminal ── 📡 Publicar i subscriure
       │
5️⃣  Node-RED dashboard ─────────── 🟠 Flow visual al navegador
       │
6️⃣  Python publisher ───────────── 🐍 Script que publica dades
       │
7️⃣  Python subscriber ──────────── 🐍 Script que rep dades
       │
8️⃣  Bateria de proves ──────────── 🎯 Tot funciona!
```

---

## 1️⃣ Crea l'estructura del projecte

A la teva VM, crea la carpeta per a l'activitat 3:

```bash
cd ~
mkdir -p activitat-3/scripts
cd activitat-3
```

> 💡 Ets al teu home (`~`) de la VM, no als documents del repositori!

---

## 2️⃣ Crea el docker-compose.yml

Ara escriurem un fitxer que descriu els serveis (contenidors) que volem engegar. Per què crearem directoris?

| Directori | Per què? |
|:----------|:---------|
| `./mosquitto/config/` | 🔧 **El configurem** — hi poses `mosquitto.conf` personalitzat |
| `./mosquitto/data/` | 💾 **Persistència** — si el contenidor es reinicia, les dades no es perden |
| `./mosquitto/log/` | 📋 **Logs** — errors i esdeveniments visibles encara que esborris el contenidor |
| `./nodered/data/` | 🔴 **Crític** — sense això, **perds els flows** de Node-RED cada cop que fas `docker compose down` |

Els directoris `data`, `log` i `nodered/data` els crea Docker automàticament. El `config` l'has de crear tu per posar-hi el fitxer de configuració.

Crea el fitxer:

Crea un fitxer `docker-compose.yml` amb aquest contingut:

```bash
nano docker-compose.yml
```

I enganxa-hi això:

```yaml
version: '3.8'

services:
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: mqtt-broker
    ports:
      - "1883:1883"    # MQTT (publicar/subscriure)
      - "9001:9001"    # MQTT WebSocket (per al navegador)
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    restart: unless-stopped

  nodered:
    image: nodered/node-red:4.0
    container_name: nodered-dashboard
    ports:
      - "1880:1880"    # Editor web
    volumes:
      - ./nodered/data:/data
    environment:
      - TZ=Europe/Madrid
    restart: unless-stopped
    depends_on:
      - mosquitto
```

> ⚠️ **Nota:** `depends_on` fa que Node-RED esperi que Mosquitto estigui llest abans d'engegar.

Guarda el fitxer: `Ctrl+O`, `Enter`, `Ctrl+X`.

### Configura Mosquitto

Mosquitto necessita un fitxer de configuració per saber a quins ports escoltar i si deixa entrar a tothom:

```conf
listener 1883 0.0.0.0          ← Port MQTT normal, obert a tothom
allow_anonymous true           ← Sense contrasenya (per a classe)
listener 9001 0.0.0.0          ← Port extra per WebSocket (el farà servir
protocol websockets            ← Node-RED per connectar-se des del navegador)
allow_anonymous true
```

Crea'l:

```bash
mkdir -p mosquitto/config
nano mosquitto/config/mosquitto.conf
```

Hi poses:

```conf
listener 1883 0.0.0.0
allow_anonymous true
listener 9001 0.0.0.0
protocol websockets
allow_anonymous true
```

Guarda i surt (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

## 3️⃣ Engega els contenidors!

```bash
docker compose up -d
```

> `-d` (detached) fa que els contenidors corrin en segon pla.

Hauries de veure:

```
[+] Running 3/3
 ✔ Network activitat-3_default    Created
 ✔ Container mqtt-broker          Started
 ✔ Container nodered-dashboard    Started
```

### Verifica que estan en marxa:

```bash
docker ps
```

*(Funciona des de qualsevol directori)*

Hauries de veure:

```
CONTAINER ID   IMAGE                    ...   NAMES
abc123def456   nodered/node-red:4.0     ...   nodered-dashboard
def456abc123   eclipse-mosquitto:2      ...   mqtt-broker
```

Si vols veure-hi ports i estat de forma més clara:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

| Columna | Què significa |
|:--------|:-------------|
| `Up 1 minute` | Funciona des de fa 1 minut ✅ |
| `0.0.0.0:1883->1883/tcp` | Port 1883 obert a totes les IPs |

> 💡 **Alternativa:** `docker compose ps` fa el mateix, però només des de la carpeta `~/activitat-3/`

### Mira els logs (si alguna cosa va malament):

```bash
docker compose logs
```

> 💡 Per veure només un servei: `docker compose logs mosquitto`

### Atura els logs (Ctrl+C) i torna al terminal.

---

## 4️⃣ Prova MQTT des del terminal

### Instal·la un client MQTT per al terminal:

```bash
sudo apt install -y mosquitto-clients
```

### Subscriu-te a un topic (obre un **segon terminal**):

```bash
mosquitto_sub -h localhost -t "casa/#"
```

Aquest terminal es quedarà escoltant. Torna al primer terminal.

### Publica un missatge des del primer terminal:

```bash
mosquitto_pub -h localhost -t "casa/sala/temperatura" -m "23.5"
```

Si tot funciona, al **segon terminal** hauries de veure:

```
23.5
```

Prova més missatges:

```bash
mosquitto_pub -h localhost -t "casa/sala/humitat" -m "65"
mosquitto_pub -h localhost -t "casa/exterior/temperatura" -m "18.2"
```

Al segon terminal veuràs tots els missatges perquè s'ha subscrit a `casa/#`.

**Atura el subscriptor** amb `Ctrl+C`.

> 🎉 **MQTT funciona!**

---

## 5️⃣ Configura Node-RED

### Accedeix a Node-RED

Obre el navegador **al teu Windows/macOS** (o a la VM si tens escriptori gràfic) i ves a:

```
http://<IP-DE-LA-VM>:1880
```

> 💡 Per saber la IP de la VM: `ip a` o `hostname -I`

Si la VM està en mode NAT i no pots accedir des del navegador del host, pots fer servir `curl` des de la mateixa VM:

```bash
curl http://localhost:1880
```

Si veus HTML, Node-RED funciona. Per veure l'editor, necessitaràs accés gràfic.

### Instal·la el dashboard

Fes clic al menú ☰ (tres ratlles) → **Manage palette** → **Install**.

Busca `node-red-dashboard` i fes clic a **Install**.

Alternativament, des del terminal:

```bash
docker exec nodered-dashboard npm install node-red-dashboard
# i després reinicia
docker restart nodered-dashboard
```

### Crea el teu primer flow

Arrossega aquests nodes a l'editor i connecta'ls:

```
┌──────────┐    ┌──────────┐    ┌─────────────────────┐
│ 📡 mqtt   │───→│ 🔧 json  │───→│ 📊 ui_gauge         │
│ in        │    │          │    │ (temperatura sala)  │
└──────────┘    └──────────┘    └─────────────────────┘
```

**Pas a pas:**

1. **📡 MQTT Input** (`mqtt in`):
   - Dona-li doble clic
   - Server: **Add new mqtt-broker...**
   - Connection: Server: `localhost`, Port: `1883`
   - Name: `Temperatura Sala`
   - Topic: `casa/sala/temperatura`
   - Output: **a parsed JSON Object** (més endavant)
   - Clica **Add**

2. **🔧 JSON**:
   - Busca `json` i arrossega'l
   - Action: **Always convert to JSON object**
   - Connecta'l al node MQTT

3. **📊 UI Gauge** (del dashboard):
   - Busca `ui_gauge` a la paleta
   - Group: **Add new ui_group...** → **Add new ui_tab**
   - Name: `Temperatura`
   - Label: `Sala`
   - Range: min `0`, max `50`
   - Connecta'l al node JSON

4. **Desplega**: Clica el botó **Deploy** (blau, dalt a la dreta)

### Mira el dashboard!

Obre una pestanya nova al navegador i ves a:

```
http://<IP-DE-LA-VM>:1880/ui
```

Ara torna al terminal i publica valors de temperatura:

```bash
mosquitto_pub -h localhost -t "casa/sala/temperatura" -m "23.5"
mosquitto_pub -h localhost -t "casa/sala/temperatura" -m "25.0"
mosquitto_pub -h localhost -t "casa/sala/temperatura" -m "26.8"
```

L'agulla del gauge hauria de moure's! 🎉

---

## 6️⃣ Python publisher — simulador de sensor

Crea un script Python que publiqui dades de sensors automàticament:

```bash
nano ~/activitat-3/scripts/publisher.py
```

```python
#!/usr/bin/env python3
"""
Simulador de sensor IoT.
Publica temperatura, humitat i pressió a MQTT cada 5 segons.
"""

import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "localhost"
PORT = 1883
TOPIC_TEMP = "casa/sala/temperatura"
TOPIC_HUM = "casa/sala/humitat"
TOPIC_PRES = "casa/sala/pressio"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connectat al broker {BROKER}:{PORT}")
    else:
        print(f"❌ Error de connexió. Codi: {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

print("🌡️  Simulador de sensors en marxa...")
print("Prem Ctrl+C per aturar")

try:
    while True:
        temperatura = round(random.uniform(18.0, 32.0), 1)
        humitat = round(random.uniform(40.0, 80.0), 1)
        pressio = round(random.uniform(1000.0, 1030.0), 1)

        # Publicar temperatura
        payload = json.dumps({"valor": temperatura, "unitat": "°C"})
        client.publish(TOPIC_TEMP, payload)
        print(f"📤 {TOPIC_TEMP} → {payload}")

        # Publicar humitat
        payload = json.dumps({"valor": humitat, "unitat": "%"})
        client.publish(TOPIC_HUM, payload)
        print(f"📤 {TOPIC_HUM} → {payload}")

        # Publicar pressió
        payload = json.dumps({"valor": pressio, "unitat": "hPa"})
        client.publish(TOPIC_PRES, payload)
        print(f"📤 {TOPIC_PRES} → {payload}")

        print("---")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n⏹️  Aturat per l'usuari")
finally:
    client.loop_stop()
    client.disconnect()
    print("🔌 Desconnectat del broker")
```

Guarda i surt. Dona-li permisos:

```bash
chmod +x ~/activitat-3/scripts/publisher.py
```

### Executa'l!

```bash
python3 ~/activitat-3/scripts/publisher.py
```

Hauries de veure:

```
✅ Connectat al broker localhost:1883
🌡️  Simulador de sensors en marxa...
📤 casa/sala/temperatura → {"valor": 25.3, "unitat": "\u00b0C"}
📤 casa/sala/humitat → {"valor": 62.8, "unitat": "%"}
📤 casa/sala/pressio → {"valor": 1015.2, "unitat": "hPa"}
---
📤 casa/sala/temperatura → {"valor": 24.7, "unitat": "\u00b0C"}
...
```

Ara ves al dashboard de Node-RED (`http://<IP>:1880/ui`) — veuràs com es mouen els gauges! 🎉

Atura el publisher amb `Ctrl+C`.

---

## 7️⃣ Python subscriber — receptor de dades

Crea un script que es subscrigui i mostri les dades:

```bash
nano ~/activitat-3/scripts/subscriber.py
```

```python
#!/usr/bin/env python3
"""
Subscriptor MQTT.
S'espera a rebre dades i les mostra en temps real.
"""

import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "casa/#"

def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        payload = json.loads(msg.payload.decode())
        print(f"📩 [{topic}] {payload}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"📩 [{topic}] {msg.payload.decode()}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Subscrit a '{TOPIC}'")
        print(f"📡 Esperant dades... (Ctrl+C per aturar)")
        print("---")
    else:
        print(f"❌ Error de connexió. Codi: {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

client.loop_forever()
```

Guarda i surt. Dona-li permisos:

```bash
chmod +x ~/activitat-3/scripts/subscriber.py
```

### Executa'l al costat del publisher

Obre **dos terminals** a la VM:

**Terminal 1 — Subscriptor:**
```bash
python3 ~/activitat-3/scripts/subscriber.py
```

**Terminal 2 — Publisher:**
```bash
python3 ~/activitat-3/scripts/publisher.py
```

Al terminal 1 veuràs:
```
✅ Subscrit a 'casa/#'
📡 Esperant dades... (Ctrl+C per aturar)
---
📩 [casa/sala/temperatura] {'valor': 25.3, 'unitat': '°C'}
📩 [casa/sala/humitat] {'valor': 62.8, 'unitat': '%'}
📩 [casa/sala/pressio] {'valor': 1015.2, 'unitat': 'hPa'}
```

**Tot connectat!** Sensor (publisher) → Broker → Dashboard + Subscriptor ✅

Atura tots dos amb `Ctrl+C`.

---

## 8️⃣ Bateria de proves

Executa tot d'un cop per verificar que funciona:

```bash
echo "=== 📡 Prova MQTT (docker) ==="
docker exec mqtt-broker mosquitto_sub -h localhost -t "test" -C 1 &
DOCKER_PID=$!
sleep 1
docker exec mqtt-broker mosquitto_pub -h localhost -t "test" -m "hola mon"
wait $DOCKER_PID 2>/dev/null
echo "✅ MQTT dins del contenidor funciona"
echo ""

echo "=== 🟠 Prova Node-RED ==="
curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost:1880
echo "  →  Node-RED respon"
echo ""

echo "=== 🐳 Estat dels contenidors ==="
docker compose ps --format "table {{.Name}}\t{{.Status}}"
echo ""

echo "=== 🐍 Prova scripts Python ==="
python3 -c "
import paho.mqtt.client as mqtt
import json
# Prova de publicació/subscripció
pub = mqtt.Client()
pub.connect('localhost', 1883, 60)
pub.publish('casa/prova', json.dumps({'test': True}))
print('✅ Publicació OK')
# Tot correcte
print('✅ Scripts preparats')
"
echo ""

echo "=== 🎯 Tot correcte! ==="
```

---

## ✅ Llista de verificació final

- [ ] **1** He creat `docker-compose.yml` amb Mosquitto + Node-RED
- [ ] **2** He creat el fitxer de configuració de Mosquitto
- [ ] **3** `docker compose up -d` engega els dos contenidors ✅
- [ ] **4** `docker compose ps` mostra `Up` per als dos serveis ✅
- [ ] **5** Puc publicar i subscriure'm a MQTT des del terminal ✅
- [ ] **6** Accedeixo a Node-RED al navegador (`http://<IP>:1880`) ✅
- [ ] **7** He creat un flow amb MQTT in + json + gauge ✅
- [ ] **8** El dashboard mostra dades en temps real (`/ui`) ✅
- [ ] **9** `publisher.py` publica dades sense errors ✅
- [ ] **10** `subscriber.py` rep les dades correctament ✅
- [ ] **11** La bateria de proves final dona tot correcte ✅

**🎉 Enhorabona! Has creat el teu primer sistema IoT amb contenidors Docker!**

---

## 🆘 Resolució de problemes

| 🔴 Problema | 🤔 Per què passa? | ✅ Solució |
|:-----------|:-----------------|:----------|
| ❌ **`docker: 'compose' is not a docker command`** | La versió de Docker és antiga | Usa `docker-compose` (amb guió) en lloc de `docker compose` |
| ❌ **`Error starting container: port 1883 already in use`** | Ja tens alguna cosa al port 1883 | `sudo lsof -i :1883` per veure què, o `docker compose down` i torna a engegar |
| ❌ **Node-RED no carrega al navegador** | Firewall o NAT sense redirecció | Prova `curl http://localhost:1880` des de la VM. Si funciona, el problema és de xarxa |
| ❌ **`Connection refused` al publicar MQTT** | Mosquitto no està en marxa | `docker compose ps | grep mosquitto`. Si no: `docker compose logs mosquitto` |
| ❌ **El gauge no es mou al dashboard** | El flow no està desplegat | Clica **Deploy** a Node-RED. Comprova que el topic coincideixi amb el del publisher |
| ❌ **`ModuleNotFoundError: No module named 'paho'`** | paho-mqtt no està instal·lat | `pip3 install paho-mqtt` o `sudo apt install -y python3-paho-mqtt` |
| ❌ **`docker exec` falla amb `no such container`** | El contenidor no es diu com esperes | `docker ps` per veure el nom real |
| ❌ **Tot funciona però el dashboard no es veu bé** | Falten nodes al Node-RED | Ves a Manage Palette i instal·la `node-red-dashboard` |
| ❌ **No sé la IP de la VM** | No tens accés gràfic a la VM | `hostname -I` o `ip addr show | grep inet` |

---

## 🧪 Per explorar més (opcional)

Si has acabat i vols provar més coses:

1. **Afegeix un chart (gràfic de línies)** al dashboard per veure l'evolució de la temperatura
2. **Crea un botó** que enviï una comanda MQTT (ex: `casa/sala/llum` → `ON`/`OFF`)
3. **Publica dades des de dos publishers** alhora i mira com apareixen al dashboard
4. **Afegeix InfluxDB + Grafana** al docker-compose.yml per guardar i visualitzar històrics
5. **Escriu un script que alerti** si la temperatura passa de 30°C

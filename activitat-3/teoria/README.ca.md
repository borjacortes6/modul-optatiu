# 📚 Teoria: L'ecosistema IoT en contenidors

## Abans de començar...

A les activitats anteriors vas instal·lar Docker i les eines necessàries. Ara toca **construir un sistema IoT complet** amb 4 contenidors que treballen plegats per rebre, processar, emmagatzemar i visualitzar dades de sensors i PLCs reals.

```💻 La teva màquina virtual (Ubuntu Server)
   │
   ├── Activitat 1: 🐧 Ubuntu nu
   ├── Activitat 2: 🐳 Docker + eines instal·lats
   │
   └── Activitat 3: 🚀 Ecosistema IoT complet!
         · 📡 Mosquitto   → Broker MQTT (missatgeria)
         · 🔧 Node-RED    → Processament visual
         · 🗄️ InfluxDB   → Base de dades temporal
         · 📊 Grafana     → Dashboards i gràfics
```

> ✅ **Objectiu:** Entendre com funcionen els 4 contenidors clau de l'ecosistema IoT i com es comuniquen entre ells i amb dispositius reals (sensors, PLCs amb MODBUS).

---

## 🌐 Els 4 contenidors de l'ecosistema IoT

```📦 Dades reals              🐳 DINS DOCKER
                             
ESP32 / Sensor / PLC                                    
    │                         
    │ ── MQTT ─────────────▶  ┌─────────────────────────┐     
    │                         │  📡 Mosquitto            │     
    │                         │  (MQTT Broker)           │     
    │                         └────────┬────────────────┘     
    │                                  │                      
    │                         ┌────────▼────────────────┐     
    │                         │  🔧 Node-RED             │     
    │                         │  (Processar dades)      │     
    │                         └────────┬────────────────┘     
    │                                  │                      
    │                         ┌────────▼────────────────┐     
    │                         │  🗄️ InfluxDB            │     
    │                         │  (Emmagatzemar)         │     
    │                         └────────┬────────────────┘     
    │                                  │                      
    │                         ┌────────▼────────────────┐     
    │                         │  📊 Grafana              │     
    │                         │  (Visualitzar)          │     
    │                         └─────────────────────────┘

  🔌 PLC industrial          🐳 DINS DOCKER
  (MODBUS TCP/RTU)
       │
       │ ── MODBUS ────────▶  ┌─────────────────────────┐
       │                      │  🔧 Node-RED             │
       │                      │  (amb node Modbus)      │
       │                      └─────────────────────────┘
```

| Contenidor | Port | Funció | Analogia |
|:-----------|:-----|:-------|:---------|
| 📡 **Mosquitto** | 1883 | Broker MQTT — rep i reparteix missatges | *El carter* |
| 🔧 **Node-RED** | 1880 | Processament visual — connecta serveis | *El manetes* |
| 🗄️ **InfluxDB** | 8086 | Base de dades de sèries temporals | *La nevera* |
| 📊 **Grafana** | 3000 | Dashboards i gràfics interactius | *La pissarra* |

**Com flueixen les dades:**

```
Sensor/PLC → MQTT → Mosquitto → Node-RED → InfluxDB → Grafana
                   📡            🔧          🗄️         📊
                  (rebre)     (processar)  (guardar)  (mostrar)
```

---

## 📡 1️⃣ Mosquitto — El carter

```📡 Mosquitto (port 1883)
├── Rep missatges MQTT dels sensors
├── Els classifica per temes (topics)
│   · sensors/temperatura
│   · sensors/humitat
│   · actuadors/llum
└── Els reparteix a qui els escolti

🎯 Analogia: El carter — rep cartes i les deixa
   a les bústies correctes
```

**Mosquitto** és el **broker MQTT**, el cor de la comunicació en qualsevol sistema IoT. Tots els missatges passen per ell.

### Com funciona MQTT?

MQTT és un protocol de missatgeria **lleuger** dissenyat per a IoT. Pensa en un **xat** on els dispositius publiquen missatges en canals (topics) i altres dispositius s'hi subscriuen.

```┌─────────────────────────────────────────────────────────┐
│                    📡 BROKER MQTT                         │
│                    (Mosquitto)                            │
│                                                           │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ 🌡️ Sensor    │   │ 💻 Dashboard  │   │ 📱 App mòbil │  │
│  │ publica:     │   │ subscrit a:  │   │ subscrit a:  │  │
│  │ "sensors/    │   │ "sensors/    │   │ "sensors/    │  │
│  │  temperatura"│   │  temperatura"│   │  temperatura"│  │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘  │
│         │                  ▲                  ▲          │
└─────────┼──────────────────┼──────────────────┼──────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                     Totes les dades
                     passen pel broker
```

### 📡 Termes clau

| Terme | Significat | Analogia |
|:------|:-----------|:---------|
| **Broker** | Servidor central que rep i distribueix missatges | *"La centraleta de correus"* |
| **Publisher** | Dispositiu que envia dades | *"Qui envia una carta"* |
| **Subscriber** | Dispositiu que rep dades | *"Qui rep la carta"* |
| **Topic** | Canal on es publiquen els missatges | *"La direcció de la carta"* |
| **Payload** | El contingut del missatge | *"El text de la carta"* |

### 📂 Topics MQTT

Els topics tenen estructura de carpetes:

```bash
sensors/temperatura       → 23.5
sensors/humitat           → 65
plc/cinta1/velocitat      → 1200
plc/cinta1/temperatura    → 45.2
actuadors/llum            → ON
```

Es poden fer **subscripcions amb comodins**:
| Patró | Què captura |
|:------|:-----------|
| `sensors/+` | Tots els sensors |
| `plc/cinta1/#` | **Tot** el que passa a la cinta 1 del PLC |
| `+/temperatura` | Totes les temperatures de qualsevol dispositiu |

---

## 🔧 2️⃣ Node-RED — El manetes

```🔧 Node-RED (port 1880)
├── Programació visual (arrossegar i soltar)
├── Connecta:
│   · MQTT → rep dades
│   · InfluxDB → guarda dades
│   · MODBUS → llegeix PLCs industrials
│   · HTTP → APIs externes
│   · GPIO → hardware real
└── Fàcil: no cal saber programar

🎯 Analogia: El manetes — connecta coses entre si
   com si fossin peces de Lego
```

Node-RED és una eina visual per connectar dispositius IoT. Es programa **arrossegant blocs** (nodes) i connectant-los amb cables.

```┌──────────────────────────────────────────────────────────┐
│  🟠 NODE-RED EDITOR (al navegador)                        │
│                                                            │
│  ┌──────────┐    ┌──────────┐    ┌────────────────────┐   │
│  │ 📡 MQTT   │───→│ 🔧       │───→│ 📊 Dashboard       │   │
│  │ Input     │    │ Function │    │ Gauge + Chart      │   │
│  └──────────┘    └──────────┘    └────────────────────┘   │
│                                                            │
│  ┌──────────┐    ┌──────────┐    ┌────────────────────┐   │
│  │ 🏭 MODBUS │───→│ 🔧       │───→│ 🗄️ InfluxDB       │   │
│  │ Read      │    │ Function │    │ Output             │   │
│  └──────────┘    └──────────┘    └────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

| Concepte | Què és | Exemple |
|:---------|:-------|:--------|
| **Node d'entrada** | Rep dades | MQTT Input, MODBUS Read, Inject |
| **Node de processament** | Transforma dades | Function, Template, Switch |
| **Node de sortida** | Envia o mostra dades | MQTT Output, InfluxDB Out, Debug |
| **Flow** | Conjunt de nodes connectats | Un flux complet |
| **Dashboard** | Interfície visual amb gràfics | UI Gauge, UI Chart, UI Button |

---

## 🏭 Comunicació MODBUS amb PLCs

Node-RED pot parlar directament amb **PLCs industrials** gràcies al protocol **MODBUS**.

### Què és un PLC?

Un **PLC (Programmable Logic Controller)** és un ordinador industrial dissenyat per controlar maquinària en fàbriques, cintes transportadores, sistemes d'automatització, etc.

```┌──────────────────────────────────────────────────────────┐
│  🏭 A LA FÀBRICA                                          │
│                                                            │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐   │
│  │ ⚙️ CINTA 1   │───→│ 🏭 PLC       │───→│ 🔧 NODE-RED │   │
│  │ Velocitat     │    │ (MODBUS)    │    │            │   │
│  │ Temperatura   │    │             │    │ · Llegeix  │   │
│  │ Estat motor   │    │ Registres:  │    │ · Converteix│   │
│  └──────────────┘    │ · %MW100     │    │ · Envia a  │   │
│                      │ · %MW101     │    │   MQTT     │   │
│  ┌──────────────┐    │ · %MW102     │    └──────┬─────┘   │
│  │ ⚙️ CINTA 2   │───→│             │           │          │
│  │ ...          │    └──────────────┘           ▼          │
│  └──────────────┘                              📡 MQTT     │
└──────────────────────────────────────────────────────────┘
```

### Què és MODBUS?

**MODBUS** és un protocol de comunicació industrial creat el 1979. És l'estàndard més utilitzat al món per connectar dispositius d'automatització (PLCs, sensors, actuadors).

| Característica | Valor |
|:--------------|:------|
| 🏭 **Ús principal** | Comunicació amb PLCs i dispositius industrials |
| 📅 **Creat** | 1979 per Modicon (ara Schneider Electric) |
| 🌍 **Estàndard** | Obert, gratuït, el més usat del món |
| 🔗 **Variants** | MODBUS RTU (sèrie) i MODBUS TCP (xarxa) |

### MODBUS RTU vs TCP

```MODBUS RTU (sèrie)
┌─────────────┐        ┌─────────────┐
│   🖥️ PC     │────────│ 🏭 PLC       │
│  (Master)   │  RS-485 │  (Slave)    │
│             │  (cable │   Id: 1     │
│             │   físic)│             │
└─────────────┘        └─────────────┘
• Cable USB/RS-485 (connexió física)
• Un sol dispositiu amos (master), molts esclaus (slaves)
• Fins a 1200 metres de distància
• Velocitat: 9600-115200 bauds


MODBUS TCP (xarxa)
┌─────────────┐        ┌─────────────┐
│   🖥️ PC     │════════│ 🏭 PLC       │
│  (Client)   │  TCP   │  (Server)   │
│             │  (port │   IP:       │
│             │   502) │   192.168.x │
└─────────────┘        └─────────────┘
• Cable Ethernet (xarxa normal)
• Molts clients poden llegir el mateix PLC
• Fins a 100 metres (o més amb switches)
• Molt més ràpid que RTU
```

### Què llegeix Node-RED del PLC?

Un PLC emmagatzema les dades en **registres** — com si fossin variables dins del PLC:

| Registre (MODBUS) | Què guarda | Exemple de valor |
|:------------------|:-----------|:----------------|
| `%MW100` | Velocitat cinta 1 | 1200 RPM |
| `%MW101` | Temperatura motor | 45.2 °C |
| `%MW102` | Estat bomba (ON/OFF) | 1 (ON) |
| `%MW103` | Comptador de peces | 1547 unitats |
| `%MX0.0` | Sensor de presència | TRUE |

Node-RED amb el node **node-red-contrib-modbus** pot:
- **Llegir** registres del PLC (Read Holding Registers)
- **Escriure** valors al PLC (Write Single Register)
- **Llegir** bobines i entrades digitals
- Publicar les dades llegides a MQTT o guardar-les a InfluxDB

### Integració MODBUS → MQTT

```PLC (MODBUS)              Node-RED                   MQTT
┌──────────┐    MODBUS    ┌──────────┐    MQTT     ┌──────────┐
│  %MW100  │─────────────▶│ 🟠       │────────────▶│ 📡       │
│  = 1200  │   read       │ Llegeix  │  publish    │ Mosquitto│
│          │              │ registre │             │          │
│          │              │ i        │             │          │
│  %MW101  │              │ publica  │             │          │
│  = 45.2  │              │ a MQTT   │             │          │
└──────────┘              └──────────┘             └──────────┘
                              │
                              │ (també guarda a InfluxDB)
                              ▼
                         ┌──────────┐
                         │ 🗄️       │
                         │ InfluxDB │
                         └──────────┘
```

**Flux complet des del PLC fins al dashboard:**

```
🏭 PLC (MODBUS TCP) → 🔧 Node-RED llegeix registres
                        ↓
                      📡 Publica a MQTT (topic: "plc/cinta1/velocitat")
                        ↓
                      🗄️ Node-RED guarda a InfluxDB
                        ↓
                      📊 Grafana mostra en gràfic
```

---

## 🗄️ 3️⃣ InfluxDB — La nevera

```🗄️ InfluxDB (port 8086)
├── Base de dades de sèries temporals
├── Perfecta per guardar:
│   · Temperatura cada 5 segons
│   · Humitat cada minut
│   · CPU/RAM cada 10 segons
│   · Velocitat de cinta (PLC) cada segon
└── Consultes ràpides: "dóna'm l'última hora"

🎯 Analogia: Una nevera on poses dades amb data
   de caducitat (les velles s'esborren soles)
```

Una **base de dades de sèries temporals (TSDB)** està optimitzada per a dades que arriben contínuament amb una marca de temps.

### InfluxDB vs Base de dades normal

| Característica | 🗄️ InfluxDB (TSDB) | 🐘 PostgreSQL (SQL normal) |
|:--------------|:--------------------|:--------------------------|
| **Dissenyat per a** | Dades amb timestamp | Dades relacionals |
| **Exemple** | "Temperatura cada 5s" | "Usuaris, comandes" |
| **Velocitat escriptura** | ⚡ 1M punts/segon | 🐢 10K files/segon |
| **Neteja automàtica** | ✅ Retention policies | ❌ Cal esborrar manualment |
| **Consum de disc** | 🪶 Molt eficient | 🏋️ Molt pesat per a dades temporals |

Les dades s'emmagatzemen així:

```
Measurement: temperatura
┌──────────────────────────┬──────────┬───────┬──────┐
│ time                     │ sensor   │ valor │ unitat│
├──────────────────────────┼──────────┼───────┼──────┤
│ 2025-03-20T10:00:00Z     │ sala     │ 23.5  │ °C   │
│ 2025-03-20T10:00:05Z     │ sala     │ 23.7  │ °C   │
│ 2025-03-20T10:00:10Z     │ sala     │ 23.6  │ °C   │
│ 2025-03-20T10:00:05Z     │ exterior │ 15.2  │ °C   │
│ 2025-03-20T10:00:10Z     │ cinta1   │ 45.2  │ °C   │
└──────────────────────────┴──────────┴───────┴──────┘
```

Cada dada té:
- **time** — Quan es va registrar
- **tags** — Etiquetes per filtrar (sensor, ubicació, màquina)
- **fields** — El valor numèric
- **measurement** — El nom de la "taula" (temperatura, humitat, velocitat...)

---

## 📊 4️⃣ Grafana — La pissarra

```📊 Grafana (port 3000)
├── Dashboards bonics i interactius
├── Gràfics de:
│   · Línies (temperatura al temps)
│   · Barres (comparatives)
│   · Gauges (termòmetres)
│   · Mapes (geolocalització)
│   · Taules (valors precisos)
└── Consulta dades d'InfluxDB

🎯 Analogia: Una pissarra on veus tot el que passa
   a la teva instal·lació
```

Grafana és l'eina de visualització més utilitzada en IoT i monitorització. **No guarda dades** — les consulta d'InfluxDB (o altres fonts) i les mostra.

```┌──────────────────────────────────────────────────────────┐
│  📊 GRAFANA DASHBOARD (al navegador)                      │
│                                                            │
│  ┌─────────────────┐  ┌────────────────────────────────┐  │
│  │  🌡️ Temperatura   │  │  📈 Evolució (última hora)    │  │
│  │  ┌─────────┐     │  │  ╱╲    ╱╲                     │  │
│  │  │  25.3°C │     │  │ ╱  ╲  ╱  ╲                    │  │
│  │  └─────────┘     │  │╱    ╲╱    ╲___╱╲              │  │
│  │  Gauge           │  └────────────────────────────────┘  │
│  └─────────────────┘                                       │
│  ┌─────────────────┐  ┌────────────────────────────────┐  │
│  │  💧 Humitat      │  │  📊 Barres (últimes 24h)      │  │
│  │      65%        │  │  ██  ██  ██                    │  │
│  │  ─────●─────    │  │  ██  ██  ██  ██               │  │
│  │  Mínim 40%      │  │  ██  ██  ██  ██  ██           │  │
│  └─────────────────┘  └────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## 🐳 L'arquitectura completa de l'activitat

```┌───────────────────────────────────────────────────────────┐
│                   🖥️ La teva VM Ubuntu                      │
│                                                             │
│   📡 port 1883     🔧 port 1880    🗄️ port 8086           │
│   📊 port 3000                                              │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │  🐳 DOCKER COMPOSE                                  │  │
│   │                                                     │  │
│   │  ┌──────────┐    ┌──────────┐    ┌──────────────┐  │  │
│   │  │ 📡       │◄───│ 🔧       │───▶│ 🗄️           │  │  │
│   │  │ Mosquitto│    │ Node-RED │    │ InfluxDB     │  │  │
│   │  │          │    │          │    │              │  │  │
│   │  │ Broker   │    │ · MQTT   │    │ Base de      │  │  │
│   │  │ MQTT     │    │ · MODBUS │    │ dades        │  │  │
│   │  └──────────┘    │ · Influx │    └──────┬───────┘  │  │
│   │                  └──────────┘           │          │  │
│   │                                    ┌────▼──────┐   │  │
│   │                                    │ 📊 Grafana │   │  │
│   │                                    │ (visual)   │   │  │
│   │                                    └────────────┘   │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   🐍 Python                        🏭 PLC (simulat)        │
│   · publisher.py                   · MODBUS TCP            │
│   · subscriber.py                  · Registres %MW         │
└───────────────────────────────────────────────────────────┘
```

**Com funcionen les dades:**
1. **Sensors/PLCs** publiquen dades a MQTT o les exposen per MODBUS
2. **Mosquitto** rep i redistribueix els missatges MQTT
3. **Node-RED** es subscriu a MQTT, llegeix MODBUS, processa i:
   - Envia dades al dashboard visual
   - Guarda a **InfluxDB** per a l'històric
4. **Grafana** consulta InfluxDB i mostra gràfics bonics
5. **Python** publica dades simulades i s'hi subscriu

---

## 📖 Vocabulari clau

| Terme | Significat | 🧠 Per recordar-ho... |
|:------|:-----------|:---------------------|
| **MQTT** | Protocol de missatgeria per IoT | *"Missatgeria lleugera per dispositius petits"* |
| **Broker** | Servidor MQTT | *"La centraleta de correus"* |
| **Topic** | Canal de missatges | *"Com un hashtag, però en arbre"* |
| **Publicar** | Enviar un missatge | *"Fer un tweet a un topic"* |
| **Subscriure** | Rebre missatges d'un topic | *"Seguir un tema per rebre actualitzacions"* |
| **Node-RED** | Eina visual per IoT | *"Scratch per a IoT"* |
| **Flow** | Conjunt de nodes connectats | *"Un programa fet de blocs"* |
| **Dashboard** | Interfície gràfica | *"Punteres i gràfics al navegador"* |
| **MODBUS** | Protocol industrial per PLCs | *"L'idioma de les fàbriques"* |
| **MODBUS TCP** | MODBUS per Ethernet (port 502) | *"MODBUS per xarxa"* |
| **MODBUS RTU** | MODBUS per cable sèrie (RS-485) | *"MODBUS per cable físic"* |
| **PLC** | Ordinador industrial | *"El cervell de la màquina"* |
| **Registre (%MW)** | Memòria del PLC | *"La llibreta d'anotacions del PLC"* |
| **InfluxDB** | Base de dades temporal (TSDB) | *"La nevera de dades"* |
| **TSDB** | Time Series Database | *"Base de dades dissenyada per al temps"* |
| **Grafana** | Eina de visualització | *"La pissarra de l'IoT"* |
| **docker compose up** | Engegar tots els contenidors | *"Prémer el botó de start"* |
| **docker compose down** | Aturar i esborrar contenidors | *"Prémer stop i netejar"* |

---

## ❓ Preguntes freqüents

**❓ Per què MQTT i no HTTP?**
HTTP necessita que el client pregunti sempre (polling). MQTT és **push**: el broker t'envia les dades automàticament quan canvien. Ideal per IoT.

**❓ Puc trencar la VM jugant amb contenidors?**
No. Si un contenidor peteja, simplement `docker compose down` i tornes a engegar. **El sistema queda intacte.**

**❓ Què passa si aturo Mosquitto?**
Node-RED i Python es quedaran esperant. Quan tornis a engegar Mosquitto, la comunicació es restablirà automàticament.

**❓ Puc accedir al dashboard des del meu mòbil?**
Sí! Si la VM està en mode **Bridge** (IP pròpia), troba la IP de la VM (`ip a`) i accedeix a `http://<IP-VM>:1880` (Node-RED) o `http://<IP-VM>:3000` (Grafana) des de qualsevol dispositiu de la mateixa xarxa.

**❓ I si no tinc un PLC real?**
Cap problema! Hi ha eines que simulen un PLC MODBUS TCP. Les fem servir a classe per fer proves sense necessitar hardware real.

**❓ Per què Docker Compose i no Docker run per a cada contenidor?**
Docker Compose ho fa tot amb un sol fitxer i una sola comanda. Quan tinguis 10 serveis funcionant (InfluxDB, Grafana, Node-RED, Mosquitto, etc.), no voldràs escriure 10 `docker run` cada cop.

**❓ MQTT és segur?**
Per defecte no té contrasenya. En producció es configura amb usuari i contrasenya o certificats TLS. Per a classe, ho deixem obert per simplificar.

**❓ Quina diferència hi ha entre MODBUS i MQTT?**
MODBUS és per llegir/escriviu registres d'un dispositiu (normalment a la mateixa xarxa local). MQTT és per publicar/subscriure's a missatges (pot ser a través d'internet). En un sistema IoT real, **es complementen**: MODBUS llegeix el PLC, MQTT transporta les dades.

**❓ Puc tenir tot això en un sol contenidor?**
Tècnicament sí, però **no es fa**. Cada servei va al seu contenidor perquè sigui independent, actualitzable i reemplaçable. A més, si un servei peteja, els altres segueixen funcionant.

# 📚 Teoria: Contenidors en acció — MQTT i Node-RED

## Abans de començar...

A les activitats anteriors vas instal·lar Docker i les eines necessàries. Ara toca **posar-les a treballar** creant un sistema IoT real amb contenidors.

```💻 La teva màquina virtual (Ubuntu Server)
   │
   ├── Activitat 1: 🐧 Ubuntu nu
   ├── Activitat 2: 🐳 Docker + eines instal·lats
   │
   └── Activitat 3: 🚀 Contenidors en acció!
         · Mosquitto (broker MQTT)        → 📡
         · Node-RED (dashboard visual)     → 📊
         · Python (publicador/subscriptor) → 🐍
```

> ✅ **Objectiu:** Executar un stack IoT complet amb Docker Compose i entendre com es comuniquen els serveis.

---

## 🧠 Com funciona MQTT?

MQTT és un protocol de missatgeria **lleuger** dissenyat per a IoT. Pensa en un **xat** on els dispositius publiquen missatges en canals (topics) i altres dispositius s'hi subscriuen.

```┌─────────────────────────────────────────────────────────┐
│                    📡 BROKER MQTT                         │
│                    (Mosquitto)                            │
│                                                           │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ 🌡️ Sensor    │   │ 💻 Dashboard  │   │ 📱 App mòbil │  │
│  │ publica:     │   │ subscrit a:  │   │ subscrit a:  │  │
│  │ "casa/sala/  │   │ "casa/sala/  │   │ "casa/sala/  │  │
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
casa/sala/temperatura     → 23.5
casa/sala/humitat         → 65
casa/exterior/temperatura → 18.2
casa/exterior/llum        → ON
```

Es poden fer **subscripcions amb comodins**:
| Patró | Què captura |
|:------|:-----------|
| `casa/sala/+` | Tots els sensors de la sala |
| `casa/+/temperatura` | Totes les temperatures de casa |
| `casa/#` | **Tot** el que passi a casa |

---

## 🟠 Què és Node-RED?

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
│  │ 🐍 HTTP   │───→│ 🔧       │───→│ 💾 Envia a base   │   │
│  │ Request   │    | Template │    │ de dades           │   │
│  └──────────┘    └──────────┘    └────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

| Concepte | Què és | Exemple |
|:---------|:-------|:--------|
| **Node d'entrada** | Rep dades | MQTT Input, HTTP Input, Inject |
| **Node de processament** | Transforma dades | Function, Template, Switch |
| **Node de sortida** | Envia o mostra dades | MQTT Output, HTTP Response, Debug |
| **Flow** | Conjunt de nodes connectats | Un flux complet |
| **Dashboard** | Interfície visual amb gràfics | UI Gauge, UI Chart, UI Button |

---

## 🐳 L'arquitectura d'aquesta activitat

```┌───────────────────────────────────────────────────────────┐
│                   🖥️ La teva VM Ubuntu                      │
│                                                             │
│   🌐 http://localhost:1880      📡 1883 (MQTT)              │
│         │                              │                    │
│   ┌─────▼──────────┐    ┌──────────────▼─────┐             │
│   │  🟠 Node-RED    │    │  📡 Mosquitto       │             │
│   │  · Dashboard    │◄───│  (Broker MQTT)     │             │
│   │  · Flows        │    │                    │             │
│   └────────────────┘    └──────────▲──────────┘             │
│                                    │                        │
│                           ┌────────┴────────┐               │
│                           │  🐍 Python       │               │
│                           │  · publisher.py  │               │
│                           │  · subscriber.py │               │
│                           └─────────────────┘               │
│                                                             │
│   🐳 Docker Compose ho gestiona TOT                         │
└───────────────────────────────────────────────────────────┘
```

**Com funciona:**
1. **Mosquitto** és el broker MQTT — tots els missatges passen per ell
2. **Node-RED** es subscriu a topics MQTT i mostra les dades al dashboard
3. **Python** publica missatges (simulant sensors) i s'hi subscriu
4. Tot corre dins **contenidors Docker** gestionats per **Docker Compose**

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
Sí! Si la VM està en mode **Bridge** (IP pròpia), troba la IP de la VM (`ip a`) i accedeix a `http://<IP-VM>:1880` des de qualsevol dispositiu de la mateixa xarxa.

**❓ Per què Docker Compose i no Docker run per a cada contenidor?**
Docker Compose ho fa tot amb un sol fitxer i una sola comanda. Quan tinguis 10 serveis funcionant (InfluxDB, Grafana, Node-RED, Mosquitto, etc.), no voldràs escriure 10 `docker run` cada cop.

**❓ MQTT és segur?**
Per defecte no té contrasenya. En producció es configura amb usuari i contrasenya o certificats TLS. Per a classe, ho deixem obert per simplificar.

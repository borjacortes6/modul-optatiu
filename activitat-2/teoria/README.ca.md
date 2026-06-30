# 📚 Teoria: Què és Docker i per què el necessitem?

## Abans de començar...

A l'activitat anterior vas instal·lar Ubuntu Linux en una màquina virtual. Ara li donarem vida instal·lant **Docker**, l'eina que fa servir el 90% dels projectes IoT i cloud del món.

```💻 La teva màquina virtual (Ubuntu Server)
   │
   ├── Activitat 1: 🐧 Ubuntu nu
   │     · Sense programes extra
   │     · Només terminal
   │
   └── Activitat 2: 🐳 Ubuntu + Docker
         · Docker instal·lat
         · Python + MQTT
         · Preparat per IoT!
```

> ✅ **Objectiu:** Instal·lar Docker i les eines necessàries per començar amb IoT a la teva màquina virtual.

---

## 🧠 Què és Docker?

**Docker** és un programa que permet crear i executar **contenidors**. Un contenidor és com una "mini màquina virtual" molt lleugera.

```┌──────────────────────────────────────────────────────────┐
│  🌍 EL MÓN REAL                                           │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  🖥️ UBUNTU (la teva VM)                              │ │
│  │                                                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │ 📦 Node-RED  │  │ 🗄️ InfluxDB │  │ 📊 Grafana   │   │ │
│  │  │ (contenidor) │  │ (contenidor)│  │ (contenidor)│   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │ │
│  │                                                        │ │
│  │  🐳 DOCKER ENGINE (el motor de contenidors)            │ │
│  │                                                        │ │
│  │  🐧 UBUNTU SERVER (el sistema operatiu)                │ │
│  └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘```

### Contenidors vs Màquines virtuals

```📊 Diferències clau

                    ┌──────────────────────┐    ┌──────────────────────┐
                    │   📦 CONTENIDOR       │    │   🖥️ MÀQUINA VIRTUAL │
                    └──────────────────────┘    └──────────────────────┘

    Arrencada       ⚡ Segons                 🐢 Minuts
    Mida            📏 MB                     💿 GB
    RAM que gasta   🪶 Molt poca              🏋️ Tota la RAM assignada
    Comparteix      💞 El nucli de Linux       ❌ Cada VM té el seu SO
    SO amfitrió                                    
    Portabilitat    📦 Un fitxer .tar           📦 Un fitxer .ova
    Ús típic        🎯 Una app per contenidor  🖥️ Un sistema complet
```

> 💡 **Analogia:** Una màquina virtual és com llogar un pis sencer. Un contenidor és com llogar una habitació — tot és més ràpid, barat i lleuger.

---

## 🐳 Per què Docker a IoT?

En IoT, Docker és **imprescindible** perquè:

```┌──────────────────────────────────────────────────┐
│  🎯 PER QUÈ DOCKER A IoT?                         │
│                                                    │
│  1️⃣  📦 **Empaquetat**                             │
│      · Cada servei va al seu contenidor            │
│      · Mosquitto (MQTT) en un, Node-RED en un...  │
│                                                    │
│  2️⃣  ⚡ **Lleuger**                                │
│      · Pots tenir 5 serveis en 1 GB de RAM        │
│      · Ideal per ordinadors modestos              │
│                                                    │
│  3️⃣  🔄 **Reproduïble**                            │
│      · Funciona igual a qualsevol lloc            │
│      · Si funciona al teu portàtil, funciona      │
│        al servidor, al mini PC, al núvol...       │
│                                                    │
│  4️⃣  🔌 **Connectat**                              │
│      · Tots els contenidors es parlen entre ells  │
│      · Mosquitto ↔ Node-RED ↔ InfluxDB ↔ Grafana │
└──────────────────────────────────────────────────┘```

---

## 📦 Què instal·larem?

| Programa | Què és | Per a què serveix |
|:---------|:-------|:-----------------|
| 🐳 **Docker Engine** | Motor de contenidors | Per crear i executar contenidors |
| 🐙 **Docker Compose** | Orquestrador de contenidors | Per llençar diversos contenidors alhora |
| 🐍 **Python 3** | Llenguatge de programació | Per programar sensors, clients MQTT... |
| 📡 **paho-mqtt** | Llibrearia Python per MQTT | Per connectar-se al broker MQTT |

---

## 📖 Vocabulari clau

| Terme | Significat | 🧠 Per recordar-ho... |
|:------|:----------|:---------------------|
| **Contenidor** | Entorn aïllat per executar una app | *"Un procés amb la seva pròpia habitació"* |
| **Imatge** | Plantilla per crear contenidors | *"Com un ISO, però per a contenidors"* |
| **Docker Engine** | El programa que gestiona contenidors | *"El cor de Docker"* |
| **Docker Compose** | Eina per gestionar múltiples contenidors | *"Una recepta per llençar tot alhora"* |
| **docker-compose.yml** | Fitxer de configuració de Compose | *"La llista de la compra dels contenidors"* |
| **docker pull** | Descarregar una imatge | *"Com baixar un programa de internet"* |
| **docker run** | Crear i iniciar un contenidor | *"Com executar un programa"* |
| **docker ps** | Llistar contenidors en marxa | *"Veure què està funcionant"* |

---

## ❓ Preguntes freqüents (teoria)

**❓ Docker només funciona a Linux?**
Sí, Docker fa servir el nucli de Linux. Al Windows o macOS, Docker Desktop crea una VM Linux petita al darrere.

**❓ Puc trencar el meu Ubuntu jugant amb Docker?**
No. Si esborres un contenidor, les dades es perden només dins del contenidor. **El teu Ubuntu queda intacte.**

**❓ Quants contenidors puc tenir?**
Tants com memòria lliure tinguis. Una VM amb 2 GB pot portar 5-10 contenidors sense problemas.

**❓ Què és millor, instal·lar programes directament o usar Docker?**
Per a classe farem servir Docker perquè és la manera professional. Al món real, Docker és l'estàndard.

**❓ Docker fa que l'ordinador vagi més lent?**
Els contenidors gairebé no tenen sobrecàrrega. Si res, van **més ràpids** que instal·lar programes directament.

# 📚 Teoria: InfluxDB + Grafana — Emmagatzemar i visualitzar dades

## Abans de començar...

A l'activitat 3 vas construir un sistema IoT amb Mosquitto (MQTT) i Node-RED, i vas crear un dashboard en directe amb gauges. Però hi ha un problema: **quan tanquis el dashboard, les dades es perden**.

Per solucionar-ho necessites:

- 🗄️ **InfluxDB** — Una base de dades pensada per a **sèries temporals** (dades que arriben amb una marca de temps)
- 📊 **Grafana** — Una eina de **visualització avançada** que crea dashboards bonics amb gràfics històrics

```
🌡️ Sensor/publisher ──→ 📡 Mosquitto ──→ 🔧 Node-RED ──→ 🗄️ InfluxDB ──→ 📊 Grafana
                            (MQTT)        (processar)     (guardar)       (visualitzar)
```

> ✅ **Objectiu:** Entendre com funciona una base de dades de sèries temporals i com crear dashboards professionals amb Grafana.

---

## 🗄️ 1️⃣ InfluxDB — La nevera de dades

```
🗄️ InfluxDB (port 8086)
├── Base de dades de sèries temporals (Time Series DB)
├── Cada dada porta una marca de temps (timestamp)
├── Optimitzat per: moltes dades que arriben constantment
├── NO és com MySQL o PostgreSQL
└── Perfecte per a: sensors, mètriques, logs, IoT
```

### Què és una sèrie temporal?

Una **sèrie temporal** és simplement una llista de valors mesurats al llarg del temps:

```
Temps                  | Temperatura
2024-01-15 10:00:00   | 23.5
2024-01-15 10:00:03   | 23.8
2024-01-15 10:00:06   | 24.1
2024-01-15 10:00:09   | 23.9
...                   | ...
```

Cada dada té:
- **Valor** (ex: 23.5)
- **Timestamp** (ex: 10:00:03)
- **Tags** (etiquetes per classificar, ex: `aula=1`, `sensor=temperatura`)

### Conceptes clau d'InfluxDB

| Concepte | Què és? | Exemple |
|:---------|:--------|:--------|
| **Bucket** | "Carpeta" on es guarden dades | `sensors_aula1` |
| **Measurement** | Tipus de dada | `temperatura` o `humitat` |
| **Field** | El valor numèric | `valor=23.5` |
| **Tag** | Etiqueta per classificar | `aula=1`, `alumne=NomAlumne` |
| **Timestamp** | Quan es va mesurar | `2024-01-15T10:00:03Z` |

### Base de dades de sèries temporals vs tradicional

| Base de dades tradicional (MySQL) | Base de dades temporal (InfluxDB) |
|:----------------------------------|:----------------------------------|
| Taules amb files i columnes | Sèries de valors en el temps |
| Millor per: usuaris, comandes, inventari | Millor per: sensors, mètriques, logs |
| Consultes SQL: `SELECT * FROM usuaris` | Consultes Flux: `from(bucket:"...")` |
| Pensa en dades que canvien | Pensa en dades que arriben constantment |

> 🎯 **Analogia:** InfluxDB és com una **nevera** — hi poses dades i es conserven fresques amb la seva data. MySQL és com un **arxivador** — està tot classificat en carpetes.

---

## 📊 2️⃣ Grafana — La pissarra de dades

```
📊 Grafana (port 3000)
├── Crea dashboards amb gràfics bonics
├── Es connecta a moltes fonts: InfluxDB, MySQL, Prometheus, etc.
├── Panels: time series, gauges, bar charts, tables, maps
├── Alertes: envia notificacions si alguna cosa va malament
└── Open source i gratuït
```

### Com funciona Grafana

```
┌──────────────────────────────────────────────────────┐
│  📊 GRAFANA (al navegador, port 3000)                │
│                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ 📡 Conexió    │  │ 📈 Panell    │  │ 📋 Dashboard │ │
│  │ a InfluxDB   │──│ Time Series  │──│ amb molts    │ │
│  │ (Data Source)│  │ + Gauge      │  │ panells      │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└──────────────────────────────────────────────────────┘
```

### Termes clau de Grafana

| Concepte | Què és? |
|:---------|:--------|
| **Data Source** | Font de dades (InfluxDB, MySQL, etc.) |
| **Dashboard** | Llenç on col·loques panells |
| **Panel** | Un gràfic, gauge, taula o mapa |
| **Query** | Consulta per obtenir les dades |
| **Time Range** | Interval de temps a mostrar (15m, 1h, 7d...) |
| **Alert** | Notificació automàtica si es compleix una condició |

### Per què Grafana i no el Dashboard de Node-RED?

| Node-RED Dashboard | Grafana |
|:-------------------|:--------|
| Dades **en directe** (ara) | Dades **històriques** (ahir, setmana passada) |
| Gauges senzills | Gràfics de línies, barres, taules, mapes |
| Sense configuració avançada | Alertes, anotacions, variables |
| Bo per veure l'instant | Bo per veure **l'evolució** |

> 🎯 **Analogia:** Node-RED Dashboard és com el **quadre de comandament d'un cotxe** (velocitat ara). Grafana és com **l'informe de viatge** (velocitat mitjana, màxima, evolució).

---

## 🔗 3️⃣ Com flueixen les dades — El pipeline complet

Ara tens el sistema complet:

```
🌡️ publisher.py (cada 3s)
        │
        │  MQTT
        ▼
📡 Mosquitto (port 1883)
        │
        │  MQTT
        ▼
🔧 Node-RED (port 1880)
        │
        ├──→ 📊 Dashboard (gauges en directe)
        │
        └──→ 🗄️ InfluxDB (port 8086)
                 │
                 │  Consultes (Flux / SQL)
                 ▼
              📊 Grafana (port 3000)
                 │
                 └──→ 📈 Gràfics històrics
```

### Què passa quan executes el publisher?

1. `publisher.py` envia `25.3` al topic `NomAlumne/aula_1/temperatura`
2. **Mosquitto** rep el missatge i l'encamina
3. **Node-RED** el rep (subscrit al topic) i:
   - L'envia al **gauge** del dashboard (en directe)
   - L'escriu a **InfluxDB** (per guardar-lo)
4. **Grafana** llegeix d'InfluxDB i mostra gràfics bonics

### Per què és útil?

- Pots veure **l'evolució de la temperatura** de tota la setmana
- Pots comparar **ahir vs avui**
- Pots posar **alertes** (si la temperatura passa de 30°C, envia un email)
- Pots crear **dashboards compartibles** amb el teu equip

---

## 🧪 4️⃣ InfluxDB 3.x — Novetats

InfluxDB 3.x (la versió que instal·larem) té algunes novetats importants:

| Canvi | Abans (2.x) | Ara (3.x) |
|:------|:-----------|:----------|
| **Llenguatge de consultes** | Flux (propi) | **SQL** + InfluxQL |
| **Autenticació** | Token | **Token** (igual) |
| **Emmagatzematge** | TSM (propi) | **Apache Parquet** + object store |
| **Rendiment** | Bo | **10x més ràpid** |
| **UI Web** | Sí (port 8086) | **Sí** (port 8086) |

> ✅ Amb InfluxDB 3.x pots fer consultes amb **SQL** normal, cosa que el fa molt més accessible.

---

## ✅ Resum

- 🗄️ **InfluxDB** guarda dades de sensors amb marca de temps
- 📊 **Grafana** les visualitza en gràfics interactius
- 🔧 **Node-RED** fa de pont entre MQTT i InfluxDB
- 📡 **Mosquitto** transporta les dades dels sensors
- 🔗 El pipeline complet: **Sensor → MQTT → Node-RED → InfluxDB → Grafana**

A la pràctica següent ho muntaràs pas a pas! 🚀

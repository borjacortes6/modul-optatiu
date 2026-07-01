# 📚 Teoria: DS18B20 + ESP32 — Connectar sensors reals a IoT

## Abans de començar...

Fins ara tot el sistema IoT ha estat **virtual**: sensors simulats dins de contenidors Docker, dades falses generades per scripts Python. Ara toca connectar **hardware real**.

El **DS18B20** és un sensor de temperatura digital, barat (~2€), precís (±0.5°C) i molt fàcil d'usar. L'**ESP32** és un microcontrolador amb WiFi i Bluetooth integrat. Junts formen el **dispositiu IoT perfecte** per començar.

> ✅ **Objectiu:** Entendre com funciona el sensor DS18B20, el protocol 1-Wire, i com es connecta físicament a l'ESP32.

---

## 1️⃣ El sensor DS18B20

### Què és?

El **DS18B20** és un sensor de temperatura digital fabricat per Maxim Integrated (ara Analog Devices). Mesura temperatures de **-55°C a +125°C** amb una precisió de **±0.5°C** entre -10°C i +85°C.

```
        DS18B20 (vista frontal)
        ┌──────────────────┐
        │                  │
        │    DS18B20       │
        │                  │
        │  ┌──┐ ┌──┐ ┌──┐ │
        │  │  │ │  │ │  │ │
        └──┴──┴─┴──┴─┴──┴─┘
           │    │    │
          GND  DATA VDD
          (1)   (2)  (3)
```

### Pinout

| Pin | Nom | Funció | Connecta a |
|:----|:----|:-------|:-----------|
| 1 | **GND** | Terra | GND de l'ESP32 |
| 2 | **DATA** | Dades (1-Wire) | GPIO4 + resistor 4.7kΩ a 3.3V |
| 3 | **VDD** | Alimentació | 3.3V de l'ESP32 |

> ⚠️ **L'ordre dels pins depèn del fabricant!** Mira sempre la serigrafia de la teva placa. Algunes plaques tenen l'ordre: **VDD, DATA, GND**.

### Característiques principals

| Propietat | Valor |
|:----------|:------|
| Rang de temperatura | -55°C a +125°C |
| Precisió | ±0.5°C (de -10°C a +85°C) |
| Resolució | 9 a 12 bits (configurable) |
| Temps de conversió | 93ms (9 bits) a 750ms (12 bits) |
| Protocol | **1-Wire** (un sol cable per dades) |
| Alimentació | 3.0V – 5.5V |
| Consum | ~1mA (actiu), ~750nA (standby) |
| Adreça única | Cada sensor té un ID de 64 bits gravat de fàbrica |

### Per què el DS18B20?

| Avantatge | Per què importa |
|:----------|:----------------|
| 🌡️ **Precís** | ±0.5°C és suficient per a la majoria de projectes IoT |
| 🔗 **1-Wire** | Un sol pin de dades — pots connectar **molts sensors** al mateix GPIO |
| 🔢 **Digital** | No cal ADC ni calibratge — la temperatura surt en graus directament |
| 💰 **Barat** | ~2€ per sensor, ideal per a l'aula |
| 📏 **Fàcil de cablejar** | Només 3 cables (VCC, GND, DATA) |

---

## 2️⃣ El protocol 1-Wire

El **1-Wire** és un protocol de comunicació que, com el seu nom indica, necessita **un sol cable** per transmetre dades (a part dels cables d'alimentació i terra).

### Com funciona?

```
   ┌────── 3.3V ──────┐
   │                   │
   │    ┌─[4.7kΩ]────┐ │
   │    │            │ │
   ├────┴────┐  ┌────┴─┴────┐
   │  ESP32  │  │  DS18B20  │
   │  GPIO4  │─┘│  DATA     │
   │  GND    │───│  GND      │
   │  3.3V   │───│  VDD      │
   └─────────┘   └──────────┘
```

### Per què cal un resistor pull-up?

El bus 1-Wire funciona amb **lògica de drenador obert**:
- Quan el dispositiu vol enviar un **0**, connecta el cable a GND (baixa la tensió)
- Quan vol enviar un **1**, deixa el cable lliure, i el **resistor pull-up** puja la tensió a 3.3V

Sense el resistor de **4.7kΩ**, el cable queda "al volant" i el senyal és impredictible. El sensor no funcionarà correctament.

```
Sense resistor:    ╎╎╎╎╎╎╎╎╎╎╎╎╎╎╎╎╎╎  (senyal indefinit)
Amb resistor:      3.3V ──────────
                   0V   ▁▁▁▁▁▁▁▁▁▁▁▁  (senyal clar)
```

> 🎯 **Analogia:** El pull-up és com una **molla** que manté la porta tancada. Quan algú vol obrir-la (enviar un 0), estira del pom (baixa la tensió). Si ningú estira, la molla torna a tancar (torna a 3.3V).

### Seqüència de comunicació

Per llegir la temperatura, l'ESP32 fa:

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│   RESET  │ → │ SKIP ROM │ → │CONVERT T │ → │ ESPERA   │
│          │   │  (0xCC)  │   │  (0x44)  │   │  750ms   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                     ↓
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ LLEGEIX  │ ← │ READ     │ ← │ SKIP ROM │ ← │   RESET  │
│ temp (°C)│   │SCRATCHPAD│   │  (0xCC)  │   │          │
│          │   │  (0xBE)  │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Com funciona la conversió?

El sensor intern té un **oscil·lador** la freqüència del qual canvia amb la temperatura. Un comptador mesura aquesta freqüència i la converteix en un valor digital de **12 bits** (per defecte).

| Bits de resolució | Temps de conversió | Precisió |
|:-----------------|:------------------|:---------|
| 9 bits | 93.75ms | 0.5°C |
| 10 bits | 187.5ms | 0.25°C |
| 11 bits | 375ms | 0.125°C |
| **12 bits** (per defecte) | **750ms** | **0.0625°C** |

---

## 3️⃣ L'ESP32 — El cervell del dispositiu

L'**ESP32** és un microcontrolador fabricat per Espressif Systems amb:

```
┌──────────────────────────────────────┐
│              ESP32                   │
│                                      │
│  ┌────────────────────────┐          │
│  │  Processador           │          │
│  │  Tensilica Xtensa LX6  │          │
│  │  2 nuclis a 240MHz     │          │
│  └───────────┬────────────┘          │
│              │                       │
│  ┌───────────┴────────────┐          │
│  │  WiFi 802.11 b/g/n     │          │
│  │  Bluetooth 4.2 BR/EDR +│          │
│  │  BLE                   │          │
│  └────────────────────────┘          │
│                                      │
│  GPIO pins: 34 (programables)        │
│  ADC: 2 × 12 bits (18 canals)        │
│  RAM: 520 KB                         │
│  Flash: 2 MB / 4 MB / 16 MB          │
│  Tensió: 3.3V                        │
└──────────────────────────────────────┘
```

### Per què ESP32 i no Arduino Uno?

| Característica | ESP32 | Arduino Uno |
|:--------------|:------|:------------|
| WiFi | ✅ **Integrat** | ❌ Cal mòdul extern |
| Velocitat | 240 MHz | 16 MHz |
| RAM | 520 KB | 2 KB |
| Preu | ~5€ | ~3€ + mòdul WiFi (10€) |
| MQTT | ✅ Client nadiu | ❌ Cal biblioteca + ESP8266 |
| Pins | 34 GPIO | 14 GPIO |

> 🎯 **Analogia:** L'ESP32 és com un **mòbil barat** (ho té tot integrat). L'Arduino és com un **rellotge de polsera** (fa una cosa, però la fa bé). Per a IoT, l'ESP32 guanya.

---

## 4️⃣ Esquema de connexions complet

```
ESP32                      DS18B20
┌────────┐                ┌──────┐
│    3.3V├────────────────┤ VDD  │
│        │                │      │
│        │    ┌─[4.7kΩ]──┤ DATA │
│   GPIO4├────┘          │      │
│        │                │      │
│     GND├────────────────┤ GND  │
└────────┘                └──────┘
```

### Llista de materials

| Component | Quantitat | Preu aprox. |
|:----------|:----------|:------------|
| ESP32 (qualsevol model) | 1 | ~5€ |
| Sensor DS18B20 | 1 | ~2€ |
| Resistor 4.7kΩ | 1 | ~0.10€ |
| Cables Dupont | 3 | ~0.50€ |
| Protoboard (opcional) | 1 | ~1€ |

**Total: ~8€ per alumne** (sense l'ESP32, que es pot reutilitzar)

---

## ✅ Resum

| Concepte | Què és? |
|:---------|:--------|
| **DS18B20** | Sensor de temperatura digital, protocol 1-Wire |
| **1-Wire** | Protocol amb un sol cable de dades + resistor pull-up |
| **GPIO4** | Pin de l'ESP32 on connectem el DATA del sensor |
| **Pull-up 4.7kΩ** | Resistance necessària per al bus 1-Wire |
| **ESP32** | Microcontrolador amb WiFi integrat, ideal per IoT |
| **ESP-IDF** | Framework oficial d'Espressif per programar l'ESP32 en C |

A la pràctica següent ho muntaràs tot i veuràs les dades en acció! 🚀

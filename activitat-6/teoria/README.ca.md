# 📚 Teoria: BME280 + ESP32 — Temperatura, humitat i pressió amb I2C

## Abans de començar...

Fins ara tot el sistema IoT ha estat **virtual**: sensors simulats dins de contenidors Docker, dades falses generades per scripts Python. Ara toca connectar **hardware real**.

El **BME280** és un sensor ambiental de Bosch, capaç de mesurar **temperatura, humitat i pressió atmosfèrica** en un sol xip. Costa ~3€ i es comunica per **I2C**, un protocol que només necessita **2 cables** (SDA + SCL). L'**ESP32** és un microcontrolador amb WiFi i Bluetooth integrat. Junts formen el **dispositiu IoT perfecte** per començar.

> ✅ **Objectiu:** Entendre com funciona el sensor BME280, el protocol I2C, i com es connecta físicament a l'ESP32.

---

## 1️⃣ El sensor BME280

### Què és?

El **BME280** és un sensor ambiental fabricat per **Bosch Sensortec**. Mesura **temperatura, humitat relativa i pressió baromètrica** tot en un xip de 2.5 × 2.5 mm.

```
        BME280 (vista superior)
        ┌──────────────────┐
        │                  │
        │   ┌──────────┐  │
        │   │ ████████ │  │
        │   │ ██  ████ │  │
        │   └──────────┘  │
        │                  │
        └──────────────────┘
         1.5mm × 1.5mm
       (mida real del xip)
```

Les plaques breakout que trobareu porten el xip en una PCB petita amb els pins accessibles:

```
        ┌────────────────────────────┐
        │  BME280  Breakout          │
        │ ┌──────────────────────┐   │
        │ │   ████████████████   │   │
        │ └──────────────────────┘   │
        │                            │
        │ VCC  GND  SCL  SDA   CSB  │
        └────────────────────────────┘
```

### Pinout

| Pin | Nom | Funció | Connecta a |
|:----|:----|:-------|:-----------|
| 1 | **VCC** | Alimentació (1.71V – 3.6V) | 3.3V de l'ESP32 |
| 2 | **GND** | Terra | GND de l'ESP32 |
| 3 | **SCL** | Rellotge I2C | GPIO22 de l'ESP32 |
| 4 | **SDA** | Dades I2C | GPIO21 de l'ESP32 |
| 5 | **CSB** | Chip Select (SPI) / SDO (I2C addr) | GND (per addr 0x76) o 3.3V (0x77) |

> ⚠️ **L'ordre dels pins depèn del fabricant de la breakout!** Mira sempre la serigrafia de la teva placa. L'ordre més comú és: **VCC, GND, SCL, SDA**.

### Característiques principals

| Propietat | Valor |
|:----------|:------|
| Rang de temperatura | -40°C a +85°C |
| Precisió temperatura | ±1.0°C (de 0°C a 65°C) |
| Rang humitat | 0% a 100% RH |
| Precisió humitat | ±3% RH (de 20% a 80%) |
| Rang pressió | 300 hPa a 1100 hPa |
| Precisió pressió | ±1.0 hPa (a 25°C / 950 hPa) |
| Protocol | **I2C** (fins 3.4 MHz) o SPI |
| Adreça I2C | **0x76** (CSB/SDO a GND) o **0x77** (a 3.3V) |
| Alimentació | 1.71V – 3.6V |
| Consum | ~0.5μA (standby), ~2.8μA (lectura) |

### Per què el BME280?

| Avantatge | Per què importa |
|:----------|:----------------|
| 🌡️ **3 en 1** | Temperatura + humitat + pressió en un sol sensor |
| 🔗 **I2C** | Només 2 pins (SDA + SCL) — pots connectar molts dispositius al mateix bus |
| 🔢 **Digital** | No cal ADC ni calibratge — les dades surten compensades |
| 💰 **Barat** | ~3€ per sensor, ideal per a l'aula |
| ⚡ **Baix consum** | Ideal per a projectes amb bateria |
| 📏 **Fàcil de cablejar** | 4 cables (VCC, GND, SDA, SCL), **sense resistències addicionals** |

### Comparativa: DS18B20 vs BME280

| Característica | DS18B20 | BME280 |
|:---------------|:--------|:--------|
| Temperatura | ✅ ±0.5°C | ✅ ±1.0°C |
| Humitat | ❌ | ✅ ±3% |
| Pressió | ❌ | ✅ ±1.0 hPa |
| Protocol | 1-Wire (1 pin) | I2C (2 pins) |
| Pull-up extern | ✅ 4.7kΩ obligatori | ❌ No cal (pull-ups interns ESP32) |
| Temps lectura | 750ms | ~5ms |
| Preu | ~2€ | ~3€ |

> 🎯 **Per a IoT educatiu, el BME280 guanya:** 3 sensors en 1, sense resistors extres, i lectures instantànies.

---

## 2️⃣ El protocol I2C

**I2C** (Inter-Integrated Circuit) és un protocol de comunicació sèrie que necessita **2 cables**: **SCL** (rellotge) i **SDA** (dades).

### Com funciona?

```
   ┌────── 3.3V ────────────────────────────┐
   │                                        │
   │  ┌─[Pull-up]──┐   ┌─[Pull-up]──┐      │
   │  │  (intern)  │   │  (intern)  │      │
   │  ├────┴─────┐ ├───┴──────┐ ├──┴─────┐ │
   │  │  ESP32   │ │ BME280   │ │ Altres │ │
   │  │ GPIO21   ├─┤ SDA      ├─┤ I2C    ├─┤
   │  │ GPIO22   ├─┤ SCL      ├─┤        ├─┤
   │  │ 3.3V     ├─┤ VCC      │ │        │ │
   │  │ GND      ├─┤ GND      │ │        │ │
   │  └──────────┘ └──────────┘ └────────┘ │
   └────────────────────────────────────────┘
```

### Com es diferencia del 1-Wire?

| Característica | 1-Wire (DS18B20) | I2C (BME280) |
|:---------------|:------------------|:--------------|
| Cables de dades | 1 (DATA) | 2 (SDA + SCL) |
| Rellotge | No (asíncron) | Sí (síncron) |
| Velocitat | ~16 kbps | 100-400 kbps (estàndard) |
| Dispositius per bus | Molts (ID únic 64 bits) | Fins 127 (adreça 7 bits) |
| Pull-up extern | Obligatori 4.7kΩ | Opcional (pull-ups interns ESP32) |
| Complexitat del driver | Bit-banging (temporització crítica) | Driver hardware (automàtic) |

### Per què l'ESP32 fa I2C millor que 1-Wire?

L'ESP32 té un **perifèric I2C dedicat** al hardware. Quan l'uses:

- ✅ El hardware gestiona els timings automàticament
- ✅ Pots llegir/qualsevol dispositiu I2C amb poques línies de codi
- ✅ L'ESP32 ja té pull-ups interns configurables
- ❌ El 1-Wire requereix **bit-banging** (temporització manual amb microsegons)

> 🎯 **Analogia:** I2C és com un **autobús amb horari** (SCL dona el ritme). 1-Wire és com un **carrer sense semàfors** (tothom va pel seu compte). I2C és més fàcil per a l'ESP32 perquè té el hardware específic.

### Com funciona la comunicació I2C?

```
┌───────────────── TRANSFERÈNCIA I2C ─────────────────┐
│                                                      │
│  START  │ ADREÇA(7) │ R/W │ ACK │ DADES(8) │ ACK │ STOP
│                                                      │
│  Exemple: Llegir temperatura del BME280              │
│                                                      │
│  ┌─────┐ ┌──────────┐ ┌──┐ ┌───┐ ┌──────┐ ┌───┐ ┌──┐
│  │ S   │ │ 0x76 (EC)│ │W │ │ A │ │0xF4  │ │ A │ │ P│
│  └─────┘ └──────────┘ └──┘ └───┘ └──────┘ └───┘ └──┘
│   (escriu al registre ctrl_meas per iniciar mesura)
│                                                   
│  ┌─────┐ ┌──────────┐ ┌──┐ ┌───┐ ┌────────┐ ┌───┐ ┌──┐
│  │ S   │ │ 0x76 (EC)│ │R │ │ A │ │0xF7..FC│ │ N │ │ P│
│  └─────┘ └──────────┘ └──┘ └───┘ └────────┘ └───┘ └──┘
│   (llegeix 6 bytes: pressió(3) + temperatura(3))
└──────────────────────────────────────────────────────┘
```

### L'adreça I2C

Cada dispositiu I2C té una adreça única al bus. El BME280 pot tenir:

| Pin CSB/SDO | Adreça I2C | 
|:------------|:-----------|
| Connectat a **GND** | **0x76** (per defecte) |
| Connectat a **3.3V** | **0x77** |

> Si només tens un BME280, deixa CSB sense connectar o a GND i l'adreça serà 0x76.

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
│  I2C: 2 controladors hardware        │
│  ADC: 2 × 12 bits (18 canals)        │
│  RAM: 520 KB                         │
│  Flash: 2 MB / 4 MB / 16 MB          │
│  Tensió: 3.3V                        │
└──────────────────────────────────────┘
```

### Pins I2C de l'ESP32

L'ESP32 té **2 controladors I2C** (I2C0 i I2C1). Els pins per defecte són:

| Controlador | SDA | SCL |
|:------------|:----|:----|
| **I2C_NUM_0** | GPIO21 | GPIO22 |
| I2C_NUM_1 | GPIO25 | GPIO26 |

> ✅ Al nostre projecte fem servir **I2C_NUM_0** amb **GPIO21 (SDA)** i **GPIO22 (SCL)**.

### Per què ESP32 i no Arduino Uno?

| Característica | ESP32 | Arduino Uno |
|:--------------|:------|:------------|
| WiFi | ✅ **Integrat** | ❌ Cal mòdul extern |
| I2C hardware | ✅ **2 controladors** | ✅ 1 controlador |
| Velocitat | 240 MHz | 16 MHz |
| RAM | 520 KB | 2 KB |
| Preu | ~5€ | ~3€ + mòdul WiFi (10€) |
| MQTT | ✅ Client nadiu | ❌ Cal biblioteca + ESP8266 |
| Pins | 34 GPIO | 14 GPIO |

> 🎯 **Analogia:** L'ESP32 és com un **mòbil barat** (ho té tot integrat). L'Arduino és com un **rellotge de polsera** (fa una cosa, però la fa bé). Per a IoT, l'ESP32 guanya.

---

## 4️⃣ Esquema de connexions complet

```
ESP32                      BME280 (breakout)
┌────────┐                ┌──────────────┐
│    3.3V├────────────────┤ VCC          │
│        │                │              │
│   GPIO21├───────────────┤ SDA          │
│   (SDA) │                │              │
│   GPIO22├───────────────┤ SCL          │
│   (SCL) │                │              │
│        │                │              │
│     GND├────────────────┤ GND          │
│        │                │              │
│        │                │ CSB ── GND   │
└────────┘                └──────────────┘
                           (addr: 0x76)
```

> ⚠️ **No calen resistències externes!** L'ESP32 té pull-ups interns que activem des del codi.

### Llista de materials

| Component | Quantitat | Preu aprox. |
|:----------|:----------|:------------|
| ESP32 (qualsevol model) | 1 | ~5€ |
| Sensor BME280 (breakout) | 1 | ~3€ |
| Cables Dupont (femella-femella) | 4 | ~0.50€ |
| Protoboard (opcional) | 1 | ~1€ |

**Total: ~9€ per alumne** (sense l'ESP32, que es pot reutilitzar)

---

## ✅ Resum

| Concepte | Què és? |
|:---------|:--------|
| **BME280** | Sensor ambiental: temperatura + humitat + pressió, protocol I2C |
| **I2C** | Protocol amb 2 cables (SDA + SCL), síncron, fins a 127 dispositius al bus |
| **GPIO21 / GPIO22** | Pins I2C per defecte de l'ESP32 (SDA / SCL) |
| **Adreça 0x76** | Adreça I2C del BME280 (si CSB/SDO està a GND) |
| **ESP32** | Microcontrolador amb WiFi integrat i 2 controladors I2C hardware |
| **ESP-IDF** | Framework oficial d'Espressif per programar l'ESP32 en C |
| **espressif/bme280** | Component oficial per al BME280 — s'instal·la automàticament |

A la pràctica següent ho muntaràs tot i veuràs les dades en acció! 🚀

# 🛠️ Pràctica: ESP32 + BME280 — Temperatura, humitat i pressió al teu sistema IoT

## Objectius

- Connectar físicament un sensor BME280 a un ESP32 per I2C
- Compilar i flashejar el firmware amb ESP-IDF
- Veure les dades (temperatura, humitat, pressió) publicar-se al broker MQTT
- Visualitzar les 3 magnituds a Node-RED i Grafana

---

## ⚙️ Abans de començar

### Materials necessaris

```
✅ ESP32 (qualsevol model)
✅ Sensor BME280 (breakout amb pins)
✅ 4 cables Dupont (femella-femella)
✅ (Opcional) Protoboard
```

> ❌ **No cal resistor pull-up extern** — l'ESP32 té pull-ups interns per I2C que activem des del codi.

### Programari a la VM

> 📖 Si encara no tens ESP-IDF instal·lat, segueix la **guia d'instal·lació**:
> 👉 [`../instalacio-esp-idf.md`](../instalacio-esp-idf.md)

```bash
# Comprova que tens el projecte
ls ~/esp/esp32-mqtt-temp/main/
# Hauries de veure: CMakeLists.txt  esp32-mqtt-temp.c  idf_component.yml

# Comprova que l'ESP32 es veu
ls /dev/ttyUSB*
# Hauria de sortir: /dev/ttyUSB0
```

### Contenidors en marxa

Assegura't que els contenidors Docker funcionen:

```bash
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Hauries de veure: `mqtt-broker`, `nodered-dashboard`, `influxdb`, `grafana`.

---

## 1️⃣ Connectar el BME280 a l'ESP32

### Cablejat

Connecta els cables **amb l'ESP32 desendollat** per evitar curtcircuits:

```
ESP32                    BME280
─────                    ──────

 Pin 3.3V ────────────── VCC   (alimentació)
 GPIO21  ────────────── SDA   (dades I2C)
 GPIO22  ────────────── SCL   (rellotge I2C)
 GND     ────────────── GND   (terra)
                       
 CSB     ────────────── GND   (adreça 0x76)
```

### Procediment pas a pas

1. Agafa el **BME280 breakout** i identifica els seus pins (mira la serigrafia)
2. Connecta **VCC** → al pin **3.3V** de l'ESP32
3. Connecta **GND** → al pin **GND** de l'ESP32
4. Connecta **SDA** → al pin **GPIO21** de l'ESP32
5. Connecta **SCL** → al pin **GPIO22** de l'ESP32
6. **(Opcional)** Connecta **CSB** → **GND** per assegurar adreça 0x76

```
          ┌─────────────────────────────┐
          │  Protoboard (opcional)      │
          │                             │
          │  BME280     ESP32           │
          │  ┌───┐      ┌───┐          │
          │  │VCC├──────┤3.3V│          │
          │  │SDA├──────┤21 │          │
          │  │SCL├──────┤22 │          │
          │  │GND├──────┤GND│          │
          │  │CSB├──────┤GND│          │
          │  └───┘      └───┘          │
          └─────────────────────────────┘
```

> ⚠️ **No necessites cap resistor!** L'ESP32 activa els pull-ups interns des del codi.

### Verificació visual

Un cop cablejat, connecta l'ESP32 al USB. El LED blau de l'ESP32 hauria de parpellejar breument (indicador d'arrencada).

---

## 2️⃣ El codi firmware

El codi ja està preparat al projecte `~/esp/esp32-mqtt-temp/`. Fem-hi un cop d'ull:

### Estructura del projecte

```
esp32-mqtt-temp/
├── CMakeLists.txt           → Configuració del projecte
├── sdkconfig                → Configuració de l'ESP-IDF
├── main/
│   ├── CMakeLists.txt       → Registra els fitxers font
│   ├── idf_component.yml    → Declara dependències (BME280, I2C bus)
│   └── esp32-mqtt-temp.c    → WiFi + MQTT + lectura del sensor
└── managed_components/      → Descarregat automàticament
    ├── espressif__bme280/   → Driver oficial del BME280
    └── espressif__i2c_bus/  → Driver I2C genèric
```

### Com es descarreguen les dependències?

El fitxer `main/idf_component.yml` declara les dependències:

```yaml
dependencies:
  espressif/bme280: '*'
```

Quan executes `idf.py build`, l'ESP-IDF:

1. Llegeix `idf_component.yml`
2. Descarrega `espressif/bme280` (i la seva dependència `espressif/i2c_bus`)
3. Els col·loca a `managed_components/`
4. Compila tot junt

> ✅ **No cal baixar res manualment!** L'ESP-IDF ho fa tot sol.

### Què fa el codi?

**`esp32-mqtt-temp.c`** — El programa principal:

| Tasca | Què fa |
|:------|:-------|
| `app_main()` | Inicialitza NVS, netif, **BME280**, WiFi, MQTT |
| `bme280_init_sensor()` | Crea bus I2C (GPIO21/22) + inicialitza BME280 |
| `wifi_init_sta()` | Connecta al WiFi amb IP fixa 192.168.0.201 |
| `mqtt_app_start()` | Connecta al broker MQTT (la VM) |
| `sensor_task()` | Cada 5s: llegeix BME280 + publica per MQTT |

### Configura que pots canviar

Al principi de `esp32-mqtt-temp.c`:

```c
#define WIFI_SSID        "el_teu_wifi"
#define WIFI_PASS        "la_teva_contrasenya"
#define MQTT_BROKER      "mqtt://192.168.0.57:1883"
#define MQTT_TOPIC       "alumne/aula/temperatura"

// Pins I2C per al BME280
#define I2C_MASTER_SCL   GPIO_NUM_22   // GPIO22 — SCL
#define I2C_MASTER_SDA   GPIO_NUM_21   // GPIO21 — SDA
```

> ℹ️ Si tens el sensor a uns pins I2C diferents, canvia `I2C_MASTER_SDA` i `I2C_MASTER_SCL` als GPIO correctes.

### L'API del BME280

La llibreria oficial `espressif/bme280` exposa funcions senzilles:

| Funció | Què fa |
|:-------|:-------|
| `bme280_create(bus, addr)` | Crea el handle del sensor |
| `bme280_default_init(sensor)` | Configura amb valors per defecte (mode normal) |
| `bme280_read_temperature(sensor, &temp)` | Temperatura en °C |
| `bme280_read_pressure(sensor, &press)` | Pressió en hPa |
| `bme280_read_humidity(sensor, &hum)` | Humitat relativa en % |

Els tres sensors es llegeixen de forma independent:

```c
float temperature, pressure, humidity;

bme280_read_temperature(bme280_sensor, &temperature);
bme280_read_pressure(bme280_sensor, &pressure);
bme280_read_humidity(bme280_sensor, &humidity);

// Resultat: temperature = 23.45°C
//           pressure    = 1013.25 hPa
//           humidity    = 55.2%
```

### Format del missatge MQTT

El JSON que s'envia al broker conté les 3 magnituds:

```json
{
  "temperatura": 23.45,
  "humitat": 55.20,
  "pressio": 1013.25,
  "unitats": "celsius|%|hPa",
  "counter": 0
}
```

---

## 3️⃣ Compilar el firmware

### Configurar l'entorn ESP-IDF

```bash
cd ~/esp/esp32-mqtt-temp
export IDF_PATH=~/esp/esp-idf
export PATH="$IDF_PATH/tools:$PATH"
export PATH="$HOME/.espressif/python_env/idf5.4_py3.11_env/bin:$PATH"
```

> 💡 Per no haver d'escriure això cada cop, pots crear un alias:
> ```bash
> alias get_idf='export IDF_PATH=~/esp/esp-idf && export PATH="$IDF_PATH/tools:$PATH" && export PATH="$HOME/.espressif/python_env/idf5.4_py3.11_env/bin:$PATH"'
> ```

### Compilar

```bash
cd ~/esp/esp32-mqtt-temp
idf.py build
```

Sortida esperada:
```
...
-- I2C_BUS: 1.5.2
-- BME280: 0.1.1
...
Project build complete. To flash, run:
 idf.py flash
```

> ⚠️ Si hi ha errors de compilació, llegeix el missatge d'error. Normalment són:
> - **Includes faltants** → afegeix `#include` al .c
> - **Tipus incorrectes** → comprova la declaració de la funció
> - **Dependències no trobades** → assegura't que tens connexió a Internet

---

## 4️⃣ Flashejar l'ESP32

Assegura't que l'ESP32 està connectat per USB i es veu a `/dev/ttyUSB0`:

```bash
ls /dev/ttyUSB*
# /dev/ttyUSB0
```

Flasheja el firmware:

```bash
idf.py -p /dev/ttyUSB0 flash --flash-mode dio --flash-freq 40m --flash-size 2MB
```

Sortida esperada:
```
...
Hash of data verified.
Hard resetting via RTS pin...
Done
```

> ⚠️ Si tens un ESP32 amb 2MB de flash, cal posar `--flash-mode dio --flash-freq 40m --flash-size 2MB`. Amb ESP32 de 4MB o 16MB, només `idf.py -p /dev/ttyUSB0 flash` és suficient.

---

## 5️⃣ Veure el monitor sèrie

Un cop flashejat, pots veure la sortida en temps real:

```bash
idf.py -p /dev/ttyUSB0 monitor
```

Hauries de veure:
```
I (1234) esp32-bme280: ✅ BME280 inicialitzat (I2C: SDA=GPIO21, SCL=GPIO22)
I (2345) esp32-bme280: 📡 IP fixa: 192.168.0.201
I (3456) esp32-bme280: ✅ WiFi connectat!
I (4567) esp32-bme280: ✅ MQTT: connectat al broker!
I (5678) esp32-bme280: 🌡️  Iniciant lectures del BME280...
I (5679) esp32-bme280: 📤 Enviat: 23.45°C / 55.20% / 1013.25hPa → alumne/aula/temperatura
I (10680) esp32-bme280: 📤 Enviat: 23.48°C / 55.10% / 1013.22hPa → alumne/aula/temperatura
```

Per sortir del monitor: `Ctrl + ]`

> ⚠️ **Errors típics:**
> - `❌ Error creant bus I2C` → Comprova el cablejat I2C (SDA/GPIO21, SCL/GPIO22)
> - `❌ Error inicialitzant BME280` → Comprova que el sensor rep 3.3V i que CSB està a GND
> - `WiFi: reintent N/10` → Comprova SSID i password
> - `MQTT: error` → Comprova que el broker Mosquitto estigui en marxa

---

## 6️⃣ Verificar que les dades arriben al broker

Des de la VM, subscriu-te al topic per veure les dades en directe:

```bash
docker exec mqtt-broker mosquitto_sub -h localhost -t "alumne/aula/temperatura"
```

Hauries de veure missatges cada 5 segons:
```json
{"temperatura": 23.45, "humitat": 55.20, "pressio": 1013.25, "unitats": "celsius|%|hPa", "counter": 0}
{"temperatura": 23.48, "humitat": 55.10, "pressio": 1013.22, "unitats": "celsius|%|hPa", "counter": 1}
{"temperatura": 23.38, "humitat": 55.30, "pressio": 1013.18, "unitats": "celsius|%|hPa", "counter": 2}
```

> Per aturar: `Ctrl + C`

---

## 7️⃣ Veure les dades a Node-RED i Grafana

### Node-RED

Obre al navegador (des de Windows o des de la VM):

```
http://192.168.0.57:1880
```

Afegeix un **MQTT input node** que escolti `alumne/aula/temperatura` i connecta'l a un **debug node** per veure les dades. Desglossa el JSON amb un **JSON parser** per separar temperatura, humitat i pressió.

O al dashboard (si tens el flow de temperatura):

```
http://192.168.0.57:1880/ui
```

### Grafana

```
http://192.168.0.57:3000
```

Si has configurat InfluxDB com a font de dades, les dades de l'ESP32 (temperatura, humitat i pressió) apareixeran als gràfics. Pots crear:

- 📊 **Gauge** de temperatura actual
- 📈 **Time series** de les 3 magnituds superposades
- 🎯 **Stat** amb humitat mínima/màxima

---

## 8️⃣ Prova sense WiFi (amb el monitor USB)

Si no tens WiFi disponible, pots veure les dades directament pel monitor sèrie:

```bash
idf.py -p /dev/ttyUSB0 monitor
```

El sensor llegirà temperatura, humitat i pressió encara que no es connecti a Internet — el WiFi és només per enviar les dades al broker.

---

## 9️⃣ Per explorar més (opcional)

1. **Canvia els pins I2C** — Connecta SDA/SCL a altres GPIO i actualitza la configuració
2. **Afegeix un segon BME280** — Canvia CSB a 3.3V per usar l'adreça 0x77 i connecta'l al mateix bus
3. **Millora la precisió** — Canvia el mostreig a `BME280_SAMPLING_X4` o `X8` per lectures més estables
4. **Altímetre** — El BME280 permet calcular l'altitud a partir de la pressió atmosfèrica
5. **IP automàtica** — Treu la IP fixa i deixa que el router assigni IP via DHCP

---

## ✅ Llista de verificació final

- [ ] **1** He connectat el BME280 a l'ESP32 (VCC→3.3V, GND→GND, SDA→GPIO21, SCL→GPIO22) ✅
- [ ] **2** He connectat CSB a GND (adreça I2C 0x76) ✅
- [ ] **3** He compilat el firmware amb `idf.py build` ✅
- [ ] **4** He flashejat l'ESP32 amb `idf.py -p /dev/ttyUSB0 flash` ✅
- [ ] **5** El monitor mostra les 3 lectures (temperatura, humitat, pressió) ✅
- [ ] **6** Les dades arriben al broker MQTT (`mosquitto_sub`) ✅
- [ ] **7** Puc veure les 3 magnituds a Node-RED / Grafana ✅

**🎉 Felicitats! Tens un sensor ambiental real connectat al teu sistema IoT!**

---

## ❓ Per a l'informe

1. Quina diferència hi ha entre el protocol **I2C** i el **1-Wire**? Quins avantatges té cadascun?
2. Per què el BME280 **no necessita** un resistor pull-up extern, a diferència del DS18B20?
3. Què significa l'adreça **0x76**? Per què cal connectar CSB a GND?
4. El BME280 mesura 3 magnituds. Podria l'ESP32 llegir-les alhora? Quina limitació del protocol I2C ho permet?
5. Si volguessis connectar 3 BME280 al mateix bus I2C, com ho faries? Quants en pots connectar com a màxim?

---

## 🧪 Exercici "fes-ho tu sol"

**Crea un programa que llegeixi el BME280 i publiqui les dades a 3 topics MQTT separats:**

- `alumne/aula/temperatura`
- `alumne/aula/humitat`
- `alumne/aula/pressio`

Pistes:
- Modifica el codi `esp32-mqtt-temp.c` per publicar 3 cops (un per topic)
- Cada missatge ha de ser un JSON senzill: `{"valor": 23.45, "unitat": "°C"}`
- Mantén el counter només al topic de temperatura

*(No hi ha solució donada — forma part de l'exercici!)*

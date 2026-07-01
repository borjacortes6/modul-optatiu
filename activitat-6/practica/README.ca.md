# 🛠️ Pràctica: ESP32 + DS18B20 — Temperatura real al teu sistema IoT

## Objectius

- Connectar físicament un sensor DS18B20 a un ESP32
- Compilar i flashejar el firmware amb ESP-IDF
- Veure la temperatura publicar-se al broker MQTT
- Visualitzar les dades a Node-RED i Grafana

---

## ⚙️ Abans de començar

### Materials necessaris

```
✅ ESP32 (qualsevol model)
✅ Sensor DS18B20
✅ Resistor 4.7kΩ (o 4.700Ω)
✅ 3 cables Dupont (femella-femella)
✅ (Opcional) Protoboard
```

### Programari a la VM

```bash
# Comprova que tens el projecte
ls ~/esp/esp32-mqtt-temp/main/
# Hauries de veure: CMakeLists.txt  ds18b20.c  ds18b20.h  esp32-mqtt-temp.c

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

## 1️⃣ Connectar el DS18B20 a l'ESP32

### Cablejat

Connecta els cables **amb l'ESP32 desendollat** per evitar curtcircuits:

```
ESP32                    DS18B20
─────                    ───────

 Pin 3.3V ────────────── VDD  (alimentació)
 GPIO4    ───[4.7kΩ]─── DATA (dades)
          │              ~~~
          └──────────────┤   (el mateix pin DATA!)
                         
 GND      ────────────── GND  (terra)
```

### Procediment pas a pas

1. Agafa el **DS18B20** i identifica els seus pins (mira la serigrafia)
2. Connecta **VDD** (3.3V) → al pin **3.3V** de l'ESP32
3. Connecta **GND** → al pin **GND** de l'ESP32
4. Connecta **DATA** → al pin **GPIO4** de l'ESP32
5. **Important:** Connecta el resistor **4.7kΩ** entre el cable DATA i el cable 3.3V (pull-up)

```
          ┌─────────────────────────────┐
          │  Protoboard (opcional)      │
          │                             │
          │  3.3V ──┬──[4.7kΩ]──┬────  │
          │         │           │      │
          │  GPIO4 ─┘           │      │
          │                     │      │
          │  GND ────────────── ┘      │
          └─────────────────────────────┘
```

> ⚠️ **Sense el resistor 4.7kΩ, el sensor NO funcionarà.** No te l'oblidis!

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
│   ├── ds18b20.h            → Capçalera del driver
│   ├── ds18b20.c            → Driver 1-Wire per DS18B20
│   └── esp32-mqtt-temp.c    → WiFi + MQTT + lectura del sensor
```

### Què fa el codi?

**`ds18b20.c`** — Implementa el protocol 1-Wire amb **bit-banging** (control manual dels temps):

| Funció | Què fa |
|:-------|:-------|
| `ds18b20_init(GPIO_NUM_4)` | Configura el pin GPIO4 per al sensor |
| `ds18b20_read_temp()` | Envia RESET → CONVERT → ESPERA → READ i retorna °C |

**`esp32-mqtt-temp.c`** — El programa principal:

| Tasca | Què fa |
|:------|:-------|
| `app_main()` | Inicialitza NVS, netif, DS18B20, WiFi, MQTT |
| `wifi_init_sta()` | Connecta al WiFi amb IP fixa 192.168.0.201 |
| `mqtt_app_start()` | Connecta al broker MQTT (la VM) |
| `temp_task()` | Cada 5s: llegeix sensor + publica per MQTT |

### Configura que pots canviar

Al principi de `esp32-mqtt-temp.c`:

```c
#define WIFI_SSID        "el_teu_wifi"
#define WIFI_PASS        "la_teva_contrasenya"
#define MQTT_BROKER      "mqtt://192.168.0.57:1883"
#define MQTT_TOPIC       "alumne/aula/temperatura"
#define DS18B20_GPIO     GPIO_NUM_4   // GPIO del sensor
```

> ℹ️ Si tens el sensor a un GPIO diferent, canvia `GPIO_NUM_4` al número correcte.

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
Project build complete. To flash, run:
 idf.py flash
```

> ⚠️ Si hi ha errors de compilació, llegeix el missatge d'error. Normalment són:
> - **Includes faltants** → afegeix `#include` al .c
> - **Tipus incorrectes** → comprova la declaració de la funció

---

## 4️⃣ Flashejar l'ESP32

Assegura't que l'ESP32 està connectat per USB i es veu a `/dev/ttyUSB0`:

```bash
ls /dev/ttyUSB*
# /dev/ttyUSB0
```

Flasheja el firmware:

```bash
cd ~/esp/esp32-mqtt-temp
idf.py -p /dev/ttyUSB0 flash
```

Sortida esperada:
```
...
Hash of data verified.
Hard resetting via RTS pin...
Done
```

---

## 5️⃣ Veure el monitor sèrie

Un cop flashejat, pots veure la sortida en temps real:

```bash
idf.py -p /dev/ttyUSB0 monitor
```

Hauries de veure:
```
I (1234) esp32-ds18b20: DS18B20 inicialitzat al GPIO 4
I (2345) esp32-ds18b20: 📡 IP fixa: 192.168.0.201
I (3456) esp32-ds18b20: ✅ WiFi connectat!
I (4567) esp32-ds18b20: ✅ MQTT: connectat al broker!
I (5678) esp32-ds18b20: 🌡️  Iniciant lectures del DS18B20...
I (5679) esp32-ds18b20: Temperatura: 23.45°C
I (5679) esp32-ds18b20: 📤 Enviat: 23.45°C → alumne/aula/temperatura
```

Per sortir del monitor: `Ctrl + ]`

> ⚠️ **Errors típics:**
> - `No s'ha detectat cap sensor al bus 1-Wire` → Comprova el cablejat, el resistor i el GPIO
> - `WiFi: reintent N/10` → Comprova SSID i password
> - `MQTT: error` → Comprova que el broker Mosquitto estigui en marxa

---

## 6️⃣ Verificar que les dades arriben al broker

Des de la VM, subscriu-te al topic per veure les dades en directe:

```bash
docker exec mqtt-broker mosquitto_sub -h localhost -t "alumne/aula/temperatura"
```

Hauries de veure missatges cada 5 segons:
```
{"temperatura": 23.45, "unitat": "celsius", "counter": 0}
{"temperatura": 23.50, "unitat": "celsius", "counter": 1}
{"temperatura": 23.38, "unitat": "celsius", "counter": 2}
```

> Per aturar: `Ctrl + C`

---

## 7️⃣ Veure les dades a Node-RED i Grafana

### Node-RED

Obre al navegador (des de Windows o des de la VM):

```
http://192.168.0.57:1880
```

Afegeix un **MQTT input node** que escolti `alumne/aula/temperatura` i connecta'l a un **debug node** per veure les dades.

O al dashboard (si tens el flow de temperatura):

```
http://192.168.0.57:1880/ui
```

### Grafana

```
http://192.168.0.57:3000
```

Si has configurat InfluxDB com a font de dades, les dades de l'ESP32 apareixeran als gràfics.

---

## 8️⃣ Prova sense WiFi (amb el monitor USB)

Si no tens WiFi disponible, pots veure la temperatura directament pel monitor sèrie:

```bash
idf.py -p /dev/ttyUSB0 monitor
```

El sensor llegirà temperatura encara que no es connecti a Internet — el WiFi és només per enviar les dades al broker.

---

## 9️⃣ Per explorar més (opcional)

1. **Canvia el GPIO** — Connecta el DS18B20 a un altre pin (GPIO2, GPIO5...) i canvia la configuració
2. **Afegeix un segon DS18B20** — El protocol 1-Wire permet múltiples sensors al mateix bus
3. **Resolució** — Canvia la resolució del sensor (12 bits → 9 bits per lectures més ràpides)
4. **IP automàtica** — Treu la IP fixa i deixa que el router assigni IP via DHCP

---

## ✅ Llista de verificació final

- [ ] **1** He connectat el DS18B20 a l'ESP32 (VCC→3.3V, GND→GND, DATA→GPIO4) ✅
- [ ] **2** He posat el resistor 4.7kΩ entre DATA i 3.3V (pull-up) ✅
- [ ] **3** He compilat el firmware amb `idf.py build` ✅
- [ ] **4** He flashejat l'ESP32 amb `idf.py -p /dev/ttyUSB0 flash` ✅
- [ ] **5** El monitor mostra "DS18B20 inicialitzat" i lectures de temperatura ✅
- [ ] **6** Les dades arriben al broker MQTT (`mosquitto_sub`) ✅
- [ ] **7** Puc veure la temperatura a Node-RED / Grafana ✅

**🎉 Felicitats! Tens un sensor de temperatura real connectat al teu sistema IoT!**

---

## ❓ Per a l'informe

1. Per què cal un resistor de 4.7kΩ al bus 1-Wire? Què passaria si no el poséssim?
2. Quina diferència hi ha entre un sensor analògic i un de digital (com el DS18B20)?
3. Per què l'ESP32 triga 750ms entre lectures de temperatura?
4. Què és el bit-banging i per què l'hem fet servir al driver `ds18b20.c`?
5. Si volguessis posar 5 sensors DS18B20 al mateix bus, com ho faries? Què cal canviar al codi?

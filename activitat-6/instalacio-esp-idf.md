# 🔧 Instal·lació de ESP-IDF per als alumnes

## Què és ESP-IDF?

**ESP-IDF** (Espressif IoT Development Framework) és el kit de desenvolupament oficial d'Espressif per programar els microcontroladors **ESP32** en **C**. Inclou:

- **Toolchain** (compilador creuat) per compilar C → binari ESP32
- **Llibreries oficials** (WiFi, MQTT, I2C, GPIO, etc.)
- **Eines de terminal** (`idf.py`) per compilar, flashejar i monitoritzar
- **Component Manager** per baixar llibreries (com `espressif/bme280`) automàticament

---

## 📋 Requisits de la VM

| Component | Mínim | Recomanat |
|:----------|:------|:----------|
| Disc dur | **8 GB** lliures | 15 GB |
| RAM | 2 GB | 4 GB |
| CPU | 2 nuclis | 4 nuclis |
| SO | Ubuntu 22.04 / 24.04 / 26.04 | Ubuntu 24.04 LTS |
| Internet | ✅ Imprescindible | — |

> ⚠️ La descàrrega ocupa ~1.5 GB. Amb el projecte compilat, caldran uns **3 GB** totals per a ESP-IDF.

---

## 1️⃣ Instal·lar dependències del sistema

Obre un terminal a la teva VM i executa:

```bash
sudo apt update
sudo apt install -y git wget flex bison gperf python3 python3-pip \
  python3-venv cmake ninja-build ccache libffi-dev libssl-dev \
  dfu-util libusb-1.0-0
```

> Això instal·la el **compilador, Python, CMake i eines USB** necessàries.

---

## 2️⃣ Descarregar ESP-IDF

```bash
mkdir -p ~/esp
cd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git -b v5.4
```

> 📦 **Descàrrega:** ~500 MB de codi font.
> ⏱ **Temps:** 1-5 minuts (depèn de la velocitat d'Internet).

Si la descàrrega s'interromp, pots continuar-la amb:

```bash
cd ~/esp/esp-idf && git pull --recurse-submodules
```

---

## 3️⃣ Instal·lar el toolchain

```bash
cd ~/esp/esp-idf
./install.sh esp32
```

> Això descarrega el **compilador creuat** (xtensa-esp32-elf-gcc), el **Python environment** i totes les eines necessàries.
>
> ⏱ **Temps:** 5-15 minuts.
> 📦 **Mida:** ~1 GB addicional.

Sortida esperada al final:
```
All done! You can now run:
  . ./export.sh
```

---

## 4️⃣ Clonar el projecte del professor

```bash
cd ~/esp
git clone https://github.com/borjacortes6/modul-optatiu.git
```

> Aquest repo conté la teoria i les pràctiques. El codi del firmware el tens a `~/esp/modul-optatiu/activitat-6/practica/`.

**Però el projecte ESP-IDF amb el codi C és independent.** El professor us donarà l'enllaç o el trobareu a les instruccions de la pràctica.

Per ara, crea un projecte de prova per verificar que tot funciona:

---

## 5️⃣ Verificar la instal·lació

### Prova amb un projecte nou

```bash
cd ~/esp
cp -r esp-idf/examples/get-started/hello_world .
cd hello_world
```

### Activar l'entorn ESP-IDF

```bash
cd ~/esp/hello_world
export IDF_PATH=~/esp/esp-idf
export PATH="$IDF_PATH/tools:$PATH"
export PATH="$HOME/.espressif/python_env/idf5.4_py3.11_env/bin:$PATH"
```

> 💡 Per no haver d'escriure això cada cop, crea un **alias**:
> ```bash
> alias get_idf='export IDF_PATH=~/esp/esp-idf && export PATH="$IDF_PATH/tools:$PATH" && export PATH="$HOME/.espressif/python_env/idf5.4_py3.11_env/bin:$PATH"'
> ```
>
> Afegeix-lo al final de `~/.bashrc` perquè es carregui automàticament:
> ```bash
> echo 'alias get_idf='\''export IDF_PATH=~/esp/esp-idf && export PATH="$IDF_PATH/tools:$PATH" && export PATH="$HOME/.espressif/python_env/idf5.4_py3.11_env/bin:$PATH"'\''' >> ~/.bashrc
> source ~/.bashrc
> ```

### Compilar

```bash
idf.py build
```

Sortida esperada:
```
...
Project build complete. To flash, run:
 idf.py flash
```

> ⏱ **Primera compilació:** 2-5 minuts (les següents són més ràpides gràcies a la cache).

---

## 6️⃣ (Opcional) Provar amb un ESP32

Si teniu l'ESP32 connectat per USB:

```bash
# Comprovar que el sistema el detecta
ls /dev/ttyUSB*

# Si no surt res, prova:
ls /dev/ttyACM*
```

Si detecta el dispositiu, flasheja i veu la sortida:

```bash
idf.py -p /dev/ttyUSB0 flash monitor
```

Sortida esperada:
```
Hello world!
This is esp32 chip with 2 CPU cores, WiFi/BLE...
Restarting in 10 seconds...
```

Per sortir del monitor: `Ctrl + ]`

---

## 🧹 Neteja (si todo funciona)

Un cop verificat, pots esborrar el projecte de prova:

```bash
cd ~/esp
rm -rf hello_world
```

---

## ❓ Resolució de problemes

### `git clone` falla per timeout

```bash
# Prova amb un clon superficial
git clone --depth 1 https://github.com/espressif/esp-idf.git -b v5.4
```

### `./install.sh` falla per espai

Allibera espai al disc:
```bash
# Neteja caché de apt
sudo apt clean
# Mira quant espai queda
df -h ~
```

### `idf.py build` no troba el toolchain

```bash
# Assegura't que l'entorn està activat
get_idf  # o source export.sh

# Reinstal·la el toolchain
cd ~/esp/esp-idf
./install.sh esp32
```

### `ls /dev/ttyUSB0` no apareix

Causes possibles:
- L'ESP32 no està connectat per USB
- El cable USB només porta alimentació (cal un cable amb dades)
- La VM no té el **USB passthrough** activat a VirtualBox

**A VirtualBox:**
1. Tanca el terminal de la VM
2. Ves a **Dispositius → USB** → Selecciona "USB Serial Converter (CP2102)" o "Silicon Labs CP210x"
3. Torna a obrir el terminal i prova `ls /dev/ttyUSB*`

> ⚠️ Si l'USB es desconnecta tot sol, a VirtualBox posa el controlador a **USB 1.1 (OHCI)** en comptes d'USB 2.0 o 3.0.

### Error: `Wrong flash size` al flashejar

Els ESP32 de **2MB** necessiten paràmetres especials:

```bash
idf.py -p /dev/ttyUSB0 flash --flash-mode dio --flash-freq 40m --flash-size 2MB
```

Els de **4MB o 16MB** funcionen amb el `idf.py -p /dev/ttyUSB0 flash` normal.

> 👀 **Com saber quina flash tens?** Quan connectes l'ESP32 i obres el monitor, el firmware mostra la mida de flash detectada automàticament.

---

## ✅ Resum de comandes útils

| Comanda | Què fa |
|:--------|:-------|
| `get_idf` | Activa l'entorn ESP-IDF (després de crear l'alias) |
| `idf.py build` | Compila el projecte |
| `idf.py -p /dev/ttyUSB0 flash` | Flasheja l'ESP32 |
| `idf.py -p /dev/ttyUSB0 monitor` | Mostra la sortida sèrie de l'ESP32 |
| `idf.py -p /dev/ttyUSB0 flash monitor` | Flasheja i obre monitor (seguit) |
| `idf.py clean` | Neteja fitxers compilats |
| `idf.py fullclean` | Neteja tot (inclou managed_components) |
| `idf.py reconfigure` | Torna a configurar (després de canviar `idf_component.yml`) |

---

## 📚 Referències

- [Documentació oficial ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/v5.4/)
- [Guia d'instal·lació pas a pas (en)](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32/get-started/index.html)
- [Componentes del registre oficial](https://components.espressif.com/)

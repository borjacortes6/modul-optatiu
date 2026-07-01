# 🛠️ Pràctica: Connectar la VM a la xarxa local (Bridge)

## Objectius

- Canviar la xarxa de la VM de **NAT** a **Bridge** a VirtualBox
- Comprovar que la VM obté una IP del rang de la LAN
- Utilitzar `ipconfig` a Windows per veure la IP de l'amfitrió
- Fer **ping** entre Windows i la VM per verificar connectivitat
- Accedir als serveis IoT (Node-RED, Grafana, InfluxDB) **des de Windows**

---

## Abans de començar

Assegura't que:

- ✅ La VM Ubuntu està **engegada** (dins VirtualBox)
- ✅ Tens els contenidors de l'activitat 3/4 funcionant:
  ```bash
  docker ps
  ```
  Hauries de veure: `mqtt-broker`, `nodered-dashboard`, `influxdb`, `grafana`

---

## 1️⃣ Canviar la xarxa de NAT a Bridge

Aquesta configuració es fa **des de l'amfitrió Windows**, NO dins la VM.

### Pas a pas a VirtualBox

1. **Apaga la VM** des del terminal de la VM:
   ```bash
   sudo shutdown now
   ```

2. Obre **VirtualBox** al Windows

3. Selecciona la teva VM (Ubuntu) → clic dret → **Configuración / Settings**

4. Ves a la pestanya **Red / Network**

5. Al **Adaptador 1**, canvia de:
   ```
   ❌ NAT
   ✅ Adaptador puente / Bridged Adapter
   ```

6. Al desplegable **Nombre / Name**, selecciona la teva targeta de xarxa:
   - Si usas **WiFi**: selecciona'l (ex: "Wi-Fi", "Realtek RTL8821CE", "Intel Wi-Fi 6")
   - Si usas **cable**: selecciona "Realtek PCIe GbE" o similar

   ```
   ┌──────────────────────────────────────────┐
   │  Adaptador puente                         │
   │  Nombre: [Realtek PCIe GbE Family... ▼]  │
   └──────────────────────────────────────────┘
   ```

7. Prem **Aceptar / OK**

8. **Engega la VM** des de VirtualBox

> ⚠️ Si la VM es queda sense internet després del canvi, prova amb un altre adaptador (WiFi vs cable).

---

## 2️⃣ Comprovar la nova IP de la VM

Quan la VM hagi arrencat, comprova la nova IP:

```bash
ip addr show | grep "inet "
```

Hauries de veure una IP com:

```
inet 192.168.0.xx/24 brd 192.168.0.255 scope global dynamic noprefixroute enp0s3
```

| Què veus? | Significat |
|:----------|:-----------|
| **192.168.0.xx** | La nova IP de la VM a la LAN |
| **/24** | Màscara 255.255.255.0 |
| **dynamic** | L'ha donada el router (DHCP) |
| **enp0s3** | La interfície de xarxa |

> 💡 **Guarda aquesta IP!** La faràs servir per connectar-te des de Windows.

Exemple: `192.168.0.57`

---

## 3️⃣ Trobar la IP de Windows amb `ipconfig`

Ara, des de **Windows**, obre un **Símbol del sistema (CMD)**:

```cmd
ipconfig
```

Busca la secció de la teva targeta de xarxa activa:

```
Adaptador de Ethernet (o WiFi):
   Dirección IPv4. . . . . . . . . . : 192.168.0.22
   Máscara de subred . . . . . . . . : 255.255.255.0
   Puerta de enlace predeterminada . .: 192.168.0.1
```

| Concepte | Valor teòric | A la teva xarxa |
|:---------|:-------------|:----------------|
| **IP Windows** | 192.168.0.xx | **192.168.0.22** |
| **Màscara** | 255.255.255.0 | 255.255.255.0 |
| **Gateway** | 192.168.0.1 | 192.168.0.1 |

### Comprova: estan a la mateixa xarxa?

- Windows: `192.168.0.22` → xarxa `192.168.0.0`
- VM: `192.168.0.57` → xarxa `192.168.0.0`
- ✅ **Sí!** Ambdós estan a la xarxa `192.168.0.0` → es poden comunicar

---

## 4️⃣ Prova de connectivitat: `ping`

El **ping** envia un paquet a un altre dispositiu i mesura quant triga a tornar. És la manera més bàsica de comprovar si dos dispositius es veuen a la xarxa.

### 4.1 Ping des de la VM cap a Windows

Des de la VM, fes ping al Windows:

```bash
ping 192.168.0.22
```

Exemple de sortida correcta:
```
PING 192.168.0.22 (192.168.0.22) 56(84) bytes of data.
64 bytes from 192.168.0.22: icmp_seq=1 ttl=128 time=1.25 ms
64 bytes from 192.168.0.22: icmp_seq=2 ttl=128 time=0.98 ms
--- 192.168.0.22 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss
```

> ❌ Si **no** reps resposta, pot ser que el firewall de Windows bloquegi el ping (ICMP). Prova el ping des de Windows cap a la VM.

### 4.2 Ping des de Windows cap a la VM

Des de **CMD al Windows**:

```cmd
ping 192.168.0.57
```

(on `192.168.0.57` és la IP de la teva VM)

Exemple de sortida correcta:
```
Haciendo ping a 192.168.0.57 con 32 bytes de datos:
Respuesta desde 192.168.0.57: bytes=32 tiempo=1ms TTL=64
Respuesta desde 192.168.0.57: bytes=32 tiempo=1ms TTL=64

Estadísticas de ping para 192.168.0.57:
    Paquetes: enviados = 2, recibidos = 2, perdidos = 0
```

| Resultat del ping | Què vol dir? |
|:------------------|:-------------|
| ✅ **Recibidos = 2** | La connexió funciona perfectament |
| ❌ **Perdidos = 2** | Firewall o problema de xarxa |

> 🔍 Si el ping falla, comprova:
> - Que el firewall de Windows estigui desactivat **temporalment** per provar
> - Que ambdós dispositius estiguin a la mateixa xarxa (mateix router)
> - Que la IP de la VM sigui correcta

---

## 5️⃣ Accedir als serveis IoT des de Windows

Ara que tens connectivitat, pots obrir els serveis de la VM **al navegador de Windows**.

### Node-RED (dashboard d'sensors)

Al navegador del Windows:

```
http://192.168.0.57:1880
```

| Què veuràs? | URL |
|:------------|:----|
| Editor de flows | `http://192.168.0.57:1880` |
| Dashboard (gauges) | `http://192.168.0.57:1880/ui` |

```
┌────────────────────────────────────────────┐
│                                            │
│   📊 NODE-RED DASHBOARD desde WINDOWS      │
│                                            │
│   ┌──────────────┐  ┌──────────────┐       │
│   │  Temperatura │  │   Humitat    │       │
│   │   ┌─────┐    │  │   ┌─────┐    │       │
│   │   │23.5 │    │  │   │ 65% │    │       │
│   │   └─────┘    │  │   └─────┘    │       │
│   │         Aula │  │        Aula  │       │
│   └──────────────┘  └──────────────┘       │
│                                            │
└────────────────────────────────────────────┘
```

### Grafana (dashboards històrics)

```
http://192.168.0.57:3000
```

**Login:** admin / admin123

### InfluxDB (base de dades)

```
http://192.168.0.57:8086
```

**Login:** admin / admin123

### Resum de connexions

| Servei | Port | URL des de Windows | Funció |
|:-------|:-----|:--------------------|:-------|
| **Node-RED** | 1880 | `http://192.168.0.57:1880` | Editor de flows |
| **Node-RED UI** | 1880 | `http://192.168.0.57:1880/ui` | Dashboard d'sensors |
| **Grafana** | 3000 | `http://192.168.0.57:3000` | Gràfics històrics |
| **InfluxDB** | 8086 | `http://192.168.0.57:8086` | Base de dades |
| **Mosquitto** | 1883 | `192.168.0.57:1883` | Broker MQTT |

> 💡 **Important:** Ara pots accedir als serveis **des de qualsevol dispositiu de la xarxa** (mòbil, tauleta) posant la mateixa URL.

---

## 6️⃣ Prova completa: tot funciona des de Windows

### Pas 1: Engega el publisher a la VM

```bash
cd ~/activitat-3
python3 publisher.py
```

### Pas 2: Des de Windows, obre Grafana

```
http://192.168.0.57:3000
```

Obre el dashboard **Sensors Aula 1** i posa autorefresh a 5s.

### Pas 3: Des de Windows, obre Node-RED Dashboard

```
http://192.168.0.57:1880/ui
```

**Compara les dues visualitzacions:**

| Eina | Què veus? | Com s'actualitza? |
|:-----|:-----------|:-----------------|
| 📊 Node-RED Dashboard | Gauges en directe (ara) | Automàtic (temps real) |
| 📈 Grafana | Gràfics de línies (evolució) | Cada 5s (autorefresh) |

### Pas 4: Des de Windows, obre InfluxDB

```
http://192.168.0.57:8086
```

Explora les dades guardades al bucket `sensors`.

---

## 7️⃣ Prova-ho des del mòbil (opcional)

Si estàs a la mateixa xarxa WiFi, obre al mòbil:

```
http://192.168.0.57:1880/ui
http://192.168.0.57:3000
```

> ⚠️ Si no funciona, comprova que el router permeti tràfic entre dispositius WiFi i cable (normalment sí).

---

## ✅ Llista de verificació final

- [ ] **1** He canviat la xarxa de la VM de NAT a Bridge a VirtualBox ✅
- [ ] **2** La VM té una IP del rang 192.168.0.x (`ip addr`) ✅
- [ ] **3** He trobat la IP de Windows amb `ipconfig` ✅
- [ ] **4** El **ping** funciona entre Windows i la VM ✅
- [ ] **5** Puc obrir Node-RED des de Windows (`http://192.168.0.xx:1880`) ✅
- [ ] **6** Puc obrir Grafana des de Windows (`http://192.168.0.xx:3000`) ✅
- [ ] **7** Puc obrir InfluxDB des de Windows (`http://192.168.0.xx:8086`) ✅
- [ ] **8** He provat des del mòbil (opcional) ✅

**🎉 Felicitats! La teva VM ja és un dispositiu més de la xarxa!**

---

## 🧪 Per explorar més (opcional)

1. **IP fixa (reservació DHCP)** — Configura al router perquè la VM sempre tingui la mateixa IP
2. **Més dispositius** — Connecta't des d'un mòbil o tauleta als dashboards
3. **Hostname** — Dona un nom a la VM per no haver de recordar la IP:
   ```bash
   sudo hostnamectl set-hostname ubuntu-iot
   ```
4. **Port forwarding** — Si algun dia tornes a NAT, pots accedir als serveis configurant port forwarding a VirtualBox

## ❓ Per a l'informe

1. Quina IP té la VM? I Windows? Estan a la mateixa xarxa? Com ho saps?
2. Quina diferència hi ha entre NAT i Bridge? Quan faries servir cada mode?
3. Què significa la màscara 255.255.255.0? Quants dispositius poden connectar-se a la mateixa xarxa?
4. El ping ha funcionat? Si no, què ha pogut passar?
5. Des de quins dispositius pots accedir als serveis IoT (Node-RED, Grafana) i per què?

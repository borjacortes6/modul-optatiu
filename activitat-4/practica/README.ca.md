# 🛠️ Pràctica: InfluxDB + Grafana — Emmagatzemar i visualitzar dades

## Objectius

- Afegir **InfluxDB** al teu sistema IoT per guardar dades de sensors
- Connectar **Node-RED** a InfluxDB per escriure-hi dades automàticament
- Configurar **Grafana** per crear dashboards històrics
- Veure l'evolució de la temperatura i la humitat en gràfics de línies

---

## Abans de començar

Assegura't que tens els contenidors de l'activitat 3 funcionant:

```bash
docker ps
```

Hauries de veure:
```
mqtt-broker         Up
nodered-dashboard   Up
```

Si no, engega'ls:

```bash
cd ~/activitat-3
docker compose up -d
```

---

## 1️⃣ Afegir InfluxDB + Grafana al docker-compose.yml

Obre el fitxer `docker-compose.yml`:

```bash
nano ~/activitat-3/docker-compose.yml
```

Afegeix els dos nous serveis **al final**, abans de l'última línia buida:

```yaml
  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    ports:
      - "8086:8086"
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: admin
      DOCKER_INFLUXDB_INIT_PASSWORD: admin123
      DOCKER_INFLUXDB_INIT_ORG: iot
      DOCKER_INFLUXDB_INIT_BUCKET: sensors
      DOCKER_INFLUXDB_INIT_RETENTION: 7d
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: elmeutoken
    volumes:
      - ./influxdb/data:/var/lib/influxdb2
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin123
    volumes:
      - ./grafana/data:/var/lib/grafana
    restart: unless-stopped
    depends_on:
      - influxdb
```

**Atenció als espais!** Han de tenir la mateixa indentació que els serveis `mosquitto` i `nodered` (2 espais).

Guarda i surt (`Ctrl+X`, `Y`, `Enter`).

### Explica què has afegit

| Servei | Imatge | Port | Funció |
|:-------|:-------|:-----|:-------|
| **influxdb** | `influxdb:2.7` | 8086 | Base de dades de sèries temporals |
| **grafana** | `grafana/grafana:latest` | 3000 | Dashboards i gràfics |

> El token `elmeutoken` el faràs servir més tard per connectar Node-RED i Grafana a InfluxDB.
> La contrasenya d'admin és `admin123` (en un entorn real la canviaries!).

---

## 2️⃣ Preparar directoris i engegar

Crea les carpetes necessàries:

```bash
mkdir -p ~/activitat-3/influxdb/data
mkdir -p ~/activitat-3/grafana/data
```

Dona permisos per evitar errors de permisos:

```bash
sudo chown -R 1000:1000 ~/activitat-3/influxdb/data
sudo chown -R 472:472 ~/activitat-3/grafana/data   # 472 = usuari grafana dins del contenidor
```

Ara engega els nous serveis:

```bash
cd ~/activitat-3
docker compose up -d
```

Espera uns 10–15 segons que arrenquin. Comprova que tot estigui `Up`:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Hauries de veure:
```
mqtt-broker         Up
nodered-dashboard   Up (healthy)
influxdb            Up
grafana             Up
```

> ⚠️ Si `influxdb` o `grafana` no arrenquen, pots mirar els logs amb `docker compose logs influxdb` o `docker compose logs grafana`.

---

## 3️⃣ Comprovar que InfluxDB funciona

Obre el navegador a la VM i ves a:

```
http://localhost:8086
```

Hauries de veure la pantalla d'inici d'InfluxDB. Ja hauria d'estar configurat automàticament (gràcies a les variables d'entorn):
- **Usuari:** `admin`
- **Password:** `admin123`
- **Organització:** `iot`
- **Bucket:** `sensors`
- **Token:** `elmeutoken`

Per comprovar-ho des del terminal:

```bash
# Llista buckets
docker exec influxdb influx bucket list --org iot --token elmeutoken
```

Hauries de veure:
```
ID                      Name            Retention       Shard group duration    Organization ID         Type
xxxxxxxxxxxxxxxxxxxx    sensors         168h0m0s        24h0m0s                 xxxxxxxxxxxxxxxxxxxx    user
```

> ✅ InfluxDB està llest per rebre dades!

---

## 4️⃣ Connectar Node-RED a InfluxDB

Node-RED necessita un node especial per connectar-se a InfluxDB. Instal·la'l:

```bash
docker exec nodered-dashboard npm install node-red-contrib-influxdb
```

Espera que s'instal·li. Quan acabi, reinicia Node-RED:

```bash
docker restart nodered-dashboard
```

Espera 10 segons que es reiniciï, després obre:

```
http://localhost:1880
```

Ara hauries de veure un nou node a la paleta esquerra: **influxdb out** (a la categoria **storage** o buscant "influx").

---

## 5️⃣ Actualitzar el flow de Node-RED

Ara has d'afegir un node **influxdb out** al teu flow perquè les dades es guardin automàticament a InfluxDB.

### Pas 1: Configurar el servidor InfluxDB

1. Arrossega un node **influxdb out** (categoria **storage**)
2. Dona-li **doble clic**
3. A **Server**, clica el botó ⊞ **Add new influxdb...**
4. Al camp **InfluxDB Version**, selecciona **2.0**
5. Configura:

| Camp | Valor |
|:-----|:------|
| **Name** | `InfluxDB` |
| **URL** | `http://influxdb:8086` |
| **Token** | `elmeutoken` |

6. Clica **Add**

> ⚠️ **Important:** Si els camps que veus són **Host, Port, Database, Username, Password** (en lloc d'URL, Token), és que el **Version** està en mode `1.x`. Canvia'l a **2.0**.

### Pas 2: Configurar el node influxdb out

Ara, al mateix node, configura:

| Camp | Valor |
|:-----|:------|
| **Name** | `Guardar temperatura` |
| **Organization** | `iot` |
| **Bucket** | `sensors` |
| **Measurement** | `temperatura` |

Deixa **Tag Name** i **Tag Value** buits.

Clica **Done**.

### Pas 3: Connectar-ho tot

Ara connecta els nodes d'aquesta manera:

```
📡 MQTT tempertura ──┬──→ 📊 gauge (temperatura)
                      │
                      └──→ 🗄️ influxdb out (Guardar temperatura)
```

Per fer-ho:
1. Fes clic a la sortida del **MQTT input** de temperatura
2. Arrossega un cable fins al node **influxdb out**
3. El cable es ramificarà automàticament (ja tens el gauge connectat)

> ⚠️ **No facis servir el cable antic!** Si treus el cable del gauge i el poses al influxdb, el gauge deixarà de rebre dades. Només cal afegir un **segon cable** des del MQTT input cap al influxdb.

### Pas 4: Repetir per a la humitat

1. Arrossega un altre **influxdb out**
2. Configura'l:
   - **Server**: selecciona `InfluxDB` (el que has creat abans)
   - **Name**: `Guardar humitat`
   - **Organization**: `iot`
   - **Bucket**: `sensors`
   - **Measurement**: `humitat`
3. Connecta'l a la sortida del **MQTT input d'humitat**

### Pas 5: Desplega

Clica **Deploy** (blau, dalt a la dreta).

Si tot va bé, no hauries de veure errors. Les dades ara es guarden automàticament a InfluxDB mentre el publisher estigui en marxa!

---

## 6️⃣ Prova que es guarden dades

Obre un terminal i executa el publisher:

```bash
cd ~/activitat-3
python3 publisher.py
```

Espera 10-15 segons perquè es publiquin unes quantes lectures, després obre **un altre terminal** i comprova InfluxDB:

```bash
# Consulta les dades de temperatura
docker exec influxdb influx query '
  from(bucket:"sensors")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "temperatura")
' --org iot --token elmeutoken
```

Hauries de veure alguna cosa com:
```
Result: _result
Table: keys: [_field, _measurement, aula]
           _time                  _value  _field  _measurement
 2024-01-15T10:00:03Z   25.3       valor   temperatura
 2024-01-15T10:00:06Z   24.7       valor   temperatura
 2024-01-15T10:00:09Z   26.8       valor   temperatura
```

Prova també amb la humitat:

```bash
docker exec influxdb influx query '
  from(bucket:"sensors")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "humitat")
' --org iot --token elmeutoken
```

> ✅ Si veus dades, InfluxDB està guardant correctament!

Atura el publisher amb `Ctrl+C`.

---

## 7️⃣ Configurar Grafana

Obre Grafana al navegador:

```
http://localhost:3000
```

**Login:**
- **Usuari:** `admin`
- **Contrasenya:** `admin123`

> ℹ️ La primera vegada et demanarà canviar la contrasenya. Pots saltar-ho (botó **Skip**).

### 7.1 Afegir InfluxDB com a font de dades

1. Al menú esquerre, ves a **Connections** → **Data Sources**
2. Clica **Add data source**
3. Busca i selecciona **InfluxDB**

Configura:

| Camp | Valor |
|:-----|:------|
| **Query Language** | **Flux** |
| **HTTP URL** | `http://influxdb:8086` |
| **Auth** | Deixa-ho per defecte (res) |
| **Organization** | `iot` |
| **Token** | `elmeutoken` |
| **Default Bucket** | `sensors` |

Clica **Save & test** (a baix a la dreta).

Hauries de veure un missatge verd: *"Data source is working"* ✅

### 7.2 Crear un dashboard de temperatura

1. Al menú esquerre, ves a **Dashboards**
2. Clica **New** → **New Dashboard**
3. Clica **Add visualization** (o el botó **+ Add** / **Add panel** que aparegui)
4. Al panell de la dreta, selecciona:
   - **Data source**: `InfluxDB` (el que acabes de crear)

> ⚠️ **Grafana v13:** Si no veus el botó **Add visualization**, busca un **+** a la barra superior o clica **Add** → **Visualization**.

**Query Language:** selecciona **Flux**

Al quadre de text de la query, escriu **cada línia per separat** (pitja Enter després de cada `|>`):

```flux
from(bucket: "sensors")
|> range(start: v.timeRangeStart, stop: v.timeRangeStop)
|> filter(fn: (r) => r._measurement == "temperatura")
```

> ⚠️ **Important:** Cada `|>` va en una **línia nova**. No ho posis tot seguit!

### 7.3 Configurar el panell

Un cop creada la visualització, a la **dreta** veuràs un panell amb pestanyes. A la pestanya **Field** (o **Standard options**), configura:

| Camp | Valor |
|:-----|:------|
| **Title** | `Temperatura Aula` |

Per l'escala i unitats:
- **Unit**: selecciona `Temperature > °C` (o escriu "celsius" al cercador)
- **Min**: `0`
- **Max**: `50`

> ⚠️ A la v13 de Grafana, aquestes opcions poden estar a **Field** → **Standard options** o al desplegable **Unit**. Si no veus "Min/Max", deixa-ho per defecte — el gràfic s'ajustarà automàticament.

### 7.4 Tornar al dashboard

Clica **Back to dashboard** (fletxa a dalt a l'esquerra).

### 7.5 Afegir panell d'humitat

1. Clica **Add** → **Visualization**
2. Selecciona `InfluxDB`
3. Query:

```flux
from(bucket: "sensors")
|> range(start: v.timeRangeStart, stop: v.timeRangeStop)
|> filter(fn: (r) => r._measurement == "humitat")
```

4. **Title**: `Humitat Aula`
5. **Unit**: `Percent (0-100)` (o escriu "percent")
6. **Min**: `0`, **Max**: `100`

### 7.6 Desar el dashboard

1. Clica la **icona de disquet** (📁) dalt de tot
2. **Dashboard name**: `Sensors Aula 1`
3. Clica **Save**

---

## 8️⃣ Veure-ho tot en acció!

Ara tens el sistema complet funcionant:

```
🌡️ publisher.py ──→ 📡 Mosquitto ──→ 🔧 Node-RED ──→ 🗄️ InfluxDB ──→ 📊 Grafana
                                            │
                                            └──→ 📊 Dashboard (gauges)
```

### Prova final

1. Obre Grafana al navegador: `http://localhost:3000`
2. Obre el dashboard **Sensors Aula 1**
3. En un terminal, executa el publisher:
   ```bash
   cd ~/activitat-3
   python3 publisher.py
   ```

Hauries de veure:
- 📊 **Grafana**: gràfics de línies que es van actualitzant cada cop que refresquis (F5)
- 🟠 **Node-RED** (`/ui`): gauges en directe

> ⚠️ Grafana **no s'actualitza sol** com Node-RED. Has de clicar el botó **Refresh** o posar un autorefresh (a dalt a la dreta, selecciona cada 5s o 10s).

### Compara les dues visualitzacions

| Eina | Què mostra? | Com s'actualitza? |
|:-----|:-----------|:-----------------|
| **Node-RED Dashboard** | Valor **ara** (gauge) | En temps real (automàtic) |
| **Grafana** | Evolució **històrica** (gràfic línies) | Manual o autorefresh cada X segons |

Atura el publisher amb `Ctrl+C`.

---

## 🎯 Tot funcionant!

```
📦 ECOSISTEMA IoT COMPLET:
────────────────────────
📡 Mosquitto   ──  Missatgeria MQTT
🔧 Node-RED    ──  Processament + Dashboard
🗄️ InfluxDB   ──  Base de dades temporal
📊 Grafana     ──  Dashboards històrics
```

**Has après a:**
- Configurar una base de dades de sèries temporals (InfluxDB)
- Connectar Node-RED a InfluxDB per guardar dades automàticament
- Crear dashboards professionals amb Grafana
- Comparar visualització en directe vs històrica

---

## ✅ Llista de verificació final

- [ ] **1** He afegit `influxdb` i `grafana` al `docker-compose.yml`
- [ ] **2** `docker compose up -d` engega els 4 contenidors ✅
- [ ] **3** Puc accedir a InfluxDB (`http://localhost:8086`) ✅
- [ ] **4** He instal·lat `node-red-contrib-influxdb` ✅
- [ ] **5** He afegit nodes `influxdb out` al flow ✅
- [ ] **6** Les dades es guarden a InfluxDB (ho he comprovat amb `influx query`) ✅
- [ ] **7** He configurat InfluxDB com a data source a Grafana ✅
- [ ] **8** Tinc un dashboard a Grafana amb temperatura i humitat ✅
- [ ] **9** Tot funciona: publisher → Mosquitto → Node-RED → InfluxDB → Grafana ✅

**🎉 Felicitats! Tens un sistema IoT complet amb emmagatzematge i visualització avançada!**

---

## 🧪 Per explorar més (opcional)

1. **Autorefresh a Grafana** — Configura'l perquè es refresqui cada 5s
2. **Alerta de temperatura** — Crea una alerta a Grafana si passa de 30°C
3. **Més sensors** — Afegeix pressió o lluminositat al publisher i al dashboard
4. **Variables de dashboard** — Crea un selector d'aula per filtrar les dades
5. **Docker Compose watch** — Afegeix `profiles` per no haver d'engegar-ho tot sempre

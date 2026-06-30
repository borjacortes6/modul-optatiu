# 🖥️ Pràctica 2: Instal·la Docker i prepara l'entorn IoT

**🎯 Objectiu:** Instal·lar Docker, Docker Compose i les eines Python per IoT al teu Ubuntu.

**⏱ Durada estimada:** 20-30 minuts

---

## 📋 Què necessites?

| 🔧 Requisit | 📝 Detall |
|:-----------|:----------|
| 💻 La teva VM Ubuntu | De l'Activitat 1 (engegada i funcionant) |
| 🌐 Connexió a Internet | Per descarregar els paquets |
| 💾 Disc lliure | 2 GB mínim |

> ⚠️ **Important:** Si no tens la VM de l'Activitat 1, fes-la primer!

---

## 🗺️ Mapa de la pràctica

```1️⃣  Accedir a la VM ──────────────── 🔌 SSH o finestra directa
        │
2️⃣  Actualitzar el sistema ────────── 🔄 sudo apt update
        │
3️⃣  Instal·lar Docker ─────────────── 🐳 docker.io
        │
4️⃣  Verificar Docker ──────────────── ✅ hello-world
        │
5️⃣  Afegir alumne al grup docker ─── 👤 sense sudo
        │
6️⃣  Instal·lar Docker Compose ─────── 🐙 docker-compose
        │
7️⃣  Instal·lar Python i paho-mqtt ── 🐍 pip3
        │
8️⃣  Prova de concepte ─────────────── 🎯 tot funciona!
```

---

## 1️⃣ Accedeix a la teva màquina virtual

Engega la VM de l'Activitat 1 i fes login:

```ubuntu-dev login: alumne
Password: ********

alumne@ubuntu-dev:~$ _     ← 🎉 Ja ets dins!
```

> 💡 **Consell:** Si vas configurar SSH (recomanat), pots connectar-te des del teu Windows/macOS:
> ```bash
> ssh alumne@10.0.2.15   # o la IP que tingui la teva VM
> ```

---

## 2️⃣ Actualitza el sistema

Abans d'instal·lar res, és bona pràctica actualitzar:

```bash
sudo apt update
```

Hauries de veure alguna cosa com:

```Hit:1 http://archive.ubuntu.com/ubuntu resolute InRelease
Hit:2 http://archive.ubuntu.com/ubuntu resolute-updates InRelease
Hit:3 http://security.ubuntu.com/ubuntu resolute-security InRelease
Reading package lists... Done
```

Ara actualitza els paquets instal·lats:

```bash
sudo apt upgrade -y
```

> ⏳ Això pot trigar uns minuts si fa temps que no actualitzes.

---

## 3️⃣ Instal·la Docker

Docker és als repositoris oficials d'Ubuntu. Instal·lar-lo és tan senzill com:

```bash
sudo apt install -y docker.io
```

La sortida serà llarga. Quan acabi, Docker ja estarà instal·lat.

``````
┌─────────────────────────────────────────────────────┐
│  ⏳ S'està instal·lant...                           │
│                                                     │
│  Setting up docker.io (20.10.24) ...                │
│  Created symlink /etc/systemd/system/... → ...      │
│                                                     │
│  ✅ Instal·lat!                                     │
└─────────────────────────────────────────────────────┘```

### ▶️ Engega Docker (si no ho ha fet sol)

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

> `enable` fa que Docker arrenqui sol quan engeguis la VM.
> `start` l'engega ara.

---

## 4️⃣ Verifica que Docker funciona

```bash
docker --version
```

Hauries de veure:

```Docker version 20.10.24+dfsg1, build 297e128```

Ara la prova definitiva:

```bash
sudo docker run hello-world
```

``````
────────────────────────────────────────────
Hello from Docker!
This message shows that your installation
appears to be working correctly.
────────────────────────────────────────────

✅ Docker funciona correctament!
```

> 🎉 Docker està instal·lat i funcionant! A la pràctica 3 veurem com crear contenidors de veritat.

---

## 5️⃣ Afegeix l'usuari al grup docker

Per evitar haver d'escriure `sudo` cada cop:

```bash
sudo usermod -aG docker $USER
```

**Important:** Tanca sessió i torna a entrar (o reinicia la VM):

```bash
exit
# ... i torna a fer login
```

> 💡 Si no surts de sessió, els canvis de grup no s'aplicaran. Pots provar `newgrp docker` si no vols sortir.

Ara prova **sense sudo**:

```bash
docker run hello-world
```

Si funciona sense `sudo` → ✅ **Perfecte!**

---

## 6️⃣ Instal·la Docker Compose

```bash
sudo apt install -y docker-compose
```

Verifica:

```bash
docker-compose --version
```

```docker-compose version 1.29.2, build unknown```

---

## 7️⃣ Instal·la Python i les eines MQTT

### Python 3 (ja ve amb Ubuntu)

```bash
python3 --version
```

```Python 3.11.x```

### pip (gestor de paquets Python)

```bash
sudo apt install -y python3-pip python3-venv
```

### paho-mqtt (per connectar-se a MQTT)

```bash
sudo apt install -y python3-paho-mqtt
```

Verifica:

```bash
python3 -c "import paho.mqtt.client; print('✅ paho-mqtt OK')"
```

---

## 8️⃣ Prova de concepte: tot funciona!

Executa aquesta bateria de proves d'un sol cop:

```bash
echo "=== 🐳 Prova Docker ==="
docker --version

echo ""
echo "=== 🐙 Prova Docker Compose ==="
docker-compose --version

echo ""
echo "=== 🐍 Prova Python ==="
python3 --version

echo ""
echo "=== 📡 Prova paho-mqtt ==="
python3 -c "import paho.mqtt.client; print('✅ OK')"

echo ""
echo "=== 🎯 Tot correcte! ==="
```

Hauries de veure **totes** les proves sense errors.

---

## ✅ Llista de verificació final

Marca les caselles quan hagis completat cada pas:

- [ ] **1** He fet `sudo apt update && sudo apt upgrade -y`
- [ ] **2** He instal·lat Docker: `sudo apt install -y docker.io`
- [ ] **3** `docker --version` mostra la versió ✅
- [ ] **4** `sudo docker run hello-world` funciona ✅
- [ ] **5** He afegit l'usuari al grup `docker`
- [ ] **6** `docker run hello-world` funciona **sense sudo** ✅
- [ ] **7** He instal·lat `docker-compose` i `docker-compose --version` funciona ✅
- [ ] **8** `python3 --version` mostra la versió ✅
- [ ] **9** `python3 -c "import paho.mqtt.client"` no dona error ✅
- [ ] **10** La bateria de proves final dona tot correcte ✅

**🎉 Enhorabona! Ja tens l'entorn IoT preparat!** A la pràctica 3 veurem com crear el primer contenidor.

---

## 🆘 Resolució de problemes

| 🔴 Problema | 🤔 Per què passa? | ✅ Solució |
|:-----------|:-----------------|:----------|
| ❌ **`E: Unable to locate package docker.io`** | No has fet `sudo apt update` abans | `sudo apt update` i després prova de nou |
| ❌ **`permission denied` al executar Docker** | L'usuari no és al grup docker | `sudo usermod -aG docker $USER` i reinicia sessió |
| ❌ **`Cannot connect to the Docker daemon`** | El servei Docker no està en marxa | `sudo systemctl start docker` |
| ❌ **Docker funciona amb `sudo` però no sense** | No vas reiniciar sessió després d'afegir-te al grup | Surt (`exit`) i torna a entrar a la VM |
| ❌ **`docker: command not found`** | Docker no s'ha instal·lat o la ruta no està al PATH | `sudo apt install -y docker.io` i `which docker` |
| ❌ **`Unable to locate package python3-paho-mqtt`** | No has fet `sudo apt update` | `sudo apt update && sudo apt install -y python3-paho-mqtt` |
| ❌ **`Failed to fetch http://archive.ubuntu.com/...`** | La VM no té connexió a Internet | Comprova la xarxa: `ping 8.8.8.8`. Si no funciona, revisa que la xarxa de la VM sigui NAT o Bridge |
| ❌ **Tot `apt install` falla** | No hi ha espai al disc | `df -h` per veure l'espai. Si està ple: `sudo apt autoremove` i `sudo apt clean` |
| ❌ **`python3 -c "import paho..."` dona error** | paho-mqtt no instal·lat | `sudo apt install -y python3-paho-mqtt` |

# 🖥️ Pràctica 1: Crea el teu entorn de treball virtual

**🎯 Objectiu:** Instal·lar VirtualBox al teu ordinador i crear una màquina virtual amb Ubuntu Linux, exactament com fem a classe.

**⏱ Durada estimada:** 45-60 minuts

---

## 📋 Què necessites?

| 🔧 Requisit | 📝 Detall |
|:-----------|:----------|
| 💻 Ordinador | Windows, macOS o Linux |
| 🌐 Internet | per descarregar els programes |
| 💾 Disc lliure | **10 GB** com a mínim |
| 🧠 RAM | **4 GB** (millor 8 GB) |
| 🧊 USB | per gravar la ISO (o arrenca directe) |

> 💡 **Si tens dubtes** en qualsevol pas, pregunta abans de seguir!

---

## 🗺️ Mapa de la pràctica

```
1️⃣  Instal·lar VirtualBox ──────────────────── 🔗 virtualbox.org
        │
2️⃣  Descarregar Ubuntu ─────────────────────── 🔗 ubuntu.com
        │
3️⃣  Crear la màquina virtual ───────────────── 🖱️ 3 clics
        │
4️⃣  Instal·lar Ubuntu dins la VM ───────────── 💿 ISO
        │
5️⃣  Instal·lar Guest Additions ─────────────── 🔧 millores
        │
6️⃣  Configurar el sistema ──────────────────── ⚙️ a punt!
```

---

## 1️⃣ Instal·lar Oracle VirtualBox

### 📥 Descarrega'l

**🔗 Enllaç directe:** [descarregar VirtualBox](https://www.virtualbox.org/wiki/Downloads)

Quan obris la web, veuràs una taula com aquesta:

```
┌─────────────────────────────────────────────┐
│  Oracle VirtualBox 7.2.8                    │
│                                             │
│  ▶ Windows hosts        ← clica aquí si     │
│  ▶ OS X hosts           ← ets Windows      │
│  ▶ Linux hosts          ← o aquí si ets    │
│  ▶ Solaris hosts        ← macOS/Linux      │
│                                             │
│  🔗 Extension Pack       ← descarrega      │
│                           també aquest!     │
└─────────────────────────────────────────────┘
```

**📦 Has de descarregar DÓS fitxers:**

| Fitxer | Per a què serveix |
|:-------|:-----------------|
| `VirtualBox-7.2.8-Win.exe` (si ets Windows) | El programa principal |
| `Oracle_VM_VirtualBox_Extension_Pack-7.2.8.vbox-extpack` | USB 3.0, xHCI, encriptació |

### 🛠️ Instal·lació

<details>
<summary><b>🪟 Si ets Windows — clica aquí</b></summary>

1. Fes doble clic a `VirtualBox-7.2.8-Win.exe`
2. **Següent → Següent → Següent** (tot per defecte)
3. Quan aparegui aquesta finestra:

```
┌──────────────────────────────────────────┐
│  ⚠️ Advertiment de Xarxa                │
│                                          │
│  Les interfícies de xarxa es           │
│  restabliran. Connexió a Internet       │
│  interrompuda momentàniament.           │
│                                          │
│        [ Sí ]     [ No ]                │
└──────────────────────────────────────────┘
```

👉 Clica **Sí** (no passa res, es reconnecta sol)

4. Finalitzar → **Finish**

</details>

<details>
<summary><b>🍏 Si ets macOS — clica aquí</b></summary>

1. Obre el fitxer `.dmg` descarregat
2. Fes doble clic al paquet `.pkg`
3. Segueix l'assistent
4. macOS et demanarà permís:

   **Preferències del Sistema → Seguretat i Privacitat → Permet**

</details>

<details>
<summary><b>🐧 Si ets Linux — clica aquí</b></summary>

```bash
# Des de la terminal:
sudo apt update
sudo apt install -y virtualbox-7.2
```

O, si has descarregat el `.deb`:

```bash
cd ~/Descàrregues
sudo dpkg -i VirtualBox-7.2*.deb
sudo apt install -f
```

</details>

### 📦 Instal·lar l'Extension Pack

Quan tinguis VirtualBox obert:

```
1. Obre VirtualBox
2. Menú → Fitxer → Eines → Gestor d'Extension Pack
3. Clica el botó ➕
4. Selecciona el fitxer .vbox-extpack que has descarregat
5. Accepta la llicència
```

✅ **Verifica que funciona:**

```bash
# Obre un terminal i escriu:
VBoxManage --version

# 👇 Hauries de veure alguna cosa com:
7.2.8r123456
```

---

## 2️⃣ Descarregar Ubuntu 26.04 LTS

**🔗 Enllaç directe:** [descarregar Ubuntu Server](https://ubuntu.com/download/server)

A la web, tria:

```
┌─────────────────────────────────────────────┐
│  Ubuntu 26.04 LTS                           │
│  Resolute Raccoon                           │
│                                             │
│  📥 Download Ubuntu Server     ← clica aquí │
│                                             │
│  💡 Alternative: Ubuntu Desktop             │
│     si vols escriptori gràfic               │
└─────────────────────────────────────────────┘
```

- **Ubuntu Server** (recomanat) — sense finestres, només terminal, consumeix pocs recursos
- **Ubuntu Desktop** — amb escriptori gràfic (més bonic, però gasta més RAM)

> ⚠️ **Important:** Desa la ISO a la carpeta `Descàrregues` o `Downloads` perquè la trobis fàcilment.

---

## 3️⃣ Crear la màquina virtual

### 🔌 Obre VirtualBox

Veuràs una pantalla com aquesta:

```
┌─────────────────────────────────────────────────────┐
│  Oracle VM VirtualBox Manager                       │
│  ─────────────────────────────────────────────      │
│  🔵 Nova   ⚙️ Configuració   ▶ Inicia                │
│  ┌────────────────────────────────────────────┐     │
│  │                                            │     │
│  │          ⭐ 'Benvingut a VirtualBox!'       │     │
│  │                                            │     │
│  │          Clica 'Nova' per començar         │     │
│  │                                            │     │
│  └────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

👉 **Clica el botó blau "Nova"** (o prem `Ctrl+N`)

### ✏️ Configura la VM

**Pas 1 — Nom i sistema:**

```
┌──────────────────────────────────────────────┐
│  Crear màquina virtual                       │
│                                              │
│  Nom:     [ Ubuntu 26.04 LTS              ] │ ← posa aquest nom
│  Carpeta: (deixa la que ve per defecte)     │
│  ISO:     [ ... ] 📁                      │ ← selecciona la ISO
│                                              │
│  ☐ Skip Unattended Installation             │
│                                              │
│  [↩ Enrere]           [▶ Següent]          │
└──────────────────────────────────────────────┘
```

**Pas 2 — RAM:**

```
┌──────────────────────────────────────────────┐
│  Mida de la memòria                         │
│                                              │
│   ───●─────────────────────────────────      │
│   1GB           4GB                    8GB   │
│       👆 arrossega fins aquí!                │
│                                              │
│  [↩ Enrere]           [▶ Següent]          │
└──────────────────────────────────────────────┘
```

👉 Arrossega el punt fins a **4096 MB** (4 GB)

**Pas 3 — Disc dur:**

```
┌──────────────────────────────────────────────┐
│  Disc dur                                   │
│                                              │
│  ○ No afegir disc virtual                    │
│  ● Crear un disc virtual ara                 │
│  ○ Usar un disc virtual existent             │
│                                              │
│  [↩ Enrere]           [▶ Següent]          │
└──────────────────────────────────────────────┘
```

👉 Deixa marcat **"Crear un disc virtual ara"**

```
┌──────────────────────────────────────────────┐
│  Tipus de disc                              │
│                                              │
│  ● VDI (VirtualBox Disk Image)               │ ← recomanat
│  ○ VMDK                                      │
│  ○ VHD                                       │
│                                              │
│  [↩ Enrere]           [▶ Següent]          │
└──────────────────────────────────────────────┘
```

```
┌──────────────────────────────────────────────┐
│  Tipus d'emmagatzematge                     │
│                                              │
│  ○ Mida fixa (ocupa tot ara)                 │
│  ● Reservat dinàmicament  ← millor opció!  │
│                                              │
│  [↩ Enrere]           [▶ Següent]          │
└──────────────────────────────────────────────┘
```

**Pas 4 — Mida del disc:**

```
┌──────────────────────────────────────────────┐
│  Mida del disc                              │
│                                              │
│   ───────────●─────────────────              │
│   4GB         25GB                   50GB    │
│               👆 25 GB són suficients        │
│                                              │
│  [↩ Enrere]           [▶ Finalitza]        │
└──────────────────────────────────────────────┘
```

### 📊 Resum de la configuració

| Paràmetre | Valor que has de posar |
|:-----------|:-----------------------|
| 🖥️ **Nom** | `Ubuntu 26.04 LTS` |
| 💿 **ISO** | La que has descarregat |
| 🧠 **RAM** | **4096 MB** (4 GB) |
| ⚡ **CPU** | **2 nuclis** |
| 💾 **Disc** | **25 GB** (dinàmic) |
| 🌐 **Xarxa** | NAT (ja ve per defecte) |

> 🛑 **ATENCIÓ:** Si no canvies la RAM a 4 GB, Ubuntu anirà molt lent.

---

## 4️⃣ Instal·lar Ubuntu a la VM

### ▶️ Engega la màquina

Selecciona la VM i clica el botó **▶ Iniciar** (verd).

La pantalla es transformarà en la finestra de la VM:

```
┌─── "Ubuntu 26.04 LTS" [En marxa] ──────┐
│                                         │
│    [🐧 Grub Menu]                       │
│                                         │
│    ▶ Try or Install Ubuntu              │
│      Ubuntu (safe graphics)             │
│      OEM install (for manufacturers)    │
│      Boot from next volume              │
│                                         │
│    Tria la primera opció i prem ENTER   │
│                                         │
└─────────────────────────────────────────┘
```

### 📝 Passos de la instal·lació

```
Pas 1: 🗣️  Idioma
┌─────────────────────────────────────┐
│  Tria: English                      │
└─────────────────────────────────────┘

Pas 2: ⌨️  Teclat
┌─────────────────────────────────────┐
│  Layout: Spanish                    │
│  Variant: Spanish / Catalan         │
└─────────────────────────────────────┘

Pas 3: 🌐  Xarxa
┌─────────────────────────────────────┐
│  Deixa per defecte (DHCP)          │
│  Hauries de veure una IP tipus     │
│  10.0.2.15 (xarxa NAT)             │
└─────────────────────────────────────┘

Pas 4: 🌍  Mirror
┌─────────────────────────────────────┐
│  Tria: Spain                        │
└─────────────────────────────────────┘

Pas 5: 💾  Disc
┌─────────────────────────────────────┐
│  Use an entire disk                 │
│  [📦 Ubuntu 26.04 LTS ...]         │
│                                     │
│  Marca: [x] Set up this disk       │
│                                     │
│  [Done]                             │
└─────────────────────────────────────┘

Pas 6: 👤  Crea l'usuari
┌─────────────────────────────────────┐
│  Your name: [ El teu nom        ]  │
│  Server name: [ ubuntu-dev      ]  │
│  Username: [ alumne            ]   │
│  Password: [ ********         ]    │
│  Confirm:  [ ********         ]    │
└─────────────────────────────────────┘

Pas 7: 🔑  SSH
┌─────────────────────────────────────┐
│  [x] Install OpenSSH server        │ ← marca això!
│                                     │
│  Import SSH identity: No            │
└─────────────────────────────────────┘

Pas 8: 📦  Snaps
┌─────────────────────────────────────┐
│  Pots deixar-ho sense res marcat   │
│  (o triar Docker si vols)          │
└─────────────────────────────────────┘
```

### ✅ Instal·lació completada!

Quan acabi, veuràs:

```
┌─────────────────────────────────────┐
│  ✅ Installation complete!          │
│                                     │
│  ▶ Reboot Now                       │ ← clica aquí!
└─────────────────────────────────────┘
```

**⚠️ Quan reiniciï, treu la ISO:**

1. A la barra de menú de la VM: **Dispositius → Optical Drives → Treure disc de la unitat**
2. O simplement prem **Enter** quan et demani *"Remove the installation medium"*

### 🎉 Primera connexió

```
Ubuntu 26.04 LTS ubuntu-dev tty1

ubuntu-dev login: alumne
Password: ********

alumne@ubuntu-dev:~$ _     ← 🎉 Ja ets dins!
```

---

## 5️⃣ Instal·lar les Guest Additions

> ✨ Les **Guest Additions** fan que tot funcioni millor: el ratolí es mou lliure, pots compartir carpetes, i la pantalla es redimensiona automàticament.

### 📀 Muntar el CD

A la barra de menú de la VM:

```
Dispositivos → Insert Guest Additions CD image...
```

Dins la VM, fes:

```bash
# 1. Instal·la les eines necessàries
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r)

# 2. Munta el CD
sudo mount /dev/cdrom /mnt

# 3. Executa l'instal·lador
cd /mnt
sudo sh ./VBoxLinuxAdditions.run --nox11

# 4. Reinicia
sudo reboot
```

✅ **Comprova que funciona:**

```bash
alumne@ubuntu-dev:~$ lsmod | grep vbox

# 👇 Hauries de veure:
vboxguest  524288  4
vboxsf     28672   1
vboxvideo  40960   0
```

> 💡 **Consell:** Si després configures carpetes compartides, apareixeran a `/media/sf_<nom_carpeta>`. Per accedir-hi:
> ```bash
> sudo usermod -aG vboxsf $USER
> ```
> Tanca sessió i torna a entrar.

### 📋 Copiar i enganxar entre el teu ordinador i la VM

Un cop tens les Guest Additions instal·lades, activar el porta-retalls compartit és molt fàcil:

**Pas 1 — Tanca la VM (apaga-la)**

```bash
sudo poweroff
```

**Pas 2 — Configura el porta-retalls a VirtualBox**

Selecciona la VM (sense engegar-la) i ves a:

```
┌──────────────────────────────────────────────┐
│  VM → Configuració → General                  │
│                                               │
│  ┌───────────────────────────────────────┐   │
│  │  General │ Sistema │ Pantalla │ ...   │   │
│  └───────────────────────────────────────┘   │
│                                               │
│  Ves a la pestanya:                           │
│  ┌───────────────────────────────────────┐   │
│  │  Bàsic │ Avançat │ Descripció │       │   │
│  │                                         │   │
│  │  ☑ Porta-retalls compartit:            │   │
│  │     [Bidireccional              ▼]     │   │
│  │             ┌───────────────┐           │   │
│  │             │ Desactivat    │           │   │
│  │             │ Des del host  │           │   │
│  │             │ Des del guest │           │   │
│  │             │ ✅Bidireccional│ ← tria  │   │
│  │             └───────────────┘  aquest! │   │
│  │                                         │   │
│  │  ☑ Arrossegar i soltar:                │   │
│  │     [Bidireccional              ▼]     │   │
│  └───────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

👉 Tria **Bidireccional** a les dues opcions.

**Pas 3 — Engega la VM i prova-ho**

```bash
# A l'Ubuntu, copia alguna cosa:
echo "Hola des d'Ubuntu!" | tee /tmp/prova.txt
cat /tmp/prova.txt   # selecciona el text amb el ratolí
```

Ara, a **Windows/macOS/Linux (host)**: prem `Ctrl+V` (o `Cmd+V`) i enganxa el text.

**Prova també al revés:** copia text del teu ordinador i enganxa'l dins de la VM.

> ✅ **Funciona!** Ja pots copiar codi de les pràctiques al teu ordinador i enganxar-lo a la VM sense escriure-ho a mà.

---

## 6️⃣ Configuració final

### 🔄 Actualitza el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 🏷️ Canvia el nom del teu ordinador

```bash
sudo hostnamectl set-hostname ubuntu-dev
```

### 🛠️ Eines útils

```bash
sudo apt install -y htop neofetch git curl wget tree
```

Prova `neofetch` per veure informació del teu sistema:

```
alumne@ubuntu-dev:~$ neofetch
       .-/+oossssoo+/-.               alumne@ubuntu-dev
   `:+ssssssssssssssssss+:`           -----------------
 -:+ssssssssssssssssssyssss+-         OS: Ubuntu 26.04 LTS
.osssssssssssssssssssssssssssso.      Kernel: 7.0.0-22-generic
.osssssssssssssssssssssssssssso.      Uptime: 5 mins
:+ssssssssssssssssssssssssssssss+:    Packages: 345
:+ssssssssssssssssssssssssssssss+:    Shell: bash 5.2
 -:+ssssssssssssssssssssssssss:-      CPU: Intel i3-10110U (2) @ 2.1GHz
   .-/+oossssoo+/-.                   Memory: 521MiB / 3.3GiB
```

### 🔐 Clau SSH per GitHub (opcional)

```bash
ssh-keygen -t ed25519 -C "alumne@ubuntu-dev"
cat ~/.ssh/id_ed25519.pub
```

👉 Copia el text que surti i afegeix-lo a [github.com/settings/keys](https://github.com/settings/keys)

### 💾 Swap si tens poca RAM (opcional)

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## ✅ Llista de verificació final

Marca les caselles quan hagis completat cada pas:

- [ ] **1** VirtualBox instal·lat
- [ ] **2** Extension Pack instal·lat
- [ ] **3** Ubuntu ISO descarregada
- [ ] **4** VM creada amb 4 GB RAM + 2 nuclis + 25 GB disc
- [ ] **5** Ubuntu instal·lat dins la VM
- [ ] **6** Guest Additions instal·lades
- [ ] **7** `sudo apt update && sudo apt upgrade` fet
- [ ] **8** Copiar i enganxar funciona (Bidireccional)
- [ ] **9** Pots fer `neofetch` i veure informació del sistema

**🎉 Enhorabona! Tens un entorn de treball Ubuntu complet!**

---

## 🆘 Resolució de problemes

| 🔴 Problema | 🤔 Per què passa? | ✅ Solució |
|:-----------|:-----------------|:----------|
| ❌ **"VT-x is not available"** | La virtualització està desactivada a la BIOS | Reinicia l'ordinador, entra a la BIOS (F2/F10/DEL) i activa **Intel VT-x** o **AMD-V** |
| ❌ **La VM no arrenca** | L'ordre d'arrencada no prioritza el CD | VM → Configuració → Sistema → Marca "CD/DVD" primer |
| ❌ **Ratolí tancat dins la finestra** | Guest Additions no instal·lades | Ves a la Part 5 i instal·la-les |
| ❌ **No veig la carpeta compartida** | No ets del grup vboxsf | `sudo usermod -aG vboxsf $USER` i reinicia sessió |
| ❌ **Tot va molt lent** | Poca RAM assignada | Augmenta la RAM a 4 GB (o més) |
| ❌ **No puc fer SSH** | Xarxa en NAT | Canvia a **Bridge** a Configuració → Xarxa |
| ❌ **No puc copiar i enganxar** | Porta-retalls no configurat o Guest Additions no instal·lades | 1️⃣ Instal·la Guest Additions (Part 5), 2️⃣ VM → Configuració → General → Avançat → **Bidireccional** |
| ❌ **La pantalla es veu petita** | Guest Additions no instal·lades | Part 5 — instal·la les Guest Additions |
| ❌ **No recordo la contrasenya** | Error humà | Millor tornar a crear la VM (són 15 minuts) |

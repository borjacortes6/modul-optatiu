# Pràctica 1: Instal·lació de VirtualBox i creació d'una VM amb Ubuntu

**Objectiu:** Instal·lar Oracle VirtualBox a l'ordinador amfitrió i crear una màquina virtual amb Ubuntu 26.04 LTS.

**Durada estimada:** 45-60 minuts

---

## Requisits previs

- Ordinador amb **Windows, macOS o Linux**
- Connexió a Internet
- Almenys **10 GB d'espai lliure** al disc dur
- Almenys **4 GB de RAM** (8 GB recomanats)

---

## Part 1: Instal·lar Oracle VirtualBox

### 1.1 Descarregar VirtualBox

1. Obre el navegador i ves a: https://www.virtualbox.org/wiki/Downloads
2. Selecciona el paquet corresponent al teu sistema operatiu amfitrió:

| Sistema amfitrió | Paquet a descarregar |
|-----------------|----------------------|
| Windows         | `VirtualBox-7.2.8-123456-Win.exe` |
| macOS           | `VirtualBox-7.2.8-123456-OSX.dmg` |
| Linux Ubuntu    | `VirtualBox-7.2.8-123456-Ubuntu-jammy_amd64.deb` |
| Linux Fedora    | `VirtualBox-7.2.8-123456-Fedora-38.x86_64.rpm` |

> ✅ **Consell:** Descarrega també el *Extension Pack* (`Oracle_VM_VirtualBox_Extension_Pack-7.2.8.vbox-extpack`) de la mateixa pàgina. Afegeix suport per USB 3.0, xHCI i encriptació de discs.

### 1.2 Instal·lar VirtualBox

**A Windows:**
- Executa l'instal·lador `.exe`
- Segueix l'assistent (deixa tot per defecte)
- Quan et pregunti sobre *Network Interfaces*, fes clic a **Instal·lar** (la xarxa es tallarà moments)

**A macOS:**
- Obre el fitxer `.dmg`
- Fes doble clic al paquet `.pkg` i segueix la instal·lació
- Concedeix els permisos de seguretat si macOS ho demana (Preferències del Sistema → Seguretat i Privacitat)

**A Linux Ubuntu/Debian:**
```bash
# Instal·lar dependències
sudo apt update
sudo apt install -y wget build-essential

# Instal·lar VirtualBox des del .deb descarregat
cd ~/Descàrregues
sudo dpkg -i VirtualBox-7.2*.deb
sudo apt install -f   # resol dependències pendents

# O bé afegir el repositori oficial per rebre actualitzacions automàtiques:
wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc | sudo gpg --dearmor -o /usr/share/keyrings/oracle-vbox.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-vbox.gpg] https://download.virtualbox.org/virtualbox/debian $(lsb_release -sc) contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list
sudo apt update
sudo apt install -y virtualbox-7.2
```

### 1.3 Instal·lar l'Extension Pack

```bash
# Des del terminal (Linux/macOS):
VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-7.2.8.vbox-extpack

# A Windows: Obre VirtualBox → Fitxer → Eines → Gestor d'Extension Pack
# o fes doble clic al fitxer .vbox-extpack
```

**Verificació:**
```bash
VBoxManage --version
# Sortida esperada: 7.2.8r123456 (o similar)
```

---

## Part 2: Descarregar Ubuntu 26.04 LTS

1. Ves a: https://ubuntu.com/download/server
2. Descarrega la imatge ISO de **Ubuntu 26.04 LTS (Server)** o **Desktop** segons les teves necessitats
3. Guarda-la en un lloc on la trobis fàcilment (p. ex. `~/Descàrregues/` o `~/Downloads/`)

> ⚠ **Nota:** Per a entorns de desenvolupament IoT i servidors, la versió **Server** (sense entorn gràfic) és suficient i consumeix menys recursos.

---

## Part 3: Crear la màquina virtual

### 3.1 Configuració inicial

Obre VirtualBox i fes clic a **Nova** (o `Ctrl+N`).

- **Nom:** `Ubuntu 26.04 LTS`
- **Carpeta:** (deixa la que ve per defecte)
- **ISO Image:** Selecciona el fitxer `.iso` descarregat
- **Tipus:** Linux
- **Versió:** Ubuntu (64-bit)

Paràmetres recomanats:

| Paràmetre | Valor | Notes |
|-----------|-------|-------|
| **RAM** | 4096 MB (4 GB) | Mínim 2048 MB |
| **CPU** | 2 nuclis | Mínim 1, màxim ½ dels nuclis físics |
| **Disc dur** | 25-50 GB | Mida dinàmica recomanada |
| **VRAM** | 16-128 MB | Més per a Desktop env. gràfic |
| **Xarxa** | NAT | Per defecte, es pot canviar a Bridge més tard |
| **Controlador** | SATA | Per defecte |

### 3.2 Configurar les xarxes

**NAT (per defecte):**
- La VM comparteix l'adreça IP del host
- La VM pot accedir a Internet
- El host NO pot accedir directament a la VM (cal redirecció de ports)

**Bridge (per a accés directe a la LAN):**
- La VM obté una IP pròpia al router (ex: 192.168.1.x)
- El host pot connectar-se a la VM (SSH, servidors)
- Configuració: VM → Configuració → Xarxa → Mode: `Aurat`

### 3.3 Configurar la carpeta compartida (opcional)

Després d'instal·lar les Guest Additions (Part 5), es pot crear una carpeta compartida:

1. VM → Configuració → Carpetes Compartides
2. Clica la icona de carpeta amb el signe `+`
3. Selecciona una carpeta del host (ex: `~/compartit`)
4. Activa **Muntatge Automàtic** i **Permanent**

### 3.4 Configurar la memòria de vídeo

- Per a Ubuntu **Server** (sense escriptori): 16 MB són suficients
- Per a Ubuntu **Desktop**: 128 MB (o almenys 64 MB)

---

## Part 4: Instal·lar Ubuntu a la VM

### 4.1 Iniciar la instal·lació

1. Selecciona la VM i fes clic a **Inicia** (verd)
2. La VM arrencarà des de la ISO d'Ubuntu
3. Selecciona l'idioma (català o anglès)

### 4.2 Passos de la instal·lació (Ubuntu Server)

| Pas | Acció |
|-----|-------|
| **Idioma** | Selecciona l'idioma de la instal·lació |
| **Teclat** | Tria la disposició: `Spanish` o `Catalan` |
| **Xarxa** | Deixa per defecte (DHCP) |
| **Mirror** | Selecciona el país més proper per al repositori de paquets |
| **Disc** | `Use entire disk` (el disc de la VM) |
| **Perfil** | Introdueix: nom, nom d'usuari (`vboxuser` o el que prefereixis), contrasenya |
| **SSH** | Activa `Install OpenSSH server` per gestionar-la remotament |
| **Snaps** | Selecciona els que necessitis (o cap per a una instal·lació mínima) |

### 4.3 Finalitzar i reiniciar

1. Quan la instal·lació acabi, selecciona **Reboot**
2. La VM et demanarà d'expulsar la ISO (Ctrl+D o des de: Dispositius → Optical Drives → Treure disc de la unitat)

### 4.4 Primera connexió

Inicia sessió amb l'usuari i contrasenya que vas crear:

```bash
# Connexió local (des de la consola de VirtualBox)
Ubuntu 26.04 LTS ubuntu tty1
ubuntu login: vboxuser
Password: 
```

```bash
# Connexió remota per SSH (si tens la xarxa en Bridge)
# Des del host:
ssh vboxuser@<IP-de-la-VM>
```

---

## Part 5: Instal·lar les Guest Additions

Les *Guest Additions* milloren la integració entre el host i el guest: ratolí lliure, portaretalls compartit, carpetes compartides, i redimensionament automàtic de la pantalla.

### 5.1 Muntar la ISO de Guest Additions

Des de la finestra de la VM:
- Dispositius → Insert Guest Additions CD image...

### 5.2 Instal·lar al guest

Dins de la VM:

```bash
# Instal·lar dependències
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r)

# Muntar el CD (si no s'ha muntat automàticament)
sudo mount /dev/cdrom /mnt

# Executar l'instal·lador
cd /mnt
sudo sh ./VBoxLinuxAdditions.run --nox11

# Reiniciar
sudo reboot
```

**Verificació:**
```bash
# Comprovar que els mòduls estan carregats
lsmod | grep vbox
# Sortida: vboxguest, vboxsf, vboxvideo
```

> ✅ A partir d'aquí, si configures carpetes compartides al host, apareixeran a `/media/sf_<nom_carpeta>` a la VM (cal que l'usuari sigui del grup `vboxsf`).

---

## Part 6: Configuració post-instal·lació

### 6.1 Actualitzar el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 6.2 Configurar el nom de la màquina (hostname)

```bash
sudo hostnamectl set-hostname ubuntu-dev
# Comprovar:
hostnamectl
```

### 6.3 Millorar la consola (opcional)

```bash
sudo apt install -y htop neofetch git curl wget tree
neofetch  # mostra informació del sistema
```

### 6.4 Configurar clau SSH (opcional)

```bash
ssh-keygen -t ed25519 -C "vboxuser@ubuntu-dev"
cat ~/.ssh/id_ed25519.pub
# Afegeix aquesta clau al teu GitHub/GitLab per pujar codi sense contrasenya
```

### 6.5 Assignar memòria swap (si cal)

```bash
# Si tens poca RAM (4 GB o menys), afegeix 2 GB de swap:
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
# Fer-lo permanent:
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Verificació final

```bash
echo "=== Sistema ==="
uname -a
echo "=== Memòria ==="
free -h
echo "=== Disc ==="
df -h /
echo "=== VirtualBox ==="
lsmod | grep -E 'vboxguest|vboxsf'
echo "=== Usuari ==="
whoami
echo "=== Xarxa ==="
ip addr show | grep inet
```

---

## Resolució de problemes

| Problema | Causa probable | Solució |
|----------|---------------|---------|
| La VM no arrenca des de la ISO | Ordre d'arrencada incorrecte | VM → Configuració → Sistema → Marca "CD/DVD" primer |
| "VT-x is not available" | Virtualització desactivada a la BIOS | Reinicia el host, entra a la BIOS/UEFI i activa Intel VT-x / AMD-V |
| No es veu el ratolí dins la guest | Guest Additions no instal·lades | Instal·la les Guest Additions com a la Part 5 |
| La carpeta compartida no es veu | Usuari no al grup vboxsf | `sudo usermod -aG vboxsf $USER` i reinicia sessió |
| La VM es penja | Poca RAM assignada | Augmenta la RAM a 4096 MB a la configuració de la VM |
| No hi ha so | Controlador d'àudio incorrecte | VM → Configuració → Àudio → Controlador: Intel HD Audio |
| SSH no connecta | Xarxa en NAT o tallafocs | Canvia a Bridge o afegeix redirecció de ports |
| No es pot redimensionar la pantalla | Guest Additions no instal·lades o sessió gràfica | Verifica `lsmod | grep vboxvideo` |

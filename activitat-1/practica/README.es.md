# Práctica 1: Instalación de VirtualBox y creación de una VM con Ubuntu

**Objetivo:** Instalar Oracle VirtualBox en el ordenador anfitrión y crear una máquina virtual con Ubuntu 26.04 LTS.

**Duración estimada:** 45-60 minutos

---

## Requisitos previos

- Ordenador con **Windows, macOS o Linux**
- Conexión a Internet
- Al menos **10 GB de espacio libre** en el disco duro
- Al menos **4 GB de RAM** (8 GB recomendados)

---

## Parte 1: Instalar Oracle VirtualBox

### 1.1 Descargar VirtualBox

1. Abre el navegador y ve a: https://www.virtualbox.org/wiki/Downloads
2. Selecciona el paquete correspondiente a tu sistema operativo anfitrión:

| Sistema anfitrión | Paquete a descargar |
|------------------|----------------------|
| Windows          | `VirtualBox-7.2.8-123456-Win.exe` |
| macOS            | `VirtualBox-7.2.8-123456-OSX.dmg` |
| Linux Ubuntu     | `VirtualBox-7.2.8-123456-Ubuntu-jammy_amd64.deb` |
| Linux Fedora     | `VirtualBox-7.2.8-123456-Fedora-38.x86_64.rpm` |

> ✅ **Consejo:** Descarga también el *Extension Pack* (`Oracle_VM_VirtualBox_Extension_Pack-7.2.8.vbox-extpack`) de la misma página. Añade soporte para USB 3.0, xHCI y cifrado de discos.

### 1.2 Instalar VirtualBox

**En Windows:**
- Ejecuta el instalador `.exe`
- Sigue el asistente (deja todo por defecto)
- Cuando pregunte sobre *Network Interfaces*, haz clic en **Instalar** (la red se cortará momentáneamente)

**En macOS:**
- Abre el archivo `.dmg`
- Haz doble clic en el paquete `.pkg` y sigue la instalación
- Concede los permisos de seguridad si macOS lo solicita (Preferencias del Sistema → Seguridad y Privacidad)

**En Linux Ubuntu/Debian:**
```bash
# Instalar dependencias
sudo apt update
sudo apt install -y wget build-essential

# Instalar VirtualBox desde el .deb descargado
cd ~/Descargas
sudo dpkg -i VirtualBox-7.2*.deb
sudo apt install -f   # resuelve dependencias pendientes

# O añadir el repositorio oficial para recibir actualizaciones automáticas:
wget -O- https://www.virtualbox.org/download/oracle_vbox_2016.asc | sudo gpg --dearmor -o /usr/share/keyrings/oracle-vbox.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-vbox.gpg] https://download.virtualbox.org/virtualbox/debian $(lsb_release -sc) contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list
sudo apt update
sudo apt install -y virtualbox-7.2
```

### 1.3 Instalar el Extension Pack

```bash
# Desde el terminal (Linux/macOS):
VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-7.2.8.vbox-extpack

# En Windows: Abre VirtualBox → Archivo → Herramientas → Gestor de Extension Pack
# o haz doble clic en el archivo .vbox-extpack
```

**Verificación:**
```bash
VBoxManage --version
# Salida esperada: 7.2.8r123456 (o similar)
```

---

## Parte 2: Descargar Ubuntu 26.04 LTS

1. Ve a: https://ubuntu.com/download/server
2. Descarga la imagen ISO de **Ubuntu 26.04 LTS (Server)** o **Desktop** según tus necesidades
3. Guárdala en un lugar donde la encuentres fácilmente (p. ej. `~/Descargas/`)

> ⚠ **Nota:** Para entornos de desarrollo IoT y servidores, la versión **Server** (sin entorno gráfico) es suficiente y consume menos recursos.

---

## Parte 3: Crear la máquina virtual

### 3.1 Configuración inicial

Abre VirtualBox y haz clic en **Nueva** (o `Ctrl+N`).

- **Nombre:** `Ubuntu 26.04 LTS`
- **Carpeta:** (deja la que viene por defecto)
- **ISO Image:** Selecciona el archivo `.iso` descargado
- **Tipo:** Linux
- **Versión:** Ubuntu (64-bit)

Parámetros recomendados:

| Parámetro | Valor | Notas |
|-----------|-------|-------|
| **RAM** | 4096 MB (4 GB) | Mínimo 2048 MB |
| **CPU** | 2 núcleos | Mínimo 1, máximo ½ de los núcleos físicos |
| **Disco duro** | 25-50 GB | Tamaño dinámico recomendado |
| **VRAM** | 16-128 MB | Más para Desktop con entorno gráfico |
| **Red** | NAT | Por defecto, se puede cambiar a Bridge más tarde |
| **Controlador** | SATA | Por defecto |

### 3.2 Configurar las redes

**NAT (por defecto):**
- La VM comparte la dirección IP del host
- La VM puede acceder a Internet
- El host NO puede acceder directamente a la VM (requiere redirección de puertos)

**Bridge (para acceso directo a la LAN):**
- La VM obtiene una IP propia en el router (ej: 192.168.1.x)
- El host puede conectarse a la VM (SSH, servidores)
- Configuración: VM → Configuración → Red → Modo: `Puente`

### 3.3 Configurar la carpeta compartida (opcional)

Después de instalar las Guest Additions (Parte 5), se puede crear una carpeta compartida:

1. VM → Configuración → Carpetas Compartidas
2. Haz clic en el icono de carpeta con el signo `+`
3. Selecciona una carpeta del host (ej: `~/compartido`)
4. Activa **Montaje Automático** y **Permanente**

### 3.4 Configurar la memoria de vídeo

- Para Ubuntu **Server** (sin escritorio): 16 MB son suficientes
- Para Ubuntu **Desktop**: 128 MB (o al menos 64 MB)

---

## Parte 4: Instalar Ubuntu en la VM

### 4.1 Iniciar la instalación

1. Selecciona la VM y haz clic en **Iniciar** (verde)
2. La VM arrancará desde la ISO de Ubuntu
3. Selecciona el idioma (catalán, castellano o inglés)

### 4.2 Pasos de la instalación (Ubuntu Server)

| Paso | Acción |
|------|--------|
| **Idioma** | Selecciona el idioma de instalación |
| **Teclado** | Elige la disposición: `Spanish` o `Catalan` |
| **Red** | Deja por defecto (DHCP) |
| **Mirror** | Selecciona el país más cercano para el repositorio de paquetes |
| **Disco** | `Use entire disk` (el disco de la VM) |
| **Perfil** | Introduce: nombre, nombre de usuario (`vboxuser` o el que prefieras), contraseña |
| **SSH** | Activa `Install OpenSSH server` para gestionarla remotamente |
| **Snaps** | Selecciona los que necesites (o ninguno para una instalación mínima) |

### 4.3 Finalizar y reiniciar

1. Cuando la instalación termine, selecciona **Reboot**
2. La VM te pedirá que expulses la ISO (Ctrl+D o desde: Dispositivos → Optical Drives → Quitar disco de la unidad)

### 4.4 Primera conexión

Inicia sesión con el usuario y contraseña que creaste:

```bash
# Conexión local (desde la consola de VirtualBox)
Ubuntu 26.04 LTS ubuntu tty1
ubuntu login: vboxuser
Password: 
```

```bash
# Conexión remota por SSH (si tienes la red en Bridge)
# Desde el host:
ssh vboxuser@<IP-de-la-VM>
```

---

## Parte 5: Instalar las Guest Additions

Las *Guest Additions* mejoran la integración entre el host y el guest: ratón libre, portapapeles compartido, carpetas compartidas, y redimensionamiento automático de la pantalla.

### 5.1 Montar la ISO de Guest Additions

Desde la ventana de la VM:
- Dispositivos → Insert Guest Additions CD image...

### 5.2 Instalar en el guest

Dentro de la VM:

```bash
# Instalar dependencias
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r)

# Montar el CD (si no se ha montado automáticamente)
sudo mount /dev/cdrom /mnt

# Ejecutar el instalador
cd /mnt
sudo sh ./VBoxLinuxAdditions.run --nox11

# Reiniciar
sudo reboot
```

**Verificación:**
```bash
# Comprobar que los módulos están cargados
lsmod | grep vbox
# Salida: vboxguest, vboxsf, vboxvideo
```

> ✅ A partir de aquí, si configuras carpetas compartidas en el host, aparecerán en `/media/sf_<nombre_carpeta>` en la VM (debes pertenecer al grupo `vboxsf`).

---

## Parte 6: Configuración post-instalación

### 6.1 Actualizar el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 6.2 Configurar el nombre de la máquina (hostname)

```bash
sudo hostnamectl set-hostname ubuntu-dev
# Comprobar:
hostnamectl
```

### 6.3 Mejorar la consola (opcional)

```bash
sudo apt install -y htop neofetch git curl wget tree
neofetch  # muestra información del sistema
```

### 6.4 Configurar clave SSH (opcional)

```bash
ssh-keygen -t ed25519 -C "vboxuser@ubuntu-dev"
cat ~/.ssh/id_ed25519.pub
# Añade esta clave a tu GitHub/GitLab para subir código sin contraseña
```

### 6.5 Asignar memoria swap (si es necesario)

```bash
# Si tienes poca RAM (4 GB o menos), añade 2 GB de swap:
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
# Hacerlo permanente:
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Verificación final

```bash
echo "=== Sistema ==="
uname -a
echo "=== Memoria ==="
free -h
echo "=== Disco ==="
df -h /
echo "=== VirtualBox ==="
lsmod | grep -E 'vboxguest|vboxsf'
echo "=== Usuario ==="
whoami
echo "=== Red ==="
ip addr show | grep inet
```

---

## Resolución de problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| La VM no arranca desde la ISO | Orden de arranque incorrecto | VM → Configuración → Sistema → Marca "CD/DVD" primero |
| "VT-x is not available" | Virtualización desactivada en la BIOS | Reinicia el host, entra a la BIOS/UEFI y activa Intel VT-x / AMD-V |
| No se ve el ratón dentro del guest | Guest Additions no instaladas | Instala las Guest Additions como en la Parte 5 |
| La carpeta compartida no se ve | Usuario no está en el grupo vboxsf | `sudo usermod -aG vboxsf $USER` y reinicia sesión |
| La VM se cuelga | Poca RAM asignada | Aumenta la RAM a 4096 MB en la configuración de la VM |
| No hay sonido | Controlador de audio incorrecto | VM → Configuración → Audio → Controlador: Intel HD Audio |
| SSH no conecta | Red en NAT o cortafuegos | Cambia a Bridge o añade redirección de puertos |
| No se puede redimensionar la pantalla | Guest Additions no instaladas o sesión gráfica | Verifica `lsmod | grep vboxvideo` |

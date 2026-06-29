# 📚 Teoria: Màquines virtuals i Ubuntu Linux

## Abans de començar...

Per què fem servir una màquina virtual en lloc d'instal·lar Ubuntu directament al nostre ordinador?

```
💻 El teu ordinador
   ├── 🪟 Tens Windows (o macOS)
   ├── 📁 Tens els teus fitxers, fotos, jocs...
   ├── ⚙️ Tot funciona bé
   │
   └── 🤔 Però vols aprendre Linux...
        └── Sense trencar res!
              ↓
        🖥️ Una màquina virtual!
```

> ✅ **Solució:** Instal·les VirtualBox (com un "ordinador dins de l'ordinador") i hi poses Ubuntu. Si alguna cosa va malament, simplement esborres la màquina virtual i la tornes a crear. **L'ordinador real queda intacte.**

---

## 🧠 Què és una màquina virtual?

Una **màquina virtual (VM)** és un ordinador simulat dins del teu ordinador real.

```
┌──────────────────────────────────────────────────────┐
│  🌍 EL MÓN REAL                                      │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  🖥️ TEU ORDINADOR (HOST)                      │  │
│  │  Windows / macOS / Linux                       │  │
│  │  RAM real: 8 GB | Disc real: 256 GB           │  │
│  │                                                │  │
│  │  ┌─────────────────────────────────────────┐   │  │
│  │  │  🧩 ORACLE VIRTUALBOX                  │   │  │
│  │  │  (El programa que crea la màquina       │   │  │
│  │  │   virtual dins del teu ordinador)       │   │  │
│  │  │                                         │   │  │
│  │  │  ┌─────────────────────────────────┐    │   │  │
│  │  │  │  🐧 MÀQUINA VIRTUAL (GUEST)    │    │   │  │
│  │  │  │  Ubuntu 26.04 LTS              │    │   │  │
│  │  │  │  RAM virtual: 4 GB             │    │   │  │
│  │  │  │  Disc virtual: 25 GB           │    │   │  │
│  │  │  │  CPU virtual: 2 nuclis         │    │   │  │
│  │  │  │                                │    │   │  │
│  │  │  │  🔧 Guest Additions            │    │   │  │
│  │  │  │  (Milloren el rendiment)       │    │   │  │
│  │  │  └─────────────────────────────────┘    │   │  │
│  │  └─────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### 🎯 Avantatges de les màquines virtuals

| Avantatge | Què significa |
|:----------|:--------------|
| 🛡️ **Aïllament** | El que passi dins la VM no afecta el teu ordinador |
| 📦 **Portabilitat** | Pots copiar la VM a un altre ordinador i funciona |
| 📸 **Snapshots** | Pots fer una foto de l'estat i tornar-hi si alguna cosa falla |
| 🧪 **Experimentació** | Pots provar coses sense por de trencar res |
| 💰 **Gratuït** | VirtualBox és lliure, Ubuntu és lliure |

---

## 🧩 Què és Oracle VirtualBox?

**VirtualBox** és un programa gratuït que permet crear i gestionar màquines virtuals.

| Característica | Detall |
|:--------------|:--------|
| 🏢 **Creador** | Oracle Corporation |
| 💵 **Preu** | **Gratuït** (fins i tot per a ús professional) |
| 💻 **Sistemes** | Windows, macOS, Linux, Solaris |
| 📦 **Tipus** | Hypervisor de tipus 2 (s'executa dins d'un SO normal) |
| 🔌 **Extension Pack** | Funcions extra: USB 3.0, xHCI, encriptació |

### Per què VirtualBox i no un altre?

```
Programa       │ Gratuït │ Fàcil │ Multiplataforma │
───────────────┼─────────┼───────┼─────────────────┤
VirtualBox     │    ✅   │  ✅   │       ✅        │ ← Millor opció
VMware Player  │    ✅   │  ✅   │       ❌        │   per a classe
Hyper-V        │    ✅   │  ❌   │       ❌        │
QEMU/KVM       │    ✅   │  ❌   │       ❌        │
Parallels      │    ❌   │  ✅   │       ❌        │
```

---

## 🐧 Per què Ubuntu Linux?

Ubuntu és la distribució Linux més utilitzada al món. És com la "versió fàcil" de Linux.

### Ubuntu vs altres Linux

```
📊 Linux més populars

Ubuntu       ████████████████████  (més usat, més tutorials)
Debian       ████████████
Fedora       █████████
Arch         ██████
Mint         █████████████

🎯 Ubuntu: El millor per començar
```

### ⭐ Per què Ubuntu per a IoT i programació?

| Motiu | Explicació |
|:------|:-----------|
| 📖 **Documentació** | Qualsevol dubte que tinguis, algú ja l'ha resolt a Google |
| 🔧 **Eines de desenvolupament** | ESP-IDF, Python, GCC... tot funciona a Ubuntu sense problemes |
| 🏷️ **LTS** (Long Term Support) | 5 anys d'actualitzacions de seguretat, no cal reinstal·lar cada any |
| 📦 **Repositoris** | Milers de programes disponibles amb `sudo apt install` |
| 👥 **Comunitat** | Fòrums, xats, tutorials... sempre hi ha algú per ajudar |

### Quina versió trio?

| Ubuntu Server | Ubuntu Desktop |
|:-------------|:--------------|
| 🖥️ **Només terminal** | 🪟 **Amb escriptori gràfic** |
| ⚡ Més lleuger | 🐢 Consumeix més recursos |
| ✅ **Recomanat per a classe** | ❌ Millor per a ús d'oficina |
| Perfecte per IoT i servidors | Té Firefox, LibreOffice... |

> 💡 **Per a aquesta assignatura:** Servidor. Treballarem per terminal i SSH. L'escriptori gràfic no el necessitarem.

---

## 📖 Vocabulari clau

Aprèn aquestes paraules, les veuràs a tot arreu:

| Terme | Significat | 🧠 Per recordar-ho... |
|:------|:----------|:---------------------|
| **Host** | L'ordinador real on tens VirtualBox | *"Host = Hospital, és on està tot"* |
| **Guest** | El sistema convidat (Ubuntu dins la VM) | *"Guest = convidat, és el visitant"* |
| **Hypervisor** | El programa que gestiona les VMs | *VirtualBox és l'hypervisor* |
| **vCPU** | Nucli virtual assignat a la VM | *CPU virtual, no el real* |
| **VRAM** | Memòria de vídeo virtual | *Per a la pantalla* |
| **NAT** | Xarxa: la VM comparteix IP del host | *Com si estigués darrere del host* |
| **Bridge** | Xarxa: la VM té IP pròpia | *Com si estigués connectada directament al router* |
| **Snapshot** | Foto de l'estat de la VM | *Com un punt de guardat en un videojoc* |
| **Guest Additions** | Drivers per millorar el guest | *El "pack de millores"* |
| **VDI** | Format de disc de VirtualBox | *El fitxer on es guarda la VM* |
| **ISO** | Fitxer d'imatge d'un CD/DVD | *Com un CD en un fitxer* |

---

## ❓ Preguntes freqüents (teoria)

**❓ Puc tenir més d'una màquina virtual?**
Sí, tantes com espai al disc tinguis. Pots tenir Ubuntu, Windows, etc.

**❓ Si esborro la VM, s'afecta l'ordinador?**
No. Esborrar la VM és com tirar un fitxer a la paperera. El teu Windows/macOS segueix igual.

**❓ Per què la VM va més lenta que el meu ordinador?**
Perquè només té una part dels recursos (RAM, CPU). Si li assignes 4 GB, només té 4 GB encara que el teu ordinador en tingui 16.

**❓ Puc portar la VM a casa en un USB?**
Sí! Pots exportar la VM a un fitxer i portar-la a un altre ordinador amb VirtualBox.

**❓ Què passa si tanco la finestra de la VM sense apagar-la?**
Pots fer **"Guardar l'estat"** (ve a ser com hibernar-la) o simplement **"Apagar la VM"**.

**❓ I si vull un altre Linux en lloc d'Ubuntu?**
VirtualBox funciona amb qualsevol sistema: Debian, Fedora, Linux Mint, etc. Però per a classe farem servir Ubuntu.

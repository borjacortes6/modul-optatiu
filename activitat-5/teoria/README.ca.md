# 🌐 Teoria: Xarxa Local (LAN) — Connectar la VM a la xarxa real

## Abans de començar...

Fins ara, la teva màquina virtual Ubuntu s'ha connectat a internet amb mode **NAT** de VirtualBox. Això vol dir que la VM **comparteix** la connexió del teu ordinador, però **no és visible** a la xarxa local.

Però en entorns IoT reals, els dispositius (Raspberry Pi, PLCs, sensors) estan connectats a la **xarxa local** i són accessibles des de qualsevol altre dispositiu de la xarxa. Necessites que la teva VM es comporti com un **ordinador més de la xarxa**.

> ✅ **Objectiu:** Entendre què és una xarxa local (LAN), com funcionen les IPs privades, i preparar la VM per ser accessible des de Windows.

---

## 1️⃣ Què és una xarxa local (LAN)?

Una **LAN** (Local Area Network) és un conjunt d'ordinadors connectats entre si dins d'un espai físic limitat: casa teva, l'aula, una oficina.

```
         ┌───────────────────── Router (192.168.0.1) ─────────────────────┐
         │                         │                                      │
         │       ┌─────────────────┼──────────────────┐                   │
         │       │                 │                  │                   │
         ▼       ▼                 ▼                  ▼                   │
      🌐 Internet              🔌 Switch / WiFi                          │
                               │        │        │                       │
                               ▼        ▼        ▼                       │
                            ┌────┐  ┌────┐  ┌────┐                      │
                            │ PC │  │ VM │  │ 📱 │                      │
                            │Win │  │Ubu │  │mòb │                      │
                            └────┘  └────┘  └────┘                      │
                         192.168.  192.168.  192.168.                    │
                         0.22      0.57      0.xx                       │
```

Tots els dispositius es comuniquen a través del **router**, que:
- Dóna una **IP única** a cada dispositiu (DHCP)
- Permet que es vegin entre ells
- Dóna accés a internet (si el router hi està connectat)

### Característiques d'una LAN

| Propietat | Descripció |
|:----------|:-----------|
| **Abast** | Limitada a un espai físic (casa, aula, edifici) |
| **Velocitat** | Alta (100 Mbps – 1 Gbps o més) |
| **Connexió** | Cable (Ethernet) o WiFi |
| **IPs** | Privades (192.168.xx.xx, 10.xx.xx.xx, 172.16.xx.xx) |
| **Accés** | Els dispositius es veuen entre ells directament |

> 🎯 **Analogia:** La LAN és com una **casa compartida**. Cada habitació (dispositiu) té una adreça (IP) única. El router és la **porta d'entrada** que connecta la casa amb el carrer (internet).

---

## 2️⃣ Adreces IP privades — El rang 192.168.xx.xx

### Què és una adreça IP?

Una **adreça IP** és com el **número de telèfon** del teu ordinador a la xarxa. Permet que els dispositius es trobin i es parlin entre ells.

Format: **4 números separats per punts**, cadascun entre **0 i 255**:

```
192 . 168 . 0 . 57
─┬──  ─┬──  ─┬── ─┬─
xarxa  xarxa  host host
```

### IPs privades vs públiques

Hi ha rangs d'IPs **reservats per a xarxes locals** (mai s'usen directament a internet):

| Rang privat | Màscara | Ús típic |
|:------------|:--------|:---------|
| **10.0.0.0** – 10.255.255.255 | 255.0.0.0 | Xarxes grans (empreses, universitats) |
| **172.16.0.0** – 172.31.255.255 | 255.240.0.0 | Xarxes mitjanes |
| **192.168.0.0** – 192.168.255.255 | 255.255.0.0 | **Xarxes domèstiques** (la més comuna) |

La teva xarxa usa el rang **192.168.0.xx** (el més típic en routers domèstics).

> **IP pública:** La que té el teu router a internet (ex: 88.22.33.123). Tots els dispositius de casa teva **comparteixen** aquesta IP per sortir a internet.
>
> **IP privada:** La que té cada dispositiu dins la teva LAN (ex: 192.168.0.22 per Windows, 192.168.0.57 per la VM).

```
🌐 Internet (IP pública: 88.22.33.123)
        │
   ┌────┴────┐
   │ Router  │ ← Tots surten per aquí
   └────┬────┘
        │
   ┌────┼────┐
   │    │    │
192.168. 192.168. 192.168.
  0.22   0.57    0.xx
(Windows) (VM)   (mòbil)
```

---

## 3️⃣ Màscara de subxarxa (255.255.255.0)

La **màscara de subxarxa** defineix quina part de la IP identifica la **xarxa** i quina part identifica el **dispositiu** (host).

```
IP:          192 . 168 . 0 . 57
Màscara:     255 . 255 . 255 . 0
             ──┬──  ──┬──  ──┬──  ─┬─
              xarxa         host
```

### Com es llegeix?

| Part de la màscara | Significat |
|:-------------------|:-----------|
| **255.255.255**.0 | Els primers **3 números** identifiquen la **xarxa** → `192.168.0` |
| 255.255.255.**0** | L'últim número identifica el **dispositiu** → `.57` |

Amb la màscara **255.255.255.0** (/24 en notació CIDR):

- **Xarxa:** `192.168.0.0` (tots els dispositius comencen per `192.168.0.`)
- **Hosts disponibles:** Del `.1` al `.254` (254 dispositius possibles)
- **Especial:** `.0` = la xarxa, `.255` = broadcast (tots els dispositius)

### Exemple amb la teva xarxa

| Dispositiu | IP | Màscara | Xarxa |
|:-----------|:---|:--------|:------|
| Router | 192.168.0.1 | 255.255.255.0 | 192.168.0.0 |
| Windows | 192.168.0.22 | 255.255.255.0 | 192.168.0.0 |
| VM Ubuntu | 192.168.0.57 | 255.255.255.0 | 192.168.0.0 |

Tots tres estan a la **mateixa xarxa** (`192.168.0.0`), per tant es poden comunicar directament.

> 🎯 **Analogia:** La màscara de subxarxa és com el **codi postal** dels dispositius. Si dos dispositius tenen el mateix codi postal (mateixa xarxa), poden enviar-se cartes directament sense passar per l'oficina central.

### Notació CIDR

També veuràs les IPs escrites amb una barra:

| Escrit | Significa |
|:-------|:----------|
| `192.168.0.57/24` | Màscara 255.255.255.0 (24 bits a 1) |
| `192.168.0.57/16` | Màscara 255.255.0.0 (16 bits a 1) |

El número després de la barra és quants bits de la IP estan marcats com a "xarxa".

---

## 4️⃣ NAT vs Bridge — Dues maneres de connectar la VM

Quan la VM es connecta a la xarxa, VirtualBox ofereix diversos modes:

### Mode NAT (el que tenies)

```
Windows (192.168.0.22)          🌐 Internet
        │                            │
        │     ┌─────────────┐        │
        └─────┤ VirtualBox  ├────────┘
              │    NAT      │
              └──────┬──────┘
                     │
                ┌────┴────┐
                │ VM (10.0.2.15) │
                └─────────┘
```

| Avantatges | Inconvenients |
|:-----------|:--------------|
| ✅ La VM surt a internet | ❌ La VM **no es veu** des de Windows |
| ✅ Configuració zero | ❌ IP interna (10.0.2.x) diferent de la LAN |

### Mode Bridge (com ho tindràs ara)

```
Windows (192.168.0.22)    VM (192.168.0.57)   🌐 Internet
        │                        │                 │
        └────────────────────────┼─────────────────┘
                                 │
                           ┌─────┴────┐
                           │  Router  │
                           └──────────┘
                        192.168.0.1
```

| Avantatges | Inconvenients |
|:-----------|:--------------|
| ✅ La VM té IP real de la xarxa (192.168.0.57) | ❌ La VM gasta una IP del rang |
| ✅ Windows pot accedir a la VM directament | ❌ Cal configurar el mode manualment |
| ✅ La VM es comporta com un PC normal | |

> 🎯 **Analogia:** NAT és com estar **dins d'una habitació tancada** amb una finestra que dona al carrer. Bridge és com **sortir al carrer** i barrejar-te amb tothom.

---

## 5️⃣ Per què necessites Bridge per a IoT?

En un entorn IoT real, els dispositius (sensors, PLCs, Raspberry Pi) estan connectats a la xarxa local amb IPs reals. Necessites que la teva VM es comporti igual perquè:

- **Windows pugui accedir als dashboards** (Node-RED, Grafana) des del navegador
- **Altres dispositius** (mòbils, tauletes) puguin veure les dades
- Puguis **simular un entorn real** on els dispositius es comuniquen per xarxa

```
            ┌─────────┐
            │ 📱 Mòbil │
            └────┬────┘
                 │ WiFi
    ┌────────────┼────────────┐
    │       ┌────┴────┐       │
    │       │ Router  │       │
    │       │192.168.0.1      │
    │       └────┬────┘       │
    │            │             │
┌───┴───┐  ┌────┴────┐  ┌────┴────┐
│Windows│  │   VM    │  │Raspberry│
│0.22   │  │0.57     │  │Pi 0.xx  │
└───────┘  └─────────┘  └─────────┘
  Grafana     Node-RED     Sensor
```

---

## ✅ Resum

| Concepte | Què és? |
|:---------|:--------|
| **LAN** | Xarxa local que connecta dispositius dins un espai físic |
| **IP privada** | Adreça única dins la xarxa local (ex: 192.168.0.57) |
| **Màscara /24** | 255.255.255.0 → 254 dispositius possibles a la mateixa xarxa |
| **NAT** | La VM comparteix xarxa, però no és visible (IP 10.0.2.x) |
| **Bridge** | La VM té IP real de la LAN (IP 192.168.0.x) i és accessible |

A la pràctica següent canviaràs la VM a mode Bridge i ho comprovaràs! 🚀

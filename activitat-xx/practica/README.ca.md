# 🔗 Pràctica: Accedir a la teva VM des de qualsevol lloc amb Tailscale

**🎯 Objectiu:** Instal·lar Tailscale a la VM i als teus dispositius per accedir als serveis IoT des de qualsevol lloc (classe, casa, carrer...).

**⏱ Durada estimada:** 20-30 minuts

> 💡 **Situació:** Tens la VM amb Ubuntu a classe (o a casa) i vols accedir-hi
> des del mòbil, des del portàtil a la biblioteca, o des de qualsevol xarxa.

---

## 📋 Què necessites?

| 🔧 Requisit | 📝 Detall |
|:-----------|:----------|
| 🖥️ **VM Ubuntu** | Engegada i connectada a internet (Bridge o NAT) |
| 🌐 **Internet** | Tant a la VM com al dispositiu des d'on et connectis |
| 📱 **Mòbil o portàtil** | Per accedir-hi des de fora |
| 👤 **Compte** | Google, Microsoft, GitHub o Apple (per autenticar-te) |

---

## 🗺️ Mapa de la pràctica

```
1️⃣  Instal·lar Tailscale a la VM ─────────── sudo apt install
        │
2️⃣  Autenticar la VM ──────────────────────── enllaç al navegador
        │
3️⃣  Comprovar la IP Tailscale ─────────────── tailscale status
        │
4️⃣  Instal·lar Tailscale al Windows ──────── tailscale.com/download
        │
5️⃣  Instal·lar Tailscale al mòbil ─────────── App Store / Google Play
        │
6️⃣  Provar l'accés remot ──────────────────── Node-RED, Grafana, SSH
        │
7️⃣  Fer-lo permanent ──────────────────────── systemd enable
```

---

## 1️⃣ Instal·lar Tailscale a la VM (Ubuntu)

Obre un terminal dins la teva màquina virtual Ubuntu i executa:

```bash
# Descarregar i instal·lar (1 comanda)
curl -fsSL https://tailscale.com/install.sh | sh
```

> ⏱ **Espera** que s'instal·li. Només triga uns segons.

**Verificació:**
```bash
tailscale version
```
Hauries de veure: `1.98.8` o similar ✅

---

## 2️⃣ Autenticar la VM

Engega la connexió amb Tailscale:

```bash
sudo tailscale up
```

Et sortirà un enllaç com aquest:

```
To authenticate, visit:

    https://login.tailscale.com/a/ab3e2db0135ec
```

> 🔗 **Copia l'enllaç** i obre'l al navegador del teu ordinador o mòbil.

A la pàgina de Tailscale:

1. **Inicia sessió** amb un compte:
   - Google (el més fàcil)
   - Microsoft
   - GitHub
   - Apple

2. Confirma que vols afegir el dispositiu

3. Torna al terminal — automàticament es tanca la connexió

**Comprovació:**
```bash
tailscale status
```
Hauries de veure:

```
100.104.113.64  ubuntu  elteucompte@  linux  -
```

> 🎉 **Ja tens la VM connectada a la teva xarxa privada!**

---

## 3️⃣ Trobar la IP Tailscale de la VM

```bash
tailscale ip -4
```

Et mostrarà una IP tipus: **`100.104.113.64`**

> 🔑 **Guarda aquesta IP!** La faràs servir per accedir des de qualsevol lloc.

A partir d'ara, sempre que estiguis connectat a Tailscale, podràs accedir:
- Node-RED: `http://100.104.113.64:1880`
- Grafana: `http://100.104.113.64:3000`
- InfluxDB: `http://100.104.113.64:8086`
- SSH: `ssh vboxuser@100.104.113.64`

---

## 4️⃣ Configuració al Windows (o portàtil)

Per accedir des del teu ordinador des de qualsevol xarxa:

### 📥 Descarrega Tailscale

**🔗** https://tailscale.com/download

| Sistema | Què descarregues |
|:--------|:-----------------|
| 🪟 **Windows** | `TailscaleSetup.exe` |
| 🍏 **macOS** | `Tailscale.dmg` |
| 🐧 **Linux** | `tailscale_amd64.deb` o `.rpm` |

### 🛠️ Instal·lació

1. Fes doble clic al fitxer descarregat
2. Segueix l'assistent (tot per defecte)
3. Quan obris l'app, **inicia sessió amb el MATEIX compte** que vas fer servir a la VM

``` 
┌──────────────────────────────────────────────┐
│  Tailscale                                   │
│                                              │
│  ✅ Dispositius connectats:                  │
│     🖥️ ubuntu         100.104.113.64        │
│     💻 aquest PC      100.104.x.x            │
│                                              │
│  🟢 Connectat a xarxa mesh                   │
└──────────────────────────────────────────────┘
```

### 🔍 Prova d'accés

Obre el navegador al Windows i ves a:

```
http://100.104.113.64:1880
```

Hauries de veure la interfície de **Node-RED**! 🎉

---

## 5️⃣ Configuració al mòbil (Android / iOS)

Per accedir des del mòbil, per exemple a la cafeteria o al parc:

### 📱 Instal·lar

| Sistema | On trobar-ho |
|:--------|:-------------|
| 📱 **Android** | Google Play → cerca "Tailscale" |
| 📱 **iPhone** | App Store → cerca "Tailscale" |

### 🔑 Autenticar

1. Obre l'app
2. **Inicia sessió** amb el mateix compte
3. Automàticament veuràs els teus dispositius

```
┌──────────────────────┐
│ Tailscale            │
│                      │
│ 🟢 ubuntu            │
│    100.104.113.64    │
│                      │
│ 🟢 Aquest mòbil      │
│    100.104.x.x       │
└──────────────────────┘
```

### 🌐 Accedir des del mòbil

Obre el navegador del mòbil i escriu:

```
http://100.104.113.64:1880
```

**Això és increïble!** Tens Node-RED al mòbil sense necessitat d'instal·lar res al router. 🎉

> 💡 **Consell:** Desa l'enllaç com a marcador a la pantalla d'inici del mòbil
> i semblarà una app nativa!

---

## 6️⃣ Prova de connectivitat

### 🧪 Proves que has de fer

| # | Prova | Com | Resultat esperat |
|:-:|:------|:----|:----------------|
| 1 | 📡 **Node-RED des de Windows** | `http://100.104.113.64:1880` | Veus la interfície |
| 2 | 📊 **Grafana des de Windows** | `http://100.104.113.64:3000` | Veus el login |
| 3 | 📱 **Node-RED des del mòbil** | `http://100.104.113.64:1880` | Funciona en 4G/5G |
| 4 | 🔐 **SSH des del Windows** | `ssh vboxuser@100.104.113.64` | Terminal remot |
| 5 | 📱 **SSH des del mòbil** | App Termius / JuiceSSH | Terminal al mòbil! |

### 🔐 Com fer SSH des del mòbil

| App | Sistema | Preu |
|:----|:--------|:-----|
| **Termius** | Android / iOS | Gratis |
| **JuiceSSH** | Android | Gratis |
| **Shelly** | iOS | Gratis |

Configura:
- **Host:** `100.104.113.64`
- **Usuari:** `vboxuser`
- **Contrasenya:** la que vas posar a Ubuntu

---

## 7️⃣ Fer-ho permanent (inici automàtic)

Perquè Tailscale s'iniciï sol cada cop que engeguis la VM:

```bash
sudo systemctl enable --now tailscaled
```

**Comprova que està actiu:**
```bash
sudo systemctl status tailscaled
```

Busca: `Active: active (running)` ✅

> 🔄 A partir d'ara, cada cop que engeguis la VM, Tailscale s'activarà sol.
> ***Recorda: si apagues la VM, el Tailscale dins la VM també s'atura!***

---

## 8️⃣ Més enllà: Activar MagicDNS (opcional)

En lloc de recordar la IP `100.104.113.64`, pots fer servir el nom de la VM:

1. Ves a [https://login.tailscale.com/admin/dns](https://login.tailscale.com/admin/dns)
2. Activa **MagicDNS**
3. Ara pots accedir a:

```
http://ubuntu:1880   → Node-RED
http://ubuntu:3000   → Grafana
ssh vboxuser@ubuntu  → SSH
```

---

## ✅ Llista de verificació (checklist)

| # | Fet? | Pas |
|:-:|:----:|:----|
| 1 | ☐ | Instal·lar Tailscale a la VM amb `curl ... \| sh` |
| 2 | ☐ | Executar `sudo tailscale up` i autenticar al navegador |
| 3 | ☐ | Anotar la IP Tailscale: `tailscale ip -4` |
| 4 | ☐ | Instal·lar Tailscale al Windows (tailscale.com) |
| 5 | ☐ | Instal·lar Tailscale al mòbil (App Store / Google Play) |
| 6 | ☐ | Provar Node-RED: `http://100.x.x.x:1880` des del mòbil |
| 7 | ☐ | Provar Grafana: `http://100.x.x.x:3000` des del Windows |
| 8 | ☐ | Provar SSH: `ssh vboxuser@100.x.x.x` des de Windows |
| 9 | ☐ | Activar inici automàtic: `sudo systemctl enable --now tailscaled` |

---

## 🐛 Resolució de problemes

| Problema | Possible causa | Solució |
|:---------|:--------------|:--------|
| ❌ `tailscale up` no mostra enllaç | Falta internet | Comprova `ping 8.8.8.8` |
| ❌ L'enllaç no obre res | Tallafocs | Prova amb un altre navegador |
| ❌ No veig la IP 100.x.x.x | No autenticat | Torna a executar `sudo tailscale up` |
| ❌ No puc accedir des del mòbil | Mòbil no autenticat | Obre l'app de Tailscale i inicia sessió |
| ❌ `http://100.x.x.x:1880` no carrega | Node-RED aturat | Comprova `docker ps` a la VM |
| ❌ VM apagada | L'has apagada | Engega-la — Tailscale només funciona si la VM està encesa! |

---

## 📝 Per a l'informe

Inclou a l'informe:

1. **Captura de pantalla** de `tailscale status` mostrant la teva VM
2. **Captura** del Node-RED al navegador del mòbil (o Windows) accedint per Tailscale
3. **Quina IP Tailscale** té la teva VM?
4. **Per què** Tailscale funciona sense obrir ports al router?

---

## 🧠 Fes-ho tu sol!

Si ho has entès tot, prova:

1. Pots accedir a **Grafana** des del mòbil? Per què serviria veure els gràfics de temperatura al mòbil?

2. I si vols compartir l'accés amb un company? Tailscale permet **fins a 3 usuaris gratis**. Com li donaries accés al teu company perquè vegi Node-RED?

3. **Repte extra:** Instal·la Tailscale també al Windows i prova de fer ping des del Windows a la VM per la IP Tailscale:
   ```cmd
   ping 100.104.113.64
   ```
   Què observes? (pista: és més ràpid que per la IP local perquè...?)

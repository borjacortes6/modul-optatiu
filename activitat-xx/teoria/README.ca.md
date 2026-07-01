# 🌐 Teoria: Accés remot amb Tailscale — La teva VPN màgica

## Abans de començar...

Has aconseguit posar la teva màquina virtual a la xarxa local (Bridge) i pots accedir als serveis IoT des de Windows: Node-RED, Grafana, InfluxDB... 🎉

Però hi ha un problema:

``` 
🏠 A CASA (o a classe)
   ├── 💻 Windows ──→ 192.168.0.xx
   │                    └── Pots veure la VM
   │
   └── 🖥️ VM Ubuntu ──→ 192.168.0.57
                        └── Node-RED :1880 ✅
                        └── Grafana  :3000 ✅
                           
☕ AL CAFÈ / 🏫 UN ALTRE INSTITUT / 🏖️ VACANCES
   ├── 💻 Portàtil ──→ 192.168.??
   │                    └── ❌ No veu la VM
   │
   └── 🖥️ VM Ubuntu ──→ 192.168.0.57 (a casa)
                        └── Inaccessible!
```

> 🎯 **Problema:** La IP `192.168.0.57` només existeix dins de la teva xarxa local.
> Si no hi estàs connectat, no hi pots accedir.

**Necessitem una solució per accedir als nostres serveis des de qualsevol lloc.**

---

## 1️⃣ Què és una VPN?

Una **VPN** (Virtual Private Network) crea un túnel xifrat entre dos dispositius a través d'internet, com si estiguessin a la **mateixa xarxa física**, encara que estiguin a quilòmetres de distància.

```
┌─────────────────────────────────────────────────────────────────┐
│                         🌍 INTERNET                              │
│                                                                  │
│   ┌──────────────┐          ┌──────────────┐                    │
│   │  📱 Mòbil    │          │  🖥️ VM       │                    │
│   │  (carrer)    │  ════════│  (casa)      │                    │
│   │  100.104.x.x │  TÚNEL   │  100.104.x.x │                    │
│   │              │  XIFRAT  │              │                    │
│   │  ┌────────┐  │  ════════│  ┌────────┐  │                    │
│   │  │App     │  │          │  │:1880   │  │                    │
│   │  │NodeRED │──║══════════║──│Node-RED│  │                    │
│   │  └────────┘  │          │  └────────┘  │                    │
│   └──────────────┘          └──────────────┘                    │
│                                                                  │
│   🛡️ Tot el trànsit va xifrat — ningú pot espiar el que fas     │
└─────────────────────────────────────────────────────────────────┘
```

| Concepte | Explicació | Analogia |
|:---------|:-----------|:---------|
| **VPN** | Xarxa privada virtual que connecta dispositius a través d'internet | Un **passadís privat** que connecta dos edificis separats |
| **Túnel xifrat** | Les dades viatgen encriptades entre els dispositius | Una **carta dins d'una caixa forta tancada** |
| **IP virtual** | L'adreça que rep cada dispositiu dins la xarxa VPN (tipus `100.x.x.x`) | El **número d'habitació** al passadís privat |

---

## 2️⃣ Les opcions per accedir des de fora

Abans de triar, mirem quines opcions existeixen per accedir a la teva xarxa local des de fora:

### Comparativa de solucions

| Solució | Com funciona | Cal obrir ports? | Cost | Dificultat |
|:--------|:------------|:-----------------|:-----|:-----------|
| 🔥 **Cloudflare Tunnel** | Cloudflare fa de pont entre tu i la VM | ❌ No | Gratis | Mitjana |
| 🥇 **Tailscale** | Xarxa mesh WireGuard automàtica | ❌ No | Gratis (3 usuaris) | **Fàcil** |
| 🔧 **WireGuard manual** | VPN clàssica que configures tu | ✅ 1 port | Gratis | Difícil |
| 🌐 **DDNS + Port forwarding** | Obrir ports al router i IP dinàmica | ✅ Diversos ports | Gratis | Mitjana |
| ☁️ **Servidor al núvol** | Llogues un servidor sempre accessible | ❌ No | ~7€/mes | Fàcil |

### Per què Tailscale?

``` 
┌─────────────────────────────────────────────────────┐
│                                                      │
│  🏆 TAILSCALE — La solució guanyadora                │
│                                                      │
│  1️⃣ Instal·lar i autenticar → 2 minuts              │
│  2️⃣ No cal tocar el router                          │
│  3️⃣ Funciona darrere de qualsevol firewall           │
│  4️⃣ Funciona a l'institut (fins i tot amb CGNAT)    │
│  5️⃣ Gratis per a 3 usuaris                          │
│                                                      │
│  👉 Perfecte per al profe: accedeix des de casa      │
│     al Node-RED, Grafana... sense complicacions      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 3️⃣ Com funciona Tailscale?

Tailscale és una **VPN moderna** construïda sobre **WireGuard**, però amb la màgia afegida de gestionar tota la configuració automàticament.

### Arquitectura

```
                       ┌──────────────────┐
                       │   ☁️ Tailscale    │
                       │  Coordination     │
                       │  Server           │
                       └────────┬─────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
   ┌──────────────┐     ┌──────────────┐      ┌──────────────┐
   │  🖥️ VM       │     │  💻 Windows  │      │  📱 Mòbil    │
   │  Ubuntu      │     │  (casa)      │      │  (carrer)    │
   │              │     │              │      │              │
   │  100.104.x.x │◄═══►│  100.104.y.y │◄════►│  100.104.z.z │
   │              │     │              │      │              │
   └──────────────┘     └──────────────┘      └──────────────┘
                           ════════════════
                          Connexió directa
                          (WireGuard P2P)
```

| Component | Què fa |
|:----------|:--------|
| **🖥️ Cada dispositiu** | Té instal·lat Tailscale i una IP única `100.x.x.x` |
| **☁️ Servidor de coordinació** | Només ajuda a presentar els dispositius entre si (no hi passen dades) |
| **🔗 WireGuard** | Protocol VPN ultrarràpid i segur que connecta directament els dispositius |

> **🔑 La clau:** Tailscale fa tota la configuració complicada automàticament. Tu només
> has d'instal·lar-lo i autenticar-te amb el teu compte.

### Característiques clau

| Característica | Per què mola? |
|:---------------|:--------------|
| ⚡ **P2P directe** | Les dades van directe entre dispositius, no passen per cap servidor intermedi |
| 🛡️ **WireGuard** | El protocol VPN més segur i ràpid del mercat |
| 🔄 **Autoreconnexió** | Si perds la connexió, es reconnecta sol |
| 📱 **Multiplataforma** | Windows, Linux, macOS, iOS, Android |
| 🧩 **No cal configurar res** | Zero configuració: instal·les i ja funciona |
| 🔌 **Integració amb SSO** | Pots fer servir Google, Microsoft, GitHub... |

---

## 4️⃣ Tailscale vs Cloudflare Tunnel

Per a què serveix cada un?

```
┌────────────────────────────────────────────────────────────────┐
│                         TU XARXA                               │
│                                                                │
│   ┌──────────────────────────────────────────────────┐         │
│   │  🏠 LAN LOCAL (192.168.0.xx)                     │         │
│   │                                                    │         │
│   │  🖥️ VM Ubuntu                                     │         │
│   │     ├── Node-RED (:1880)    ◄──── ─ ─ ─ ─ ─ ─┐  │         │
│   │     ├── Grafana (:3000)     ◄──── ─ ─ ─ ─ ─ ─┤  │         │
│   │     └── SSH (:22)           ◄──── ─ ─ ─ ─ ─ ─┤  │         │
│   └──────────────────────────────────────────────────┘         │
│                      ▲                         ▲               │
│                      │                         │               │
│              ┌───────┴───────┐         ┌───────┴────────┐      │
│              │  Tailscale    │         │  Cloudflare    │      │
│              │  (per a tu)   │         │  Tunnel        │      │
│              │               │         │  (per a tots)  │      │
│              │  100.x.x.x    │         │  domini.com    │      │
│              └───────────────┘         └────────────────┘      │
│                      ▲                         ▲               │
│                      │                         │               │
│              ┌───────┴───────┐         ┌───────┴────────┐      │
│              │  👨‍🏫 Profe   │         │  👩‍🎓 Alumnes  │      │
│              │  (SSH + tot)  │         │  (només web)   │      │
│              └───────────────┘         └────────────────┘      │
└────────────────────────────────────────────────────────────────┘
```

| Per a qui? | Eina | Què permet? |
|:------------|:-----|:------------|
| 👨‍🏫 **El profe** | **Tailscale** | SSH, Node-RED, Grafana, InfluxDB — accés complet des de qualsevol lloc |
| 👩‍🎓 **Els alumnes** | Cloudflare Tunnel | Node-RED i Grafana des de casa, sense instal·lar res (només un navegador) |

> 💡 **Resum:** Tailscale és per a tu (accés total), Cloudflare Tunnel és per exposar
> serveis concrets als alumnes sense que hagin d'instal·lar res.

---

## 5️⃣ Conceptes clau per recordar

| Concepte | Què és | Com es veu |
|:---------|:-------|:-----------|
| **Tailscale IP** | L'adreça del dispositiu dins la xarxa VPN | `100.x.x.x` |
| **Node** | Cada dispositiu amb Tailscale instal·lat | `ubuntu`, `windows`, `android` |
| **Mesh** | Xarxa on tots els nodes es connecten entre si directament | Connexions P2P |
| **Coordination Server** | El servidor que presenta els nodes (no hi passen dades) | gestionat per Tailscale |
| **MagicDNS** | En lloc d'usar IPs, pots usar noms com `ubuntu` | `ssh vboxuser@ubuntu` |

---

## 📝 Resum

| Idea clau | Explicació |
|:----------|:-----------|
| 🎯 **Problema** | No pots accedir a la teva LAN des de fora |
| ✅ **Solució** | Tailscale crea una xarxa VPN privada que funciona sempre |
| ⚡ **Màgia** | No cal obrir ports al router ni fer configuracions complicades |
| 📱 **Accés** | Des de qualsevol dispositiu: portàtil, mòbil, tauleta |
| 🆓 **Cost** | Gratis per a 3 usuaris |

> ✅ **Ara que entens la teoria, passa a la pràctica per instal·lar-ho!**

# Activitat 1: Creació d'un escriptori virtual amb VirtualBox i Ubuntu Linux

## Teoria

### Què és una màquina virtual?

Una màquina virtual (VM) és un entorn de sistema operatiu que s'executa dins d'un altre sistema operatiu fent servir software de virtualització. Permet:

- **Aïllament** — El sistema convidat no interfereix amb l'amfitrió
- **Portabilitat** — Es pot moure entre ordinadors físics
- **Snapshots** — Capturar l'estat de la VM per poder restaurar-lo
- **Requeriments mínims** — No cal hardware dedicat

### Oracle VirtualBox

**VirtualBox** és un hypervisor de tipus 2 (hostejat) gratuït i de codi obert mantingut per Oracle. Característiques principals:

- **Gratuït** — Sense llicències, fins i tot per a ús comercial
- **Multiplataforma** — S'instal·la a Windows, macOS, Linux i Solaris
- **Suport ampli** — Virtualitza la majoria de sistemes x86/x86_64
- **Guest Additions** — Drivers i eines de millora per al sistema convidat (accés al porta-retalls, carpetes compartides, pantalla redimensionable)
- **xHCI / USB 3.0** — Suport natiu per a dispositius USB

### Per què triar Ubuntu Linux?

Ubuntu és una de les distribucions Linux més populars, basada en Debian. Avantatges per a entorns IoT i desenvolupament:

- **LTS (Long Term Support)** — versions estables amb 5 anys de suport
- **Repositoris extensos** — Paquets actualitzats per a eines de desenvolupament
- **Comunitat activa** — Documentació abundant i suport en línia
- **ESP-IDF i eines encastades** — Suport complet per a toolchains creuades
- **Snap i APT** — Gestors de paquets moderns

### Arquitectura de virtualització

```
┌─────────────────────────────────────────────┐
│     Ordinador físic (Host)                  │
│  Windows / macOS / Linux                    │
│  ┌───────────────────────────────────────┐  │
│  │  Oracle VirtualBox (Hypervisor)       │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │  Màquina virtual (Guest)        │  │  │
│  │  │  Ubuntu 26.04 LTS               │  │  │
│  │  │  vCPU: 2 │ RAM: 4 GB │ 50 GB   │  │  │
│  │  │  ┌───────────────────────────┐  │  │  │
│  │  │  │  Guest Additions          │  │  │  │
│  │  │  │  (Drivers + eines)        │  │  │  │
│  │  │  └───────────────────────────┘  │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Terminologia clau

| Terme | Descripció |
|-------|------------|
| **Host** | Sistema operatiu amfitrió on s'executa VirtualBox |
| **Guest** | Sistema operatiu convidat dins la VM |
| **Hypervisor** | Programari que gestiona les màquines virtuals |
| **vCPU** | Nucli de CPU virtual assignat a la VM |
| **VRAM** | Memòria de vídeo dedicada a la VM |
| **NAT** | Mode de xarxa per defecte: la VM comparteix l'IP del host |
| **Bridge** | Mode de xarxa on la VM té IP pròpia a la LAN |
| **Snapshot** | Captura de l'estat complet d'una VM |
| **Guest Additions** | Conjunt de drivers i utilitats per millorar el rendiment i la integració del guest |
| **VMDK / VDI** | Formats de disc virtual de VMware i VirtualBox respectivament |

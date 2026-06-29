# Actividad 1: Creación de un escritorio virtual con VirtualBox y Ubuntu Linux

## Teoría

### ¿Qué es una máquina virtual?

Una máquina virtual (VM) es un entorno de sistema operativo que se ejecuta dentro de otro sistema operativo mediante software de virtualización. Permite:

- **Aislamiento** — El sistema invitado no interfiere con el anfitrión
- **Portabilidad** — Se puede mover entre ordenadores físicos
- **Snapshots** — Capturar el estado de la VM para poder restaurarlo
- **Requisitos mínimos** — No hace falta hardware dedicado

### Oracle VirtualBox

**VirtualBox** es un hypervisor de tipo 2 (alojado) gratuito y de código abierto mantenido por Oracle. Características principales:

- **Gratuito** — Sin licencias, incluso para uso comercial
- **Multiplataforma** — Se instala en Windows, macOS, Linux y Solaris
- **Soporte amplio** — Virtualiza la mayoría de sistemas x86/x86_64
- **Guest Additions** — Drivers y herramientas de mejora para el sistema invitado (acceso al portapapeles, carpetas compartidas, pantalla redimensionable)
- **xHCI / USB 3.0** — Soporte nativo para dispositivos USB

### ¿Por qué elegir Ubuntu Linux?

Ubuntu es una de las distribuciones Linux más populares, basada en Debian. Ventajas para entornos IoT y desarrollo:

- **LTS (Long Term Support)** — Versiones estables con 5 años de soporte
- **Repositorios extensos** — Paquetes actualizados para herramientas de desarrollo
- **Comunidad activa** — Documentación abundante y soporte en línea
- **ESP-IDF y herramientas embebidas** — Soporte completo para toolchains cruzadas
- **Snap y APT** — Gestores de paquetes modernos

### Arquitectura de virtualización

```
┌─────────────────────────────────────────────┐
│     Ordenador físico (Host)                 │
│  Windows / macOS / Linux                    │
│  ┌───────────────────────────────────────┐  │
│  │  Oracle VirtualBox (Hypervisor)       │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │  Máquina virtual (Guest)        │  │  │
│  │  │  Ubuntu 26.04 LTS               │  │  │
│  │  │  vCPU: 2 │ RAM: 4 GB │ 50 GB   │  │  │
│  │  │  ┌───────────────────────────┐  │  │  │
│  │  │  │  Guest Additions          │  │  │  │
│  │  │  │  (Drivers + herramientas) │  │  │  │
│  │  │  └───────────────────────────┘  │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Terminología clave

| Término | Descripción |
|---------|------------|
| **Host** | Sistema operativo anfitrión donde se ejecuta VirtualBox |
| **Guest** | Sistema operativo invitado dentro de la VM |
| **Hypervisor** | Software que gestiona las máquinas virtuales |
| **vCPU** | Núcleo de CPU virtual asignado a la VM |
| **VRAM** | Memoria de vídeo dedicada a la VM |
| **NAT** | Modo de red por defecto: la VM comparte la IP del host |
| **Bridge** | Modo de red donde la VM tiene IP propia en la LAN |
| **Snapshot** | Captura del estado completo de una VM |
| **Guest Additions** | Conjunto de drivers y utilidades para mejorar el rendimiento e integración del guest |
| **VMDK / VDI** | Formatos de disco virtual de VMware y VirtualBox respectivamente |

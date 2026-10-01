# POLARIS — Catálogo de sensores, nodos y gateway (referencia)

**Estado:** DESIGNED (integración física FUTURE_WORK; simulación por fases)  
**Hardware de referencia declarado:** Raspberry Pi 5 (gateway), **STM32 NUCLEO N657X0-Q** (nodo MCU, serie N6) — ver [ADR-0008](../adr/0008-edge-hardware-reference.md)

---

## Principio

POLARIS **no** despliega “todos los sensores del mundo” en cada sitio. Cada **SiteProfile** declara:

- `priority_hazards[]`
- `sensor_configuration[]` (tipos, buses, calibración, frecuencia)
- `communication_profile` (LoRa, LTE, Wi‑Fi, store-and-forward, …)
- `energy_profile`

El catálogo global define **tipos medibles reutilizables**; el sitio elige un subconjunto.

---

## Capas de medición (variables, no marcas)

| Capa | Variables típicas | Uso en hazards |
|------|-------------------|----------------|
| Meteorología | T, RH, presión, viento, ráfaga, radiación, lluvia acumulada | heat, cyclone, wildfire, flood, drought |
| Hidrología | nivel agua, caudal, velocidad flujo | flood, flash flood, tsunami (coastal) |
| Suelo / pendiente | humedad suelo, inclinación, desplazamiento mm | landslide, erosion |
| Geofísica | aceleración, velocidad, inclinación estructural | earthquake, volcano, subsidence |
| Ambiente | PM2.5/PM10, CO, gas, visibilidad | smoke, wildfire, volcano |
| Energía / salud nodo | V, I, SOC, temperatura PCB | resiliencia, no hazard directo |
| Posición / tiempo | GNSS fix, PPS | georreferencia, EEW timing |

---

## Mapa hazard → observaciones → familias de sensor

| Hazard (POLARIS) | Modos | Observaciones mínimas | Familias de nodo |
|------------------|-------|------------------------|------------------|
| River / pluvial flood | forecast, nowcast, detection | lluvia, nivel río/cuenca, opcional suelo | Hydro, Weather |
| Flash flood | nowcast, rapid detection | lluvia intensa, nivel arroyo, radar pluvial si disponible | Hydro, Weather |
| Landslide | susceptibility, nowcast | inclinómetro, desplazamiento, humedad suelo, lluvia | Slope |
| Wildfire | risk, detection, propagation | humedad combustible, T/RH/viento, PM, cámara IR opcional | Fire, Weather |
| Drought | outlook, monitoring | lluvia acumulada, humedad suelo, NDVI (satélite) | Weather, Slope |
| Heat | forecast | T, humedad, índices derivados | Weather, Urban |
| Cyclone / typhoon | forecast, impact | presión, viento, lluvia, oleaje (costa) | Weather, Coastal |
| Smoke | detection, forecast | PM2.5, visibilidad | Air quality |
| Earthquake | rapid detection, EEW, impact | acelerómetro (no predicción) | Seismic (experimental) |
| Tsunami | event-triggered | presión marina, nivel mar, trigger sísmico | Coastal + Seismic |
| Volcano | monitoring | gas (SO₂, CO₂), inclinación, sismica local | Volcano |
| Erosion / subsidence | monitoring | inclinación, GNSS, nivel | Slope, Structural |

**CHI:** solo cuando dos capas comparten un sitio (ej. lluvia + pendiente → flood + landslide).

---

## Familias de nodo de referencia (SKU lógicos)

| Familia | Sensores típicos (interfaces) | MCU típico | Notas |
|---------|----------------------------------|------------|--------|
| **Weather Node** | pluviómetro, T/RH (I²C), presión, anemómetro (pulso/UART) | STM32 N657X0-Q | bajo consumo, muestreo 1–15 min |
| **Hydro Node** | ultrasonido/radar nivel, presión hidrostática, caudómetro | STM32 N657X0-Q | crítico para flood detection |
| **Slope Node** | inclinómetro, crack meter, humedad suelo | STM32 | landslide |
| **Fire Node** | T ambiente, humedad combustible, PM | STM32 | wildfire |
| **Urban Node** | T/RH, ruido, PM, opcional cámara | Pi 5 o STM32+Pi | ciudad densa |
| **Seismic Node** | MEMS/geófono (experimental) | STM32 N6 (DSP/ML edge opcional) | **nunca** “predicción” |
| **Coastal Node** | nivel mar, presión, oleaje | STM32 + gateway robusto | tsunami/cyclone costa |
| **Air / Volcano Node** | electrochemical / NDIR gas | STM32 | volcano, smoke |
| **Gateway** | radio(s), backhaul, buffer, hora | **Raspberry Pi 5** (+ HAT LoRa/LTE) | store-and-forward |
| **Edge concentrator** | agregación local, reglas no críticas | Pi 5 o N6 según ADR | no sustituye autoridad alerta |

Cantidad **física** por sitio: típicamente **3–12 nodos** + **1–2 gateways**; simulación puede modelar **N nodos virtuales** por escenario.

---

## Gateway — estructura lógica

```
[Sensores] → [Bus: I²C/SPI/UART/1-Wire/ADC] → [STM32 nodo: sample → QC → pack → TX]
      → [Radio sub-GHz / LoRaWAN / Wi‑Fi] → [Gateway Pi 5: RX → buffer → ingest_time + event_time]
      → [Backhaul: Ethernet / LTE / satellite] → [POLARIS Core API / MQTT]
```

Responsabilidades **Gateway (Pi 5)**:

- sincronización de tiempo (NTP/GNSS cuando exista)
- cola persistente si backhaul cae (**store-and-forward**)
- no reescribir `event_time` con hora de llegada
- health: RSSI, packet loss, firmware version
- opcional: LoRaWAN network server local (ChirpStack) — ADR si se adopta

Responsabilidades **Nodo (STM32 NUCLEO N657X0-Q)**:

- máquina de estados: BOOT → SELF_TEST → SAMPLE → FILTER → PACKAGE → TRANSMIT → SLEEP
- calibración versionada en flash
- watchdog, brownout, bajo consumo
- ML en edge **solo** no crítico (ej. detección de artefacto); PHI/alerta oficial **no** en LLM/ML opaco

---

## Comunicaciones y antenas (Forge)

Multi-bearer por **SiteProfile** — no solo LoRaWAN.

| Bearer | Rol típico | Antena (ingeniería sistema) |
|--------|------------|-----------------------------|
| LoRa / sub-GHz | nodos → gateway rural | monopolo/Yagi según enlace; link budget FSPL |
| Wi‑Fi | urbano corto alcance | PCB trace / externa 2.4/5 GHz |
| Ethernet | gateway fijo | cableado |
| LTE / 4G / 5G / LTE-M / NB-IoT | backhaul | integrada o externa; no simular PHY completo |
| Satellite / NTN | respaldo remoto | patch/planar; latencia alta |
| Store-and-forward | gateway offline | N/A |

Forge modela: potencia TX, sensibilidad RX, pérdidas, duty cycle LoRa (SF/BW/CR), latencia, pérdida de paquetes, interferencia — **no** sustituye simulación electromagnética de onda completa (ADR/antenna EM validation aparte).

---

## Calidad de sensor (simulación obligatoria)

Por sensor: valor verdadero → respuesta → bias, drift, ruido, cuantización, saturación, dropout, fallo, consumo energético (ver README_SIMULATION_ENGINEERING).

**GCI** en plataforma refleja: frescura, completitud, acuerdo entre fuentes, flags QC.

---

## Evidencia en repo (V1 IoT sim slice)

| Componente | Evidencia |
|------------|-----------|
| Catálogo `configs/devices/` (`weather-node`, `hydro-node`, `gateway-pi5`) | IMPLEMENTED (SIMULATED) |
| Modelos lluvia + nivel | IMPLEMENTED en `simulation/python/iot/sensors.py` |
| Enlace LoRa abstracto + FSPL stub | IMPLEMENTED en `simulation/python/iot/comm.py` |
| Gateway Pi 5 + store-and-forward | IMPLEMENTED en `simulation/python/iot/gateway.py` |
| Pipeline → GCI → PHI → DRAFT | IMPLEMENTED vía `run_flood_slice` (lluvia → PHI; nivel ingestado) |
| Firmware | PLACEHOLDER (`firmware/node/main.c`, `firmware/gateway/gateway_stub.py`) |
| Hardware desplegado / LIVE IoT | NOT IMPLEMENTED |

Runner: `python -m simulation.python.iot_run --scenario simulation/scenarios/iot-bogota-demo.yaml --seed 42`  
API: `POST /v1/ingest/iot`

---

## Conteo honesto

| Concepto | Número |
|----------|--------|
| Familias de nodo de referencia | **9** (+ gateway) |
| Tipos de variable medible (catálogo) | **~25–35** (según granularidad) |
| Sensores físicos distintos en un despliegue multi-hazard típico | **~8–15** tipos, **3–12** nodos |
| Hazards en scope POLARIS | **12+** — cubiertos por **combinación** de familias, no 1 sensor = 1 hazard |
| Implementado hoy en repo | **2** nodos lógicos SIMULATED + gateway sim; sin PCB producción |

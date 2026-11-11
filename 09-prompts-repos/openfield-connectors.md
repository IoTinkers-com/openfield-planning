# Prompt de arranque · openfield-connectors

Rol: adaptadores a dispositivos/sistemas externos + `simulators/` de OpenField (IoTinkers).

## Contexto obligatorio (leer antes de empezar)
- `openfield-planning/AGENTS.md` — reglas.
- `openfield-planning/DECISIONS.md` — decisiones D1–D17.
- `openfield-planning/03-adr/` — en especial ADR-0001 (térmica), ADR-0010 (simulación),
  ADR-0009 (contratos), ADR-0016 (límite industrial).
- `openfield-planning/04-esquemas/` — contrato que los adaptadores **EMITEN**
  (`thermal-capture`, `observation`, `media-item`, `session`).
- `openfield-planning/07-simulacion-y-pruebas.md` — simuladores y pruebas de contrato.

## Principio
Los **simuladores son las pruebas de contrato** de los adaptadores reales (D10). Un adaptador
real es aceptable solo si pasa las mismas pruebas que su simulador.

## Simuladores (Fase 0)
1. Cámara térmica T0–T2 · 2. Repetición de sesiones + rutas GPX · 3. Inventario ficticio
QR/TAG · 4. Telemetría MQTT (detalle en `07-simulacion-y-pruebas.md`).

## Adaptadores (Pro / Industrial)
- `thermal/` — Lepton 3.5 (T2), MLX90640 (T1) vía `flirpy` (MIT) → contrato canónico.
- `gps/` — NMEA → WGS84.
- `onvif/` — `@2bad/onvif` (MIT) [Industrial].
- `opcua/` — `node-opcua` / `open62541` [Industrial].
- `sensorthings/` — OGC SensorThings [Industrial].

## Integración de tecnologías propietarias (ADR-0001)
FLIR/Seek **no se excluyen**: se integran vía SDK o wrappers open source en la capa de
adaptador, normalizando al contrato canónico y conservando el original como evidencia.

## Criterios de aceptación
Fase 0: los 4 simuladores generan documentos que pasan `04-esquemas/` (via `validate_schemas.py`).
Pro: cada adaptador real pasa las pruebas de contrato de su simulador. Industrial: conectores
OPC UA/ONVIF/SensorThings pasan las mismas pruebas.

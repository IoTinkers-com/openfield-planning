# 01 · Niveles de escalamiento

> Estado: borrador · Tanda A · OpenField (IoTinkers)

## 1. Definición de niveles
| Nivel | Definición | Criterio de entrada | Criterio de salida |
| --- | --- | --- | --- |
| **Maker** | Costo cercano a cero; hardware de consumo o simulado. | Fase 0, sin hardware. | Flujo completo validado en simulación. |
| **Pro** | Pilotos reales y pagados; hardware intermedio. | 1 cliente piloto. | Flujo real estable + térmica radiométrica. |
| **Industrial** | Certificable e integrable (OPC UA, ONVIF, CMMS/SCADA/GIS). | Requisitos de cliente o regulación. | Conectores que pasan pruebas de contrato. |

## 2. Escalamiento por repositorio

### 2.1 `openfield-wearable`
- **Maker:** PWA en navegador + simuladores; térmica T0 (imagen con paleta, simulada).
- **Pro:** PWA + Capacitor; térmica T1 (MLX90640 32×24) y T2 (Lepton 3.5 vía USB); Whisper local.
- **Industrial:** app nativa/ruggedizada; T3 (alta resolución + parámetros de calibración); cámaras OPC UA/ONVIF.

### 2.2 `openfield-platform`
- **Maker:** Docker local, monousuario, SQLite + filesystem.
- **Pro:** VPS; Postgres+PostGIS + object storage; export STAC y OGC API Features (lectura).
- **Industrial:** on-premise; multiempresa; retención legal; alta disponibilidad.

### 2.3 `openfield-connectors`
- **Maker:** simuladores (térmica T0–T2, repetición de sesiones, rutas GPX, inventario QR/TAG, telemetría MQTT).
- **Pro:** adaptadores reales (térmica USB/BLE, GPS, tus).
- **Industrial:** OPC UA, ONVIF, SensorThings, CMMS/SCADA/GIS.

## 3. Tabla por dimensión
| Dimensión | Maker | Pro | Industrial |
| --- | --- | --- | --- |
| Hardware de captura | Teléfono de consumo / emulador | Teléfono + térmica T1–T2 | Equipo dedicado, T3, cámaras IP |
| Conectividad | Wi-Fi | Celular 4G/5G + Wi-Fi | VPN, MQTT, OPC UA |
| Almacenamiento | SQLite + filesystem | Postgres+PostGIS + objetos | + archivado y retención legal |
| Despliegue | Docker local | VPS (demo) | On-premise |
| Usuarios | 1 (`tenant_id` ya presente) | Piloto (1–pocos) | Multiempresa |
| Estándares de datos | JSON Schema propio | + STAC, GeoJSON, OGC API Features | + OPC UA, ONVIF, SensorThings |

## 4. Regla de paso entre niveles
Un nivel superior **no reescribe** el contrato de datos: agrega capacidad manteniendo el
contrato canónico (D9). El paso Maker→Pro es acumulativo; Pro→Industrial agrega estándares
de integración sin cambiar el núcleo de captura/estructuración.

## 5. Decisión / Supuesto / Pregunta abierta
- **Decisión:** los 3 niveles y su definición (D1, D5, D9, D16).
- **Supuesto:** el hardware intermedio de Pro (MLX90640, Lepton 3.5) es el indicado en D1; su disponibilidad/precio vigentes se verifican al comprar en Fase 2 — `[VERIFICAR]`.
- **Supuesto:** "Industrial" llega cuando un cliente lo exija, no por defecto.
- **Pregunta abierta:** ¿el on-premise Industrial se entregará como Docker Compose, Helm o binario? → se decide en `05-estructura-repos.md`.

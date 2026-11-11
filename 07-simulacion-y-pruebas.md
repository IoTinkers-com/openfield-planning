# 07 · Simulación y pruebas

> Estado: borrador · Tanda D · OpenField (IoTinkers)

## 1. Principio
Los **simuladores son las pruebas de contrato** (D10 · ADR-0010): emiten exactamente lo que un
adaptador real emitiría, y un conector real es aceptable solo si pasa las mismas pruebas que su
simulador. La Fase 0 se completa sin hardware.

## 2. Catálogo de simuladores
| Simulador | Qué emite | Contrato que ejercita |
| --- | --- | --- |
| Cámara térmica T0–T2 | `ThermalCapture` (T0 paleta; T1/T2 matriz °C) + `MediaItem` thermal | D1 (T0–T3) |
| Repetición de sesiones grabadas | `Session` + `MediaItem` (RGB/audio) de una sesión real | D4 (offline-first) |
| Rutas GPX | `Session.location` / `MediaItem.geometry` (WGS84) | D2 (georreferenciación) |
| Inventario ficticio con QR/TAG | `Asset` + `AssetIdentifier` + `Observation` | D3, ADR-0017 |
| Telemetría MQTT | `Observation` (SensorThings) vía broker local | D9 (SensorThings) |

Todos los simuladores viven en `openfield-connectors/simulators/` y generan documentos que
validan contra `04-esquemas/` (via `validate_schemas.py`).

## 3. Pruebas de contrato
Para cada adaptador real existe un par (simulador, adaptador) que debe cumplir lo mismo:
1. **Emitir el mismo esquema** (validación JSON Schema idéntica).
2. **Mismo nivel de capacidad** (p. ej. adaptador T2 vs simulador T2: misma forma de
   `temperature_matrix_c` y `resolution`).
3. **Mismos campos mínimos** (`schema_version`, `tenant_id`, `id`, vínculos `asset_id`).

El simulador fija la referencia; el adaptador real la persigue.

## 4. Criterios de aceptación por nivel
| Nivel | Criterio de aceptación |
| --- | --- |
| **Maker** | Fase 0: los 5 simuladores generan documentos que pasan `validate_schemas.py`; el flujo completo (captura→presentación) corre local con datos simulados, sin comprar nada. |
| **Pro** | Cada adaptador real (térmica USB/BLE, GPS, tus) pasa las pruebas de contrato de su simulador; un piloto real ingiere datos end-to-end. |
| **Industrial** | Los conectores OPC UA/ONVIF/SensorThings pasan las mismas pruebas de contrato; la exportación STAC/OGC API Features es leíble por herramientas externas. |

## 5. Relación con el arnés
- `validate_schemas.py` valida ejemplos contra esquemas (ya en verde con 11 esquemas).
- En Fase 0, los simuladores se ejecutan como scripts que escriben documentos y se validan con
  el mismo arnés, garantizando paridad simulador↔adaptador.

## 6. Decisión / Supuesto / Pregunta abierta
- **Decisión:** los 5 simuladores de D10 son el conjunto mínimo de pruebas de contrato.
- **Decisión:** la aceptación de un conector real se mide por pasar las pruebas de su simulador.
- **Supuesto:** en Fase 0 los simuladores son scripts deterministas (misma entrada → misma salida) para poder usarse como *golden files*.
- **Pregunta abierta:** ¿los *golden files* se guardan como fixtures versionados en `contracts/`? → se decide al iniciar Fase 1.

# 06 · Backlog MVP

> Estado: borrador · Tanda E · OpenField (IoTinkers)
> Caso de uso principal: inventario de equipos eléctricos/industriales (D12).
> Regla de trazabilidad: cada historia cita el ADR de su decisión (`check_traceability.py`).

## Fases
- **Fase 0 — sin hardware:** validar el flujo completo con simuladores, sin comprar nada (D10).
- **Fase 1 — flujo real mínimo:** app PWA + plataforma en VPS, con un piloto real.
- **Fase 2 — primer hardware:** térmica radiométrica real (T1/T2) y prueba en iPhone.

---

## Fase 0 — Sin hardware (simulado)

### Épica 0-A: Plataforma y contrato de datos (ADR-0005, ADR-0009, ADR-0013)

- [ ] H0-A1: Repositorio `openfield-platform` con Docker Compose (API + PostgreSQL/PostGIS + object storage local) (ADR-0005).
  - **Criterios:** `docker compose up` levanta todos los servicios; el endpoint de salud responde 200.
  - **Dependencias:** ninguna.

- [ ] H0-A2: Los 11 JSON Schemas como fuente de verdad y validados en CI (ADR-0009).
  - **Criterios:** `validate_schemas.py` pasa; cada esquema tiene ≥1 ejemplo válido y ≥1 inválido.
  - **Dependencias:** H0-A1.

- [ ] H0-A3: Ingesta con validación contra el esquema y dedupe por `id` (ADR-0004, ADR-0009).
  - **Criterios:** un documento sin `tenant_id` es rechazado con error legible; reenviar el mismo `id` no crea duplicado.
  - **Dependencias:** H0-A2.

- [ ] H0-A4: `tenant_id` en toda consulta/persistencia, aun con un solo usuario (ADR-0013).
  - **Criterios:** los datos de un tenant no son visibles para otro.
  - **Dependencias:** H0-A2.

### Épica 0-B: Simuladores como pruebas de contrato (ADR-0010)

- [ ] H0-B1: Simulador de cámara térmica T0–T2 (ADR-0001, ADR-0010).
  - **Criterios:** genera `ThermalCapture` válido para T0 (matriz null) y T2 (matriz °C + resolución); pasa `validate_schemas.py`.
  - **Dependencias:** H0-A2.

- [ ] H0-B2: Simulador de inventario con QR/TAG equivalentes (ADR-0003, ADR-0017).
  - **Criterios:** dos identificadores (p. ej. QR y TAG) resuelven al mismo `Asset`.
  - **Dependencias:** H0-A2.

- [ ] H0-B3: Simulador de repetición de sesiones grabadas + rutas GPX (ADR-0002, ADR-0004).
  - **Criterios:** reproduce `Session` + `MediaItem` con `geometry` WGS84 y `captured_at` del dispositivo.
  - **Dependencias:** H0-B1.

- [ ] H0-B4: Simulador de telemetría MQTT → `Observation` (ADR-0009).
  - **Criterios:** un tópico MQTT produce `Observation` con `observed_at` (= phenomenonTime).
  - **Dependencias:** H0-A2.

### Épica 0-C: Presentación mínima (ADR-0002, ADR-0009)

- [ ] H0-C1: Dashboard web con mapa (Leaflet) + galería de medios (ADR-0002).
  - **Criterios:** los medios con `geometry` aparecen en el mapa en su coordenada; los de interior se listan junto al activo.
  - **Dependencias:** H0-A3.

---

## Fase 1 — Flujo real mínimo

### Épica 1-A: App de captura PWA (ADR-0008, ADR-0004)

- [ ] H1-A1: PWA que captura RGB + GPS + audio, genera `Session`/`MediaItem` y encola localmente (ADR-0004, ADR-0008).
  - **Criterios:** funciona sin conexión; genera `id` único en el dispositivo; la cola persiste en IndexedDB.
  - **Dependencias:** H0-A3.

- [ ] H1-A2: Indicador visible de grabación + registro de consentimiento (ADR-0015).
  - **Criterios:** no se captura sin consentimiento registrado; el indicador es visible durante la grabación.
  - **Dependencias:** H1-A1.

- [ ] H1-A3: Subida reanudable con `tus` a la plataforma (ADR-0004).
  - **Criterios:** una subida interrumpida se reanuda desde el byte anterior sin reenviar todo.
  - **Dependencias:** H1-A1.

- [ ] H1-A4: Transcripción local (Whisper) con `engine` registrado y respaldo en plataforma (ADR-0007).
  - **Criterios:** cada `Transcript` declara su `engine`; si el dispositivo no puede, la plataforma transcribe.
  - **Dependencias:** H1-A1.

### Épica 1-B: Plataforma en VPS demo (ADR-0005)

- [ ] H1-B1: Desplegar el stack Docker Compose en un VPS con HTTPS (ADR-0005, ADR-0011).
  - **Criterios:** la PWA del iPhone accede por HTTPS (túnel Cloudflare o dominio).
  - **Dependencias:** H0-A1, H1-A3.

- [ ] H1-B2: Export STAC + OGC API Features de lectura (ADR-0009).
  - **Criterios:** cada `MediaItem` se expone como STAC Item (id, geometry, datetime, assets) y se consulta por OGC API Features.
  - **Dependencias:** H0-A3.

### Épica 1-C: Estructuración por plantillas (ADR-0006, ADR-0017)

- [ ] H1-C1: `FormTemplate`/`FormResponse` configurables para inventario (ADR-0006).
  - **Criterios:** crear una plantilla y responderla vinculada a `asset_id`; los campos validan contra la plantilla.
  - **Dependencias:** H0-A3.

- [ ] H1-C2: Resolución de identificadores (QR/TAG/OCR) a `Asset` canónico (ADR-0003, ADR-0017).
  - **Criterios:** dado un valor leído, se resuelve al activo y se desambigua explícitamente (no por similitud).
  - **Dependencias:** H0-B2.

---

## Fase 2 — Primer hardware

### Épica 2-A: Térmica radiométrica real (ADR-0001)

- [ ] H2-A1: Adaptador Lepton 3.5 (T2) → contrato canónico (ADR-0001).
  - **Criterios:** pasa las mismas pruebas de contrato que el simulador T2 (misma forma de `temperature_matrix_c` y `resolution`).
  - **Dependencias:** H0-B1, Fase 1 completa.

- [ ] H2-A2: Adaptador MLX90640 (T1) → contrato canónico (ADR-0001).
  - **Criterios:** pasa las pruebas de contrato del simulador T1.
  - **Dependencias:** H0-B1.

### Épica 2-B: Prueba en iPhone real (ADR-0008, ADR-0011)

- [ ] H2-B1: Validar límites de Safari/iOS (Background Sync, purga IndexedDB, GPS en primer plano, WASM Whisper) (ADR-0008, ADR-0011).
  - **Criterios:** documento con qué funciona y qué no en el iPhone; el flujo offline no depende de Background Sync.
  - **Dependencias:** H1-A1.

---

## Trazabilidad
Todo ítem `- [ ]` cita al menos un ADR. `check_traceability.py` verifica que cada ADR citado existe
y declara `Estado:`. Los criterios de aceptación son verificables de forma automática o manual
(fase por fase). Fase 0 se completa sin comprar nada.

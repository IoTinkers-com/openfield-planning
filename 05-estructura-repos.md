# 05 · Estructura de repositorios

> Estado: borrador · Tanda D · OpenField (IoTinkers)

## 1. Vista general
4 repos bajo la organización GitHub `iotinkers-com`. Los 3 de código se diseñan para que el
**contrato de datos** (JSON Schemas) sea el punto de acople, no el código compartido.

| Repo | Rol | Nivel que cubre |
| --- | --- | --- |
| `openfield-wearable` | Captura (PWA, firmware, hardware de referencia) | Maker → Pro → Industrial |
| `openfield-platform` | Backend, ingesta, almacenamiento, estructuración, UI, informes | Maker → Pro → Industrial |
| `openfield-connectors` | Adaptadores a dispositivos/sistemas externos + `simulators/` | Maker → Pro → Industrial |
| `openfield-planning` | Este paquete documental | — |

## 2. Árbol por repositorio

### 2.1 `openfield-wearable`
```
openfield-wearable/
├── app/                  # PWA (TypeScript)
│   ├── src/
│   │   ├── hardware/     # capa de acceso desacoplada (cámara, GPS, mic, térmica)
│   │   ├── capture/      # sesiones, medios, consentimiento (D15)
│   │   ├── queue/        # cola local (IndexedDB) + tus-js-client (D4)
│   │   ├── transcribe/   # Whisper local (WASM) o respaldo (D7)
│   │   └── schema/       # validación local contra el contrato
│   ├── public/           # manifest + service worker
│   └── capacitor/        # wrappers nativos (después, D8)
├── firmware/             # firmware de referencia (Pro/Industrial)
├── hardware/             # hardware de referencia (CERN-OHL, D14)
└── tests/                # pruebas de captura y límites de plataforma
```

### 2.2 `openfield-platform`
```
openfield-platform/
├── schemas/              # JSON Schemas canónicos (fuente de verdad) + ejemplos
├── api/                  # ingesta (FastAPI): endpoints + tus + autenticación
├── domain/               # sesiones, assets, medios, observaciones, formularios
├── storage/              # Postgres+PostGIS + object storage (interfaz S3)
├── export/               # STAC + OGC API Features (pygeoapi)
├── ui/                   # dashboard web (mapa + galería + informes)
├── workers/              # transcripción de respaldo, estructuración asistida (D6)
└── deploy/               # docker-compose (local/VPS/on-premise)
```

### 2.3 `openfield-connectors`
```
openfield-connectors/
├── simulators/           # térmica T0–T2, GPX, inventario QR/TAG, telemetría MQTT (D10)
├── adapters/
│   ├── thermal/          # FLIR/Seek/MLX90640 -> contrato canónico (D1)
│   ├── gps/              # NMEA -> WGS84 (D2)
│   ├── onvif/            # cámaras IP (Industrial)
│   ├── opcua/            # OPC UA (Industrial)
│   └── sensorthings/     # SensorThings (Industrial)
├── contracts/            # pruebas de contrato (idénticas para simulador y real)
└── tests/
```

## 3. Responsabilidades por repo
- **wearable**: producir `Session`, `MediaItem`, `ThermalCapture`, `Transcript`, `SyncEvent`
  conforme al contrato; offline-first (D4); no persiste nada fuera de su cola local.
- **platform**: recibir, validar, almacenar y estructurar; exponer STAC/OGC API Features;
  es la fuente de verdad de `Asset`/`AssetIdentifier`/`FormTemplate`/`FormResponse`.
- **connectors**: traducir entradas externas al contrato canónico (o exportar desde él);
  `simulators/` emite exactamente lo mismo que un adaptador real.

## 4. Contratos entre repos
- **Contrato de datos (canónico):** los JSON Schemas de `04-esquemas/` viven como fuente de
  verdad en `openfield-platform/schemas/`. Los otros repos los consumen como dependencia
  versionada (`openfield-schemas` empaquetado o copia *vendored* con chequeo de paridad en CI).
  Regla: solo se agregan campos (D9); un sensor nuevo no toca plataforma (D1, D10).
- **Contrato de ingesta:** API autenticada (HTTP + `tus` para medios); dedupe por `id`; la
  plataforma valida contra el esquema y rechaza con error legible.
- **Contrato de exportación:** STAC y OGC API Features (lectura) desde Pro; SensorThings/OPC
  UA/ONVIF solo mediante conectores en Industrial (D9).

## 5. CI mínimo por repo
| Repo | Chequeos en CI |
| --- | --- |
| `openfield-planning` | `validate_schemas.py`, `check_traceability.py`, `check_docs.py` |
| `openfield-wearable` | lint + build PWA + validación de fixtures contra el contrato |
| `openfield-platform` | lint + tests de ingesta + `validate_schemas.py` + export STAC |
| `openfield-connectors` | pruebas de contrato: simulador y adaptador real deben pasar lo mismo |

CI = GitHub Actions (org `iotinkers-com`). Un commit por tanda es la práctica de referencia.

## 6. Catálogo de componentes open source
| Componente | Rol | Licencia | Riesgo de abandono | Alternativa |
| --- | --- | --- | --- | --- |
| FastAPI | API/ingesta | MIT | Bajo (activo) | Starlette (MIT) |
| PostgreSQL + PostGIS | Metadatos espaciales | PostgreSQL License / GPLv2+ | Bajo | SQLite (Maker) |
| SeaweedFS | Object storage | Apache-2.0 | Comunidad menor que MinIO | MinIO (AGPLv3 + mantenimiento, evitar), RustFS (Apache-2.0, temprano) |
| PySTAC / stac-fastapi / pgSTAC | STAC | Apache-2.0 / MIT / MIT | Bajo | — |
| pygeoapi | OGC API Features | MIT | Bajo | GeoServer (GPL-2.0) |
| Eclipse Mosquitto | MQTT | EPL-2.0 | Bajo | EMQX (Apache-2.0) |
| node-opcua / open62541 | OPC UA | MIT / MPL-2.0 | Bajo | asyncua |
| @2bad/onvif | ONVIF | MIT | Bajo (activo) | node-onvif, onvif (MIT) |
| faster-whisper / whisper.cpp | Audio→texto local | MIT | Bajo | openai/whisper (MIT) |
| Capacitor | Wrapper PWA | MIT | Bajo | — |
| Leaflet / OpenLayers | Mapas | BSD-2 | Bajo | — |
| tusd / tus-js-client / tus-py-client | Subida reanudable | MIT | Bajo | — |
| PROJ / pyproj | Reproyección UTM/SIRGAS2000 | X/MIT | Bajo | — |
| ffmpeg | Procesamiento de video | LGPL-2.1+ (GPL con `--enable-gpl`) | Bajo | — |
| flirpy | Lectura de térmica FLIR | `[VERIFICAR]` (se confirma al adoptar) | Medio (comunidad) | pylepton (`[VERIFICAR]`, antiguo) |

## 7. Decisión / Supuesto / Pregunta abierta
- **Decisión:** los JSON Schemas son la fuente de verdad en `openfield-platform/schemas/`; los demás repos los consumen versionados.
- **Decisión:** el acceso a medios va tras una interfaz S3-compatible — Maker usa filesystem local, Pro usa SeaweedFS (Apache-2.0), Industrial puede usar SeaweedFS multi-nodo o el almacenamiento del cliente.
- **Decisión:** despliegue Maker/Pro = Docker Compose single-host; Industrial on-premise = Docker Compose como base, Helm solo si el cliente ya opera Kubernetes.
- **Supuesto:** el paquete `openfield-schemas` empieza como copia *vendored* + chequeo de paridad, sin publicar a un registro.
- **Pregunta abierta:** ¿registro de paquetes (PyPI/npm) privado o público? → se decide al iniciar Fase 1.

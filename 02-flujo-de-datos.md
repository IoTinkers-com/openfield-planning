# 02 · Flujo de datos

> Estado: borrador · Tanda A · OpenField (IoTinkers)

## 1. Visión del flujo (8 etapas)
```
[captura] → [preprocesamiento] → [transporte] → [ingesta] → [almacenamiento] → [estructuración] → [presentación] → [integración externa]
 wearable       wearable           red           platform       platform           platform          platform          connectors
```
Cada etapa define **tecnología, protocolo y estándar** por nivel (Maker / Pro / Industrial).

## 2. Etapas

### 2.1 Captura
Adquisición de medios y metadatos en el equipo de campo (RGB, térmica, audio).

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | PWA: MediaDevices (getUserMedia), Geolocation, IndexedDB, Service Worker; térmica T0 simulada | HTTP local; WebRTC (live opcional) | W3C Media Capture, Geolocation API, Web App Manifest |
| Pro | PWA + Capacitor; térmica T1 (MLX90640) / T2 (Lepton 3.5) por adaptador | BLE / USB (térmica); GPS NMEA | Contrato canónico térmico (matriz °C + imagen + JSON) |
| Industrial | App nativa/ruggedizada; T3 con calibración; cámaras IP | OPC UA, ONVIF, RTSP | IEC 62541 (OPC UA), ONVIF Profile S/T |

### 2.2 Preprocesamiento en el equipo
Normalización, identificación y encolado local antes de transmitir.

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | JS en navegador: recorte/compresión, ID único (UUID), cola IndexedDB | — (local) | UUID (RFC 4122) |
| Pro | Whisper local (faster-whisper / whisper.cpp); normalización térmica a matriz °C; hash/firma | — (local) | Contrato canónico térmico; formato de transcripción con motor |
| Industrial | Edge compute dedicado; inferencia en borde; calibración radiométrica | — (local) | Parámetros de calibración radiométrica |

### 2.3 Transporte
Envío de medios y metadatos desde el equipo a la plataforma.

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | Wi-Fi local / túnel HTTPS a la máquina de desarrollo | HTTP/HTTPS | TLS |
| Pro | Celular 4G/5G + Wi-Fi; subida reanudable | tus (tus.io) sobre HTTPS; NTP (reloj) | tus v1, HTTPS |
| Industrial | VPN o túnel privado; telemetría y medios separados | MQTT (telemetría) + HTTPS/tus (medios); OPC UA | MQTT 3.1.1/5, OPC UA |

### 2.4 Ingesta
Recepción, autenticación y validación de los datos entrantes.

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | Endpoint HTTP simple (FastAPI local) | HTTP | JSON |
| Pro | API autenticada; endpoint tus; dedupe por ID | HTTPS + tus | JSON Schema (validación), OAuth/JWT |
| Industrial | Servidor OPC UA; ingesta SensorThings; colas | MQTT, OPC UA, ONVIF | SensorThings (OGC), IEC 62541 |

### 2.5 Almacenamiento
Persistencia de medios (binarios) y metadatos (estructurados y espaciales).

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | Filesystem local + SQLite | — | WGS84 (EPSG:4326) |
| Pro | PostgreSQL + PostGIS (metadatos) + object storage (SeaweedFS) para medios | S3-compatible | STAC, GeoJSON, WGS84 |
| Industrial | Igual + archivado, redundancia y retención legal | S3-compatible | + retención según normativa local |

### 2.6 Estructuración
Organización de los datos en sesiones, activos, observaciones y formularios.

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | Formularios manuales (plantillas JSON) | — | JSON Schema (`schema_version`) |
| Pro | Plantillas de formulario/checklist configurables; vínculo activo↔media↔observación | — | JSON Schema, STAC Item |
| Industrial | IA de apoyo + validación humana; normalización para CMMS/SCADA | — | Esquema canónico + mapeos a CMMS |

### 2.7 Presentación
Visualización, consulta e informes.

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | UI web simple (mapa + galería): Leaflet/OpenLayers | HTTP | GeoJSON |
| Pro | Dashboard web + informes (HTML/PDF); STAC browser | HTTP | STAC, OGC API Features |
| Industrial | GIS (QGIS/pygeoapi); dashboards CMMS/SCADA | WMS/WFS, HTTP | OGC API Features, WMS/WFS |

### 2.8 Integración externa
Exportación e interoperabilidad con sistemas del cliente.

| Nivel | Tecnología | Protocolo | Estándar |
| --- | --- | --- | --- |
| Maker | Export JSON/CSV | — | JSON |
| Pro | Export STAC + OGC API Features (lectura) | HTTP | STAC, OGC API Features |
| Industrial | Conectores OPC UA, ONVIF, SensorThings, CMMS/SCADA/GIS | OPC UA, ONVIF, MQTT | IEC 62541, ONVIF, OGC SensorThings |

## 3. Contrato canónico térmico (resumen)
Cuatro niveles de capacidad (D1 · ADR-0001): **T0** imagen con paleta · **T1** matriz de baja
resolución (p. ej. MLX90640 32×24) · **T2** radiométrica media (p. ej. Lepton 3.5) · **T3** alta
resolución con parámetros de calibración. Todo adaptador normaliza a: matriz de temperaturas
en °C + imagen renderizada + JSON (modelo de sensor, resolución, emisividad, temperatura
reflejada, distancia, nivel T0–T3). El original propietario se conserva como evidencia.

## 4. Componentes open source (licencia / riesgo / alternativa)
Catálogo completo en `05-estructura-repos.md`. Selección clave del flujo:

| Componente | Rol | Licencia | Riesgo | Alternativa |
| --- | --- | --- | --- | --- |
| FastAPI | API/ingesta | MIT | Bajo | Starlette (MIT) |
| PostgreSQL + PostGIS | Metadatos espaciales | PostgreSQL License / GPLv2+ | GPL solo si redistribuyes binarios combinados; uso server-side no contagia | SQLite (Maker) |
| SeaweedFS | Object storage | Apache-2.0 | Comunidad menor que MinIO | MinIO (AGPLv3 + repo comunitario en mantenimiento desde dic-2025 — evitar), RustFS (Apache-2.0, temprano) |
| PySTAC / stac-fastapi / pgSTAC | STAC | Apache-2.0 / MIT / MIT | Bajo | — |
| pygeoapi | OGC API Features | MIT | Bajo | GeoServer (GPL-2.0) |
| Eclipse Mosquitto | MQTT | EPL-2.0 | Bajo | EMQX (Apache-2.0) |
| node-opcua / open62541 | OPC UA | MIT / MPL-2.0 | Bajo | asyncua |
| faster-whisper / whisper.cpp | Audio→texto local | MIT | Bajo | openai/whisper (MIT) |
| Capacitor | Wrapper PWA | MIT | Bajo | — |
| Leaflet / OpenLayers | Mapas | BSD-2 | Bajo | — |
| tusd / tus-js-client | Subida reanudable | MIT | Bajo | — |

> Nota: licencias verificadas por búsqueda web (nov-2026). Librerías ONVIF (`node-onvif`,
> `onvif`, `@2bad/onvif`) MIT; ffmpeg LGPL-2.1+ (pasa a GPL si se compila con `--enable-gpl`).

## 5. Decisión / Supuesto / Pregunta abierta
- **Decisión:** las 8 etapas y su asignación a repos (wearable / platform / connectors).
- **Decisión:** WGS84 interno (EPSG:4326) y export a UTM (zona local) sobre SIRGAS2000 / densificación nacional, para Latinoamérica (D2); offline-first (D4).
- **Supuesto:** en Pro, PostGIS se usa como servicio (no se distribuye el binario combinado), por lo que GPLv2+ no fuerza liberar la app.
- **Pregunta abierta:** ¿SeaweedFS o filesystem local para Pro? → se decide en `05-estructura-repos.md`.
- **Decisión:** opciones de túnel HTTPS documentadas en ADR-0011 (Cloudflare Quick Tunnel para pruebas puntuales; túnel con nombre o Tailscale Funnel para URL estable).
- **Pregunta abierta:** con alcance multi-país Latam, la privacidad (D15) exige verificación por país; el marco chileno queda documentado en ADR-0015.

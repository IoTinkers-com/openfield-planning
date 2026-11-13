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

## Mejoras de UX/UI (revisión post-Fase 0/1)

> Hallazgos de la revisión de experiencia/interfaz sobre el dashboard y la PWA de captura ya
> construidos (sin hardware nuevo, sin romper contratos de datos). ADR-0018 documenta cómo se
> mantiene la consistencia visual entre ambas superficies y su navegación cruzada.

### Épica UX-A: Dashboard (ADR-0002, ADR-0009, ADR-0013, ADR-0017, ADR-0018)

- [ ] HUX-A1: Navegación cruzada dashboard ↔ captura mediante un enlace directo en la barra superior de cada superficie (ADR-0018).
  - **Criterios:** un clic desde el dashboard abre `/capture/`; un clic desde la captura vuelve al dashboard.
  - **Dependencias:** H0-C1, H1-A1.

- [ ] HUX-A2: Filtros por `tenant_id` y `entity_type` en el dashboard, reflejados en la URL (ADR-0013, ADR-0009).
  - **Criterios:** cambiar un filtro actualiza el mapa, la galería y la tabla sin recargar la página; la URL resultante es compartible (bookmarkable).
  - **Dependencias:** H0-C1.

- [ ] HUX-A3: Popups del mapa con la miniatura real del medio en vez de solo el `id` (ADR-0002).
  - **Criterios:** el popup de un marcador muestra la imagen de `assets.primary.href` (o un marcador de "sin imagen") y enlaza a su tarjeta en la galería.
  - **Dependencias:** H0-C1.

- [ ] HUX-A4: Agrupar medios por activo (`asset_id`) resolviendo el nombre del `Asset` (ADR-0017).
  - **Criterios:** la galería se organiza en grupos colapsables por activo; un medio sin activo resuelto se etiqueta "Sin activo asignado" en vez de omitirse.
  - **Dependencias:** H0-C1, H0-B2.

- [ ] HUX-A5: Estados vacíos claros cuando no hay medios o no hay resultados con los filtros aplicados (ADR-0018).
  - **Criterios:** sin datos se muestra un mensaje con enlace a `/capture/`; con filtros sin resultados se ofrece un botón "Limpiar filtros".
  - **Dependencias:** HUX-A2.

- [ ] HUX-A6: Layout responsive (móvil/tablet/escritorio) del dashboard (ADR-0008, ADR-0018).
  - **Criterios:** en un viewport de 375px de ancho, los filtros, el mapa y la galería no requieren scroll horizontal.
  - **Dependencias:** H0-C1.

### Épica UX-B: PWA de captura (ADR-0004, ADR-0008, ADR-0015, ADR-0018)

- [ ] HUX-B1: Indicador visual de los pasos del flujo: consentimiento → sesión → captura → sincronizar (ADR-0008, ADR-0015).
  - **Criterios:** el paso activo se resalta; un paso completado cambia de estado visualmente sin recargar la página.
  - **Dependencias:** H1-A1, H1-A2.

- [ ] HUX-B2: Indicador de conexión a internet y contador de elementos pendientes por sincronizar (ADR-0004).
  - **Criterios:** el indicador cambia entre "en línea" y "sin conexión" con los eventos `online`/`offline` del navegador; el contador de pendientes refleja el tamaño real de la cola local.
  - **Dependencias:** H1-A1, H1-A3.

- [ ] HUX-B3: Mensajes de error amigables en español para fallas de cámara, micrófono o red, sin perder el detalle técnico en el registro/log (ADR-0008).
  - **Criterios:** un permiso denegado o una falla de red muestra un mensaje accionable (qué hacer), no el mensaje crudo del navegador; el log conserva el detalle técnico.
  - **Dependencias:** H1-A1.

- [ ] HUX-B4: Diseño móvil-first con objetivos táctiles grandes y navegación de vuelta al dashboard (ADR-0008, ADR-0018).
  - **Criterios:** los botones principales son usables con el pulgar en un iPhone; existe un enlace visible de vuelta al dashboard en todo momento.
  - **Dependencias:** H1-A1.

---

## Presentación centrada en el activo (asset dossier)

> El activo (no el documento) es la unidad central de presentación (ADR-0019, deriva de D12
> y ADR-0017). Agregación de solo lectura sobre `documents`; no cambia `04-esquemas/`.

### Épica UX-C: Expediente de activo y vista de sesión (ADR-0002, ADR-0009, ADR-0013, ADR-0017, ADR-0018, ADR-0019)

- [ ] HUX-C1: `GET /assets/{id}` agrega identificadores, sesiones, medios, observaciones, transcripciones y respuestas de formulario del activo, incluidos los vinculados solo por `session_id` (ADR-0019, ADR-0013).
  - **Criterios:** respeta `tenant_id` del activo; un documento sin `asset_id` propio pero cuya sesión pertenece al activo aparece igual en el expediente; `404` si el activo no existe.
  - **Dependencias:** H0-A3, H0-B2, H1-C1.

- [ ] HUX-C2: `GET /sessions/{id}` agrega los medios, observaciones y transcripciones de una sesión, con el resumen del activo al que pertenece (ADR-0019).
  - **Criterios:** `404` si la sesión no existe; incluye un resumen `{id, name}` del activo cuando `asset_id` no es `null`.
  - **Dependencias:** H0-A3.

- [ ] HUX-C3: Una sola ruta sirve la vista HTML o el JSON agregado según el encabezado `Accept`, sin introducir un prefijo `/api` (ADR-0019, ADR-0018).
  - **Criterios:** una navegación de navegador (`Accept: text/html`) recibe la vista; un `fetch()`/prueba automatizada recibe el JSON agregado en la misma URL.
  - **Dependencias:** HUX-C1, HUX-C2.

- [ ] HUX-C4: Navegación dashboard → expediente de activo → vista de sesión → medio original (ADR-0017, ADR-0018, ADR-0019).
  - **Criterios:** el nombre del activo en la agrupación del dashboard enlaza a su expediente; cada sesión del expediente enlaza a su vista; cada medio enlaza al archivo original.
  - **Dependencias:** HUX-A4, HUX-C1, HUX-C2.

- [ ] HUX-C5: La tabla "Registro" del dashboard pasa a un panel secundario colapsado por defecto (ADR-0019).
  - **Criterios:** al cargar el dashboard, el registro de documentos está colapsado; el mapa, la galería por activo y los expedientes son la vista principal.
  - **Dependencias:** HUX-A2.

---

## Gestión de activos (registro, ciclo de vida y precarga)

> OpenField como plataforma de control y seguimiento del estado de activos industriales:
> registro con atributos configurables por tipo (ISO 55001 §7.5/7.6, estructura ISO 14224),
> ciclo de vida con desincorporación no destructiva, auditoría de cambios y precarga CSV
> con verificación en terreno (ADR-0020, ADR-0021, ADR-0022).

### Épica GA: Registro y ciclo de vida (ADR-0020, ADR-0021, ADR-0013)

- [ ] GA-1: Esquema `asset-type` y campos nuevos de `Asset`, en paridad en los 4 repos (ADR-0020, ADR-0009).
  - **Criterios:** `validate_schemas.py` pasa con 12 esquemas en planning, platform, wearable y connectors; cada ejemplo nuevo valida/falla según corresponda.
  - **Dependencias:** H0-A2.
- [ ] GA-2: CRUD de tipos de activo con atributos activables; un atributo con datos no se elimina, se desactiva (ADR-0020).
  - **Criterios:** `select` sin `options` o claves duplicadas se rechazan (422); quitar un atributo con valores en algún activo devuelve 422 y desactivarlo funciona.
  - **Dependencias:** GA-1.
- [ ] GA-3: Enrolar activo validando sus atributos contra el tipo (ADR-0020).
  - **Criterios:** falta un atributo `required` o un `select` inválido → 422; un `tag` duplicado en el tenant → 409; se crea el `AssetIdentifier` correspondiente.
  - **Dependencias:** GA-2.
- [ ] GA-4: Editar activo con historial de revisiones (ADR-0021).
  - **Criterios:** `PATCH /assets/{id}` actualiza campos permitidos, rechaza cambiar `status`/verificación por esa vía y registra `document_revisions` con antes/después.
  - **Dependencias:** GA-3.
- [ ] GA-5: Cambio de estado con motivo; `decommissioned` es terminal (ADR-0020).
  - **Criterios:** `out_of_service`/`decommissioned` sin motivo → 422; cualquier transición desde `decommissioned` → 409; la ingesta de capturas hacia un activo desincorporado → 409.
  - **Dependencias:** GA-3.
- [ ] GA-6: Eliminación lógica y restauración; los eliminados no aparecen en listados, mapa, STAC ni resolución (ADR-0021).
  - **Criterios:** `DELETE` + `include_deleted` + `restore` funcionan; eliminar un padre con hijos activos → 409; `/resolve` ignora identificadores de activos eliminados.
  - **Dependencias:** GA-4.
- [ ] GA-7: Panel `/admin/` (tipos, activos, importar, estados) (ADR-0020, ADR-0018).
  - **Criterios:** permite crear/editar tipos con su tabla de atributos, enrolar/editar activos con formulario según el tipo, cambiar estado, eliminar y restaurar; consistencia visual con `openfield.css`.
  - **Dependencias:** GA-2, GA-3, GA-6.
- [ ] GA-8: Expediente con ficha técnica, estado de verificación e historial; `Vary: Accept` (ADR-0019, ADR-0021).
  - **Criterios:** `/assets/{id}` muestra atributos del tipo con su verificación, historial de revisiones, padre e hijos; las respuestas llevan `Vary: Accept` y `Cache-Control: no-store`.
  - **Dependencias:** GA-4, HUX-C1.

### Épica PV: Precarga CSV y verificación (ADR-0022)

- [ ] PV-1: Plantilla CSV por tipo (`;`, UTF-8 con BOM) (ADR-0022).
  - **Criterios:** `GET /admin/asset-types/{id}/csv-template` devuelve `text/csv` con columnas base + `attr:<key>` solo de atributos activos, en el orden del tipo.
  - **Dependencias:** GA-2.
- [ ] PV-2: Vista previa (dry-run) con errores por fila/columna y conflictos (ADR-0022).
  - **Criterios:** `dry_run=true` (defecto) no escribe nada; reporta errores con `row`/`column`, columnas desconocidas como advertencias y una vista previa de acciones.
  - **Dependencias:** PV-1.
- [ ] PV-3: Importación idempotente por TAG o serie que no pisa atributos verificados (ADR-0022, ADR-0003).
  - **Criterios:** importar dos veces el mismo archivo da `created=0`/`unchanged`; un valor distinto sobre un atributo `confirmed`/`corrected` se reporta como conflicto sin sobrescribir; celda vacía = sin cambio.
  - **Dependencias:** PV-2, GA-3.
- [ ] PV-4: Lotes de importación con avance de verificación (ADR-0022).
  - **Criterios:** `GET /admin/import-batches` muestra conteos del lote y el progreso calculado en vivo sobre los activos importados.
  - **Dependencias:** PV-3.
- [ ] PV-5: Verificación por atributo vía API (`/assets/{id}/verify`) con `op_id` idempotente (ADR-0022, ADR-0004).
  - **Criterios:** `confirm` sin valor → 422; `correct` con valor inválido → 422; el estado del activo pasa `pending`→`in_progress`→`verified`; `asset_not_found` marca `not_found`; mismo `op_id` → `already_applied` sin revisión extra.
  - **Dependencias:** PV-3, GA-4.

### Épica PB: Pendientes para fases posteriores (ADR-0013, ADR-0015, ADR-0021)

- [ ] H-AUTH: Autenticación y autorización (roles admin/operador) en endpoints de escritura y en el panel (ADR-0013, ADR-0021).
  - **Criterios:** las rutas de mutación y `/admin/` exigen credenciales con rol suficiente; las acciones registran el actor real.
  - **Dependencias:** GA-7 (panel), despliegue con usuarios reales.
- [ ] H-PURGE: Purga física por privacidad o retención, solo admin autenticado (ADR-0015, ADR-0021).
  - **Criterios:** existe un mecanismo documentado para eliminar físicamente un documento y sus medios según política de retención, previa autorización.
  - **Dependencias:** H-AUTH.
- [ ] H-EXPORT: Exportar el registro de activos a CSV con protección contra inyección de fórmulas (ADR-0022).
  - **Criterios:** exporta activos con sus atributos; los valores que comienzan por `=`, `+`, `-` o `@` se prefijan para evitar ejecución de fórmulas en hojas de cálculo.
  - **Dependencias:** PV-3.
- [ ] H-ALEMBIC: Migraciones con Alembic en vez de ALTER idempotente (ADR-0021).
  - **Criterios:** el esquema de BD se versiona con migraciones reproducibles en SQLite y PostgreSQL.
  - **Dependencias:** GA-1 (primera migración aplicada).
- [ ] H-CORS: Restringir CORS y agregar encabezados de seguridad completos/CSP (ADR-0005).
  - **Criterios:** en producción CORS queda limitado a orígenes conocidos y se sirven cabeceras CSP sin romper Leaflet ni las vistas.
  - **Dependencias:** H-AUTH, despliegue en VPS (H1-B1).

### Épica CT: Captura y verificación en terreno — PWA (ADR-0023, ADR-0008, ADR-0022, ADR-0017)

- [ ] CT-1: Cola persistente en IndexedDB (`store.js` + `createPersistentQueue`) con reintentos que conservan `attempts`/`last_error` (ADR-0023, ADR-0004).
  - **Criterios:** encolar y recargar la página conserva los pendientes; `flush` sincroniza en orden y deja los fallidos con `attempts=1` y `last_error` acotado.
  - **Dependencias:** ninguna.
- [ ] CT-2: Catálogo offline de activos y tipos (`assets.js` + caché en `kv`) con búsqueda sin acentos y pendientes primero (ADR-0023, ADR-0022).
  - **Criterios:** con conexión descarga `/admin/assets` y `/admin/asset-types`; sin conexión usa la caché guardada; excluye `decommissioned` y eliminados.
  - **Dependencias:** CT-1, GA-7.
- [ ] CT-3: `capture.js` con operador configurable, `endSession` y `recordNote` válidos contra esquema (ADR-0023, ADR-0017).
  - **Criterios:** `startSession` acepta `operator` sin romper los defaults; `endSession` fija `ended_at`; `recordNote` emite un `Observation` válido.
  - **Dependencias:** ninguna.
- [ ] CT-4: Capa de hardware: `listCameras`/`openCamera(deviceId)`/`startAudioRecording` en `web.js` y `simulated.js` (ADR-0023).
  - **Criterios:** `enumerateDevices` filtra `videoinput` con etiqueta de respaldo; `openCamera` con `deviceId` exacto y respaldo `facingMode`; `startAudioRecording` devuelve `stop()` con `blob`, `durationMs`, `mimeType`, `autoStopped` y libera las pistas.
  - **Dependencias:** ninguna.
- [ ] CT-5: Sincronización (`sync.js` + plataforma): `transcribeAudio` con `language`, `postVerify`, `endSessionRemote`, y `POST /sessions/{id}/end` + `language` en `/transcribe` (ADR-0023, ADR-0022).
  - **Criterios:** `end` es idempotente, exige `ended_at ≥ started_at` y rechaza fechas futuras (> 5 min); `/transcribe` acepta `language` ≤ 10 caracteres.
  - **Dependencias:** GA-4.
- [ ] CT-6: Selector de activo en la PWA: búsqueda, "solo pendientes", alta de activo nuevo encolada, sesión delimitada por activo (ADR-0023, ADR-0017).
  - **Criterios:** elegir un activo cierra la sesión abierta de otro activo (encola `session-end`) e inicia una nueva; "Nuevo activo" encola asset + identificador con `data_source: "field"`.
  - **Dependencias:** CT-2, CT-3.
- [ ] CT-7: Verificar ficha técnica en terreno: confirmar/corregir/no verificable por atributo + "activo no encontrado" (ADR-0022, ADR-0023).
  - **Criterios:** el formulario se genera del tipo; corregir valida el tipo del atributo antes de encolar; el guardado encola `verify` con `op_id` idempotente y actualiza la barra de progreso.
  - **Dependencias:** CT-5, CT-6.
- [ ] CT-8: Captura con cámara elegida y nota de voz iniciar/detener libre (ADR-0023, ADR-0015).
  - **Criterios:** el selector de cámaras muestra etiquetas tras el primer permiso y la elección persiste; la nota de voz muestra cronómetro e indicador rojo (D15), tope configurable, texto editable antes de guardar; se elimina el input de duración fija.
  - **Dependencias:** CT-4, CT-6.
- [ ] CT-9: Cola y fin de sesión: lista de pendientes con detalle, sincronización por tipo de ítem y `session-end` al terminar o cambiar de activo (ADR-0023, ADR-0008).
  - **Criterios:** cada `kind` se sincroniza con su endpoint (media → upload+ingest, audio → transcribe+ingest, verify → postVerify, session-end → end, doc → ingest); tras sincronizar se refresca el catálogo; al volver a primer plano se avisa el número de pendientes.
  - **Dependencias:** CT-5, CT-7, CT-8.

### Épica EC: Edición y borrado de capturas (ADR-0021, ADR-0017, ADR-0006)

- [ ] EC-1: `PATCH /documents/{id}` con lista blanca de campos editables por entidad y `reason` (ADR-0021).
  - **Criterios:** transcript `text`/`language`, observation `type`/`value`/`unit`/`metadata`, form-response `values` (revalidado contra la plantilla)/`completed_by`, media-item `asset_id`/`metadata`, session `operator`/`ended_at`, asset-identifier `value`/`type`/`source`; clave fuera de la lista → 422; cada edición guarda revisión con el motivo.
  - **Dependencias:** GA-4.
- [ ] EC-2: Restricciones de la edición genérica (ADR-0021, ADR-0017).
  - **Criterios:** `asset`/`asset-type` → 409 (usan sus rutas); `device`/`sync-event`/`thermal-capture` → 409; documento eliminado → 409; `media-item.asset_id` debe existir y no estar eliminado ni `decommissioned`; `asset-identifier.value` único por tenant y tipo → 409 en conflicto.
  - **Dependencias:** EC-1.
- [ ] EC-3: `DELETE /documents/{id}?reason=` lógico con restauración (ADR-0021).
  - **Criterios:** soft delete para entidades de captura (media-item, observation, transcript, form-response, session, thermal-capture, asset-identifier); `asset`/`asset-type` → 409; `op_id` idempotente; doble borrado → 409; `/documents/{id}/restore` lo devuelve.
  - **Dependencias:** EC-1.
- [ ] EC-4: Dossiers muestran lo eliminado con `include_deleted=true` (ADR-0021, ADR-0019).
  - **Criterios:** `GET /assets/{id}` y `GET /sessions/{id}` aceptan `include_deleted=true`; los documentos borrados se devuelven marcados con `_deleted_at`.
  - **Dependencias:** EC-3.
- [ ] EC-5: Edición/borrado en línea en los dossiers (ADR-0021, ADR-0019).
  - **Criterios:** cada ítem del expediente y de la sesión ofrece ✎ editar, 🗑 eliminar (con motivo) y 🕘 historial; checkbox "mostrar eliminados" los muestra atenuados con Restaurar; el diálogo de historial lista revisiones con claves cambiadas.
  - **Dependencias:** EC-4.
- [ ] EC-6: Edición de ítems pendientes en la cola de la PWA (ADR-0021, ADR-0023).
  - **Criterios:** antes de sincronizar se puede editar el texto de transcript/nota, descartar media/audio, deshacer una verificación (revirtiendo el catálogo en caché) y editar el activo nuevo encolado; la edición se bloquea mientras `flush` está en curso.
  - **Dependencias:** CT-9.

### Épica CI: Captura por pantallas y cámara a pantalla completa (ADR-0024, ADR-0023, ADR-0018)

- [ ] CI-1: Router por `hash` con una pantalla por paso, Atrás del sistema y respaldo al padre (ADR-0024, ADR-0018).
  - **Criterios:** rutas `/inicio`, `/ajustes`, `/activos`, `/activos/nuevo`, `/activos/qr`, `/activo`, `/activo/verificar`, `/activo/camara`, `/activo/camara/confirmar`, `/activo/voz`, `/activo/comentario`, `/cola`; guardas de consentimiento/activo/foto pendiente; ruta desconocida → pantalla por defecto; `back()` sin historial va al padre.
  - **Dependencias:** CT-9, EC-6.
- [ ] CI-2: Menú del activo con acciones grandes y sesión persistente en `kv` (ADR-0024, ADR-0017).
  - **Criterios:** botones Verificar ficha / Fotos (con contador) / Nota de voz / Comentario / Terminar sesión; `ui.session` y `ui.currentAssetId` se restauran al recargar; activo inexistente → cierre encolado.
  - **Dependencias:** CI-1.
- [ ] CI-3: Cámara a pantalla completa con cambiar cámara, linterna, zoom y miniatura/contador (ADR-0024, ADR-0023).
  - **Criterios:** overlay CSS `100dvh` + safe-areas; torch/zoom solo si `track.getCapabilities()` los expone; cambiar cámara cicla por `enumerateDevices` y persiste; disparador con destello y vibración; el stream se detiene al salir.
  - **Dependencias:** CT-4, CI-1.
- [ ] CI-4: Confirmación por foto (Repetir / Usar foto) con regreso a la cámara (ADR-0024).
  - **Criterios:** cada disparo abre la revisión; Repetir descarta sin encolar; Usar foto encola, actualiza miniatura/contador y vuelve a la cámara; Atrás del sistema equivale a Repetir.
  - **Dependencias:** CI-3.
- [ ] CI-5: Leyenda opcional y categoría por foto en `media-item.metadata` (ADR-0024, ADR-0009).
  - **Criterios:** `caption` (≤500), `category`, `category_label`, `camera_label`, `width`/`height` persisten en `metadata` con límites en el esquema; documentos existentes sin estas claves siguen válidos.
  - **Dependencias:** CI-4.
- [ ] CI-6: Categorías de foto configurables por tipo de activo en el panel admin (ADR-0024, ADR-0020).
  - **Criterios:** `asset-type.photo_categories` (máx. 30, clave con patrón, duplicadas → 422); edición en `/admin/` con "Usar predeterminadas"; `PUT` sin el campo conserva las existentes.
  - **Dependencias:** GA-2, CI-5.
- [ ] CI-7: Expediente muestra/filtra por categoría y permite corregir leyenda/categoría (ADR-0024, ADR-0021, ADR-0019).
  - **Criterios:** `mediaCard` muestra `metadata.caption` y badge de categoría; chips de filtro en la galería del activo; diálogo "Editar medio" corrige leyenda, categoría y activo destino con revisión.
  - **Dependencias:** EC-5, CI-5.
- [ ] CI-8: GPS por `watchPosition` durante la cámara y captura en mayor resolución (ADR-0024, ADR-0002).
  - **Criterios:** el disparo no espera un fix nuevo (usa el último o la ubicación del activo); `openCamera` pide 1920×1080 ideal; `ImageCapture.takePhoto()` se usa cuando existe y cae al canvas si falla.
  - **Dependencias:** CI-3.

---

## Trazabilidad
Todo ítem `- [ ]` cita al menos un ADR. `check_traceability.py` verifica que cada ADR citado existe
y declara `Estado:`. Los criterios de aceptación son verificables de forma automática o manual
(fase por fase). Fase 0 se completa sin comprar nada.

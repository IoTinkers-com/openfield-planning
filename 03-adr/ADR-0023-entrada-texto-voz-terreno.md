# ADR-0023 · Entrada de texto/voz en terreno y selección de cámara

Estado: Aceptada
Fecha: 2026-11-13
Origen: D23 (`DECISIONS.md`) — complementa ADR-0007 y ADR-0008 (no los reemplaza)

## Contexto
La captura de comentarios en terreno debe ser rápida con guantes, con poca luz y sin
mirar la pantalla. La opción anterior grababa audio de **duración fija** (el operador
tenía que adivinar cuánto iba a hablar), no es el comportamiento estándar de una app de
notas. Además:

- Los smartphones ya traen **dictado de voz en el teclado del sistema** (Gboard en
  Android con paquetes de idioma descargables para uso sin conexión
  ([fuente](https://en.androidsis.com/how-to-activate-voice-typing-offline-in-gboard/));
  dictado en iOS). Es la vía con menos fricción: funciona dentro de cualquier input o
  textarea nativo sin permisos ni código adicional.
- La **Web Speech API** no es viable como mecanismo central: soporte incompleto y
  dependiente de servicios en línea ([soporte por navegador](https://textintoaudio.com/speech-recognition-browser-support),
  [SpeechAnalyzer en Safari](https://blog.addpipe.com/apple-speechanalyzer-api/),
  [bug WebKit #321436](https://bugs.webkit.org/show_bug.cgi?id=321436)).
- El usuario exige **reconocer las cámaras disponibles** del dispositivo: iOS ≥ 16.3
  expone las cámaras traseras individuales (gran angular, teleobjetivo) vía
  `MediaDevices` ([referencia](https://dominikschilling.de/notes/ios-access-all-back-cameras-mediadevices-api/)).
- Los activos pre-cargados por CSV (ADR-0022) se recorren en terreno **uno a uno**: la
  PWA necesita catálogo offline, verificación por atributo y enrolamiento de activos
  nuevos encontrados en sitio.

## Decisión
- **Texto:** todos los campos usan inputs nativos (`type=text/number/search`,
  `inputmode`, `select`, `textarea`). La entrada de comentarios por voz se resuelve con
  el **dictado del teclado del sistema operativo**; la PWA solo muestra una nota de
  ayuda (activar el idioma offline en Gboard). **No se usa la Web Speech API.**
- **Nota de voz:** grabación con **iniciar/detener libre** (botón ●/■, cronómetro
  visible, tope configurable por el usuario con default 5 min y auto-detención).
  MediaRecorder con el primer `mimeType` soportado de
  `audio/webm;codecs=opus`, `audio/mp4`, `audio/webm`. Indicador rojo de grabación
  mientras está activa (D15). Sin conexión el audio se encola en IndexedDB y se
  transcribe al sincronizar; con conexión se transcribe de inmediato y el texto queda
  **editable antes de guardar** (el transcript se ingesta con el texto final). Guardar
  el audio original es opcional por sesión (ADR-0007).
- **Cámaras:** tras el primer permiso, `enumerateDevices()` filtra `videoinput` y se
  selecciona por `deviceId` exacto (respaldo `facingMode` si el `deviceId` falla); la
  elección se recuerda en `localStorage` y `devicechange` refresca la lista.
- **QR:** `BarcodeDetector` donde exista ([caniuse](https://caniuse.com/mdn-api_barcodedetector));
  respaldo: búsqueda manual por tag. Un lector QR por biblioteca (p. ej. zxing-wasm,
  MIT) solo se agrega si el usuario lo confirma.
- **Catálogo y cola:** la cola pasa de memoria a **IndexedDB** (object stores `queue`
  y `kv`; los blobs se guardan como `{buffer, type}` por compatibilidad con Safari).
  El catálogo (`/admin/assets` + `/admin/asset-types`) se cachea en `kv` para el
  recorrido offline; la verificación se encola como ítem `verify` con `op_id = qid`
  (idempotente en plataforma, ADR-0022). Fin de sesión explícito (`session-end`) o al
  cambiar de activo (ADR-0017: una sesión delimitada por activo).
- Sin **Background Sync** (ADR-0008): la sincronización es explícita; al volver a
  primer plano se avisa el número de pendientes.

## Alternativas consideradas
- Whisper en WASM en el dispositivo (diferido: sigue en D8 como "por validar"; hoy
  transcribe el backend tras sincronizar).
- Web Speech API para dictado continuo (rechazado: soporte incompleto y online; el
  dictado del teclado cubre el caso con cero código).
- Duración fija de audio (rechazada por el usuario: no es el comportamiento estándar).
- Background Sync / Service Worker para reintentos (rechazado: no existe en iOS,
  ADR-0008).
- Cola solo en memoria (rechazado: se pierde al recargar la página, rompe D4).

## Consecuencias
- El operador verifica la ficha técnica atributo por atributo sin teclado salvo
  correcciones; el avance se ve en el badge y en el progreso por activo.
- La PWA funciona completa sin conexión: catálogo, sesiones, capturas, notas,
  verificaciones y enrolamientos quedan en IndexedDB hasta sincronizar.
- `recordAudio(durationMs)` queda reimplementado sobre `startAudioRecording` (contrato
  estable de la capa de hardware, D8).

# ADR-0024 · Captura por pantallas, cámara a pantalla completa y confirmación de fotos

Estado: Aceptada
Fecha: 2026-11-15
Origen: D24 (`DECISIONS.md`) — complementa ADR-0018 y ADR-0023 (no los reemplaza)

## Contexto
La PWA creció como una página larga: el stepper era decorativo y todas las secciones
convivían en una sola vista desplazable. La cámara era un `<video>` de 480 px dentro
de una tarjeta y la foto se encolaba sin revisión. El usuario pidió: **confirmar cada
imagen**, **cámara a pantalla completa con sus controles** y **un paso por pantalla
con posibilidad de regresar**. Además:

- Las fotos de terreno no son solo de la placa: el operador toma varias seguidas
  (vista general, detalles, hallazgos), por lo que la confirmación debe devolverlo a
  la cámara sin pasos extra.
- Cada foto puede llevar contexto propio: una **leyenda** opcional (dictable con el
  teclado del SO, coherente con ADR-0023) y una **categoría** que luego permita
  filtrar la evidencia en el expediente y, en el futuro, exigir ciertos tipos de
  foto para cerrar la verificación.
- Recargar la página perdía la sesión abierta: quedaba huérfana sin `session-end`.
- Cada disparo esperaba `getCurrentPosition` (hasta 20 s de timeout): la ráfaga era
  lenta.
- Los navegadores suelen dar 640×480 por defecto si no se pide más resolución.
- iPhone no ofrece `Element.requestFullscreen()` para elementos arbitrarios, y el
  soporte de `torch`/`zoom`/`ImageCapture` varía por navegador y SO.

## Decisión
- **Una pantalla por paso**, enrutadas por `location.hash` (`#/inicio`, `#/ajustes`,
  `#/activos`, `#/activos/nuevo`, `#/activos/qr`, `#/activo`, `#/activo/verificar`,
  `#/activo/camara`, `#/activo/camara/confirmar`, `#/activo/voz`,
  `#/activo/comentario`, `#/cola`). Cada navegación es una entrada del historial ⇒
  el gesto/botón Atrás del sistema vuelve a la pantalla anterior; el botón "←"
  propio usa `history.back()` y, sin historial (enlace directo/recarga), va a la
  pantalla padre. Guardas: sin consentimiento → `#/inicio`; sin activo →
  `#/activos`; confirmar sin foto → `#/activo/camara`.
- **Cámara a pantalla completa** mediante overlay CSS (`position:fixed; inset:0;
  height:100dvh`, `object-fit:cover`, `viewport-fit=cover` + `env(safe-area-inset-*)`)
  — no la Fullscreen API, ausente para elementos en iPhone. Controles: cerrar,
  nombre del activo, linterna (solo si `track.getCapabilities().torch`), cambiar
  cámara (cicla por `enumerateDevices`, persistido; oculto con una sola cámara),
  deslizador de zoom (solo si `capabilities.zoom`), miniatura de la última foto con
  contador (abre la cola), disparador con destello y vibración, y "Listo". El stream
  se **detiene al salir** de cámara/confirmar (privacidad y batería).
- **Confirmación por foto**: imagen a pantalla completa, leyenda opcional
  (`maxlength=500`), categoría con chips de un toque (opcional), **Repetir** y
  **Usar foto**; ambas vuelven a la cámara (Atrás del sistema = Repetir). El
  sistema de historial reemplaza la entrada de confirmar para que Atrás desde la
  cámara no regrese a la revisión.
- **Categorías de foto configurables por tipo de activo**:
  `asset-type.photo_categories: [{key, label, active}]` (máx. 30, aditivo). Si el
  tipo no las define (o el activo no tiene tipo), la PWA usa la lista
  predeterminada: placa de datos, vista general, detalle, hallazgo/anomalía,
  entorno/ubicación. Se editan en el panel admin; la clave se deriva de la etiqueta
  y se mantiene estable.
- **Metadatos por foto** en `media-item.metadata` (aditivo, con límites en el
  esquema): `caption` (≤500), `category` (≤50), `category_label` (≤100, copia del
  nombre al capturar, para mostrar aunque cambie la configuración), `camera_label`
  (≤200), `width`/`height`. El expediente muestra leyenda y categoría, filtra por
  categoría y permite corregir ambas (PATCH de `metadata`, ADR-0021).
- **GPS sin bloquear**: `watchPosition` mientras la cámara está abierta; cada foto
  usa el último fix (o la ubicación del activo). Se detiene al salir.
- **Resolución**: `openCamera` pide `width/height` ideal 1920×1080; `captureImage`
  usa `ImageCapture.takePhoto()` si existe y cae con gracia al canvas del frame.
- **Sesión persistente**: `session` y el activo actual se guardan en `kv` y se
  restauran al arrancar; si el activo ya no existe, la sesión se cierra encolando
  `session-end`. El alta de activo pasa de diálogo a pantalla propia.

## Alternativas consideradas
- Mantener la página única con pestañas (rechazado: el usuario pidió explícitamente
  una pantalla por paso con regreso).
- Fullscreen API del navegador (rechazada: no existe para elementos en iPhone; el
  overlay CSS cubre todos los navegadores).
- Categorías fijas en el código (rechazado: el usuario pidió configurables; la
  lista predeterminada cubre el caso sin configuración).
- Leyenda obligatoria por foto (rechazada: frenaría la ráfaga; se hace opcional).
- Comentario por foto como `Observation` vinculada por `media_item_id` (diferido:
  duplicaría documentos; `metadata.caption` es suficiente y editable, ADR-0021).
- Secuencia guiada rígida tras elegir el activo (verificar → fotos → voz →
  comentario; rechazada por el usuario: menú de acciones libre).

## Consecuencias
- La navegación interna se vuelve predecible y reversible; el índice `index.html`
  se reestructura por secciones-pantalla y pierde el stepper decorativo.
- `torch`, `zoom` e `ImageCapture` se usan solo con detección en runtime; la
  funcionalidad base no depende de ellos (R18).
- En iPhone el modo "Agregar a inicio" (standalone) oculta las barras de Safari; en
  navegador pueden asomar bordes (R19).
- Las fotos en mayor resolución ocupan más IndexedDB hasta sincronizar; los object
  URLs se revocan al salir de confirmar/cámara.
- Sesiones restaurables tras recarga: menos sesiones huérfanas en la plataforma.

| Nivel | Flujo de captura | Cámara |
|-------|------------------|--------|
| Maker | PWA + overlay CSS, una pantalla por paso | `getUserMedia`, controles opcionales según navegador |
| Pro | Mismo flujo empaquetado con Capacitor | Cámara nativa vía la misma capa de hardware (D8) |
| Industrial | Mismo flujo en dispositivos rugerizados / cámaras externas | Adaptador que emite `media-item` canónico (ADR-0001) |

# ADR-0008 · App de captura (PWA primero)

Estado: Aceptada
Fecha: 2026-11-11
Origen: D8 (`DECISIONS.md`)

## Contexto
Una app nativa por plataforma es cara; una PWA cubre Android e iOS con un solo código, pero
tiene límites en iOS/Safari.

## Decisión
- **PWA primero**, con la capa de acceso a hardware **desacoplada** para envolver con Capacitor
  o pasar a nativo después.
- Límites de PWA en iOS/Safari documentados como parte del diseño: sin Background Sync,
  IndexedDB puede purgarse si la app no está instalada, sin WebUSB/WebBluetooth, GPS solo en
  primer plano, Whisper local en WASM por validar.

## Alternativas consideradas
- Nativo desde el inicio (rechazado: doble mantenimiento sin cliente que lo pague).
- Depender de Background Sync (rechazado: no existe en iOS; offline-first se hace con subida
  explícita, no con sincronización en segundo plano).

## Consecuencias
- La capa de hardware (cámara, GPS, micrófono, térmica, almacenamiento) es una interfaz propia
  con implementación web y (futura) nativa.
- El flujo offline no depende de Background Sync: sube cuando hay conexión y la app está activa.

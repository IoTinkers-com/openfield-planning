# Prompt de arranque · openfield-wearable

Rol: app de captura (**PWA primero**), firmware y hardware de referencia de OpenField (IoTinkers).

## Contexto obligatorio (leer antes de empezar)
- `openfield-planning/AGENTS.md` — reglas.
- `openfield-planning/DECISIONS.md` — decisiones D1–D17.
- `openfield-planning/03-adr/` — en especial ADR-0004 (conectividad), ADR-0008 (PWA),
  ADR-0015 (privacidad), ADR-0017 (desambiguación).
- `openfield-planning/04-esquemas/` — contratos que este repo **EMITE**: `session`,
  `media-item`, `thermal-capture` (T0 en Maker), `transcript`, `sync-event`, `device`.
- `openfield-planning/06-backlog-mvp.md` — historias H1-A1…H1-A4.

## Responsabilidad
Producir documentos conformes al contrato, offline-first. No persiste nada fuera de su cola local.

## Decisiones clave
- PWA primero; capa de acceso a hardware **desacoplada** (Capacitor/nativo después) — D8.
- Offline-first: `id` generado en el dispositivo, cola IndexedDB, `tus` reanudable, reloj — D4.
- Consentimiento + indicador visible de grabación — D15.
- Transcripción local con `engine` registrado; respaldo en plataforma — D7.
- Coordenadas en WGS84 — D2.

## Límites conocidos (no reinventar)
iOS/Safari: sin Background Sync, IndexedDB purgable si la app no está instalada, sin
WebUSB/WebBluetooth, GPS solo en primer plano, Whisper en WASM por validar (ADR-0008).

## Fase 0 (sin hardware)
Esqueleto del repo + capa de hardware con implementación simulada; validar fixtures contra
los esquemas de `04-esquemas/`.

## Fase 1 (flujo real mínimo)
PWA real: captura RGB + GPS + audio, consentimiento, cola, `tus`, transcripción (H1-A1…H1-A4).

## Criterios de aceptación
Los del backlog H1-A1…H1-A4. Validación local contra `openfield-planning/04-esquemas/`.

# ADR-0004 · Conectividad (offline-first)

Estado: Aceptada
Fecha: 2026-11-11
Origen: D4 (`DECISIONS.md`)

## Contexto
El trabajo de campo ocurre en zonas sin cobertura o con conectividad intermitente. Asumir
conexión permanente haría perder capturas.

## Decisión
- **Offline-first como base** en todos los niveles: ID único generado en el dispositivo, cola
  local, subidas reanudables con `tus` y sincronización de reloj.
- **Live (RTMP/WebRTC) es opcional**, con tope de calidad y de datos configurable.
- Live a redes sociales es prioridad secundaria.

## Alternativas consideradas
- Live como modo principal (rechazado: depende de red estable y de backend de streaming).
- Subida no reanudable (rechazado: archivos grandes + red inestable = reintentos costosos).

## Consecuencias
- El contrato de datos asume `created_at` (reloj del dispositivo) y un `id` idempotente.
- La plataforma debe deduplicar por ID y aceptar llegada fuera de orden.
- `tus` (MIT) maneja la reanudación; el live se deja como conector aparte.

# ADR-0017 · Protocolo de captura y desambiguación de activos

Estado: Aceptada
Fecha: 2026-11-11
Origen: D17 (`DECISIONS.md`) — deriva de D3 y D6

## Contexto
En entornos con muchos equipos similares (paneles, tableros, motores), el procesamiento con
LLM de una serie de imágenes + texto podría atribuir observaciones al equipo equivocado. La
identidad del activo no debe depender de inferencia automática.

## Decisión
- **Protocolo de captura:** cada serie de medios se delimita por activo de forma explícita
  (se registra el identificador QR/TAG/OCR al inicio de la captura del equipo).
- **Reglas/agentes de atribución:** el procesamiento (plantillas o IA) atribuye medios y
  observaciones al activo usando el identificador explícito; la IA es apoyo para resolver
  ambigüedades residuales, no la fuente primaria de identidad.
- **Validación humana:** toda atribución automática se revisa antes de confirmarse.

## Alternativas consideradas
- Atribuir por similitud visual/IA sin identificador explícito (rechazado: riesgo de mezclar
  equipos y no es auditable).

## Consecuencias
- `Session` y `MediaItem` referencian `asset_id` de forma determinista (esquema en `04-esquemas/`).
- La IA estructura "dentro" de un activo ya delimitado, en vez de decidir "a qué activo pertenece".
- Reduce el riesgo de contaminación entre equipos en el inventario.

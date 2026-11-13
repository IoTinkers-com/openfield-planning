# ADR-0021 · Edición, baja lógica y auditoría de documentos

Estado: Aceptada
Fecha: 2026-11-13
Origen: D21 (`DECISIONS.md`) — complementa D4/ADR-0004 sin reemplazarlo

## Contexto
La ingesta (D4) es idempotente y solo de creación: reenviar el mismo `id` devuelve
`already_exists`. Eso funciona para la cola offline de captura, pero una plataforma de
gestión de activos necesita además **corregir** datos (un atributo mal tipeado, una
transcripción editada, un medio asignado al activo equivocado) y **dar de baja** registros
erróneos, sin perder la trazabilidad que exige ISO 55001 (trazabilidad de la información
de gestión de activos, ver ADR-0020).

Eliminar físicamente documentos rompería el expediente (ADR-0019) y la cadena de evidencia:
un activo desincorporado debe seguir mostrando su historial. Al mismo tiempo, no hay
autenticación todavía (un solo usuario, D13): las mutaciones deben quedar detrás de
servicios acotados para poder agregar autorización después sin rediseñar.

## Decisión
- **La ingesta sigue siendo idempotente y solo de creación** (se mantiene ADR-0004: la
  cola del dispositivo puede reenviar sin efectos). Las mutaciones van por **endpoints
  dedicados** (`POST /assets/{id}/status`, `PATCH /assets/{id}`, `PATCH /documents/{id}`,
  `DELETE`, `restore`), nunca re-escribiendo por re-ingesta.
- **Baja lógica (soft delete):** columna `deleted_at` en `documents`. Los documentos
  eliminados quedan fuera de listados, mapa, expediente, exportación STAC y resolución de
  identificadores por defecto, y son restaurables (`POST /documents/{id}/restore`).
  **Nada se borra físicamente en el MVP.** Eliminar ≠ desincorporar: eliminar es para
  altas erróneas; un equipo retirado se marca `decommissioned` (ADR-0020).
- **Historial de revisiones:** tabla interna `document_revisions` con `revision`,
  `action` (create/update/status/verify/delete/restore/import), `source`
  (manual/csv_import/field/api), `batch_id`, `op_id` (único, idempotencia de reintentos
  offline), `reason`, `actor`, `before`/`after` (cuerpos completos) y `created_at`.
- **Fechas del servidor:** `created_at`, `updated_at`, `status_changed_at`, `verified_at`
  y `deleted_at` los fija el servidor; el cliente no puede enviarlas. El `reason` es texto
  libre acotado (máx. 500 caracteres).
- **`actor` fijo "admin"** hasta que exista autenticación (D13: un solo usuario).
  Autenticación/autorización y protección de rutas de escritura quedan en el backlog
  (H-AUTH): el túnel de pruebas solo se expone durante pruebas controladas (R13).
- **Purga física diferida:** política de retención/eliminación física por privacidad
  (D15) queda en el backlog (H-PURGE), ejecutable solo por admin autenticado.
- El historial también cubre la **importación CSV** (`action=import`, `batch_id`) y la
  **verificación en terreno** (`action=verify`, `source=field`, ADR-0022).

## Alternativas consideradas
- Borrado físico directo (rechazado: pierde trazabilidad y rompe el expediente del activo
  desincorporado; contrario al espíritu de ISO 55001 §7.5).
- Guardar el historial **dentro** del cuerpo de los 11 esquemas canónicos (rechazado:
  ensucia el contrato de datos que también usan los conectores; el historial es un detalle
  interno de la plataforma, no parte del documento canónico que se sincroniza).
- Permitir mutación por re-ingesta con versión mayor (rechazado: rompe la idempotencia
  simple de D4; mezclar dos semánticas en un endpoint es más riesgoso que separarlas).
- Event sourcing completo (rechazado para el MVP: complejidad innecesaria; con
  `document_revisions` hay trazabilidad suficiente y el estado actual sigue en `documents`).

## Consecuencias
- Migración: `documents` gana `updated_at`, `deleted_at`, `revision` mediante ALTER
  idempotente en `init_db` (SQLite/PostgreSQL); tablas nuevas `document_revisions` e
  `import_batches`. Riesgo R14 (sin Alembic todavía, H-ALEMBIC).
- Toda mutación registra antes/después, lo que habilita auditoría y deshacer manual.
- `op_id` único evita mutaciones duplicadas por reintentos de la cola offline (complementa
  el dedupe por `id` de D4, que solo cubre creación).
- Las rutas de mutación no confían en flags ni fechas del cliente; al llegar H-AUTH se
  agrega el middleware de autenticación sin cambiar contratos.

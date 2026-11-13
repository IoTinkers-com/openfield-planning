# ADR-0022 · Precarga de activos por CSV y verificación en terreno

Estado: Aceptada
Fecha: 2026-11-13
Origen: D22 (`DECISIONS.md`) — deriva de D3, D12 y ADR-0017

## Contexto
Muchos usuarios parten de una **lista de activos existente** (export de un CMMS, planilla
del cliente, inventario anterior) que debe verificarse en terreno. Precargar esa lista es
más realista que enrolar equipo por equipo desde cero. El flujo objetivo: importar la
lista con sus atributos pre-existentes → recorrer los activos en terreno **uno a uno**
confirmando o corrigiendo cada dato → la plataforma muestra el avance de verificación.

Riesgos que la decisión debe evitar: importaciones corruptas silenciosas, duplicados por
re-importación, y sobre todo que **un dato importado se confunda con un dato verificado
en terreno** (falsa confianza en la calidad del registro, contrario a ISO 55001 §7.5/7.6,
que exige conocer la fuente y la calidad de la información, ver ADR-0020).

## Decisión
- **Plantilla CSV por tipo de activo** (`GET /admin/asset-types/{id}/csv-template`):
  encabezados base (`tag`, `name`, `functional_location`, `parent_tag`, `manufacturer`,
  `model`, `serial_number`, `criticality`, `status`, `lat`, `lon`) + una columna
  `attr:<key>` por atributo activo del tipo. Se descarga en UTF-8 con BOM y separador `;`
  (abre directo en Excel en configuraciones con coma decimal).
- **Formato aceptado:** UTF-8 con o sin BOM (respaldo latin-1), separador `,` o `;`
  (detectado), decimales con `,` o `.`, fechas `YYYY-MM-DD` o `DD-MM-YYYY`, booleanos
  `si/no/true/false/1/0/x`. Límites: **5 MB y 5 000 filas** por archivo.
- **Vista previa obligatoria (dry-run por defecto):** `POST /admin/assets/import`
  siempre puede ejecutarse con `dry_run=true` y devuelve un reporte por fila
  (errores con fila y columna, conflictos, advertencias por columnas ignoradas,
  vista previa de acciones). Solo con `dry_run=false` se escribe.
- **Emparejamiento:** por `tag` → `AssetIdentifier(type="tag")`, o por `serial_number`
  cuando no hay tag (D3: el TAG/placa del cliente es identificador equivalente).
  Duplicados dentro del archivo → error en todas las filas afectadas.
- **Re-import idempotente:** importar el mismo archivo dos veces deja `created=0` y las
  filas como `unchanged`. Una celda vacía significa "sin cambio", nunca "borrar".
- **Nunca pisa lo verificado:** si un atributo está `confirmed`/`corrected` y el CSV trae
  un valor distinto, se reporta como **conflicto** y se conserva el valor verificado
  (la corrección se resuelve en terreno o por edición manual). Cambios aplicados a
  atributos pendientes resetean su verificación a `pending`.
- **Trazabilidad de origen:** cada activo lleva `data_source` (`csv_import`/`field`/
  `manual`), `import_batch_id`, `verification_status` (`pending`/`in_progress`/`verified`/
  `not_found`) y `attribute_verification` por clave (`pending`/`confirmed`/`corrected`/
  `unverifiable`, con `previous_value`, `verified_at`, `session_id`). Un dato importado
  nace `pending`: nunca se presenta como verificado.
- **Lotes:** tabla `import_batches` con archivo, conteos (creados/actualizados/sin cambio/
  errores/conflictos), reporte completo y **avance de verificación** en vivo
  (`GET /admin/import-batches`).
- **Verificación por atributo** (`POST /assets/{id}/verify`): resultados `confirm`,
  `correct` (con `value` validado contra el tipo) o `unverifiable`, más
  `asset_not_found` para marcar el activo completo como no encontrado. `confirm` exige
  valor existente; `op_id` hace idempotente el reintento desde la cola offline (ADR-0004,
  ADR-0021).
- **Activos `decommissioned` o eliminados** no se actualizan por CSV (error en la fila);
  un cambio de `asset_type_id` tampoco se permite por CSV.

## Alternativas consideradas
- Importar XLSX directamente (diferido: requiere dependencia nueva (openpyxl/pandas); el
  CSV cubre el caso y cualquier hoja se exporta a CSV; queda en el backlog si el cliente
  lo pide).
- Sobrescribir siempre con el CSV (rechazado: destruye el trabajo de verificación en
  terreno; el conflicto explícito fuerza decisión humana).
- Emparejamiento por nombre (rechazado: los nombres no son únicos ni estables; D3 ya fija
  identificadores explícitos).
- Marcar automáticamente `verified` al importar (rechazado: un dato de planilla no fue
  verificado en sitio; sería falsa calidad de datos).
- Importación síncrona de archivos de cualquier tamaño (rechazado: límites 5 MB/5 000
  filas para el MVP; lotes mayores → importación asíncrona en fase posterior).

## Consecuencias
- El operador ve el avance real del recorrido (pendiente → verificado) por activo, por
  atributo y por lote.
- El seed incluye `sample_assets.csv` con 10 motores y una fila con error intencional para
  mostrar el dry-run.
- `attribute_verification` queda dentro del documento `Asset` (contrato canónico), mientras
  el detalle de cada cambio va a `document_revisions` (ADR-0021).
- La PWA (Tanda B) consume el catálogo con estos estados para guiar el recorrido y envía
  verificaciones con `op_id` desde su cola offline.

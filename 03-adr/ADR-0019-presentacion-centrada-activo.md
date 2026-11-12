# ADR-0019 · Presentación centrada en el activo (asset dossier)

Estado: Aceptada
Fecha: 2026-11-11
Origen: D19 (`DECISIONS.md`) — deriva de D12 y ADR-0017

## Contexto
El caso de uso principal (D12) es el inventario de equipos eléctricos/industriales: lo que
le importa al operador es el **expediente de un equipo** (sus identificadores, sesiones,
medios, observaciones, transcripciones, respuestas de formulario), no una lista plana de
documentos por tipo. Las relaciones ya existen en el contrato de datos (`04-esquemas/`) desde
ADR-0017: `Session.asset_id`, `MediaItem.asset_id`/`session_id`, `Observation.asset_id`/
`session_id`/`media_item_id`, `Transcript.session_id`/`asset_id`, `FormResponse.asset_id`/
`session_id`, `AssetIdentifier.asset_id`. El dashboard de Fase 0/1 (ADR-0018) solo mostraba
mapa + galería agrupada por activo + una tabla "Registro" de documentos sueltos; faltaba la
capa de presentación que recorre esas relaciones para armar el expediente.

## Decisión
- **El activo es la unidad central de presentación**, no el documento ni el tipo de entidad.
  El dashboard sigue siendo el punto de entrada (mapa + agrupación por activo, ADR-0018), pero
  la navegación profundiza así: dashboard → **expediente de activo** → **vista de sesión** →
  medio original.
- **Agregación de solo lectura:** `GET /assets/{id}` y `GET /sessions/{id}` recorren la tabla
  `documents` ya existente (sin índices nuevos ni cambios de modelo) y arman el expediente
  cruzando `asset_id`/`session_id`. No se cambia el contrato de `04-esquemas/`.
- **Una sola ruta, dos representaciones (content negotiation por `Accept`):** la misma URL
  (`/assets/{id}`, `/sessions/{id}`) devuelve la vista HTML para navegación de navegador
  (`Accept: text/html`) o el JSON agregado para `fetch()`/pruebas (resto de casos). Se evita
  así introducir un prefijo `/api` o un segundo esquema de rutas.
- **Sin framework de frontend:** las vistas (`asset.html`, `session.html`) son HTML/JS plano
  que reutiliza `openfield.css` y un módulo JS compartido (`dossier-common.js`), consistente
  con D8/ADR-0018.
- **El "Registro" (tabla plana de documentos) pasa a secundario:** queda disponible pero
  colapsado por defecto en el dashboard, ya no es la vista principal.

## Alternativas consideradas
- Mantener la tabla "Registro" como vista principal del dashboard (rechazado: no refleja el
  caso de uso D12; obliga a pensar en documentos sueltos en vez de en el equipo inspeccionado).
- Prefijo `/api/assets/{id}` separado de una ruta de UI `/assets/{id}` distinta (rechazado por
  ahora: duplica convenciones de URL cuando el content-negotiation por `Accept` alcanza en
  Fase 0/1; se puede introducir si aparece un consumidor API externo real).
- Vistas en un framework de frontend con enrutado de cliente (rechazado: D8/ADR-0018 fijan
  HTML/JS plano; no hay justificación de producto todavía para el costo de build/migración).
- Añadir columnas/índices por `asset_id`/`session_id` en `documents` para acelerar la
  agregación (diferido: Fase 0/1 no tiene volumen que lo justifique; ver riesgo R12).

## Consecuencias
- Nuevo módulo de solo lectura `app/dossier.py` en `openfield-platform` + vistas estáticas
  `asset.html`/`session.html` + módulo JS compartido `dossier-common.js`.
- La agregación recorre todos los documentos de un tipo por tenant y filtra en Python (mismo
  patrón que `resolve.py`); aceptable en Fase 0/1, revisar si el volumen crece (R12).
- Una `Session` con `asset_id = null` (abarca varios activos) no aparece en ningún expediente
  de activo todavía; queda como pregunta abierta para una fase posterior.
- No cambia `04-esquemas/` ni las 8 etapas del flujo (`02-flujo-de-datos.md`).

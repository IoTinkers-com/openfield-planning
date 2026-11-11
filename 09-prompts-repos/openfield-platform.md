# Prompt de arranque · openfield-platform

Rol: backend, ingesta, almacenamiento, estructuración, UI e informes de OpenField (IoTinkers).

## Contexto obligatorio (leer antes de empezar)
- `openfield-planning/AGENTS.md` — reglas.
- `openfield-planning/DECISIONS.md` — decisiones D1–D17.
- `openfield-planning/03-adr/` — en especial ADR-0005 (despliegue), ADR-0009 (contratos),
  ADR-0013 (tenant), ADR-0006 (estructuración), ADR-0017 (desambiguación).
- `openfield-planning/04-esquemas/` — **fuente de verdad** (copiar a `schemas/`). Este repo
  recibe/almacena los 11 esquemas.
- `openfield-planning/05-estructura-repos.md` — árbol y catálogo de componentes.
- `openfield-planning/06-backlog-mvp.md` — H0-A1…A4, H0-C1 (Fase 0); H1-B1/B2, H1-C1/C2 (Fase 1).

## Stack (catálogo en `05-estructura-repos.md`)
FastAPI (MIT), PostgreSQL + PostGIS (PostgreSQL License / GPLv2+), SeaweedFS (Apache-2.0),
pygeoapi (MIT), stac-fastapi / pgSTAC (MIT), tusd (MIT), Leaflet (BSD-2).

## Responsabilidad
Validar, deduplicar, almacenar y estructurar; export STAC + OGC API Features; fuente de
verdad de `Asset`, `AssetIdentifier`, `FormTemplate`, `FormResponse`.

## Decisiones clave
- Docker Compose local/VPS; interfaz S3-compatible para medios (D5, `05`).
- JSON Schema versionado: solo se agregan campos, nunca se rompen (D9).
- `tenant_id` en todo documento y consulta (D13).
- `asset_id` determinista en `media-item`, `observation` y `form-response` (ADR-0017).
- Plantillas configurables primero; IA después, con validación humana (D6).

## Fase 0 (sin hardware)
`docker compose` (API + PostGIS + object storage local) + `schemas/` + ingesta (validación y
dedupe por `id`) + dashboard con mapa (H0-A, H0-C).

## Fase 1 (flujo real mínimo)
VPS + HTTPS, export STAC + OGC API Features, `FormTemplate`/`FormResponse`, resolución de
identificadores QR/TAG/OCR a `Asset`.

## Criterios de aceptación
Los del backlog H0-A/H0-C (Fase 0) y H1-B/H1-C (Fase 1).

# ADR-0013 · Usuarios y multiempresa

Estado: Aceptada
Fecha: 2026-11-11
Origen: D13 (`DECISIONS.md`)

## Contexto
Arrancar con un solo usuario, pero sin pagar migraciones costosas al pasar a multiempresa.

## Decisión
- Un solo usuario al inicio.
- `tenant_id` en el esquema desde el día uno para pasar a multiempresa sin migraciones.

## Alternativas consideradas
- Sin tenant hasta que haga falta (rechazado: migrar datos ya capturados es caro y arriesgado).
- Multiempresa completa desde el inicio (rechazado: complejidad de autorización sin usuario real).

## Consecuencias
- Todo documento del esquema lleva `tenant_id`.
- La autorización se agrega después; el aislamiento de datos está preparado desde el modelo.

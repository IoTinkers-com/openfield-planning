# ADR-0006 · Estructuración (plantillas primero, IA después)

Estado: Aceptada
Fecha: 2026-11-11
Origen: D6 (`DECISIONS.md`)

## Contexto
El valor de la plataforma está en estructurar la evidencia de terreno. Hay dos caminos:
plantillas deterministas configurables, o IA que extrae estructura automáticamente.

## Decisión
- Primero: plantillas de formulario/checklist **configurables** (deterministas, predecibles).
- Después: IA como apoyo, **siempre con validación humana**.

## Alternativas consideradas
- IA primero (rechazado: no hay datos etiquetados aún y el resultado no es auditable al inicio).
- Estructura rígida en código (rechazado: no permite configurar formularios por cliente).

## Consecuencias
- `FormTemplate` / `FormResponse` en el esquema modelan la configuración.
- La salida de IA nunca se acepta sin revisión humana (trazabilidad y confianza).

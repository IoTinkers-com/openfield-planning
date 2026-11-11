# ADR-0005 · Despliegue

Estado: Aceptada
Fecha: 2026-11-11
Origen: D5 (`DECISIONS.md`)

## Contexto
Presupuesto objetivo cercano a US$0, con necesidad de demos live y camino a autohospedaje.

## Decisión
- Desarrollo local con Docker (Docker Compose).
- VPS pequeño solo para demos live, cuando exista un piloto pagado.
- Diseño orientado a autohospedarse (on-premise) más adelante.

## Alternativas consideradas
- Servicios cloud gestionados desde el inicio (rechazado: costo recurrente sin cliente).
- Kubernetes temprano (rechazado: complejidad no justificada en Maker/Pro).

## Consecuencias
- Todo el stack corre en un solo host (VPS o máquina del cliente).
- Sin dependencia de un proveedor cloud específico (portabilidad on-premise).
- El VPS se difiere hasta que haya ingreso; la Fase 0 corre 100 % local.

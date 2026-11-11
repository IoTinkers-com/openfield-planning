# ADR-0010 · Desarrollo guiado por simulación

Estado: Aceptada
Fecha: 2026-11-11
Origen: D10 (`DECISIONS.md`)

## Contexto
Sin presupuesto para hardware, la Fase 0 debe validar el flujo completo antes de comprar nada.

## Decisión
- Fase 0 sin hardware.
- Los simuladores (cámara térmica T0–T2, repetición de sesiones grabadas, rutas GPX,
  inventario ficticio con QR/TAG, telemetría MQTT) son **el conjunto de pruebas de contrato**
  de los conectores reales.

## Alternativas consideradas
- Empezar comprando hardware mínimo (rechazado: viola presupuesto $0 y Fase 0).
- Pruebas ad-hoc sin contrato (rechazado: no garantizan que un conector real "encaje").

## Consecuencias
- Los simuladores viven en `openfield-connectors/simulators/` y emiten exactamente lo que un
  adaptador real emitiría.
- Un conector real es aceptable solo si pasa las mismas pruebas que su simulador.

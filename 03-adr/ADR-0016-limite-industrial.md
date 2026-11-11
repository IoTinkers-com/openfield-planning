# ADR-0016 · Límite industrial (ATEX/IECEx)

Estado: Aceptada
Fecha: 2026-11-11
Origen: D16 (`DECISIONS.md`)

## Contexto
La inspección de equipos industriales puede darse cerca de atmósferas peligrosas. Es crítico no
sobrevender capacidades de seguridad.

## Decisión
- **Nunca** presentar el sistema como apto para atmósferas explosivas ni como equipo de seguridad.
- ATEX/IECEx solo se menciona como **requisito futuro del equipo completo**, sin asumir
  certificación.

## Alternativas consideradas
- Declarar compatibilidad ATEX parcial (rechazado: sería falso y legalmente riesgoso).

## Consecuencias
- El alcance documentado excluye explícitamente atmósferas explosivas y funciones de seguridad.
- La certificación (si algún día se busca) es del equipo completo, no del software.
- Los conectores industriales (OPC UA/ONVIF) son de interoperabilidad, no de seguridad funcional.

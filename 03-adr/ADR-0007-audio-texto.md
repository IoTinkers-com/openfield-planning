# ADR-0007 · Audio a texto

Estado: Aceptada
Fecha: 2026-11-11
Origen: D7 (`DECISIONS.md`)

## Contexto
El operador describe hallazgos con voz; convertirlos a texto enriquece la documentación sin
obligarlo a teclear en terreno.

## Decisión
- Local si el dispositivo lo permite (p. ej. Whisper), con respaldo en la plataforma.
- Cada transcripción registra **qué motor la generó**.
- El audio original se guarda de forma **opcional por sesión**.

## Alternativas consideradas
- Solo transcripción en la nube (rechazado: no funciona offline-first y sube audio sensible).
- Guardar siempre el audio (rechazado: costo de almacenamiento y privacidad; mejor opcional).

## Consecuencias
- `Transcript` en el esquema incluye `engine` (motor) y referencia opcional al audio.
- Dos motores posibles (dispositivo y plataforma) deben producir el mismo contrato de salida.

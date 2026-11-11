# ADR-0003 · Identificación de activos

Estado: Aceptada
Fecha: 2026-11-11
Origen: D3 (`DECISIONS.md`)

## Contexto
El mismo activo físico puede identificarse de varias formas: un QR propio generado por la
plataforma, la placa/TAG existente del cliente, o texto leído por OCR. Ninguna es universal.

## Decisión
Tres mecanismos como **identificadores equivalentes** del mismo activo:
1. QR propio generado por la plataforma.
2. TAG/placa existente del cliente (código o texto).
3. OCR sobre la placa.

El activo tiene una identidad canónica en la plataforma y N identificadores externos
(`AssetIdentifier` con tipo, valor y origen).

## Alternativas consideradas
- Un único identificador obligatorio (rechazado: no todos los activos tienen placa legible).
- Confiar solo en OCR (rechazado: frágil; se usa como apoyo, no como fuente única).

## Consecuencias
- El esquema `Asset` + `AssetIdentifier` modela la equivalencia.
- El flujo de captura puede registrar cualquier identificador y resolverlo al activo.
- La desambiguación entre equipos en el procesamiento (plantillas o IA) se define en ADR-0017.

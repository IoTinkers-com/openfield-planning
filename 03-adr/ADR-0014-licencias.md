# ADR-0014 · Licencias

Estado: Aceptada
Fecha: 2026-11-11
Origen: D14 (`DECISIONS.md`)

## Contexto
El proyecto es open source pero se reserva la posibilidad de módulos comerciales.

## Decisión
- Software: **Apache 2.0**.
- Hardware: **CERN-OHL**.
- Módulos empresariales opcionales **cerrados** más adelante.

## Alternativas consideradas
- AGPL/GPL para software (rechazado: obliga a liberar derivados en red, lo que choca con la
  opción de módulos cerrados).
- Licencia propietaria desde el inicio (rechazado: pierde adopción y colaboración).

## Consecuencias
- El núcleo queda abierto (Apache 2.0) y compatible con los componentes Apache/MIT elegidos.
- Los módulos cerrados deben mantenerse separados del núcleo para no contaminar su licencia.
- La elección de componentes evita copyleft (ver ADR-0009 y `05-estructura-repos.md`).

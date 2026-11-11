# ADR-0009 · Contratos de datos

Estado: Aceptada
Fecha: 2026-11-11
Origen: D9 (`DECISIONS.md`)

## Contexto
Los datos deben ser legibles por herramientas geoespaciales estándar y por sistemas
industriales, sin quedar atrapados en un esquema propietario.

## Decisión
- Esquema propio simple en **JSON Schema versionado** (`schema_version`): solo se agregan
  campos, nunca se rompen.
- Compatible con **GeoJSON** (geometría), **STAC** (cada medio como Item: id, geometry,
  datetime, assets) y **OGC SensorThings** (Datastream/Observation).
- Exportación **STAC** y **OGC API Features** (lectura) desde Pro.
- **SensorThings, OPC UA y ONVIF** mediante conectores en Industrial.

## Alternativas consideradas
- Solo STAC como modelo interno (rechazado: STAC es para catálogo de medios, no para sesiones/
  activos/formularios; se usa como vista de exportación).
- Esquema sin versión (rechazado: romper cambios sin control).

## Consecuencias
- `schema_version` en todo documento; la evolución es aditiva.
- STAC/GeoJSON/SensorThings son proyecciones del esquema canónico, no el esquema en sí.
- Los conectores industriales consumen/producen el mismo contrato canónico.

# ADR-0002 · Georreferenciación

Estado: Aceptada
Fecha: 2026-11-11
Origen: D2 (`DECISIONS.md`)

## Contexto
Los datos se capturan tanto en exteriores (donde hay GPS) como en interiores (donde el GPS no
está disponible). El cliente puede operar en distintos países de Latinoamérica, no solo Chile.

## Decisión
- Exteriores: GPS del dispositivo.
- Interiores: QR/TAG del activo como referencia de ubicación.
- Internamente: WGS84 (EPSG:4326), para compatibilidad con GeoJSON/STAC.
- Exportación: proyección UTM (zona según ubicación) sobre SIRGAS2000 / densificación nacional,
  para Latinoamérica (no limitado a Chile).

## Alternativas consideradas
- CRS local como almacenamiento interno (rechazado: pierde interoperabilidad GeoJSON/STAC).
- Solo WGS84 sin export (rechazado: clientes industriales requieren UTM local para planos/CMMS).

## Consecuencias
- Un solo CRS interno simplifica el modelo y la validación.
- La conversión UTM/SIRGAS2000 se hace con PROJ/pyproj (X/MIT), no a mano.
- El asset (no la coordenada GPS) es la referencia de ubicación en interiores.

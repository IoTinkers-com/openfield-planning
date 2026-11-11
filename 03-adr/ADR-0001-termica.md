# ADR-0001 · Térmica (contrato canónico T0–T3)

Estado: Aceptada
Fecha: 2026-11-11
Origen: D1 (`DECISIONS.md`)

## Contexto
La inspección de equipos eléctricos/industriales requiere térmica, pero el hardware disponible
varía por nivel: sin sensor (Maker), módulos de baja/media resolución (Pro) y cámaras
radiométricas con calibración (Industrial). Acoplar la plataforma al formato de cada fabricante
haría inviable agregar sensores sin reescribir el núcleo.

## Decisión
Contrato canónico de térmica con 4 niveles de capacidad:
- **T0** — solo imagen con paleta (visual).
- **T1** — matriz de baja resolución (p. ej. MLX90640 32×24).
- **T2** — radiométrica media (p. ej. Lepton 3.5, módulos USB).
- **T3** — alta resolución con parámetros de calibración.

Todo adaptador normaliza a: matriz de temperaturas en °C + imagen renderizada + JSON (modelo de
sensor, resolución, emisividad, temperatura reflejada, distancia, nivel T0–T3). El original
propietario se conserva como evidencia. Maker = visual (T0); radiométrica desde Pro.

## Alternativas consideradas
- Usar formatos propietarios de cada fabricante (rechazado: acopla la plataforma al hardware).
- Un único formato radiométrico para todos (rechazado: excluye Maker sin hardware y la Fase 0).

## Consecuencias
- Un sensor nuevo = solo un adaptador que emita el contrato canónico (criterio de calidad).
- Evidencia original preservada junto al dato normalizado (auditabilidad).
- Costo incremental por nivel; el esquema de térmica vive en `04-esquemas/thermal-capture`.

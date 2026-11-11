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
- Que el modelo de datos de la plataforma dependa directamente de formatos propietarios
  (rechazado: acopla el núcleo al hardware de un fabricante).
- Un único formato radiométrico para todos (rechazado: excluye Maker sin hardware y la Fase 0).

## Integración de tecnologías propietarias
Las tecnologías propietarias (FLIR Lepton/Boson, Seek, etc.) **no se excluyen**: se integran
mediante su SDK o wrappers open source en la capa de adaptador, que las normaliza al contrato
canónico y conserva el original como evidencia. Existen proyectos abiertos que facilitan la
lectura de temperaturas (p. ej. `flirpy`, `pylepton` sobre PureThermal). De hecho, Pro ya usa
Lepton 3.5 (Teledyne FLIR). La licencia y el riesgo de abandono de esos wrappers se evalúan en
`05-estructura-repos.md` si se adoptan.

## Consecuencias
- Un sensor nuevo = solo un adaptador que emita el contrato canónico (criterio de calidad).
- Evidencia original preservada junto al dato normalizado (auditabilidad).
- Costo incremental por nivel; el esquema de térmica vive en `04-esquemas/thermal-capture`.

# ADR-0020 · Registro de activos y ciclo de vida

Estado: Aceptada
Fecha: 2026-11-13
Origen: D20 (`DECISIONS.md`) — deriva de D12, D3 y ADR-0017

## Contexto
OpenField debe funcionar como plataforma de **control y seguimiento del estado de activos
industriales**, no solo como visor de capturas. El caso de uso principal (D12) es el
inventario de equipos eléctricos/industriales: los usuarios parten de una lista de equipos
(o la crean), la completan y le dan seguimiento. El `Asset` canónico solo tenía `name`,
`category` y `location`: no servía como registro de activos ni permitía enrolar,
desincorporar ni llevar estados.

Las normas de referencia:
- **ISO 55001:2024 §7.5/7.6** no prescribe una lista fija de campos: exige que la
  organización **determine** la información de gestión de activos que necesita, sus
  requisitos de atributos y calidad, y un plan de recolección, análisis y mejora de esos
  datos, con trazabilidad ([guía NQA](https://www.nqa.com/getmedia/ae470aa9-94ac-4536-b318-eb1c37ae81a5/NQA-ISO-55001-Gap-Guide-2024.pdf),
  [MARAMM cláusula por cláusula](https://maramm.org/wp-content/uploads/2026/09/etudes-maramm-n04-iso-55001-clause-by-clause-en.pdf)).
  Es decir: lo que el estándar pide es exactamente **atributos configurables por la
  organización**, no un esquema rígido universal.
- **ISO 14224:2016** aporta la estructura: clase/tipo de equipo, jerarquía de instalación
  de 9 niveles (industria → parte) y "equipment data" por clase ([vista previa ISO 14224](https://cdn.standards.iteh.ai/samples/64076/997b35a640ef4758a4ce8c7dc4ba4a7d/ISO-14224-2016.pdf),
  [resumen moksana](https://moksana.com/learn/iso-14224-equipment-hierarchy)). Se adopta la
  **estructura**; no se reproduce el Anexo A (taxonomía detallada con derechos de la norma).

## Decisión
- **Nuevo esquema `asset-type`** (12.º esquema canónico): tipo de activo con
  **atributos configurables** (`key`, `label`, `type`, `unit`, `required`, `options`,
  `active`, `order`, `verify_in_field`), `equipment_class` opcional para mapear la clase de
  equipo de la taxonomía adoptada, y `active` para retirar el tipo sin borrarlo. Los tipos
  de dato del MVP: `text`, `number`, `boolean`, `select`, `date`.
- **`Asset` gana campos opcionales** (cambio aditivo, D9): `asset_type_id`, `attributes`
  (valores de la ficha técnica validados contra el tipo), `status` + `status_reason` +
  `status_changed_at`, `parent_id` (jerarquía, estructura ISO 14224), `functional_location`,
  `manufacturer`, `model`, `serial_number`, `criticality` (A/B/C), `commissioned_at`,
  `decommissioned_at`, `data_source`, `import_batch_id`, `verification_status`,
  `verified_at`, `attribute_verification`. Los campos de verificación se detallan en
  ADR-0022.
- **Estados del ciclo de vida (enum fijo en el MVP):**
  | Estado | Significado |
  | --- | --- |
  | `planned` | Registrado, aún no en servicio. |
  | `in_service` | En servicio (estado por defecto al enrolar). |
  | `standby` | Disponible pero fuera de operación temporal. |
  | `out_of_service` | Fuera de servicio (exige motivo). |
  | `decommissioned` | Desincorporado/retirado (exige motivo; **terminal**). |
  - `decommissioned` es terminal y bloquea nuevas capturas asociadas: desincorporar no es
    eliminar; el expediente y la evidencia se conservan (ADR-0021).
- **Jerarquía por `parent_id`** (un solo nivel de anidamiento administrado por la
  aplicación; el mapeo completo a los 9 niveles de ISO 14224 es una configuración del
  cliente sobre `functional_location`/`parent_id`, no campos rígidos).
- **FormTemplate sigue siendo solo para inspecciones** (D6): la ficha técnica del activo
  (datos del equipo) y el checklist de una visita son cosas distintas.
- **Panel de administración** `/admin/` para gestionar tipos, activos e importaciones
  (ADR-0018 para la consistencia visual).

## Alternativas consideradas
- Reusar `FormTemplate`/`FormResponse` como ficha técnica (rechazado: mezcla datos maestros
  del activo con respuestas de inspección; no tiene banderas `active`/`order`/
  `verify_in_field` por atributo ni validación de valores guardados en el propio `Asset`).
- Estados del ciclo de vida configurables por tenant (diferido: el enum fijo cubre el MVP;
  una configuración por tenant se puede agregar como campos nuevos sin romper el esquema).
- Copiar el Anexo A de ISO 14224 como catálogo de tipos predefinido (rechazado: es contenido
  de la norma; el cliente define sus tipos; el seed incluye solo ejemplos genéricos).
- Campo `status` libre (rechazado: sin enum no hay semántica compartida ni reglas como
  "exigir motivo" o "terminal").

## Consecuencias
- 12 esquemas canónicos; las 4 copias (`04-esquemas/` y `schemas/` de platform, wearable y
  connectors) deben mantenerse idénticas (regla de paridad existente).
- La ingesta de `asset` con `asset_type_id` valida los `attributes` contra el tipo.
- Activos con `status = decommissioned` rechazan nuevas capturas (409 en ingesta) y quedan
  excluidos de los flujos de verificación, pero su expediente sigue consultable.
- La administración de tipos prohíbe **quitar** un atributo que ya tiene valores en algún
  activo: se desactiva (`active: false`), no se elimina, para no dejar valores huérfanos.
- Un atributo desactivado no se muestra para capturar valores nuevos pero sus valores
  existentes se conservan y se muestran.

# 08 · Riesgos y supuestos

> Estado: borrador · Tanda E · OpenField (IoTinkers)

## 1. Registro de riesgos
Probabilidad/Impacto: Alta (A) / Media (M) / Baja (B).

| # | Riesgo | Prob. | Impacto | Mitigación | ADR |
| --- | --- | --- | --- | --- | --- |
| R1 | PWA en iOS pierde la cola (IndexedDB purgable) o no sincroniza en segundo plano | M | A | Offline-first con subida explícita al volver a primer plano; no depender de Background Sync; copia de respaldo opcional | ADR-0008 |
| R2 | Whisper local en WASM no viable en el dispositivo | M | M | Respaldo de transcripción en plataforma; registrar el `engine` | ADR-0007 |
| R3 | Licencia de un componente cambia a copyleft o queda sin mantenimiento (patrón MinIO) | M | A | Preferir Apache/MIT; evitar single-vendor; alternativa documentada por componente | ADR-0014 |
| R4 | Precio/disponibilidad de hardware T1–T2 (MLX90640, Lepton 3.5) cambia | M | M | Fase 0 sin hardware; precio confirmado al comprar en Fase 2 | ADR-0001 |
| R5 | La Ley 21.719 chilena entra en vigor antes de lo previsto o cambia su alcance | M | M | Consentimiento + indicador + retención por defecto; verificar por país | ADR-0015 |
| R6 | La IA atribuye observaciones al equipo equivocado | M | A | Delimitación explícita por activo + validación humana; IA es apoyo, no identidad | ADR-0017 |
| R7 | `pylepton` descontinuado o con licencia poco clara | M | M | Usar `flirpy` (MIT, activo) o wrapper propio sobre el SDK de FLIR | ADR-0001 |
| R8 | Pérdida de capturas por fallo del dispositivo | M | A | Cola local + `tus` reanudable; `id` idempotente; dedupe en ingesta | ADR-0004 |
| R9 | Alcance multi-país Latam dispara costos de cumplimiento por país | M | M | Arrancar en Chile; `tenant_id` ya presente; verificación legal incremental | ADR-0013, ADR-0015 |
| R10 | Presentar el sistema como "seguro" o apto para atmósferas explosivas | B | A | Prohibición explícita en alcance y documentación | ADR-0016 |
| R11 | La hoja de estilos (design tokens) duplicada entre `openfield-wearable` y `openfield-platform` se desincroniza al editar solo una copia | M | B | Comentario de "copia idéntica" en cada archivo + revisar ambas copias en cada cambio visual; reevaluar extraer paquete de UI si aparece un tercer consumidor | ADR-0018 |
| R12 | El expediente de activo (`GET /assets/{id}`) escanea todos los documentos del tenant por tipo y filtra en Python (sin índice por `asset_id`/`session_id`); a escala Pro esto degrada el rendimiento | M | M | Aceptable en Fase 0/1 por volumen bajo; agregar índices o columnas generadas por `asset_id`/`session_id` cuando el volumen lo justifique | ADR-0019 |
| R13 | Endpoints de escritura y panel `/admin/` sin autenticación, expuestos por el túnel de pruebas o una red compartida | M | A | Todas las mutaciones son reversibles (baja lógica + historial); el túnel solo se expone durante pruebas controladas; autenticación/autorización en backlog (H-AUTH) antes de producción | ADR-0021, ADR-0013 |
| R14 | Migración de `documents` (columnas nuevas) sin Alembic: un ALTER manual puede fallar o divergir entre SQLite y PostgreSQL | B | M | Migración idempotente probada en ambos dialectos; Alembic en backlog (H-ALEMBIC) | ADR-0021 |
| R15 | El CSV del cliente trae codificación, separador decimal o tags duplicados inconsistentes y corrompe el registro | A | M | Vista previa (dry-run) obligatoria con reporte por fila/columna; emparejamiento por TAG; re-import idempotente que no pisa lo verificado; límites de tamaño | ADR-0022 |
| R16 | El dictado del teclado de iOS puede no estar disponible sin conexión según modelo/idioma | M | M | Nota de voz offline con transcripción en plataforma al sincronizar (respaldado por ADR-0007); supuesto a validar en el iPhone de pruebas | ADR-0023 |
| R17 | Cuota y purga de IndexedDB en iOS con blobs de medios puede perder la cola offline | M | A | Sincronizar pronto; avisar el tamaño/pendientes de la cola; no depender de Background Sync (ADR-0008) | ADR-0023, ADR-0008 |
| R18 | Soporte variable de `torch`, `zoom` e `ImageCapture` según navegador/SO: los controles pueden no existir en el dispositivo de pruebas | A | B | Detección en runtime (`track.getCapabilities()`); controles ocultos si no hay soporte; la captura base no depende de ellos | ADR-0024 |
| R19 | El "pantalla completa" en iPhone es overlay CSS (sin Fullscreen API para elementos): las barras de Safari pueden asomar y `100dvh`/safe-areas deben validarse en el dispositivo real | M | M | `viewport-fit=cover` + `env(safe-area-inset-*)`; validación manual en el iPhone por ngrok; modo standalone ("Agregar a inicio") oculta las barras | ADR-0024 |

## 2. Supuestos
- PostGIS se usa como servicio (no se distribuye binario combinado) → GPLv2+ no fuerza liberar la app (ADR-0005).
- El VPS de demo solo se paga cuando exista un piloto pagado (ADR-0005).
- "Industrial" es diseño para alcanzar certificación, no certificación inmediata (D16).
- El paquete `openfield-schemas` inicia como copia *vendored* + chequeo de paridad (05).
- En Fase 0 los simuladores son deterministas (misma entrada → misma salida) para usarse como *golden files* (07).
- Una `Session` con `asset_id = null` (abarca varios activos) no aparece todavía en ningún expediente de activo (ADR-0019); se resuelve en una fase posterior.
- Los 5 estados del ciclo de vida (`planned`/`in_service`/`standby`/`out_of_service`/`decommissioned`) cubren el MVP; estados configurables por tenant quedan para después (ADR-0020).
- El `actor` del historial es "admin" hasta que exista autenticación (ADR-0021, H-AUTH).
- La clave de emparejamiento del CSV es el TAG (o `serial_number`); nunca el nombre (ADR-0022).
- Un dato importado nace `pending`: nunca se presenta como verificado en terreno (ADR-0022).
- La reasignación de un medio a otro activo es una corrección humana auditada, no un flujo automático (ADR-0017).
- La leyenda por foto es opcional y se escribe/dicta con el teclado del SO (coherente con ADR-0023); no es un paso obligatorio (ADR-0024).
- Las categorías de foto se configuran por tipo de activo; sin configuración se usa la lista predeterminada (ADR-0024).

## 3. Preguntas abiertas (consolidadas)
- Alcance exacto del piloto Pro (qué cliente/instalación) — se define al iniciar Fase 1.
- ¿Registro de paquetes (PyPI/npm) privado o público? — al iniciar Fase 1.
- ¿*Golden files* versionados en `contracts/`? — al iniciar Fase 1.
- Fecha exacta de vigencia de la Ley 21.719 (puede postergarse a 2027) — confirmar al implementar.
- ¿Cómo presentar en el expediente las sesiones multi-activo (`Session.asset_id = null`)? — al definir el piloto Pro (ADR-0019).
- ¿Qué formato de exportación usan los CMMS de los clientes objetivo (SAP PM/Maximo)? — ajustar la plantilla CSV al tener una planilla real (ADR-0022).
- ¿Alguna categoría de foto debe ser obligatoria para cerrar la verificación (p. ej. "Placa de datos")? — se decide tras el piloto (ADR-0024).

## 4. Decisión / Supuesto / Pregunta abierta
- **Decisión:** los riesgos R1–R17 se revisan al cierre de cada fase.
- **Supuesto:** la probabilidad/impacto son estimaciones iniciales, no datos.
- **Pregunta abierta:** ¿agregar un registro formal de riesgos con dueño y fecha? → si lo pide un cliente Pro.

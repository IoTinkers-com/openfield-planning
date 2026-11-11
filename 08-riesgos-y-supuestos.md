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

## 2. Supuestos
- PostGIS se usa como servicio (no se distribuye binario combinado) → GPLv2+ no fuerza liberar la app (ADR-0005).
- El VPS de demo solo se paga cuando exista un piloto pagado (ADR-0005).
- "Industrial" es diseño para alcanzar certificación, no certificación inmediata (D16).
- El paquete `openfield-schemas` inicia como copia *vendored* + chequeo de paridad (05).
- En Fase 0 los simuladores son deterministas (misma entrada → misma salida) para usarse como *golden files* (07).

## 3. Preguntas abiertas (consolidadas)
- Alcance exacto del piloto Pro (qué cliente/instalación) — se define al iniciar Fase 1.
- ¿Registro de paquetes (PyPI/npm) privado o público? — al iniciar Fase 1.
- ¿*Golden files* versionados en `contracts/`? — al iniciar Fase 1.
- Fecha exacta de vigencia de la Ley 21.719 (puede postergarse a 2027) — confirmar al implementar.

## 4. Decisión / Supuesto / Pregunta abierta
- **Decisión:** los riesgos R1–R10 se revisan al cierre de cada fase.
- **Supuesto:** la probabilidad/impacto son estimaciones iniciales, no datos.
- **Pregunta abierta:** ¿agregar un registro formal de riesgos con dueño y fecha? → si lo pide un cliente Pro.

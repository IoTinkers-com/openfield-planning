# 00 · Visión y alcance

> Estado: borrador · Tanda A · OpenField (IoTinkers)

## 1. Visión
**OpenField** es una plataforma para capturar, georreferenciar, transmitir y estructurar
evidencia de terreno —imagen y video RGB y térmicos, y audio del operador convertido a
texto— para documentar el estado de instalaciones e inventarios industriales, con
presupuesto cercano a US$0 en la primera fase y una ruta clara hacia uso certificable e
integrable.

## 2. Alcance
**Dentro:**
- Captura georreferenciada de medios (RGB + térmica) y audio→texto.
- Contrato de datos canónico y versionado (JSON Schema), compatible con GeoJSON, STAC y
  OGC SensorThings.
- Plataforma de ingesta, almacenamiento, estructuración, presentación e informes.
- Conectores a dispositivos/sistemas externos + simuladores que cumplen los mismos contratos.
- Niveles de madurez Maker / Pro / Industrial.

**Fuera (en esta fase):**
- Código de aplicación (esto es solo planificación).
- Compras o recomendación de compra de hardware.
- Certificación ATEX/IECEx (se menciona solo como requisito futuro).

## 3. Caso de uso principal
Inventario de equipos eléctricos/industriales durante los primeros 3 meses (D12 · ADR-0012).

## 4. Usuarios y tenants
Un solo usuario al inicio. `tenant_id` en el esquema desde el día uno para pasar a
multiempresa sin migraciones (D13 · ADR-0013).

## 5. Objetivos por nivel
| Nivel | Objetivo | Métrica de éxito |
| --- | --- | --- |
| Maker | Validar el flujo completo sin hardware real (simulado). | Fase 0 completada sin comprar nada. |
| Pro | Pilotar con clientes reales y hardware intermedio (térmica radiométrica). | 1 piloto pagado con flujo real. |
| Industrial | Ser certificable e integrable (OPC UA, ONVIF, CMMS/SCADA/GIS). | Conectores que pasan pruebas de contrato. |

## 6. Principios de diseño (trazables a decisiones)
1. Offline-first como base; live es un modo opcional con tope (D4).
2. Contrato canónico único por tipo de dato; un sensor nuevo = un adaptador, sin tocar
   plataforma (D1, D9).
3. Esquema versionado que solo agrega campos, nunca rompe (D9).
4. Desarrollo guiado por simulación: los simuladores son las pruebas de contrato (D10).
5. PWA primero, con la capa de acceso a hardware desacoplada (D8).
6. Toda salida de IA con validación humana (D6).
7. Componentes open source maduros, con licencia/riesgo/alternativa documentados.
8. Privacidad por defecto: indicador de grabación, consentimiento y retención (D15).

## 7. Límites (D16 · ADR-0016)
Nunca presentar el sistema como apto para atmósferas explosivas ni como equipo de
seguridad. ATEX/IECEx solo como requisito futuro del equipo completo, sin asumir
certificación.

## 8. Repositorios y organización
Organización GitHub: `iotinkers-com`. Repos: `openfield-wearable`, `openfield-platform`,
`openfield-connectors`, `openfield-planning` (ver `DECISIONS.md`).

## 9. Resumen Maker | Pro | Industrial
| Dimensión | Maker | Pro | Industrial |
| --- | --- | --- | --- |
| Hardware | Consumo / simulado | Intermedio (térmica T1–T2) | Certificable (T3, OPC UA/ONVIF) |
| Red | Wi-Fi | Celular + Wi-Fi | VPN / MQTT / OPC UA |
| Datos | Local / Docker | Objetos + PostGIS | Archivado + retención legal |
| Despliegue | Docker local | VPS de demo | On-premise |
| Estándares | Web APIs | STAC, OGC API Features | OPC UA, ONVIF, SensorThings |

## 10. Decisión / Supuesto / Pregunta abierta
- **Decisión:** lo listado en `DECISIONS.md` (D1–D16).
- **Supuesto:** el presupuesto ≈ US$0 admite un VPS solo cuando exista un piloto pagado (D5).
- **Supuesto:** "Industrial" no implica certificación inmediata, sino diseño para alcanzarla.
- **Pregunta abierta:** alcance exacto del piloto Pro (qué cliente / instalación) — se define al iniciar la Fase 1.
- **Pregunta abierta:** base legal del audio ambiental de terceros en Chile — `[VERIFICAR]` en ADR-0015.
